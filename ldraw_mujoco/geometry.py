"""Adapt pyldraw3's parsed records to triangle surfaces, without a second parser."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
from ldraw import Colour, Model, Piece, read_model
from ldraw.errors import PartError, PartNotFoundError
from ldraw.lines import Comment, MetaCommand, Quadrilateral, Triangle

from .editing import validate_placement

LDU_TO_METERS = 0.0004
# A proper rotation: determinant +1, LDraw -Y becomes MuJoCo +Z.
BASIS = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=float)


def to_mujoco(point):
    """An LDraw point in LDU as a MuJoCo point in meters: ``0.0004 * (x, z, -y)``."""
    return BASIS @ point * LDU_TO_METERS


def normalized(name):
    return name.replace("\\", "/").casefold()


def vector(v):
    return np.array([v.x, v.y, v.z], dtype=float)


def within(instance_id, ancestor):
    """Whether an occurrence ID is ``ancestor`` itself or one of its descendants."""
    return instance_id == ancestor or instance_id.startswith(ancestor + "/")


def is_stud(reference):
    """pyldraw3's rule (part_geometry._STUD_PREFIX): a file stem starting with "stud"."""
    return Path(normalized(reference)).name.startswith("stud")


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
                result.add(obj)  # pyldraw3 pieces hash by identity.
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
        self.reference_aliases = {}
        self.origins = {}
        self.files = set()
        self.source_lines = {}
        self.placement_overrides = dict(placement_overrides or {})
        self.inverted = set()
        self.root = self._read(self.path)
        self._discover(self.root, set())
        self.inline_pieces = set()
        self._collect_inline_faces()
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
        for ident, text in self.placement_overrides.items():
            node = self.instances.get(ident)
            if node is None or node["kind"] == "model" or node.get("generated"):
                raise ValueError(f"Edit requires a type-1 occurrence ID: {ident!r}")
            validate_placement(text, original=node["source_text"])
            node["source_text"] = text
        self.selected_ids = self._select(sections)

    def _index(self, model, parent, visiting):
        """Index parsed placements, stopping at DAT boundaries (including shortcuts)."""
        key = normalized(model.name)
        if key in visiting:
            raise ValueError("Assembly reference cycle: " + " -> ".join((*visiting, key)))
        for index, piece in enumerate(model.pieces):
            generated = piece in self.inline_pieces
            if generated:
                index = "inline"
            self.piece_indices[piece] = index
            instance_id = str(index) if parent == "root" else f"{parent}/{index}"
            child = self.view.submodels.get(normalized(piece.reference))
            source = self.path if model is self.view else self.origins[model]
            line = model.source_line_for(piece)
            self.instances[instance_id] = {
                "id": instance_id,
                "parent_id": parent,
                "kind": "submodel" if child is not None else "part",
                "reference": piece.reference,
                "section": self.root.name if model is self.view else model.name,
                "source_file": str(source),
                "line": line,
                "context_comment": (
                    self.source_lines[source][line - 2]
                    if line
                    and line > 1
                    and self.source_lines[source][line - 2].lstrip().startswith("0 //")
                    else None
                ),
                "source_text": self.source_lines[source][line - 1] if line else str(piece),
            }
            if generated:
                self.instances[instance_id]["generated"] = "inline_faces"
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
            selected == "root" or within(instance_id, selected) for selected in self.selected_ids
        )

    def occurrence_id(self, occurrence):
        return "/".join(str(self.piece_indices[p.piece]) for p in occurrence.path)

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
        self.origins[model] = path  # pyldraw3 models hash by identity.

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
        if model in visited:
            return  # Instance indexing / surface expansion reports actual cycles.
        visited.add(model)
        for obj in model.objects:
            if isinstance(obj, MetaCommand) and obj.type.upper() in {"TEXMAP", "DATA"}:
                raise ValueError(
                    f"Unsupported !{obj.type} in {model.name}; use geometry-based patterns"
                )
        for piece in model.pieces:
            key = normalized(piece.reference)
            target = self.models.get(key)
            if target is None:
                local = self.origins[model].parent / piece.reference.replace("\\", "/")
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
        except PartNotFoundError as exc:
            # Some MPDs namespace their embedded DATs but leave a placement
            # unqualified. Only recover an absent exact reference, never replace
            # existing library geometry or hide a malformed part.
            key = normalized(reference)
            matches = [
                m
                for m in dict.fromkeys(self.models.values())
                if key.endswith(".dat") and normalized(m.name).endswith(" - " + key)
            ]
            if len(matches) > 1:
                choices = ", ".join(sorted(m.name for m in matches))
                raise ValueError(f"Ambiguous embedded DAT for {reference!r}: {choices}") from exc
            if matches:
                model = matches[0]
                self.models[key] = model
                self.reference_aliases[reference] = model.name
                return model.objects
            raise ValueError(f"Cannot resolve geometry {reference!r}: {exc}") from exc
        except (PartError, OSError, ValueError) as exc:
            raise ValueError(f"Cannot resolve geometry {reference!r}: {exc}") from exc

    def _collect_inline_faces(self):
        """Wrap parsed assembly surfaces in private DAT leaves; never rewrite sources.

        Keep all non-reference records in order so BFC state and face colours
        survive. References remain in their original assembly and retain their IDs.
        """
        for model in list(dict.fromkeys(self.models.values())):
            if model.name.casefold().endswith(".dat") or not any(
                isinstance(obj, (Triangle, Quadrilateral)) for obj in model.objects
            ):
                continue
            name = f"{model.name}.inline.dat"
            while normalized(name) in self.models:
                name = "_" + name
            inline = Model(
                name=name,
                objects=[obj for obj in model.objects if not isinstance(obj, Piece)],
            )
            self._register(name, inline, self.origins[model])
            piece = Piece.place(name, colour=16)
            self.inline_pieces.add(piece)
            model.objects = [
                obj for obj in model.objects if not isinstance(obj, (Triangle, Quadrilateral))
            ] + [piece]

    def occurrences(self):
        """Selected physical occurrences, with session placement overrides applied."""
        result = []
        try:
            for occurrence in self.view.iter_occurrences():
                ident = self.occurrence_id(occurrence)
                if not self.included(ident):
                    continue
                if any(within(ident, key) for key in self.placement_overrides):
                    occurrence = self._edited_occurrence(occurrence)
                result.append(occurrence)
        except PartError as exc:
            raise ValueError(f"Cannot expand {self.path}: {exc}") from exc
        return result

    def _edited_occurrence(self, occurrence):
        """Expand a private path through pyldraw3; repeated source instances stay untouched."""
        path = []
        indices = []
        for item in occurrence.path:
            indices.append(str(self.piece_indices[item.piece]))
            ident = "/".join(indices)
            piece = (
                validate_placement(self.placement_overrides[ident])
                if ident in self.placement_overrides
                else item.piece
            )
            self.piece_indices[piece] = self.piece_indices[item.piece]
            if item.piece in self.inverted:
                self.inverted.add(piece)
            path.append(replace(item, piece=piece))
        piece = path[-1].piece
        # A short private model chain lets pyldraw3 compose all ancestor affine
        # transforms and inherited colours, without mutating the source graph.
        root = current = Model(name="edit-root.ldr")
        for index, item in enumerate(path[:-1]):
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
        return replace(
            occurrence,
            piece=piece,
            part_code=piece.part,
            reference=piece.reference,
            colour=expanded.colour,
            position=expanded.position,
            matrix=expanded.matrix,
            path=tuple(path),
        )


@dataclass
class Surface:
    triangles: np.ndarray
    colours: tuple[Colour, ...]
    # True for faces reached through a stud primitive; collision hulls skip them.
    studs: np.ndarray


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
        triangles, colours, studs = [], [], []
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
                    studs.append(False)
            elif isinstance(obj, Piece):
                child = self.get(obj.reference, (*visiting, key))
                matrix, position = np.array(obj.matrix.rows), vector(obj.position)
                check_transform(matrix, position, reference)
                transformed = child.triangles @ matrix.T + position
                if (np.linalg.det(matrix) < 0) != (obj in inverted):
                    transformed = transformed[:, ::-1]
                triangles.extend(transformed)
                colours.extend(obj.colour if c.code == 16 else c for c in child.colours)
                studs.extend([True] * len(child.studs) if is_stud(obj.reference) else child.studs)
        surface = Surface(
            np.array(triangles).reshape(-1, 3, 3), tuple(colours), np.array(studs, dtype=bool)
        )
        self.cache[key] = surface
        return surface
