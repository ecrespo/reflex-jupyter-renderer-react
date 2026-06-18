"""Contract tests for the Reflex component wrapper.

These require Reflex to be installed; if it is not present they are skipped, and
the pure data-model tests still cover the serialization layer.
"""

import pytest

reflex = pytest.importorskip("reflex")

from reflex_jupyter_renderer_react.jupyter_renderer_react import (
    CSS_IMPORT,
    LIBRARY_NAME,
    JupyterNotebookViewer,
    jupyter_notebook_viewer,
)


class TestComponentContract:
    def test_library_and_tag(self):
        assert JupyterNotebookViewer.tag == "JupyterNotebookViewer"
        assert LIBRARY_NAME in str(JupyterNotebookViewer.library)

    def test_named_import(self):
        # The viewer is a named export, not a default export.
        assert JupyterNotebookViewer.is_default is False

    def test_css_import(self):
        imports = JupyterNotebookViewer().add_imports()
        assert imports[""] == CSS_IMPORT
        assert CSS_IMPORT.endswith("/dist/index.css")

    def test_props_exist(self):
        fields = JupyterNotebookViewer.get_fields()
        for prop in (
            "notebook",
            "theme",
            "show_cell_numbers",
            "show_outputs",
            "collapsible",
            "copyable",
            "class_names",
            "styles",
            "fetch_options",
        ):
            assert prop in fields, f"missing prop: {prop}"

    def test_event_triggers(self):
        triggers = JupyterNotebookViewer().get_event_triggers()
        for ev in ("on_file_load", "on_file_error", "on_error"):
            assert ev in triggers, f"missing event: {ev}"

    def test_create_with_dict_notebook(self):
        comp = jupyter_notebook_viewer(notebook={"cells": [], "nbformat": 4})
        assert comp is not None

    def test_from_url_sets_file_path(self):
        comp = JupyterNotebookViewer.from_url(
            "https://example.com/n.ipynb", fetch_options={"timeout": 5000}
        )
        assert comp is not None

    def test_from_json(self):
        comp = JupyterNotebookViewer.from_json('{"cells": [], "nbformat": 4}')
        assert comp is not None
