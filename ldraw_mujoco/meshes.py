"""Shared MjSpec mesh assets, built in part-local coordinates for one import."""

from dataclasses import dataclass, field

import mujoco
import numpy as np
import trimesh
from ldraw import Colour

from .geometry import BASIS, LDU_TO_METERS, Surfaces, triangle_mesh


def _hull(triangles, reference):
    try:
        return trimesh.convex.convex_hull(triangles.reshape(-1, 3))
    except Exception as exc:
        raise ValueError(f"Cannot build 3D collision hull for {reference}: {exc}") from exc


@dataclass
class PartMeshes:
    collision: str
    # Extreme points of the full surface, studs included, for bounds and clearance.
    bounds_points: np.ndarray
    volume: float
    # BFC inversion changes only the winding of the visual faces.
    visuals: dict[bool, list[tuple[str, Colour]]] = field(default_factory=dict)


class MeshAssets:
    def __init__(self, spec, document):
        self.spec = spec
        self.surfaces = Surfaces(document)
        self.cache = {}

    def _add(self, name, mesh, inertia):
        self.spec.add_mesh(
            name=name,
            uservert=mesh.vertices.ravel(),
            userface=mesh.faces.ravel(),
            inertia=inertia,
        )

    def get(self, reference, bake, reverse):
        """Register one hull per shape and visual groups per requested winding."""
        key = reference, tuple(bake.flat)
        assets = self.cache.get(key)
        if assets is not None and reverse in assets.visuals:
            return assets

        surface = self.surfaces.get(reference)
        if not len(surface.triangles):
            raise ValueError(f"No surface geometry for {reference}")
        triangles = surface.triangles @ (BASIS @ bake).T * LDU_TO_METERS
        if assets is None:
            # A stud would start inside the filled hull of the part above and push it
            # away, so hulls skip studs; visual meshes keep them.
            solid = triangles if surface.studs.all() else triangles[~surface.studs]
            hull = _hull(solid, reference)
            name = f"mesh_{len(self.cache)}_hull"
            self._add(name, hull, mujoco.mjtMeshInertia.mjMESH_INERTIA_CONVEX)
            outline = hull if len(solid) == len(triangles) else _hull(triangles, reference)
            assets = PartMeshes(name, np.asarray(outline.vertices), float(hull.volume))
            self.cache[key] = assets

        groups = {}
        for index, colour in enumerate(surface.colours):
            groups.setdefault(colour, []).append(index)
        if reverse:
            triangles = triangles[:, ::-1]
        visuals = []
        for index, (colour, faces) in enumerate(groups.items()):
            name = f"{assets.collision}_visual_{int(reverse)}_{index}"
            self._add(
                name, triangle_mesh(triangles[faces]), mujoco.mjtMeshInertia.mjMESH_INERTIA_SHELL
            )
            visuals.append((name, colour))
        assets.visuals[reverse] = visuals
        return assets
