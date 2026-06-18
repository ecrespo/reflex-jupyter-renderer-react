# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-18

### Added
- Initial release.
- `JupyterNotebookViewer` Reflex component wrapping `jupyter-renderer-react`.
- Full prop coverage: `notebook`, `theme`, `show_cell_numbers`, `show_outputs`,
  `collapsible`, `copyable`, `class_names`, `styles`, `fetch_options`.
- Event handlers: `on_file_load`, `on_file_error`, `on_error`.
- Convenience constructors: `JupyterNotebookViewer.from_url`, `.from_json`.
- Dependency-free notebook builders (`Notebook`, `CodeCell`, `MarkdownCell`,
  `RawCell`, output helpers) and `load_notebook` / `notebook_from_url`.
- Demo Reflex app under `jupyter_renderer_react_demo/` covering every feature.
- Spec-Driven Design artifacts under `specs/` (PRD, architecture, API,
  data model, implementation plan with phases and tasks).
- Test suite under `tests/`.
