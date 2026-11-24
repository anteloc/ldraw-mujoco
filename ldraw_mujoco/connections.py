"""Mated LDraw connections between placed parts, reduced to rigid, hinge or ball links.

pyldraw3 owns the connection features (primitives and LDCad shadow metas) and
their matching. This module places the features of each occurrence, keeps the
matches pyldraw3 confirms, and decides how two bodies are joined. Everything
here is in LDraw world coordinates (LDU, Y down). The importer turns links into
MuJoCo bodies and joints.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, replace

import networkx as nx
import numpy as np
from ldraw import (
    ConnectionContact,
    ConnectionFreedom,
    ConnectionKind,
    ConnectionSource,
    ConnectionStatus,
    CylindricalProfile,
    Matrix,
    ModelInspection,
    OccurrenceAttribution,
    OccurrenceGeometry,
    SectionShape,
    Vector,
)
from ldraw.inspection import transformed_bounds
from networkx.utils import UnionFind

from .geometry import normalized, vector

# Assumption: clutch (studs) and press fits (tyres on rims) never move or break.
RIGID_KINDS = frozenset(
    {
        ConnectionKind.STUD,
        ConnectionKind.STUD_RECEPTACLE,
        ConnectionKind.RIM_SEAT,
        ConnectionKind.TYRE_BEAD,
    }
)
# Cross-sections that cannot turn inside one another: Technic axles, square pegs.
ROLL_LOCKED = frozenset({SectionShape.AXLE, SectionShape.SQUARE})
# Deviation of a source matrix from a rotation that still counts as rounding.
ROUNDING = 1e-2
# How far mated connectors may be apart (LDU). pyldraw3's default, 0.25, misses
# rounded placements such as 0.33 LDU in 6399-1; studs are 20 LDU apart.
TOLERANCE = 0.5
# Hinge contacts between two bodies share one axis: pyldraw3's 2 degree angular
# tolerance and 1 LDU (0.4 mm) from the axis line.
PARALLEL = np.cos(np.radians(2.0))
COLLINEAR = 1.0
# Rigid links join bodies first, so rigidly connected parts form one cluster.
PRIORITY = {"rigid": 0, "hinge": 1, "ball": 2}

LDCAD = frozenset({ConnectionSource.LDCAD_SHADOW, ConnectionSource.LDCAD_INLINE})
# A proper rotation that reverses a feature's +Y axis.
REVERSE = Matrix([[1, 0, 0], [0, -1, 0], [0, 0, -1]])


@dataclass(frozen=True, eq=False)
class Link:
    """How two bodies are joined, in LDraw world coordinates (LDU)."""

    kind: str  # "rigid", "hinge" or "ball"
    point: np.ndarray  # A point on the hinge axis, or the ball center.
    axis: np.ndarray  # Unit hinge axis; unused by rigid and ball links.
    contacts: tuple[ConnectionContact, ...]  # pyldraw3's evidence.


def mated_contacts(parts, occurrences, skip=frozenset()):
    """All contacts pyldraw3 finds between placed library parts.

    ``occurrences`` are pyldraw3 ``ModelOccurrence`` objects; contact
    occurrence indices are positions in that list. References in ``skip``
    (document-local DATs) have no library connectors.
    """
    placed = tuple(
        _placed(index, occurrence, parts)
        for index, occurrence in enumerate(occurrences)
        if normalized(occurrence.reference) not in skip
    )
    inspection = ModelInspection(
        bounds=None,
        occurrences=placed,
        skipped_geometry=(),
        diagnostics=(),
        occurrence_count=len(occurrences),
    )
    return inspection.connection_contacts(tolerance=TOLERANCE)


def body_links(contacts, body_of):
    """One link per pair of bodies joined by confirmed contacts.

    ``body_of[i]`` is the body index of occurrence ``i``. Contacts within one
    body and unconfirmed (heuristic-only) contacts are ignored.
    """
    pairs = {}
    for contact in contacts:
        if contact.status is not ConnectionStatus.CONFIRMED:
            continue
        a = body_of[contact.first_occurrence.index]
        b = body_of[contact.second_occurrence.index]
        if a != b:
            pairs.setdefault((min(a, b), max(a, b)), []).append(_link(contact))
    return {pair: _combine(links) for pair, links in sorted(pairs.items())}


def forest(count, links):
    """Choose which links form the body trees; the remaining ones close loops.

    Rigid links are taken first, so rigidly connected bodies always form one
    exactly rigid cluster, and a joint inside a cluster is locked and dropped.
    A joint between two clusters that other links already join closes a loop.
    Each tree is rooted at its lowest body index.

    Returns ``(tree, loops)``. ``tree`` lists ``(body, parent, link)`` with
    parents first; roots have ``parent`` and ``link`` set to ``None``. ``loops``
    lists ``(a, b, link)``.
    """
    # Kruskal's algorithm in an explicit, deterministic order: rigid first, then by pair.
    joined, rigid = UnionFind(range(count)), UnionFind(range(count))
    graph = nx.Graph()
    graph.add_nodes_from(range(count))
    loops = []
    for (a, b), link in sorted(links.items(), key=lambda item: (PRIORITY[item[1].kind], item[0])):
        if joined[a] != joined[b]:
            joined.union(a, b)
            if link.kind == "rigid":
                rigid.union(a, b)
            graph.add_edge(a, b, link=link)
        elif rigid[a] != rigid[b]:
            loops.append((a, b, link))
    tree = []
    for root in sorted(min(component) for component in nx.connected_components(graph)):
        tree.append((root, None, None))
        tree.extend(
            (child, parent, graph.edges[parent, child]["link"])
            for parent, child in nx.bfs_edges(graph, root)
        )
    return tree, loops


def _link(contact):
    """One mated pair: rigid, a hinge about the feature axis, or a ball.

    LDCad's slide option is an editing aid, not a physical freedom: friction
    holds the axial position, so links never slide.
    """
    first, second = contact.first, contact.second
    freedoms = first.freedoms | second.freedoms
    if {first.kind, second.kind} & RIGID_KINDS or (_roll_locked(first) and _roll_locked(second)):
        kind = "rigid"
    elif ConnectionFreedom.FREE_ROTATE in freedoms:
        kind = "ball"
    elif freedoms & {ConnectionFreedom.ROTATE, ConnectionFreedom.DISCRETE_ROTATE}:
        kind = "hinge"
    else:
        kind = "rigid"
    return Link(kind, vector(first.position), vector(first.axis), (contact,))


def _roll_locked(feature):
    profile = feature.profile
    return isinstance(profile, CylindricalProfile) and profile.primary_shape in ROLL_LOCKED


def _combine(links):
    """All links between two bodies: a shared hinge axis or ball center keeps
    the joint. Anything else, such as two pins on different axes, is rigid."""
    contacts = tuple(contact for link in links for contact in link.contacts)
    rigid = Link("rigid", links[0].point, links[0].axis, contacts)
    if any(link.kind == "rigid" for link in links):
        return rigid
    hinges = [link for link in links if link.kind == "hinge"]
    if hinges:
        point, axis = hinges[0].point, hinges[0].axis
        aligned = all(abs(axis @ hinge.axis) >= PARALLEL for hinge in hinges)
        on_axis = all(
            np.linalg.norm(np.cross(link.point - point, axis)) <= COLLINEAR for link in links
        )
        return replace(hinges[0], contacts=contacts) if aligned and on_axis else rigid
    center = links[0].point
    if all(np.linalg.norm(link.point - center) <= COLLINEAR for link in links):
        return replace(links[0], contacts=contacts)
    return rigid


def _placed(index, occurrence, parts):
    """pyldraw3's placed occurrence, like ``inspect_model`` produces it.

    Bounds come from the 8 corners of the part's local box instead of every
    expanded point, which dominates ``inspect_model``'s time. They only guide
    pyldraw3's search for candidate pairs.
    """
    local = parts.geometry(occurrence.part_code)  # Cached per part by pyldraw3.
    matrix = _rotation(occurrence.matrix)
    low, high = local.bounds.min, local.bounds.max
    corners = [
        Vector(x, y, z)
        for x, y, z in itertools.product((low.x, high.x), (low.y, high.y), (low.z, high.z))
    ]
    return OccurrenceGeometry(
        attribution=OccurrenceAttribution(
            index=index,
            occurrence=occurrence,
            model_path=(),
            reference_path=(),
            source_line_path=(),
            local_step_path=(),
            effective_step_path=(),
            page_path=(),
        ),
        local=local,
        bounds=transformed_bounds(corners, position=occurrence.position, matrix=matrix),
        studs=(),
        connections=tuple(
            _socket(feature).transformed(position=occurrence.position, matrix=matrix)
            for feature in local.connections
        ),
    )


def _rotation(matrix):
    """The nearest rotation (or reflection) to a rounded source matrix.

    Workaround for pyldraw3 1.7.0, remove once it tolerates rounding: authored
    (LDCad) features on a placement more than 1e-6 from orthonormal get zero
    confidence, and rounded rotations in real models routinely are. Real scale
    or shear is kept, and still voids them.
    """
    rows = np.array(matrix.rows, dtype=float)
    u, _, vt = np.linalg.svd(rows)
    nearest = u @ vt
    return Matrix(nearest.tolist()) if np.abs(rows - nearest).max() <= ROUNDING else matrix


def _socket(feature):
    """An LDCad stud socket in pyldraw3's stud convention, same physical extent.

    Workaround for pyldraw3 1.7.0, remove once it reads LDCad sockets: LDCad
    authors a stud and its socket along the same axis, while pyldraw3's strict
    stud check wants the socket axis opposing the stud. pyldraw3 also never
    seats a round stud in LDCad's square sockets (1 x N plates and bricks).
    """
    profile = feature.profile
    if (
        feature.kind is not ConnectionKind.STUD_RECEPTACLE
        or feature.source not in LDCAD
        or not isinstance(profile, CylindricalProfile)
    ):
        return feature
    sections = tuple(
        replace(section, shape=SectionShape.ROUND)
        if section.shape is SectionShape.SQUARE
        else section
        for section in profile.sections
    )
    return replace(
        feature,
        position=(
            feature.position
            if feature.centered
            else feature.position + feature.axis * feature.length
        ),
        frame=feature.frame * REVERSE,
        profile=replace(profile, sections=sections),
    )
