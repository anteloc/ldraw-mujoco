"""Independent browser inspection. MuJoCo supplies geometry and kinematics only."""

from __future__ import annotations

import hashlib
import sys
import threading
import webbrowser
from contextlib import contextmanager

import mujoco
import numpy as np
import trimesh
from scipy.spatial.transform import Rotation


def visual_mesh(model, gid):
    """Read compiled mesh frames, or tessellate native primitives with trimesh."""
    kind, size = model.geom_type[gid], model.geom_size[gid]
    types = mujoco.mjtGeom
    if kind == types.mjGEOM_MESH:
        mid = model.geom_dataid[gid]
        va, fa = model.mesh_vertadr[mid], model.mesh_faceadr[mid]
        return (
            model.mesh_vert[va : va + model.mesh_vertnum[mid]].copy(),
            model.mesh_face[fa : fa + model.mesh_facenum[mid]].copy(),
        )
    if kind in (types.mjGEOM_PLANE, types.mjGEOM_BOX):
        extent = 2 * size.copy()
        if kind == types.mjGEOM_PLANE:
            x, y = np.maximum(size[:2], 1.0)
            return np.array([[-x, -y, 0], [x, -y, 0], [x, y, 0], [-x, y, 0]]), np.array(
                [[0, 1, 2], [0, 2, 3]]
            )
        mesh = trimesh.creation.box(extents=extent)
    elif kind in (types.mjGEOM_SPHERE, types.mjGEOM_ELLIPSOID):
        mesh = trimesh.creation.icosphere(subdivisions=3)
        mesh.vertices *= size[0] if kind == types.mjGEOM_SPHERE else size
    elif kind == types.mjGEOM_CYLINDER:
        mesh = trimesh.creation.cylinder(radius=size[0], height=2 * size[1])
    elif kind == types.mjGEOM_CAPSULE:
        mesh = trimesh.creation.capsule(radius=size[0], height=2 * size[1])
    else:
        raise ValueError(f"Browser viewer does not support geom type {int(kind)}")
    return mesh.vertices, mesh.faces


