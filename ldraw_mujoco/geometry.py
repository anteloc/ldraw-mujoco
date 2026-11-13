"""Adapt pyldraw3's parsed records to triangle surfaces, without a second parser."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import trimesh
from ldraw import Colour, Model, Piece, read_model
from ldraw.errors import PartError
from ldraw.lines import Comment, MetaCommand, Quadrilateral, Triangle

LDU_TO_METERS = 0.0004
# A proper rotation: determinant +1, LDraw -Y becomes MuJoCo +Z.
BASIS = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=float)


def normalized(name):
    return name.replace("\\", "/").casefold()


def vector(v):
    return np.array([v.x, v.y, v.z], dtype=float)


def check_transform(matrix, position, context):
    if not np.isfinite(matrix).all() or not np.isfinite(position).all():
        raise ValueError(f"Non-finite transform in {context}")
    if abs(np.linalg.det(matrix)) < 1e-12:
        raise ValueError(f"Singular transform in {context}")


def inverted_pieces(objects):
    """BFC INVERTNEXT applies to the next reference, not the entire section."""
    result, pending = set(), False
    for obj in objects:
        if isinstance(obj, Comment) and obj.text.upper().split() == ["BFC", "INVERTNEXT"]:
            pending = True
        elif isinstance(obj, Piece):
            if pending:
                result.add(id(obj))
            pending = False
    return result


class Document:
    """MPD namespace and local dependencies, with .dat files as physical leaves."""

    def __init__(self, path, parts):
        self.path = Path(path).resolve()
        self.parts = parts
        self.models = {}
        self.origins = {}
        self.files = set()
        self.root = self._read(self.path)
        self._discover(self.root, set())
        assemblies = {k: m for k, m in self.models.items() if not k.endswith(".dat")}
        if self.path.suffix.casefold() == ".dat":
            # A DAT's subparts are geometry, not separate manufactured pieces.
            self.view = Model(
                name="import-root.ldr", objects=[Piece.place(self.root.name, colour=7)]
            )
        else:
            self.view = replace(self.root)
        self.view.submodels = assemblies
        self.inverted = set().union(*(inverted_pieces(m.objects) for m in self.models.values()))

    def _register(self, name, model, path):
        key = normalized(name)
        previous = self.models.get(key)
        if previous is not None and previous is not model:
            raise ValueError(f"Ambiguous reference {name!r} in {path}")
        self.models[key] = model
        self.origins[id(model)] = path

    def _read(self, path, alias=None):
        try:
            root = read_model(path)
        except PartError as exc:
            raise ValueError(f"Cannot parse {path}: {exc}") from exc
        self.files.add(path)
        for model in (root, *root.submodels.values()):
            self._register(model.name, model, path)
        if alias and normalized(alias) != normalized(root.name):
            self._register(alias, root, path)
        return root

    def _discover(self, model, visited):
        if id(model) in visited:
            return  # pyldraw3 traversal / surface expansion reports actual cycles.
        visited.add(id(model))
        for obj in model.objects:
            if isinstance(obj, MetaCommand) and obj.type.upper() in {"TEXMAP", "DATA"}:
                raise ValueError(
                    f"Unsupported !{obj.type} in {model.name}; use geometry-based patterns"
                )
        for piece in model.pieces:
            key = normalized(piece.reference)
            target = self.models.get(key)
            if target is None:
                local = self.origins[id(model)].parent / piece.reference.replace("\\", "/")
                if local.is_file():
                    target = self._read(local.resolve(), alias=piece.reference)
                elif not key.endswith(".dat"):
                    raise ValueError(
                        f"Missing model {piece.reference!r} referenced by {model.name}"
                    )
            if target is not None:
                self._discover(target, visited)

    def objects(self, reference):
        model = self.models.get(normalized(reference))
        if model is not None:
            return model.objects
        try:
            part = self.parts.part(code=normalized(reference).removesuffix(".dat"))
            self.files.add(part.path.resolve())
            return tuple(part.objects)
        except (PartError, OSError, ValueError) as exc:
            raise ValueError(f"Cannot resolve geometry {reference!r}: {exc}") from exc

    def occurrences(self):
        for model in self.models.values():
            if not model.name.casefold().endswith(".dat") and any(
                isinstance(obj, (Triangle, Quadrilateral)) for obj in model.objects
            ):
                raise ValueError(
                    f"Inline faces in assembly {model.name}; place them in a .dat section"
                )
        try:
            return list(self.view.iter_occurrences())
        except PartError as exc:
            raise ValueError(f"Cannot expand {self.path}: {exc}") from exc


@dataclass
class Surface:
    triangles: np.ndarray
    colours: tuple[Colour, ...]


class Surfaces:
    """Cache part-local triangles; recursive primitive transforms remain affine."""

    def __init__(self, document):
        self.document = document
        self.cache = {}
        self.dropped_degenerate = 0

    def get(self, reference, visiting=()):
        key = normalized(reference)
        if key in visiting:
            raise ValueError("Geometry reference cycle: " + " -> ".join((*visiting, key)))
        if key in self.cache:
            return self.cache[key]
        objects = self.document.objects(reference)
        triangles, colours = [], []
        inverted = inverted_pieces(objects)
        clockwise = False
        for obj in objects:
            if isinstance(obj, Comment):
                tokens = obj.text.upper().split()
                if tokens and tokens[0] == "BFC":
                    if "CW" in tokens:
                        clockwise = True
                    elif "CCW" in tokens:
                        clockwise = False
            elif isinstance(obj, MetaCommand) and obj.type.upper() in {"TEXMAP", "DATA"}:
                raise ValueError(f"Unsupported !{obj.type} in {reference}")
            elif isinstance(obj, (Triangle, Quadrilateral)):
                points = np.array([vector(p) for p in obj.points])
                if not np.isfinite(points).all():
                    raise ValueError(f"Non-finite vertex in {reference}")
                faces = [(0, 1, 2)] if isinstance(obj, Triangle) else [(0, 1, 2), (0, 2, 3)]
                for face in faces:
                    tri = points[list(face)]
                    if np.linalg.norm(np.cross(tri[1] - tri[0], tri[2] - tri[0])) < 1e-10:
                        self.dropped_degenerate += 1
                        continue
                    triangles.append(tri[::-1] if clockwise else tri)
                    colours.append(obj.colour)
            elif isinstance(obj, Piece):
                child = self.get(obj.reference, (*visiting, key))
                matrix, position = np.array(obj.matrix.rows), vector(obj.position)
                check_transform(matrix, position, reference)
                transformed = child.triangles @ matrix.T + position
                if (np.linalg.det(matrix) < 0) != (id(obj) in inverted):
                    transformed = transformed[:, ::-1]
                triangles.extend(transformed)
                colours.extend(obj.colour if c.code == 16 else c for c in child.colours)
        surface = Surface(np.array(triangles).reshape(-1, 3, 3), tuple(colours))
        self.cache[key] = surface
        return surface


def triangle_mesh(triangles):
    mesh = trimesh.Trimesh(
        vertices=triangles.reshape(-1, 3),
        faces=np.arange(triangles.size // 3).reshape(-1, 3),
        process=True,
    )
    # MuJoCo requires at least four vertices even for a zero-mass visual patch.
    # Subdivision preserves a single triangle exactly, without adding thickness.
    if len(mesh.vertices) < 4:
        mesh = mesh.subdivide()
    return mesh
