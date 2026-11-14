"""Small stdio client for the installed MuJoCo MCP server, never a physics backend."""

from __future__ import annotations

import importlib.metadata
import json
import os
import sys
import sysconfig
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path


class MCPError(RuntimeError):
    """A transport, tool, or server compatibility failure."""


def server_command(*, viewer=False):
    """Use MuJoCo's native main-thread launcher for graphical macOS sessions."""
    scripts = Path(sysconfig.get_path("scripts"))
    if viewer and sys.platform == "darwin":
        executable, arguments = scripts / "mjpython", ["-m", "mujoco_mcp"]
    else:
        executable = scripts / ("mujoco-mcp.exe" if os.name == "nt" else "mujoco-mcp")
        arguments = []
    if not executable.is_file():
        raise MCPError(f"Server entrypoint missing: {executable}; install the interpreter extra")
    return str(executable), arguments


def decode_result(result):
    """The server returns JSON strings, sometimes wrapped in structuredContent."""
    if result.isError:
        raise MCPError(str(result.content))
    payload = getattr(result, "structuredContent", None)
    if payload is None:
        blocks = [c.text for c in result.content if c.type == "text"]
        if len(blocks) != 1:
            raise MCPError("Expected one JSON response from MuJoCo MCP")
        payload = blocks[0]
    if isinstance(payload, dict) and set(payload) == {"result"}:
        payload = payload["result"]
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except ValueError as exc:
            raise MCPError("MuJoCo MCP returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise MCPError("MuJoCo MCP returned a non-object response")
    if payload.get("error") or payload.get("ok") is False:
        raise MCPError(json.dumps(payload))
    if any(m.get("ok") is False for m in payload.get("modifications", [])):
        raise MCPError(json.dumps(payload))
    return payload


class MujocoClient:
    """One owned server process. All simulation calls go through its MCP session."""

    required_tools = {
        "server_diagnostics",
        "sim_load",
        "sim_reset",
        "modify_model",
        "sim_step",
        "sim_forward",
        "sim_get_state",
        "sim_set_state",
        "analyze_contacts",
    }

    def __init__(self, session):
        self.session = session

    async def call(self, tool, **arguments):
        try:
            return decode_result(await self.session.call_tool(tool, arguments))
        except MCPError:
            raise
        except Exception as exc:
            raise MCPError(f"{tool}: {exc}") from exc

    @classmethod
    @asynccontextmanager
    async def connect(cls, *, log_path=None, viewer=False):
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            distribution = importlib.metadata.distribution("mujoco-mcp-server")
        except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
            raise MCPError(
                "Install the interpreter with uv sync --locked --extra interpreter"
            ) from exc
        origin = json.loads(distribution.read_text("direct_url.json") or "{}")
        if origin.get("dir_info", {}).get("editable"):
            raise MCPError("Use the pinned, non-editable interpreter extra, not an editable server")
        executable, arguments = server_command(viewer=viewer)
        # The SDK supplies the ordinary process environment allowlist. Pass display
        # configuration explicitly so an optional viewer can work on desktop hosts.
        env = {
            k: v
            for k, v in os.environ.items()
            if k in {"DISPLAY", "WAYLAND_DISPLAY", "MUJOCO_GL"} or k.startswith("MUJOCO_MCP_")
        }
        if viewer and sys.platform == "darwin":
            # mjpython's dlopen follows a venv executable symlink. uv's Python
            # keeps libpython in the base environment, not in that venv's lib/.
            library_dir = sysconfig.get_config_var("LIBDIR") or str(Path(sys.base_prefix) / "lib")
            fallback = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "/usr/local/lib:/usr/lib")
            env["DYLD_FALLBACK_LIBRARY_PATH"] = library_dir + ":" + fallback
        params = StdioServerParameters(command=executable, args=arguments, env=env)
        if log_path is not None:
            Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        log = Path(log_path).open("w+") if log_path else tempfile.TemporaryFile(mode="w+")
        pending = None
        with log:
            try:
                async with stdio_client(params, errlog=log) as (read, write):
                    async with ClientSession(read, write) as session:
                        # Keep caller exceptions outside the SDK's task groups so
                        # ExecutionError remains catchable without except* syntax.
                        ready = False
                        try:
                            await session.initialize()
                            available, cursor = {}, None
                            while True:
                                page = await session.list_tools(cursor=cursor)
                                available.update({t.name: t for t in page.tools})
                                cursor = page.nextCursor
                                if not cursor:
                                    break
                            if missing := cls.required_tools - available.keys():
                                raise MCPError(f"MuJoCo MCP is missing tools: {sorted(missing)}")
                            if viewer and "realtime" not in available["sim_step"].inputSchema.get(
                                "properties", {}
                            ):
                                raise MCPError(
                                    "MuJoCo MCP lacks viewer playback support; update the interpreter extra"
                                )
                            client = cls(session)
                            diagnostic = await client.call("server_diagnostics")
                            version = diagnostic["version"]["mujoco_version"]
                            if version != "3.5.0":
                                raise MCPError(
                                    f"Expected MuJoCo 3.5.0 on the server, got {version}"
                                )
                            ready = True
                            yield client
                        except BaseException as exc:
                            if not ready and isinstance(exc, Exception):
                                log.seek(0)
                                pending = MCPError(
                                    f"MuJoCo MCP startup failed: {exc}\n{log.read()[-2000:]}"
                                )
                            else:
                                pending = exc
            except ExceptionGroup as exc:
                log.seek(0)
                detail = log.read()[-2000:]
                raise MCPError(f"MuJoCo MCP connection failed: {exc}\n{detail}") from exc
        if pending is not None:
            raise pending
