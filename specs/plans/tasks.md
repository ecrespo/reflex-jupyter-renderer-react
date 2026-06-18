# Task Breakdown

| Field | Value |
|---|---|
| **Project** | `reflex-jupyter-renderer-react` |
| **Status** | `IN PROGRESS` (v0.1 complete; publish pending) |
| **Version** | 1.0 |

Legend: `[x]` done · `[ ]` pending · `(P#)` phase.

---

## Phase 0 — Research
- [x] (P0) Identify upstream package, exported component, props & callbacks.
- [x] (P0) Capture the naming inconsistency (`JupyterNotebookViewer` vs `JupiterNotebookViewer`, scoped `@iomete/...`).
- [x] (P0) Review Reflex wrapping docs (library/tags, props, events, imports, custom code).
- [x] (P0) Review Reflex custom-component docs (overview, prerequisites, command reference).
- [x] (P0) Confirm `uv` as package manager.

## Phase 1 — Scaffolding
- [x] (P1) Create directory layout (`custom_components/`, demo, `tests/`, `specs/`).
- [x] (P1) Write `pyproject.toml` (name, deps, setuptools, pytest).
- [x] (P1) Add `LICENSE` (MIT), `.gitignore`, `CHANGELOG.md`.

## Phase 2 — Data Model
- [x] (P2) `Notebook`, `CodeCell`, `MarkdownCell`, `RawCell` dataclasses.
- [x] (P2) Output factories: stream / display_data / execute_result / error.
- [x] (P2) `load_notebook`, `notebook_from_url`.
- [x] (P2) Keep `models.py` free of Reflex imports.

## Phase 3 — Component Wrapper
- [x] (P3) `JupyterNotebookViewer(rx.Component)` with `library`/`tag`/`is_default`.
- [x] (P3) Declare all 9 props as `rx.Var`.
- [x] (P3) Event specs: notebook → dict; error → message string.
- [x] (P3) `add_imports()` CSS side-effect import.
- [x] (P3) `create` / `from_url` / `from_json`; override constants.
- [x] (P3) `__init__.py` public API with graceful no-Reflex fallback.

## Phase 4 — Demo App
- [x] (P4) `rxconfig.py`, `requirements.txt`, package `__init__`.
- [x] (P4) Example: typed builders + live prop controls.
- [x] (P4) Example: raw JSON string.
- [x] (P4) Example: load from URL with `on_file_load`/`on_file_error`.
- [x] (P4) Example: custom `class_names` / `styles`.
- [x] (P4) Sample `assets/demo-example.ipynb`.

## Phase 5 — Tests, Docs & Repo
- [x] (P5) `tests/test_models.py` (no Reflex).
- [x] (P5) `tests/test_component.py` (contract; `importorskip` Reflex).
- [x] (P5) Run suite green against Reflex 0.9.5 (15 passed).
- [x] (P5) SDD docs: PRD, architecture, API, data model, plan, tasks.
- [x] (P5) `README.md`.
- [x] (P5) `git init`, `main` branch, initial commit.
- [x] (P5) Create GitHub repo and push.

## Phase 6 — Publish (future)
- [ ] (P6) Verify the published upstream npm name/version; pin `LIBRARY_VERSION`.
- [ ] (P6) `reflex component build` → `uv publish` to PyPI.
- [ ] (P6) `reflex component share` (Reflex gallery).
- [ ] (P6) Smoke-test `reflex run` in the demo with the npm package resolved.
- [ ] (P6) Tag `v0.1.0` release.

## Backlog / Future
- [ ] Optional strict `nbformat` validation in the data model.
- [ ] CI workflow (lint + tests) via GitHub Actions.
- [ ] Screenshot / GIF in README once the demo runs locally.
