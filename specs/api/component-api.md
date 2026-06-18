# Component API Reference

| Field | Value |
|---|---|
| **Module** | `reflex_jupyter_renderer_react` |
| **Status** | `APPROVED` |
| **Version** | 1.0 |

---

## `jupyter_notebook_viewer(*children, **props)`

Alias of `JupyterNotebookViewer.create`. The idiomatic way to instantiate the
component (mirrors `rx.<component>` calling style).

```python
from reflex_jupyter_renderer_react import jupyter_notebook_viewer

jupyter_notebook_viewer(
    notebook=my_notebook_dict,
    theme="dark",
    show_cell_numbers=True,
    copyable=True,
    on_error=State.on_error,
    width="100%",
)
```

## Class `JupyterNotebookViewer(rx.Component)`

### Props

| Prop | Type | Default (upstream) | Description |
|---|---|---|---|
| `notebook` | `dict \| str` | required | Parsed notebook (nbformat dict), a JSON string, or a `{"filePath": "..."}` reference. |
| `theme` | `str \| dict` | `"light"` | `"light"`, `"dark"`, a predefined theme name, or a custom theme object. |
| `show_cell_numbers` | `bool` | `True` | Show execution count next to code cells. |
| `show_outputs` | `bool` | `True` | Render cell outputs. |
| `collapsible` | `bool` | `False` | Allow cells to collapse/expand. |
| `copyable` | `bool` | `True` | Show a copy button on code cells. |
| `class_names` | `dict` | `{}` | Per-part class-name overrides (`classNames`). |
| `styles` | `dict` | `{}` | Per-part inline-style overrides (`styles`). |
| `fetch_options` | `dict` | `{}` | Fetch options for URL loading: `{"headers": {...}, "timeout": 10000}`. |

> Reflex converts `snake_case` → `camelCase` automatically, so `show_cell_numbers`
> is emitted as `showCellNumbers`, `class_names` as `classNames`, etc.

### Events

| Event | Payload to Python | Fires when |
|---|---|---|
| `on_file_load` | `notebook: dict` | A notebook is successfully fetched from a `filePath`. |
| `on_file_error` | `message: str` | File loading fails (network / 404 / timeout). |
| `on_error` | `message: str` | Parsing / rendering fails. |

```python
class State(rx.State):
    status: str = "idle"

    @rx.event
    def on_loaded(self, notebook: dict):
        self.status = f"{len(notebook.get('cells', []))} cells"

    @rx.event
    def on_failed(self, message: str):
        self.status = f"error: {message}"

jupyter_notebook_viewer(
    notebook={"filePath": "https://example.com/n.ipynb"},
    on_file_load=State.on_loaded,
    on_file_error=State.on_failed,
)
```

### Class methods

#### `JupyterNotebookViewer.create(*children, notebook=None, **props)`
Standard constructor. `notebook` may be passed by keyword.

#### `JupyterNotebookViewer.from_url(url, *, fetch_options=None, **props)`
Build a viewer that lazily fetches a `.ipynb` from `url`. Sets
`notebook={"filePath": url}` and (optionally) `fetch_options`.

```python
JupyterNotebookViewer.from_url(
    "https://example.com/n.ipynb",
    fetch_options={"timeout": 10000},
    on_file_load=State.on_loaded,
)
```

#### `JupyterNotebookViewer.from_json(raw, **props)`
Build a viewer from a raw notebook JSON string.

```python
JupyterNotebookViewer.from_json(json_string, theme="dark")
```

### Module constants (override points)

| Constant | Default | Purpose |
|---|---|---|
| `LIBRARY_NAME` | `"jupyter-renderer-react"` | npm package name. |
| `LIBRARY_VERSION` | `""` | Pin a version (e.g. `"0.1.0"`); empty = latest. |
| `COMPONENT_TAG` | `"JupyterNotebookViewer"` | React named export to render. |
| `CSS_IMPORT` | `"jupyter-renderer-react/dist/index.css"` | Stylesheet side-effect import. |
| `PREDEFINED_THEMES` | `("light", "dark")` | Recognized string themes. |

See `specs/technical/architecture.md` §3.2 for the upstream naming note and how
to retarget the scoped `@iomete/...` package or the source-spelled tag.
