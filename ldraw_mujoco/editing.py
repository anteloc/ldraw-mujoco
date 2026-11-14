"""Type-1 editor fields and diagnostics; pyldraw3 still parses the placement."""

from __future__ import annotations

import math
import re
from bisect import bisect_right

import numpy as np
from ldraw.errors import PartError
from ldraw.part import colour_from_str, parse_ldraw_line

FIELDS = ("type", "colour", "x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "reference")
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


class EditError(ValueError):
    """A rejected field, with zero-based character offsets for the terminal caret."""

    def __init__(self, message, *, column, field_start, suggestion):
        super().__init__(message)
        self.column = column
        self.field_start = field_start
        self.suggestion = suggestion

    def display(self, line):
        column = len(line[: self.column].expandtabs())
        return f"{line.expandtabs()}\n{' ' * column}^\n{self}. {self.suggestion}"


def field_spans(line):
    """Editor boundaries only: the filename remainder may itself contain spaces."""
    tokens = list(re.finditer(r"\S+", line))
    spans = [(t.start(), t.end()) for t in tokens[:14]]
    if len(tokens) > 14:
        spans.append((tokens[14].start(), len(line.rstrip())))
    return spans


def validate_placement(line, *, original=None):
    """Validate editor field types, then delegate record parsing to pyldraw3."""
    spans = field_spans(line)

    def reject(index, message, suggestion, offset=0):
        start = spans[index][0] if index < len(spans) else len(line)
        raise EditError(message, column=start + offset, field_start=start, suggestion=suggestion)

    if "\n" in line or "\r" in line or "\x00" in line:
        reject(0, "Expected one placement line", "Remove the line break or NUL character")
    if len(spans) != 15:
        reject(
            len(spans),
            "Missing type-1 fields",
            "Provide colour, x y z, nine matrix values and a reference",
        )
    fields = [line[start:end] for start, end in spans]
    if fields[0] != "1":
        reject(0, "The instruction type must stay 1", "Edit the placement fields after 1")
    try:
        colour = colour_from_str(fields[1])
        if isinstance(colour, int) and colour < 0:
            raise ValueError("Negative colour code")
    except (PartError, ValueError):
        reject(
            1,
            "Invalid colour",
            "Use a nonnegative integer code, e.g. 4, or a direct colour such as 0x2FF0000",
        )
    for index in range(2, 14):
        value = fields[index]
        if not NUMBER.fullmatch(value):
            prefix = NUMBER.match(value)
            reject(
                index,
                f"{FIELDS[index]} is not a float",
                "Use one finite number, e.g. -12.5 or 1e-3",
                prefix.end() if prefix else 0,
            )
        if not math.isfinite(float(value)):
            reject(index, f"{FIELDS[index]} must be finite", "Use a smaller finite number")
    try:
        piece = parse_ldraw_line(line)
    except PartError as exc:
        reject(14, str(exc), "Provide a valid reference")
    if original is not None:
        original_fields = original.split(maxsplit=14)
        for index in (0, 1, 14):
            if fields[index] != original_fields[index]:
                reject(
                    index,
                    f"{FIELDS[index]} is read-only",
                    "Change only position and rotation values",
                )
    if abs(np.linalg.det(piece.matrix.rows)) < 1e-12:
        reject(
            5,
            "The transform matrix is singular",
            "Use an invertible matrix; identity is 1 0 0 0 1 0 0 0 1",
        )
    return piece


def editor_bindings():
    from prompt_toolkit.key_binding import KeyBindings

    bindings = KeyBindings()

    def move(event, direction):
        buffer = event.current_buffer
        starts = [token.start() for token in re.finditer(r"\S+", buffer.text)]
        if starts:
            current = max(0, bisect_right(starts, buffer.cursor_position) - 1)
            buffer.cursor_position = starts[(current + direction) % len(starts)]

    bindings.add("tab")(lambda event: move(event, 1))
    bindings.add("s-tab")(lambda event: move(event, -1))

    @bindings.add("escape")
    def cancel(event):
        event.app.exit(result=None)

    return bindings


async def edit_placement(program, ident, *, prompt=None, write=print):
    """Stage input until validation and scene preparation succeed, or discard it."""
    from prompt_toolkit import PromptSession
    from prompt_toolkit.document import Document
    from prompt_toolkit.layout.processors import AfterInput

    original = program.placement_line(ident)
    fields = original.split(maxsplit=14)
    prefix, suffix = f"1 {fields[1]} ", " " + fields[14]
    original_values = " ".join(fields[2:14])
    values, cursor = original_values, 0
    line = prefix + values + suffix
    if prompt is None:
        prompt = PromptSession().prompt_async
    bindings = editor_bindings()
    context = program.nodes[ident].get("context_comment")
    write(f"Editing {ident}: position and rotation only.")
    write("Tab/Shift+Tab: next/previous field. Enter: apply. Esc or Ctrl+C: cancel.")
    while True:
        try:
            # Fixed prefix/suffix stay outside the editable numeric buffer.
            text = values
            if context:
                write(context)
            edited = await prompt(
                prefix,
                default=Document(text, min(cursor, len(text))),
                key_bindings=bindings,
                input_processors=[AfterInput(suffix)],
            )
            if edited is None:
                break
            values = edited
            line = prefix + values + suffix
            if len(values.split()) != 12:
                raise EditError(
                    "Expected exactly 12 numeric values",
                    column=len(prefix) + len(values),
                    field_start=len(prefix),
                    suggestion="Provide x y z and nine matrix values",
                )
            validate_placement(line, original=original)
            return await program.edit(ident, original if edited == original_values else line)
        except EditError as exc:
            write(exc.display(line))
            cursor = max(0, exc.field_start - len(prefix))
            try:
                choice = await prompt("Edit the error or cancel? [e/c] ")
                while choice is not None and choice.strip().lower() not in {
                    "e",
                    "edit",
                    "",
                    "c",
                    "cancel",
                }:
                    choice = await prompt("Enter e to edit or c to cancel: ")
            except (EOFError, KeyboardInterrupt):
                break
            if choice is None or choice.strip().lower() in {"c", "cancel"}:
                break
        except (EOFError, KeyboardInterrupt):
            break
    write("Edit cancelled: the line is reverted to its value before this edit.")
    write(original)
    return None
