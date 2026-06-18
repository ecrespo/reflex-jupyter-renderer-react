# reflex-jupyter-renderer-react

[![PyPI version](https://img.shields.io/pypi/v/reflex-jupyter-renderer-react.svg)](https://pypi.org/project/reflex-jupyter-renderer-react/)
[![Python versions](https://img.shields.io/pypi/pyversions/reflex-jupyter-renderer-react.svg)](https://pypi.org/project/reflex-jupyter-renderer-react/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ecrespo/reflex-jupyter-renderer-react/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-ecrespo%2Freflex--jupyter--renderer--react-181717?logo=github)](https://github.com/ecrespo/reflex-jupyter-renderer-react)

- **Source:** https://github.com/ecrespo/reflex-jupyter-renderer-react
- **PyPI:** https://pypi.org/project/reflex-jupyter-renderer-react/
- **Issues:** https://github.com/ecrespo/reflex-jupyter-renderer-react/issues
- **Upstream React library:** https://github.com/iomete/jupyter-renderer-react

A native [Reflex](https://reflex.dev/) component that wraps the
[`jupyter-renderer-react`](https://github.com/iomete/jupyter-renderer-react) React
library, so you can render **Jupyter notebooks (`.ipynb`)** in a Reflex app —
with syntax highlighting, markdown, rich outputs, theming, collapsible cells and
copy-to-clipboard — in **pure Python**. No HTML, no `iframe`, no hand-written
JavaScript.

```python
import reflex as rx
from reflex_jupyter_renderer_react import (
    jupyter_notebook_viewer, Notebook, MarkdownCell, CodeCell, stream_output,
)

nb = Notebook(cells=[
    MarkdownCell("# Hello, notebook"),
    CodeCell("print('hi')", execution_count=1, outputs=[stream_output("hi\n")]),
])

def index() -> rx.Component:
    return jupyter_notebook_viewer(notebook=nb.to_dict(), theme="dark")

app = rx.App()
app.add_page(index)
```

## Why a native component?

| iframe / pre-rendered HTML | native component (this package) |
|---|---|
| Isolated from app state | Wired into Reflex state via events (`on_file_load`, `on_error`, …) |
| Tied to static files/routes | Reusable, `pip install`-able |
| Untyped JSON edited by hand | Typed Python builders for notebooks |
| External hosting / manual embedding | npm dependency resolved by Reflex automatically |

## Install

```bash
pip install reflex-jupyter-renderer-react
# or, with uv:
uv add reflex-jupyter-renderer-react
# or, from this repo (editable):
uv pip install -e .
```

Reflex installs the underlying npm package (`jupyter-renderer-react`) into the
compiled frontend automatically on the first `reflex run`.

## Usage

### Three ways to supply a notebook

```python
from reflex_jupyter_renderer_react import (
    jupyter_notebook_viewer, JupyterNotebookViewer, Notebook, MarkdownCell, CodeCell,
    load_notebook,
)

# 1) Typed Python builders
nb = Notebook(cells=[MarkdownCell("# Title"), CodeCell("1 + 1", execution_count=1)])
jupyter_notebook_viewer(notebook=nb.to_dict())

# 2) A raw JSON string
jupyter_notebook_viewer(notebook='{"cells": [], "nbformat": 4, "nbformat_minor": 4}')
# or: JupyterNotebookViewer.from_json(json_str)

# 3) Load from a URL or from disk
JupyterNotebookViewer.from_url("https://example.com/notebook.ipynb")
jupyter_notebook_viewer(notebook=load_notebook("assets/demo-example.ipynb"))
```

### Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `notebook` | `dict \| str` | required | Parsed dict, JSON string, or `{"filePath": "..."}`. |
| `theme` | `str \| dict` | `"light"` | `"light"`, `"dark"`, or a custom theme object. |
| `show_cell_numbers` | `bool` | `True` | Show execution count for code cells. |
| `show_outputs` | `bool` | `True` | Render cell outputs. |
| `collapsible` | `bool` | `False` | Allow cells to collapse. |
| `copyable` | `bool` | `True` | Copy button on code cells. |
| `class_names` | `dict` | `{}` | Per-part class names (`classNames`). |
| `styles` | `dict` | `{}` | Per-part inline styles (`styles`). |
| `fetch_options` | `dict` | `{}` | `{"headers": {...}, "timeout": 10000}` for URL loading. |

> Reflex converts `snake_case` props to `camelCase` automatically
> (`show_cell_numbers` → `showCellNumbers`).

### Events → Python

```python
class State(rx.State):
    status: str = "idle"

    @rx.event
    def loaded(self, notebook: dict):
        self.status = f"{len(notebook.get('cells', []))} cells loaded"

    @rx.event
    def failed(self, message: str):
        self.status = f"error: {message}"

JupyterNotebookViewer.from_url(
    "https://example.com/notebook.ipynb",
    fetch_options={"timeout": 10000},
    on_file_load=State.loaded,
    on_file_error=State.failed,
)
```

| Event | Payload | Fires when |
|---|---|---|
| `on_file_load` | `notebook: dict` | A notebook is fetched from a `filePath`. |
| `on_file_error` | `message: str` | File loading fails (network / 404 / timeout). |
| `on_error` | `message: str` | Parsing / rendering fails. |

## Demo app

A full demo lives in [`jupyter_renderer_react_demo/`](jupyter_renderer_react_demo)
and exercises every feature (typed builders, JSON string, URL loading with events,
custom styles, and live theme/prop toggles).

```bash
uv pip install -e .
cd jupyter_renderer_react_demo
uv run reflex run
```

## Building notebooks in Python

```python
from reflex_jupyter_renderer_react import (
    Notebook, MarkdownCell, CodeCell,
    stream_output, execute_result_output, error_output,
)

nb = Notebook(cells=[
    MarkdownCell("# Report"),
    CodeCell("print('hi')", execution_count=1, outputs=[stream_output("hi\n")]),
    CodeCell("2 ** 10", execution_count=2,
             outputs=[execute_result_output({"text/plain": "1024"}, execution_count=2)]),
    CodeCell("1/0", execution_count=3,
             outputs=[error_output("ZeroDivisionError", "division by zero")]),
])
data = nb.to_dict()
```

The data-model layer (`Notebook`, cells, output factories, `load_notebook`) imports
**without Reflex installed**, so it is usable in plain scripts and unit tests.

## Naming note

The upstream project has some naming inconsistencies. This wrapper centralizes
them in overridable constants and defaults to the **public, documented contract**:

| Source | Name |
|---|---|
| Public README usage | `JupyterNotebookViewer` |
| `src/index.ts` export | `JupiterNotebookViewer` (sic) |
| `package.json` name | `@iomete/jupyter-renderer-react` (GitHub registry) |

Defaults: `library = "jupyter-renderer-react"`, `tag = "JupyterNotebookViewer"`.
To retarget the scoped package or the source-spelled tag:

```python
import reflex_jupyter_renderer_react.jupyter_renderer_react as j
j.JupyterNotebookViewer.library = "@iomete/jupyter-renderer-react"
j.JupyterNotebookViewer.tag = "JupiterNotebookViewer"
```

You can also pin a version via `LIBRARY_VERSION` in
`custom_components/reflex_jupyter_renderer_react/jupyter_renderer_react.py`.

## Development

This project follows the Reflex **custom component** workflow and uses **`uv`**.

```bash
uv venv
uv pip install -e ".[dev]"
uv run pytest                 # run the tests

# Publish (custom component flow)
reflex component build        # -> dist/
uv publish                    # or: twine upload dist/*
reflex component share        # list in the Reflex gallery
```

See [`specs/`](specs) for the full Spec-Driven Design documentation: PRD,
architecture, API, data-model schema, and the phased implementation plan & tasks.

## Project structure

```
reflex-jupyter-renderer-react/
├── custom_components/reflex_jupyter_renderer_react/
│   ├── __init__.py
│   ├── jupyter_renderer_react.py   # the Reflex component
│   └── models.py                   # dependency-free notebook builders
├── jupyter_renderer_react_demo/    # runnable demo app
├── tests/                          # data-model + component contract tests
├── specs/                          # SDD: prd / technical / api / data-model / plans
├── pyproject.toml
├── README.md · CHANGELOG.md · LICENSE
```

## License

MIT © Ernesto Crespo. The upstream `jupyter-renderer-react` library is also MIT.
