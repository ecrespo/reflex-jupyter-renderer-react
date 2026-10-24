"""Typed, dependency-free builders for the Jupyter ``nbformat`` notebook shape.

These helpers let you construct a notebook (or load one from disk) in pure Python
and hand the resulting ``dict`` to :class:`JupyterNotebookViewer`. They mirror the
relevant subset of the `nbformat v4 schema
<https://nbformat.readthedocs.io/en/latest/format_description.html>`_ that the
``jupyter-renderer-react`` viewer understands.

This module deliberately imports nothing from Reflex so the data layer stays
usable for tooling and unit tests even when Reflex is not installed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

__all__ = [
    "Output",
    "stream_output",
    "display_data_output",
    "execute_result_output",
    "error_output",
    "CodeCell",
    "MarkdownCell",
    "RawCell",
    "Notebook",
    "load_notebook",
    "notebook_from_url",
]

# A source can be a single string or a list of lines (both are valid nbformat).
Source = Union[str, list]


def _norm_source(source: Source) -> Union[str, list]:
    """Return source as-is (string or list of lines), both accepted by nbformat."""
    return source


# --------------------------------------------------------------------------- #
# Outputs
# --------------------------------------------------------------------------- #
@dataclass
class Output:
    """A raw cell output already shaped as an nbformat output dict."""

    data: dict

    def to_dict(self) -> dict:
        return dict(self.data)


def stream_output(text: Source, name: str = "stdout") -> dict:
    """A ``stream`` output (stdout/stderr text)."""
    return {"output_type": "stream", "name": name, "text": _norm_source(text)}


def display_data_output(data: dict, metadata: dict | None = None) -> dict:
    """A ``display_data`` output, e.g. ``{"image/png": "<base64>"}``."""
    return {
        "output_type": "display_data",
        "data": data,
        "metadata": metadata or {},
    }


def execute_result_output(
    data: dict, execution_count: int | None = None, metadata: dict | None = None
) -> dict:
    """An ``execute_result`` output (the value of the last expression)."""
    return {
        "output_type": "execute_result",
        "data": data,
        "execution_count": execution_count,
        "metadata": metadata or {},
    }


def error_output(ename: str, evalue: str, traceback: list[str] | None = None) -> dict:
    """An ``error`` output (an exception raised by a code cell)."""
    return {
        "output_type": "error",
        "ename": ename,
        "evalue": evalue,
        "traceback": traceback or [],
    }


# --------------------------------------------------------------------------- #
# Cells
# --------------------------------------------------------------------------- #
@dataclass
class CodeCell:
    """A code cell with optional outputs."""

    source: Source
    execution_count: int | None = None
    outputs: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "cell_type": "code",
            "execution_count": self.execution_count,
            "metadata": dict(self.metadata),
            "source": _norm_source(self.source),
            "outputs": [dict(o) for o in self.outputs],
        }


@dataclass
class MarkdownCell:
    """A markdown cell."""

    source: Source
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "cell_type": "markdown",
            "metadata": dict(self.metadata),
            "source": _norm_source(self.source),
        }


@dataclass
class RawCell:
    """A raw cell (rendered verbatim)."""

    source: Source
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "cell_type": "raw",
            "metadata": dict(self.metadata),
            "source": _norm_source(self.source),
        }


Cell = Union[CodeCell, MarkdownCell, RawCell]


# --------------------------------------------------------------------------- #
# Notebook
# --------------------------------------------------------------------------- #
@dataclass
class Notebook:
    """A minimal nbformat v4 notebook builder."""

    cells: list[Cell] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    nbformat: int = 4
    nbformat_minor: int = 4

    def add(self, cell: Cell) -> "Notebook":
        """Append a cell and return ``self`` for chaining."""
        self.cells.append(cell)
        return self

    def to_dict(self) -> dict:
        return {
            "cells": [c.to_dict() for c in self.cells],
            "metadata": dict(self.metadata),
            "nbformat": self.nbformat,
            "nbformat_minor": self.nbformat_minor,
        }

    def to_json(self, *, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def load_notebook(path: Union[str, Path]) -> dict:
    """Read a ``.ipynb`` file from disk and return its parsed ``dict``."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def notebook_from_url(url: str, **fetch_options: Any) -> dict:
    """Build the ``{"filePath": url}`` reference understood by the viewer.

    Note: ``fetch_options`` are accepted for symmetry but should be passed to the
    component's ``fetch_options`` prop, not embedded in the notebook reference.
    """
    ref: dict[str, Any] = {"filePath": url}
    return ref
