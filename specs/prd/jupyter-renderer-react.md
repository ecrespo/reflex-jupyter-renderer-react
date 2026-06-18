# reflex-jupyter-renderer-react — Native Jupyter Notebook Viewer

## Product Requirements Document (PRD)

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `APPROVED` |
| **Version** | 1.0 |
| **Date** | 2026-06-18 |
| **Reviewers** | — |
| **Last updated** | 2026-06-18 |

---

## 1. Executive Summary

`reflex-jupyter-renderer-react` is a pip-installable [Reflex](https://reflex.dev/)
component that natively wraps the [`jupyter-renderer-react`](https://github.com/iomete/jupyter-renderer-react)
React library. It lets a Reflex developer render a Jupyter notebook (`.ipynb`)
inside a Reflex page — with syntax highlighting, markdown, rich outputs, theming,
collapsible cells and copy-to-clipboard — declared entirely in **pure Python**,
without writing HTML, an `iframe`, or any JavaScript.

The component exposes the full prop surface of the upstream `JupyterNotebookViewer`
component and forwards its callbacks (`onFileLoad`, `onFileError`, `onError`) to
Reflex event handlers, so the notebook viewer is reactive to and integrated with
application state. A typed, dependency-free data-model layer additionally lets
developers build notebooks programmatically or load them from disk.

## 2. Context and Problem

### 2.1 Current Situation

Reflex ships markdown and code rendering primitives, but it has **no first-class
way to render a full Jupyter notebook**. Developers who want to show notebooks in
a Reflex app today must either (a) pre-render the notebook to HTML with `nbconvert`
and embed it (losing reactivity and theming control), or (b) embed an external
viewer through an `iframe` (isolated from app state, dependent on external hosting).

Meanwhile, the React ecosystem already has `jupyter-renderer-react`, a clean React
component (`JupyterNotebookViewer`) that renders notebooks with syntax
highlighting, markdown, theming, collapsible cells and output rendering.

### 2.2 Problem

1. **No native notebook component** for Reflex apps.
2. **`iframe`/HTML approaches are isolated** from Reflex state — no way to react
   to load success/failure or rendering errors from Python.
3. **Untyped notebook JSON** is error-prone to assemble by hand.
4. **No reproducible packaging** — ad-hoc solutions are copy-pasted per project.

### 2.3 Opportunity

Package `jupyter-renderer-react` as a native, reactive, version-pinnable Reflex
custom component, with typed Python builders and events wired to state. This
benefits any Reflex developer who needs to display notebooks (documentation,
data-science portfolios, tutorial/teaching content, report viewers).

## 3. Target Users

### Persona 1: Reflex Developer
- **Description:** builds full-stack apps in Python with Reflex.
- **Primary need:** drop a notebook viewer into a page in a few lines, no JS.
- **Usage frequency:** per project.
- **Technical level:** medium/high.

### Persona 2: Data-Science / Education Author
- **Description:** publishes notebooks as part of a site or course.
- **Primary need:** render `.ipynb` from disk or a URL with consistent theming.
- **Usage frequency:** recurring.
- **Technical level:** medium.

## 4. Goals and Success Metrics

| Goal | Metric | Target |
|---|---|---|
| Native rendering | Notebook renders without iframe/HTML | 100% of nbformat v4 cells |
| Full prop parity | Upstream props exposed | 9/9 props + 3/3 callbacks |
| Reactivity | Events delivered to Python state | `on_file_load`/`on_file_error`/`on_error` |
| Easy install | `pip install reflex-jupyter-renderer-react` | one command |
| Reproducible | npm dependency resolved by Reflex | automatic on first run |
| Tested | Test suite green | 100% pass |

## 5. Scope

### 5.1 In Scope
- A `JupyterNotebookViewer` Reflex component wrapping the upstream React component.
- All documented props: `notebook`, `theme`, `show_cell_numbers`, `show_outputs`,
  `collapsible`, `copyable`, `class_names`, `styles`, `fetch_options`.
- All documented callbacks: `on_file_load`, `on_file_error`, `on_error`.
- Three notebook input shapes: parsed object, JSON string, `{filePath}` reference.
- Convenience constructors: `from_url`, `from_json`.
- Dependency-free notebook builders + `load_notebook`.
- A demo Reflex app covering every feature.
- A test suite and SDD documentation.

### 5.2 Out of Scope (v0.1)
- **Executing** notebook code (this is a *renderer*, not a kernel).
- Editing notebooks in the browser.
- Custom output MIME renderers beyond what the upstream library supports.
- Server-side conversion / `nbconvert` integration.

## 6. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Render a notebook from a parsed dict | Must |
| FR-2 | Render a notebook from a JSON string | Must |
| FR-3 | Load and render a notebook from a URL/path (`{filePath}`) | Must |
| FR-4 | Support `light`/`dark` and custom theme objects | Must |
| FR-5 | Toggle cell numbers, outputs, collapsible, copyable | Must |
| FR-6 | Apply custom `class_names` / `styles` | Should |
| FR-7 | Pass `fetch_options` for URL loading | Should |
| FR-8 | Deliver `on_file_load` with the parsed notebook | Must |
| FR-9 | Deliver `on_file_error` / `on_error` as a message string | Must |
| FR-10 | Provide typed Python notebook builders | Should |

## 7. Non-Functional Requirements

- **Compatibility:** Reflex ≥ 0.8.0, Python ≥ 3.10.
- **Packaging:** managed with `uv`; built with `reflex component build`.
- **Licensing:** MIT (matches upstream).
- **Reproducibility:** the npm package is declared via the component `library`.
- **Resilience:** the data-model layer imports without Reflex installed.

## 8. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Upstream naming inconsistency (`JupyterNotebookViewer` vs `JupiterNotebookViewer`; scoped `@iomete/...`) | Wrong import at build time | Centralize `LIBRARY_NAME`/`COMPONENT_TAG` constants; document override; default to the public README contract |
| Upstream version drift | Runtime breakage | `LIBRARY_VERSION` constant for pinning |
| Error objects not serializable | Event delivery fails | Forward only `error.message` via a custom event spec |
| CORS when loading remote `.ipynb` | URL example fails | Document `fetch_options`/CORS; provide on-disk + builder paths |

## 9. Open Questions

1. Which exact name/version is published to public npm vs the GitHub registry?
   → Mitigated by configurable constants; confirm before first PyPI release.
2. Should we add `nbconvert`-based server rendering as an optional extra? (post-0.1)
