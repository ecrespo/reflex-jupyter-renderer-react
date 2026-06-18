"""Native Reflex wrapper for the ``jupyter-renderer-react`` library.

``jupyter-renderer-react`` (by IOMETE) is a *real* React component library: it
exports a ``JupyterNotebookViewer`` React component that renders a Jupyter
notebook (``.ipynb``) with syntax highlighting, markdown, and rich outputs.
Because it ships an actual React component (and not an imperative class like some
JS libraries), wrapping it in Reflex is straightforward: declare the ``library``
and ``tag``, map each prop to an ``rx.Var``, and expose the callbacks as Reflex
event handlers.

The viewer accepts a notebook in three interchangeable shapes:

1. A parsed notebook object (a Python ``dict`` following the nbformat schema).
2. A JSON string of that object.
3. A remote/local file reference: ``{"filePath": "https://.../nb.ipynb"}``.

This module keeps the npm package name and component tag in module-level
constants so they can be overridden in one place if the upstream package is
published under a different name/registry (see the README "Naming" note).
"""

from __future__ import annotations

from typing import Any, Union

import reflex as rx
from reflex.vars.object import ObjectVar

__all__ = ["JupyterNotebookViewer", "jupyter_notebook_viewer", "LIBRARY_NAME"]

# --------------------------------------------------------------------------- #
# Package coordinates
# --------------------------------------------------------------------------- #
# The public README documents `npm install jupyter-renderer-react` and a
# `JupyterNotebookViewer` named export. The repository's package.json publishes a
# scoped name (`@iomete/jupyter-renderer-react`) to the GitHub registry, and the
# source `index.ts` exports the symbol as `JupiterNotebookViewer` (sic). We default
# to the public, documented contract and centralize both so a consumer can pin a
# version or switch to the scoped package without touching the class body.
LIBRARY_NAME = "jupyter-renderer-react"
LIBRARY_VERSION = ""  # e.g. "0.1.0"; empty string installs the latest published version.
LIBRARY = f"{LIBRARY_NAME}@{LIBRARY_VERSION}" if LIBRARY_VERSION else LIBRARY_NAME

# Named export rendered as the React tag. See the "Naming" note in the README:
# override to "JupiterNotebookViewer" if you target the in-repo source build.
COMPONENT_TAG = "JupyterNotebookViewer"

# Stylesheet shipped by the package (package.json `exports` maps `./dist/index.css`).
CSS_IMPORT = f"{LIBRARY_NAME}/dist/index.css"

# Themes recognized by the upstream `theme` prop when passed as a string.
PREDEFINED_THEMES = ("light", "dark")


def _error_event_spec(error: ObjectVar) -> tuple[rx.Var[str]]:
    """Map a JS ``Error`` object to its serializable ``message`` string.

    The upstream ``onError``/``onFileError`` callbacks receive a JS ``Error``
    instance, which is not JSON-serializable. We forward only ``error.message``
    so the Reflex event handler receives a plain ``str``.
    """
    return (error.message.to(str),)


def _notebook_event_spec(notebook: ObjectVar) -> tuple[rx.Var[dict]]:
    """Pass the loaded notebook object through to the backend as a dict."""
    return (notebook.to(dict),)


class JupyterNotebookViewer(rx.Component):
    """Render a Jupyter notebook with the ``jupyter-renderer-react`` viewer."""

    library = LIBRARY
    tag = COMPONENT_TAG
    # Named export (not `export default`), so disable default-import behavior.
    is_default = False

    # ---- Data ------------------------------------------------------------- #
    # The notebook to render. Accepts a parsed object (dict), a JSON string, or a
    # file reference dict such as {"filePath": "https://.../notebook.ipynb"}.
    notebook: rx.Var[Union[dict, str]]

    # ---- Presentation ----------------------------------------------------- #
    # "light" | "dark" | a predefined theme name | a custom theme object (dict).
    theme: rx.Var[Union[str, dict]]

    # Show the execution count (e.g. `[1]`) next to code cells.
    show_cell_numbers: rx.Var[bool]

    # Render cell outputs (stream, display_data, execute_result, error).
    show_outputs: rx.Var[bool]

    # Allow cells to be collapsed/expanded.
    collapsible: rx.Var[bool]

    # Show a "copy to clipboard" button on code cells.
    copyable: rx.Var[bool]

    # Per-part class name overrides (maps to the `classNames` prop).
    class_names: rx.Var[dict]

    # Per-part inline style overrides (maps to the `styles` prop).
    styles: rx.Var[dict]

    # ---- File loading ----------------------------------------------------- #
    # Fetch options used when `notebook` is a {"filePath": ...} reference, e.g.
    # {"headers": {"Authorization": "Bearer ..."}, "timeout": 10000}.
    fetch_options: rx.Var[dict]

    # ---- Callbacks / events ---------------------------------------------- #
    # Fired after a notebook is successfully loaded from a file path. The handler
    # receives the parsed notebook object.
    on_file_load: rx.EventHandler[_notebook_event_spec]

    # Fired when loading a notebook from a file path fails (network/404/timeout).
    on_file_error: rx.EventHandler[_error_event_spec]

    # Fired when parsing/rendering a notebook fails.
    on_error: rx.EventHandler[_error_event_spec]

    def add_imports(self) -> dict[str, Any]:
        """Side-effect import of the package stylesheet.

        The empty key tells Reflex this is a bare ``import "..."`` for CSS; the
        component's own ``library``/``tag`` import is added automatically.
        """
        return {"": CSS_IMPORT}

    @classmethod
    def create(  # type: ignore[override]
        cls,
        *children: Any,
        notebook: Union[dict, str, None] = None,
        **props: Any,
    ) -> "JupyterNotebookViewer":
        """Create a notebook viewer.

        Args:
            notebook: A parsed notebook ``dict`` (nbformat), a JSON ``str`` of the
                same, or a file reference like ``{"filePath": "https://..."}``.
                Use :func:`from_url` / :func:`from_json` for explicit intent.
            **props: Standard Reflex props plus any of the typed props above
                (``theme``, ``show_cell_numbers``, ``copyable``, event handlers...).
        """
        if notebook is not None:
            props["notebook"] = notebook
        return super().create(*children, **props)

    @classmethod
    def from_url(
        cls,
        url: str,
        *,
        fetch_options: dict | None = None,
        **props: Any,
    ) -> "JupyterNotebookViewer":
        """Create a viewer that lazily fetches a ``.ipynb`` from ``url``.

        Args:
            url: HTTP(S) URL (or served path) of the notebook file.
            fetch_options: Optional fetch options (``headers``, ``timeout``).
            **props: Other component props / event handlers.
        """
        if fetch_options is not None:
            props["fetch_options"] = fetch_options
        return cls.create(notebook={"filePath": url}, **props)

    @classmethod
    def from_json(cls, raw: str, **props: Any) -> "JupyterNotebookViewer":
        """Create a viewer from a raw notebook JSON ``str``."""
        return cls.create(notebook=raw, **props)


# Convenience alias matching the Reflex `rx.<component>` calling style.
jupyter_notebook_viewer = JupyterNotebookViewer.create
