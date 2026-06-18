# Data Model — Notebook Schema

| Field | Value |
|---|---|
| **Module** | `reflex_jupyter_renderer_react.models` |
| **Status** | `APPROVED` |
| **Version** | 1.0 |

---

## 1. Purpose

A small, **dependency-free** Python layer to build notebooks programmatically or
load them from disk, producing the exact `dict` shape the viewer consumes. It
mirrors the [nbformat v4 schema](https://nbformat.readthedocs.io/en/latest/format_description.html).
Importable without Reflex installed.

## 2. The notebook shape (nbformat v4, subset)

```jsonc
{
  "cells": [ /* Cell[] */ ],
  "metadata": { /* kernelspec, language_info, ... */ },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

### Cell types

| `cell_type` | Builder | Fields |
|---|---|---|
| `markdown` | `MarkdownCell` | `source`, `metadata` |
| `code` | `CodeCell` | `source`, `execution_count`, `outputs`, `metadata` |
| `raw` | `RawCell` | `source`, `metadata` |

`source` may be a single string or a list of line strings (both valid nbformat).

### Output types

| `output_type` | Factory | Key fields |
|---|---|---|
| `stream` | `stream_output(text, name="stdout")` | `name`, `text` |
| `display_data` | `display_data_output(data, metadata=None)` | `data` (MIME bundle), `metadata` |
| `execute_result` | `execute_result_output(data, execution_count=None, metadata=None)` | `data`, `execution_count` |
| `error` | `error_output(ename, evalue, traceback=None)` | `ename`, `evalue`, `traceback` |

A MIME bundle is a `dict` like `{"text/plain": "1024", "image/png": "<base64>"}`.

## 3. Builders

```python
from reflex_jupyter_renderer_react import (
    Notebook, CodeCell, MarkdownCell, RawCell,
    stream_output, execute_result_output, error_output, display_data_output,
)

nb = Notebook(cells=[
    MarkdownCell("# Title"),
    CodeCell(
        "print('hi')",
        execution_count=1,
        outputs=[stream_output("hi\n")],
    ),
    CodeCell(
        "2 ** 10",
        execution_count=2,
        outputs=[execute_result_output({"text/plain": "1024"}, execution_count=2)],
    ),
])

data = nb.to_dict()      # -> dict ready for jupyter_notebook_viewer(notebook=...)
text = nb.to_json()      # -> JSON string
```

`Notebook.add(cell)` appends and returns `self` for chaining.

## 4. Loading helpers

| Function | Returns | Notes |
|---|---|---|
| `load_notebook(path)` | `dict` | Reads an `.ipynb` file from disk and parses it. |
| `notebook_from_url(url)` | `{"filePath": url}` | The file-reference shape; for URL loading prefer `JupyterNotebookViewer.from_url`. |

## 5. Three ways to supply a notebook to the component

| Shape | How | When |
|---|---|---|
| Parsed dict | `notebook=nb.to_dict()` or `load_notebook(path)` | Have the data in Python. |
| JSON string | `notebook=json_string` / `from_json(...)` | Have raw JSON text. |
| File reference | `notebook={"filePath": url}` / `from_url(url)` | Fetch in the browser. |

## 6. Validation philosophy

The builders intentionally do **not** enforce a full schema validation in v0.1 —
they assemble well-formed nbformat structures by construction. Consumers needing
strict validation can run the official `nbformat` validator on `to_dict()` output
before rendering. (Optional strict validation is a candidate for a later version.)
