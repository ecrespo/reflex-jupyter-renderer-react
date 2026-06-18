"""Tests for the dependency-free notebook data model."""

import json

from reflex_jupyter_renderer_react.models import (
    CodeCell,
    MarkdownCell,
    Notebook,
    RawCell,
    error_output,
    execute_result_output,
    load_notebook,
    notebook_from_url,
    stream_output,
)


def test_notebook_to_dict_shape():
    nb = Notebook(
        cells=[MarkdownCell("# Title"), CodeCell("print(1)", execution_count=1)]
    )
    d = nb.to_dict()
    assert d["nbformat"] == 4
    assert d["nbformat_minor"] == 4
    assert isinstance(d["cells"], list) and len(d["cells"]) == 2
    assert d["cells"][0]["cell_type"] == "markdown"
    assert d["cells"][1]["cell_type"] == "code"
    assert d["cells"][1]["execution_count"] == 1


def test_code_cell_with_outputs():
    cell = CodeCell(
        "x",
        execution_count=2,
        outputs=[
            stream_output("hi\n"),
            execute_result_output({"text/plain": "1024"}, execution_count=2),
            error_output("ValueError", "boom", ["ValueError: boom"]),
        ],
    )
    d = cell.to_dict()
    assert len(d["outputs"]) == 3
    assert d["outputs"][0]["output_type"] == "stream"
    assert d["outputs"][1]["output_type"] == "execute_result"
    assert d["outputs"][2]["output_type"] == "error"


def test_raw_cell():
    assert RawCell("raw").to_dict()["cell_type"] == "raw"


def test_add_is_chainable():
    nb = Notebook().add(MarkdownCell("a")).add(MarkdownCell("b"))
    assert len(nb.cells) == 2


def test_to_json_roundtrip():
    nb = Notebook(cells=[MarkdownCell("# Hi")])
    parsed = json.loads(nb.to_json())
    assert parsed["cells"][0]["source"] == "# Hi"


def test_notebook_from_url():
    assert notebook_from_url("https://x/n.ipynb") == {"filePath": "https://x/n.ipynb"}


def test_load_notebook(tmp_path):
    p = tmp_path / "n.ipynb"
    p.write_text(json.dumps({"cells": [], "nbformat": 4, "nbformat_minor": 4}))
    data = load_notebook(p)
    assert data["nbformat"] == 4