class BrowserViewer:
    """One local Viser service; camera/GUI callbacks never modify physics state."""

    def __init__(self, model, *, enabled_bodies=None):
        import viser

        self._lock = threading.RLock()
        self.server = viser.ViserServer(host="127.0.0.1", port=0, verbose=False)
        self.url = f"http://127.0.0.1:{self.server.get_port()}"
        try:
            self.server.gui.configure_theme(
                control_width="small",
                show_share_button=False,
                show_logo=False,
            )
            self.server.gui.main_panel.dock_right()
            self.server.scene.set_up_direction("+z")
            self.server.scene.world_axes.visible = False
            self.status = self.server.gui.add_markdown("Preparing scene…")
            self.context = self.server.gui.add_checkbox("Show unplaced parts", initial_value=True)
            frame = self.server.gui.add_button("Frame model")

            @frame.on_click
            def frame_model(event):
                if event.client is not None:
                    with event.client.atomic():
                        self._frame(event.client.camera)

            @self.context.on_update
            def show_context(_):
                with self._lock:
                    self.publish(self.data.qpos, self._enabled, status=self._status)

            self.set_scene(model, enabled_bodies=enabled_bodies)

            @self.server.on_client_connect
            def configure_camera(client):
                # The default centimetre-scale zoom limit is too coarse for bricks.
                client.camera.min_orbit_distance = max(self.radius / 1000, 0.000001)
        except BaseException:
            self.server.stop()
            raise

    @property
    def connected(self):
        return bool(self.server.get_clients())

    def open(self):
        print(f"Browser viewer: {self.url}", file=sys.stderr)
        opened = webbrowser.open(self.url)
        if not opened:
            print("Could not open a browser automatically; open the URL above.", file=sys.stderr)
        return {"url": self.url, "opened": opened}

    def _frame(self, camera):
        camera.fov = np.radians(50)
        # Viser translates the look-at point along with a position change.
        camera.position = self.center + self.radius * np.array([1.3, -1.7, 1.1])
        camera.look_at = self.center
        camera.near = max(self.radius / 1000, 0.00001)
        camera.far = max(self.radius * 100, 10)

    def set_scene(self, model, *, enabled_bodies=None):
        """Replace visual assets after an accepted edit, preserving client cameras."""
        with self._lock:
            # Build before removing the old scene, so unsupported geometry is non-destructive.
            groups = {}
            gids = np.flatnonzero(model.geom_group == 0)
            for gid in gids:
                vertices, faces = visual_mesh(model, gid)
                vertices = np.asarray(vertices, dtype=np.float32)
                faces = np.asarray(faces, dtype=np.uint32)
                key = hashlib.sha256(vertices.tobytes() + faces.tobytes()).hexdigest()
                if key not in groups:
                    groups[key] = (vertices, faces, [])
                groups[key][2].append(int(gid))
            self.model = model
            self.data = mujoco.MjData(model)
            mujoco.mj_kinematics(model, self.data)
            self.cad_positions = self.data.geom_xpos.copy()
            self.cad_quaternions = Rotation.from_matrix(
                self.data.geom_xmat.reshape(-1, 3, 3)
            ).as_quat(scalar_first=True)
            bounds = []
            for vertices, _, indices in groups.values():
                for gid in indices:
                    if model.geom_bodyid[gid] != 0:
                        world = (
                            vertices @ self.data.geom_xmat[gid].reshape(3, 3).T
                            + self.cad_positions[gid]
                        )
                        bounds.extend((world.min(axis=0), world.max(axis=0)))
            if bounds:
                low, high = np.min(bounds, axis=0), np.max(bounds, axis=0)
                self.center = (low + high) / 2
                self.radius = max(np.linalg.norm(high - low) / 2, 0.005)
            else:
                self.center, self.radius = np.zeros(3), 1.0
            self._frame(self.server.initial_camera)
            with self.server.atomic():
                for handle, _ in getattr(self, "batches", []):
                    handle.remove()
                self.batches = []
                for number, (vertices, faces, indices) in enumerate(groups.values()):
                    indices = np.array(indices)
                    handle = self.server.scene.add_batched_meshes_simple(
                        f"/visual/{number}",
                        vertices,
                        faces,
                        self.cad_quaternions[indices],
                        self.cad_positions[indices],
                        batched_colors=np.round(model.geom_rgba[indices, :3] * 255).astype(
                            np.uint8
                        ),
                        batched_opacities=model.geom_rgba[indices, 3].copy(),
                        opacity=1.0,
                        lod="off",
                        side="double",
                        cast_shadow=False,
                    )
                    self.batches.append((handle, indices))
                self.publish(model.qpos0, enabled_bodies, status="Loading physics")

    def publish(self, qpos, enabled_bodies=None, *, status="Paused"):
        """Publish a snapshot without forward dynamics, contacts, or time advancement."""
        with self._lock:
            self.data.qpos[:] = qpos
            self._enabled = None if enabled_bodies is None else tuple(enabled_bodies)
            self._status = status
            mujoco.mj_kinematics(self.model, self.data)
            quats = Rotation.from_matrix(self.data.geom_xmat.reshape(-1, 3, 3)).as_quat(
                scalar_first=True
            )
            active = (
                np.ones(self.model.ngeom, dtype=bool)
                if enabled_bodies is None
                else np.isin(self.model.geom_bodyid, [0, *enabled_bodies])
            )
            opacity = self.model.geom_rgba[:, 3] * np.where(
                active, 1.0, 0.15 if self.context.value else 0.0
            )
            with self.server.atomic():
                for handle, gids in self.batches:
                    handle.batched_positions = np.where(
                        active[gids, None], self.data.geom_xpos[gids], self.cad_positions[gids]
                    ).astype(np.float32)
                    handle.batched_wxyzs = np.where(
                        active[gids, None], quats[gids], self.cad_quaternions[gids]
                    ).astype(np.float32)
                    alpha = opacity[gids].astype(np.float32)
                    # Keep fully opaque batches in the opaque render pass. Zero-alpha
                    # instances must also stop writing depth, not merely blend invisibly.
                    handle.batched_opacities = None if np.all(alpha == 1) else alpha
                    handle.batched_scales = (alpha > 0).astype(np.float32)
                self.status.content = status

    def close(self):
        self.server.stop()


@contextmanager
def browser_session(model, *, enabled=False):
    """Viewer failures leave command-line simulation available."""
    viewer = None
    if enabled:
        try:
            viewer = BrowserViewer(model)
            viewer.open()
        except Exception as exc:
            if viewer is not None:
                viewer.close()
            viewer = None
            print(f"Browser viewer unavailable: {exc}", file=sys.stderr)
    try:
        yield viewer
    finally:
        if viewer is not None:
            viewer.close()
