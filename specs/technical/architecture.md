# Technical Architecture

| Field | Value |
|---|---|
| **Component** | `reflex-jupyter-renderer-react` |
| **Status** | `APPROVED` |
| **Version** | 1.0 |
| **Date** | 2026-06-18 |

---

## 1. Overview

The package is a **thin, native Reflex wrapper** around the `jupyter-renderer-react`
React component. Because the upstream library exposes a *real React component*
(`JupyterNotebookViewer`) rather than an imperative class, no custom JavaScript
wrapper is required: Reflex can import and render the React tag directly. The
Python side declares the component's props as `rx.Var`s and its callbacks as
`rx.EventHandler`s.

```
┌──────────────────────────────────────────────────────────────────┐
│ Reflex app (Python)                                                │
│                                                                    │
│   jupyter_notebook_viewer(notebook=..., theme=..., on_error=...)   │
│        │                                                           │
│        ▼                                                           │
│   JupyterNotebookViewer(rx.Component)                              │
│     library = "jupyter-renderer-react"                             │
│     tag     = "JupyterNotebookViewer" (named import)              │
│     props   → rx.Var[...]                                          │
│     events  → rx.EventHandler[...]                                 │
│     add_imports() → "jupyter-renderer-react/dist/index.css"       │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Reflex compiler
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ Compiled frontend (React / Vite, via bun)                          │
│   import { JupyterNotebookViewer } from "jupyter-renderer-react";   │
│   import "jupyter-renderer-react/dist/index.css";                  │
│   <JupyterNotebookViewer notebook={...} theme={...} .../>          │
└──────────────────────────────────────────────────────────────────┘
```

## 2. Module Layout

```
custom_components/reflex_jupyter_renderer_react/
├── __init__.py                  # Public API; degrades gracefully without Reflex
├── jupyter_renderer_react.py    # The rx.Component wrapper (requires Reflex)
└── models.py                    # Dependency-free nbformat builders
```

The split mirrors the convention used across the author's other Reflex components
(e.g. `reflex-knightlab-timeline`): a **data layer** that is importable with no
Reflex dependency (useful for tooling and unit tests) and a **component layer**
that requires Reflex. `__init__.py` imports the component inside a `try/except
ModuleNotFoundError` so `import reflex_jupyter_renderer_react` still yields the
data model even when Reflex is absent.

## 3. Component Design

### 3.1 Library and tag

```python
LIBRARY_NAME = "jupyter-renderer-react"
LIBRARY_VERSION = ""                      # pin here, e.g. "0.1.0"
LIBRARY = f"{LIBRARY_NAME}@{LIBRARY_VERSION}" if LIBRARY_VERSION else LIBRARY_NAME
COMPONENT_TAG = "JupyterNotebookViewer"   # named export
CSS_IMPORT = f"{LIBRARY_NAME}/dist/index.css"
```

`is_default = False` because the upstream component is a **named export**, not a
default export. Reflex therefore emits `import { JupyterNotebookViewer } from ...`.

### 3.2 Naming note (important)

There is a real inconsistency upstream that this design isolates behind constants:

| Source | Symbol / name |
|---|---|
| Public README usage (Method 1) | `JupyterNotebookViewer` |
| Component directory | `components/JupyterNotebookViewer/` |
| `src/index.ts` export | `JupiterNotebookViewer` (sic — "Jupiter") |
| `package.json` `name` | `@iomete/jupyter-renderer-react` (GitHub registry) |

We **default to the public, documented contract** (`jupyter-renderer-react` +
`JupyterNotebookViewer`). To target the in-repo source build instead, override:

```python
import reflex_jupyter_renderer_react.jupyter_renderer_react as j
j.JupyterNotebookViewer.tag = "JupiterNotebookViewer"      # source spelling
j.JupyterNotebookViewer.library = "@iomete/jupyter-renderer-react"
```

### 3.3 Props

All props are declared as `rx.Var[...]`. Reflex automatically converts
`snake_case` Python names to `camelCase` in the rendered JSX, so
`show_cell_numbers` → `showCellNumbers`, `class_names` → `classNames`, etc.

| Python prop | JSX prop | Type |
|---|---|---|
| `notebook` | `notebook` | `dict \| str` |
| `theme` | `theme` | `str \| dict` |
| `show_cell_numbers` | `showCellNumbers` | `bool` |
| `show_outputs` | `showOutputs` | `bool` |
| `collapsible` | `collapsible` | `bool` |
| `copyable` | `copyable` | `bool` |
| `class_names` | `classNames` | `dict` |
| `styles` | `styles` | `dict` |
| `fetch_options` | `fetchOptions` | `dict` |

### 3.4 Events

The callbacks return values that must cross the wire to the Python backend. Two
event specs handle this:

- `_notebook_event_spec(notebook)` — forwards the loaded notebook as a `dict`
  (`on_file_load`).
- `_error_event_spec(error)` — forwards only `error.message` as a `str`, because
  a JS `Error` instance is not JSON-serializable (`on_file_error`, `on_error`).

### 3.5 Imports and styles

`add_imports()` returns `{"": CSS_IMPORT}`. The empty key is the Reflex idiom for
a bare side-effect import (`import "jupyter-renderer-react/dist/index.css";`). The
component's own `library`/`tag` import is added automatically and need not be
repeated. This also ensures the npm package is added to the frontend `package.json`.

### 3.6 Construction helpers

`create()` accepts `notebook` positionally/by keyword for ergonomics.
`from_url(url, fetch_options=...)` builds the `{"filePath": url}` reference, and
`from_json(raw)` passes a raw JSON string — both make developer intent explicit.

## 4. Data Model (`models.py`)

Pure `dataclasses` mirroring nbformat v4: `Notebook`, `CodeCell`, `MarkdownCell`,
`RawCell`, plus output factories (`stream_output`, `display_data_output`,
`execute_result_output`, `error_output`). `Notebook.to_dict()` produces the exact
shape the viewer consumes. `load_notebook(path)` reads an `.ipynb` from disk.
No Reflex import here — keeps the layer testable in isolation.

## 5. Build & Distribution

- **Package manager:** `uv` (`uv venv`, `uv pip install -e ".[dev]"`, `uv build`).
- **Build backend:** `setuptools`; sources discovered under `custom_components/`.
- **Reflex custom-component flow:** `reflex component build` produces `dist/`,
  then `uv publish` (or `twine upload`) ships to PyPI.
- **npm dependency:** Reflex installs `jupyter-renderer-react` into the compiled
  frontend automatically on first `reflex run`.

## 6. Testing Strategy

- **Data-model tests** (`tests/test_models.py`): run without Reflex; verify the
  serialized nbformat shape and helpers.
- **Component contract tests** (`tests/test_component.py`): `importorskip`
  Reflex; assert tag/library, named import, CSS import, prop presence, event
  triggers, and the construction helpers. Validated against Reflex 0.9.5.

## 7. Decisions (ADR-style)

| Decision | Rationale | Alternative rejected |
|---|---|---|
| Direct React tag wrap (no custom JS) | Upstream is a real React component | Custom-code wrapper (unnecessary complexity) |
| Forward `error.message` only | `Error` is not serializable | Passthrough whole object (would fail) |
| Configurable library/tag constants | Upstream naming is inconsistent | Hardcoding (brittle) |
| Dependency-free `models.py` | Reuse + isolated tests | Couple data to Reflex |
| `uv` for packaging | Fast, reproducible, recommended by Reflex docs | Poetry/pip-only |
