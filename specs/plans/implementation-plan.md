# Implementation Plan — Phases

| Field | Value |
|---|---|
| **Project** | `reflex-jupyter-renderer-react` |
| **Status** | `APPROVED` |
| **Version** | 1.0 |
| **Date** | 2026-06-18 |

---

## Overview

The project is delivered as a Reflex **custom component** following the official
flow (`reflex component init` → develop/test → `reflex component build` →
`uv publish`). Package management uses **`uv`**. Work is organized in six phases;
Phases 0–5 constitute the v0.1.0 release scope (all complete in this repository).

---

## Phase 0 — Research & Discovery ✅

**Goal:** understand the upstream library and the Reflex wrapping model.

- Study `jupyter-renderer-react`: exported component, props, callbacks, CSS,
  package name/registry, and the naming inconsistencies.
- Study Reflex "Wrapping React" (library/tags, props, events, imports/styles,
  custom code) and "Custom Components" (init/build/publish, prerequisites).
- Confirm `uv` as the package manager.

**Exit criteria:** documented prop/event surface and a chosen wrapping strategy
(direct React tag wrap, no custom JS).

## Phase 1 — Project Scaffolding ✅

**Goal:** a publishable custom-component skeleton.

- Layout per Reflex convention:
  `custom_components/reflex_jupyter_renderer_react/`, demo app folder,
  `pyproject.toml`, `README.md`, `LICENSE` (MIT), `.gitignore`.
- `pyproject.toml`: name `reflex-jupyter-renderer-react`, `reflex>=0.8.0` dep,
  `setuptools` backend discovering `custom_components/`, pytest config.

**Exit criteria:** `uv venv` + `uv pip install -e ".[dev]"` succeeds.

## Phase 2 — Data Model ✅

**Goal:** dependency-free notebook builders.

- `models.py`: `Notebook`, `CodeCell`, `MarkdownCell`, `RawCell`, output
  factories, `load_notebook`, `notebook_from_url`.
- No Reflex import; `to_dict()` matches nbformat v4.

**Exit criteria:** `tests/test_models.py` green without Reflex.

## Phase 3 — Component Wrapper ✅

**Goal:** the native Reflex component with full parity.

- `JupyterNotebookViewer(rx.Component)` with `library`, `tag`, `is_default=False`.
- All props as `rx.Var`; callbacks as `rx.EventHandler` with serializable specs
  (`error.message` only; notebook as dict).
- `add_imports()` for the CSS side-effect import.
- `create` / `from_url` / `from_json` constructors; configurable constants.

**Exit criteria:** component renders to the correct JSX tag; imports resolve.

## Phase 4 — Demo App ✅

**Goal:** a runnable app exercising every feature.

- `jupyter_renderer_react_demo/`: typed-builder example, JSON-string example,
  load-from-URL example with events, custom class/style example, and live
  controls (theme + every boolean prop) bound to state.
- Sample `assets/demo-example.ipynb`.

**Exit criteria:** `index()` builds; the page renders under Reflex.

## Phase 5 — Tests, Docs & Repo ✅

**Goal:** verified, documented, version-controlled.

- `tests/`: data-model + component-contract tests (validated against Reflex 0.9.5).
- SDD artifacts under `specs/` (PRD, architecture, API, data model, plan, tasks).
- `README.md`, `CHANGELOG.md`.
- Local git repo on `main`; published to GitHub.

**Exit criteria:** tests green; repository pushed.

## Phase 6 — Publish to PyPI (future)

**Goal:** make the package `pip install`-able.

- Confirm the upstream npm name/version actually published; pin `LIBRARY_VERSION`.
- `reflex component build` → `uv publish` (PyPI token per
  `specs/.../prerequisites`); optionally `reflex component share`.
- Tag a release; verify install in a clean env and a real `reflex run`.

**Exit criteria:** `uv pip install reflex-jupyter-renderer-react` works end-to-end.

---

## Tooling Commands (uv + Reflex)

```bash
# Environment
uv venv
uv pip install -e ".[dev]"

# Test
uv run pytest                 # or: .venv/bin/pytest

# Run the demo
cd jupyter_renderer_react_demo
uv run reflex run

# Build & publish the custom component
reflex component build         # produces dist/
uv publish                     # or: twine upload dist/*
reflex component share         # list in the Reflex gallery
```
