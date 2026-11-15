import time
from pathlib import Path

import mujoco
import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from ldraw_mujoco.viewer import BrowserViewer, visual_mesh


def test_display_uses_kinematics_and_preserves_affine_geometry(build, monkeypatch):
    result = build("1 47 30 -20 10 -2 .1 0 0 1 0 0 0 1 cube.dat\n")
    model = result.spec.compile()
    flags, masks, rgba = model.opt.disableflags, model.geom_contype.copy(), model.geom_rgba.copy()
    monkeypatch.setattr(mujoco, "mj_forward", lambda *_: pytest.fail("Viewer solved physics"))
    viewer = BrowserViewer(model, enabled_bodies=[])
    try:
        points = []
        for handle, gids in viewer.batches:
            for i, gid in enumerate(gids):
                if model.geom_bodyid[gid] == 0:
                    continue
                vertices, _ = visual_mesh(model, gid)
                matrix = Rotation.from_quat(handle.batched_wxyzs[i], scalar_first=True).as_matrix()
                points.extend(vertices @ matrix.T + handle.batched_positions[i])
                assert handle.batched_opacities[i] == pytest.approx(model.geom_rgba[gid, 3] * 0.15)
        expected = np.array(result.report["source_bounds_m"]) + result.report["scene_offset_m"]
        np.testing.assert_allclose(
            [np.min(points, axis=0), np.max(points, axis=0)], expected, atol=1e-8
        )
        qpos = model.qpos0.copy()
        qpos[0] += 0.1
        viewer.publish(qpos, [1])
        for handle, gids in viewer.batches:
            np.testing.assert_allclose(
                1 if handle.batched_opacities is None else handle.batched_opacities,
                model.geom_rgba[gids, 3],
            )
            np.testing.assert_allclose(
                handle.batched_positions, viewer.data.geom_xpos[gids], atol=1e-7
            )
        viewer.publish(qpos, [])
        for handle, gids in viewer.batches:
            np.testing.assert_allclose(
                handle.batched_positions, viewer.cad_positions[gids], atol=1e-7
            )
        assert model.opt.disableflags == flags
        np.testing.assert_array_equal(model.geom_contype, masks)
        np.testing.assert_array_equal(model.geom_rgba, rgba)
    finally:
        viewer.close()


@pytest.mark.integration
def test_browser_camera_context_and_reconnection(build, monkeypatch):
    from playwright.sync_api import sync_playwright

    result = build("1 4 0 0 0 1 0 0 0 1 0 0 0 1 cube.dat\n")
    with sync_playwright() as playwright:
        if not Path(playwright.chromium.executable_path).is_file():
            pytest.skip("Run uv run playwright install chromium for browser tests")
        viewer = BrowserViewer(result.spec.compile(), enabled_bodies=[])
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            # The packaged client must work without a CDN or hosted app.
            page.route(
                "**/*",
                lambda route: (
                    route.continue_() if route.request.url.startswith(viewer.url) else route.abort()
                ),
            )
            page.goto(viewer.url)
            page.get_by_text("Loading physics", exact=True).wait_for()
            page.locator("canvas[data-engine]").wait_for()
            deadline = time.monotonic() + 10
            while not viewer.connected and time.monotonic() < deadline:
                page.wait_for_timeout(50)
            assert viewer.connected
            client = next(iter(viewer.server.get_clients().values()))
            before = client.camera.position.copy()
            page.mouse.move(500, 350)
            deadline = time.monotonic() + 5
            while np.allclose(client.camera.position, before) and time.monotonic() < deadline:
                page.mouse.wheel(0, 150)
                page.wait_for_timeout(200)
            assert not np.allclose(client.camera.position, before)
            page.get_by_role("button", name="Frame model").click()
            page.wait_for_timeout(500)
            np.testing.assert_allclose(client.camera.look_at, viewer.center, atol=1e-6)
            page.get_by_label("Show unplaced parts").uncheck()
            page.wait_for_timeout(300)
            for handle, gids in viewer.batches:
                if np.any(viewer.model.geom_bodyid[gids] != 0):
                    assert np.all(handle.batched_scales[viewer.model.geom_bodyid[gids] != 0] == 0)
            viewer.publish(viewer.model.qpos0, [1], status="Paused")
            page.get_by_text("Paused", exact=True).wait_for()
            camera = client.camera.position.copy()
            viewer.set_scene(result.spec.compile(), enabled_bodies=[1])
            page.wait_for_timeout(300)
            np.testing.assert_allclose(client.camera.position, camera)
            page.reload()
            page.get_by_text("Loading physics", exact=True).wait_for()
            assert not errors
        finally:
            browser.close()
            viewer.close()
