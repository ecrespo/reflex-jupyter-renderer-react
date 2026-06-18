"""Demo app for reflex-jupyter-renderer-react.

Run from this directory with::

    reflex run

It showcases every feature of the component:

* building a notebook with typed Python builders,
* passing a raw JSON string,
* loading a notebook from a URL with load/error events,
* toggling theme and every boolean prop at runtime,
* custom class names / inline styles,
* reading callbacks (on_file_load / on_file_error / on_error) into state.
"""

from __future__ import annotations

import json

import reflex as rx

from reflex_jupyter_renderer_react import (
    CodeCell,
    MarkdownCell,
    Notebook,
    jupyter_notebook_viewer,
    stream_output,
    execute_result_output,
    error_output,
)

# --------------------------------------------------------------------------- #
# Sample data
# --------------------------------------------------------------------------- #
SAMPLE_NOTEBOOK = Notebook(
    cells=[
        MarkdownCell("# Built in Python\n\nThis notebook was created with typed builders."),
        CodeCell(
            "print('Hello, World!')",
            execution_count=1,
            outputs=[stream_output("Hello, World!\n")],
        ),
        MarkdownCell("## A returned value"),
        CodeCell(
            "2 ** 10",
            execution_count=2,
            outputs=[execute_result_output({"text/plain": "1024"}, execution_count=2)],
        ),
        CodeCell(
            "raise ValueError('boom')",
            execution_count=3,
            outputs=[error_output("ValueError", "boom", ["ValueError: boom"])],
        ),
    ]
).to_dict()

JSON_NOTEBOOK = json.dumps(
    {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "# From a JSON string"},
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "source": "sum(range(10))",
                "outputs": [
                    {
                        "output_type": "execute_result",
                        "execution_count": 1,
                        "metadata": {},
                        "data": {"text/plain": "45"},
                    }
                ],
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4,
    }
)

# A public, CORS-friendly .ipynb for the "load from URL" example.
REMOTE_NOTEBOOK_URL = (
    "https://raw.githubusercontent.com/jupyter/notebook/main/docs/source/examples/Notebook/"
    "Working%20With%20Markdown%20Cells.ipynb"
)


class DemoState(rx.State):
    """Runtime-toggleable props and event log."""

    theme: str = "light"
    show_cell_numbers: bool = True
    show_outputs: bool = True
    collapsible: bool = False
    copyable: bool = True

    load_status: str = "idle"
    last_event: str = "—"

    @rx.event
    def set_theme(self, value: str):
        self.theme = value

    @rx.event
    def toggle_cell_numbers(self, value: bool):
        self.show_cell_numbers = value

    @rx.event
    def toggle_outputs(self, value: bool):
        self.show_outputs = value

    @rx.event
    def toggle_collapsible(self, value: bool):
        self.collapsible = value

    @rx.event
    def toggle_copyable(self, value: bool):
        self.copyable = value

    @rx.event
    def on_file_load(self, notebook: dict):
        n = len(notebook.get("cells", [])) if isinstance(notebook, dict) else 0
        self.load_status = "loaded"
        self.last_event = f"on_file_load: notebook with {n} cells"

    @rx.event
    def on_file_error(self, message: str):
        self.load_status = "error"
        self.last_event = f"on_file_error: {message}"

    @rx.event
    def on_error(self, message: str):
        self.last_event = f"on_error: {message}"


def section(title: str, *children: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.heading(title, size="5"),
        *children,
        spacing="3",
        width="100%",
        padding="1.25rem",
        border="1px solid var(--gray-5)",
        border_radius="12px",
        background="var(--gray-1)",
    )


def controls() -> rx.Component:
    return section(
        "Live controls",
        rx.hstack(
            rx.text("Theme:"),
            rx.select(
                ["light", "dark"],
                value=DemoState.theme,
                on_change=DemoState.set_theme,
            ),
            spacing="2",
            align="center",
        ),
        rx.hstack(
            rx.checkbox(
                "show_cell_numbers",
                checked=DemoState.show_cell_numbers,
                on_change=DemoState.toggle_cell_numbers,
            ),
            rx.checkbox(
                "show_outputs",
                checked=DemoState.show_outputs,
                on_change=DemoState.toggle_outputs,
            ),
            rx.checkbox(
                "collapsible",
                checked=DemoState.collapsible,
                on_change=DemoState.toggle_collapsible,
            ),
            rx.checkbox(
                "copyable",
                checked=DemoState.copyable,
                on_change=DemoState.toggle_copyable,
            ),
            spacing="4",
            wrap="wrap",
        ),
        rx.text("Last event: ", rx.code(DemoState.last_event)),
        rx.text("Load status: ", rx.badge(DemoState.load_status)),
    )


def example_typed_builders() -> rx.Component:
    return section(
        "1. Typed Python builders (live props)",
        jupyter_notebook_viewer(
            notebook=SAMPLE_NOTEBOOK,
            theme=DemoState.theme,
            show_cell_numbers=DemoState.show_cell_numbers,
            show_outputs=DemoState.show_outputs,
            collapsible=DemoState.collapsible,
            copyable=DemoState.copyable,
            on_error=DemoState.on_error,
            width="100%",
        ),
    )


def example_json_string() -> rx.Component:
    return section(
        "2. Raw JSON string",
        jupyter_notebook_viewer(
            notebook=JSON_NOTEBOOK,
            theme="dark",
            width="100%",
        ),
    )


def example_from_url() -> rx.Component:
    return section(
        "3. Load from a URL (with load/error events)",
        rx.text("Fetches a remote .ipynb and reports load/error back to Python state."),
        jupyter_notebook_viewer(
            notebook={"filePath": REMOTE_NOTEBOOK_URL},
            theme=DemoState.theme,
            fetch_options={"timeout": 10000},
            on_file_load=DemoState.on_file_load,
            on_file_error=DemoState.on_file_error,
            width="100%",
        ),
    )


def example_custom_styles() -> rx.Component:
    return section(
        "4. Custom class names & inline styles",
        jupyter_notebook_viewer(
            notebook=SAMPLE_NOTEBOOK,
            theme="light",
            class_names={"root": "demo-jupyter-root"},
            styles={"root": {"borderRadius": "10px", "overflow": "hidden"}},
            width="100%",
        ),
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("reflex-jupyter-renderer-react — demo", size="8"),
            rx.text(
                "Render Jupyter notebooks in a Reflex app, in pure Python.",
                color="var(--gray-11)",
            ),
            controls(),
            example_typed_builders(),
            example_json_string(),
            example_from_url(),
            example_custom_styles(),
            spacing="5",
            width="100%",
            padding_y="2rem",
        ),
        size="3",
    )


app = rx.App()
app.add_page(index, title="reflex-jupyter-renderer-react demo")
