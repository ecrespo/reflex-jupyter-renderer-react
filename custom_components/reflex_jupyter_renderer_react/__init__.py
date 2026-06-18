"""reflex-jupyter-renderer-react.

A native Reflex component that wraps the ``jupyter-renderer-react`` library so you
can render Jupyter notebooks (``.ipynb``) in a Reflex app — with syntax
highlighting, markdown, rich outputs, themes and collapsible cells — in pure
Python.

Typical use::

    import reflex as rx
    from reflex_jupyter_renderer_react import jupyter_notebook_viewer, Notebook, CodeCell, MarkdownCell

    nb = Notebook(cells=[
        MarkdownCell("# Hello"),
        CodeCell("print('hi')", execution_count=1),
    ])

    def index() -> rx.Component:
        return jupyter_notebook_viewer(notebook=nb.to_dict(), theme="dark")

You can also load from a URL::

    from reflex_jupyter_renderer_react import JupyterNotebookViewer

    JupyterNotebookViewer.from_url("https://example.com/notebook.ipynb")
"""

from .models import (
    CodeCell,
    MarkdownCell,
    Notebook,
    Output,
    RawCell,
    display_data_output,
    error_output,
    execute_result_output,
    load_notebook,
    notebook_from_url,
    stream_output,
)

__version__ = "0.1.0"

__all__ = [
    # Data model (importable without Reflex)
    "Notebook",
    "CodeCell",
    "MarkdownCell",
    "RawCell",
    "Output",
    "stream_output",
    "display_data_output",
    "execute_result_output",
    "error_output",
    "load_notebook",
    "notebook_from_url",
    # Component (requires Reflex)
    "JupyterNotebookViewer",
    "jupyter_notebook_viewer",
    "LIBRARY_NAME",
    "COMPONENT_TAG",
    "PREDEFINED_THEMES",
]

# Keep the data-model layer importable even when Reflex is not installed.
try:
    from .jupyter_renderer_react import (
        COMPONENT_TAG,
        LIBRARY_NAME,
        PREDEFINED_THEMES,
        JupyterNotebookViewer,
        jupyter_notebook_viewer,
    )
except ModuleNotFoundError:  # pragma: no cover - only without reflex installed
    JupyterNotebookViewer = None  # type: ignore[assignment]
    jupyter_notebook_viewer = None  # type: ignore[assignment]
    LIBRARY_NAME = "jupyter-renderer-react"
    COMPONENT_TAG = "JupyterNotebookViewer"
    PREDEFINED_THEMES = ("light", "dark")
