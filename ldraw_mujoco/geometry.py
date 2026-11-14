"""Adapt pyldraw3's parsed records to triangle surfaces, without a second parser."""

from __future__ import annotations

import hashlib
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

    def __init__(self, path, parts=None, sections=None, placement_overrides=None):
        self.path = Path(path).resolve()
        if self.path.suffix.casefold() not in {".mpd", ".ldr", ".dat"}:
            raise ValueError("Input must be an .mpd, .ldr or .dat file")
        self.parts = parts
        self.models = {}
        self.origins = {}
        self.files = set()
        self.source_lines = {}
        self.placement_overrides = dict(placement_overrides or {})
        self.inverted = set()
        self.root = self._read(self.path)
        self._discover(self.root, set())
        self.available_sections = list(
            dict.fromkeys(
                m.name
                for m in self.models.values()
                if m is self.root or not m.name.casefold().endswith(".dat")
            )
        )
        assemblies = {k: m for k, m in self.models.items() if not k.endswith(".dat")}
        if self.path.suffix.casefold() == ".dat":
            # A DAT's subparts are geometry, not separate manufactured pieces.
            self.view = Model(
                name="import-root.ldr", objects=[Piece.place(self.root.name, colour=7)]
            )
        else:
            self.view = replace(self.root)
        self.view.submodels = assemblies
        self.instances = {
            "root": {
                "id": "root",
                "parent_id": None,
                "kind": "model",
                "reference": self.root.name,
                "section": self.root.name,
                "source_file": str(self.path),
                "line": None,
            }
        }
        self.piece_indices = {}
        self._index(self.view, "root", ())
        for ident in self.placement_overrides:
            if ident not in self.instances or self.instances[ident]["kind"] != "part":
                raise ValueError(f"Edit requires a physical part occurrence ID: {ident!r}")
        self.selected_ids = self._select(sections)

    def _index(self, model, parent, visiting):
        """Index parsed placements, stopping at DAT boundaries (including shortcuts)."""
        key = normalized(model.name)
        if key in visiting:
            raise ValueError("Assembly reference cycle: " + " -> ".join((*visiting, key)))
        for index, piece in enumerate(model.pieces):
            self.piece_indices[id(piece)] = index
            instance_id = str(index) if parent == "root" else f"{parent}/{index}"
            child = self.view.submodels.get(normalized(piece.reference))
            source = self.path if model is self.view else self.origins[id(model)]
            line = model.source_line_for(piece)
            self.instances[instance_id] = {
                "id": instance_id,
                "parent_id": parent,
                "kind": "submodel" if child is not None else "part",
                "reference": piece.reference,
                "section": self.root.name if model is self.view else model.name,
                "source_file": str(source),
                "line": line,
                "source_text": self.source_lines[source][line - 1] if line else str(piece),
            }
            if child is not None:
                self._index(child, instance_id, (*visiting, key))

    def _select(self, sections):
        selectors = [sections] if isinstance(sections, str) else sections
        if not selectors:
            return ["root"]
        selected = []
        for selector in selectors:
            name, separator, instance_id = selector.rpartition(":")
            if separator:
                if not name or not instance_id:
                    raise ValueError(f"Invalid selector {selector!r}; expected SECTION:ID")
                node = self.instances.get(instance_id)
                if node is None:
                    raise ValueError(
                        f"Unknown instance ID {instance_id!r} for section {name!r}. "
                        "Use inspect to list instance IDs."
                    )
                if node["kind"] == "part":
                    raise ValueError(f"{selector!r} identifies a part; select a model or submodel")
                if normalized(node["reference"]) != normalized(name):
                    raise ValueError(
                        f"Instance {instance_id!r} belongs to section {node['reference']!r}, "
                        f"not {name!r}; use {node['reference'] + ':' + instance_id!r}"
                    )
                matches = [node["id"]]
            else:
                matches = [
                    n["id"]
                    for n in self.instances.values()
                    if n["kind"] != "part" and normalized(n["reference"]) == normalized(selector)
                ]
            if not matches:
                if selector in self.instances:
                    reference = self.instances[selector]["reference"]
                    raise ValueError(
                        f"Bare instance IDs are not accepted; use SECTION:ID, "
                        f"for example {reference + ':' + selector!r}"
                    )
                if normalized(selector) in self.models:
                    raise ValueError(f"Section {selector!r} has no placements in the root model")
                raise ValueError(
                    f"Unknown section or instance {selector!r}. "
                    f"Available sections: {', '.join(self.available_sections)}. "
                    "Use inspect to list instance IDs."
                )
            if len(matches) > 1:
                choices = ", ".join(f"{self.instances[i]['reference']}:{i}" for i in matches)
                raise ValueError(f"Ambiguous section {selector!r}: use SECTION:ID: {choices}")
            if matches[0] not in selected:
                selected.append(matches[0])
        return selected

    def included(self, instance_id):
        return any(
            selected == "root" or instance_id == selected or instance_id.startswith(selected + "/")
            for selected in self.selected_ids
        )

    def occurrence_id(self, occurrence):
        return "/".join(str(self.piece_indices[id(p.piece)]) for p in occurrence.path)

    def inventory(self):
        """JSON inventory requires source files only, not meshes or a parts library."""
        return {
            "source": str(self.path),
            "source_sha256": hashlib.sha256(self.path.read_bytes()).hexdigest(),
            "source_dependencies": {
                str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(self.files)
            },
            "root_section": self.root.name,
            "available_sections": self.available_sections,
            "instances": list(self.instances.values()),
        }

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
        self.source_lines[path] = path.read_text(encoding="utf-8-sig").splitlines()
        for model in (root, *root.submodels.values()):
            self._register(model.name, model, path)
            # Reference ownership must survive filtering selected occurrences.
            self.inverted.update(inverted_pieces(model.objects))
        if alias and normalized(alias) != normalized(root.name):
            self._register(alias, root, path)
        return root

    def _discover(self, model, visited):
        if id(model) in visited:
            return  # Instance indexing / surface expansion reports actual cycles.
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
            return [
                self._edited_occurrence(o)
                if self.occurrence_id(o) in self.placement_overrides
                else o
                for o in self.view.iter_occurrences()
                if self.included(self.occurrence_id(o))
            ]
        except PartError as exc:
            raise ValueError(f"Cannot expand {self.path}: {exc}") from exc

    def _edited_occurrence(self, occurrence):
        """Expand a private path through pyldraw3; repeated source instances stay untouched."""
        from .editing import validate_placement

        ident = self.occurrence_id(occurrence)
        line = self.placement_overrides[ident]
        piece = validate_placement(line)
        # A short private model chain lets pyldraw3 compose all ancestor affine
        # transforms and inherited colours, without mutating the source graph.
        root = current = Model(name="edit-root.ldr")
        for index, item in enumerate(occurrence.path[:-1]):
            name = f"edit-ancestor-{index}.ldr"
            child = Model(name=name)
            current.objects = [
                Piece.place(
                    name,
                    colour=item.piece.colour,
                    position=item.piece.position,
                    matrix=item.piece.matrix,
                )
            ]
            root.submodels[normalized(name)] = child
            current = child
        current.objects = [piece]
        expanded = next(root.iter_occurrences())
        original = occurrence.path[-1]
        self.piece_indices[id(piece)] = self.piece_indices[id(original.piece)]
        if id(original.piece) in self.inverted:
            self.inverted.add(id(piece))
        # Resolve a newly selected local DAT through the same discovery path.
        self.origins[id(current)] = self.origins.get(id(original.model), self.path)
        self._discover(current, set())
        self.instances[ident].update(reference=piece.reference, source_text=line)
        return replace(
            occurrence,
            piece=piece,
            part_code=piece.part,
            reference=piece.reference,
            colour=expanded.colour,
            position=expanded.position,
            matrix=expanded.matrix,
            path=(*occurrence.path[:-1], replace(original, piece=piece)),
        )


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
