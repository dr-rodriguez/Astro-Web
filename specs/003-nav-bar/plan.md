# Implementation Plan: Navigation Bar with Multi-Page Structure

**Branch**: `003-nav-bar` | **Date**: 2025-01-27 | **Spec**: `specs/003-nav-bar/spec.md`
**Input**: Feature specification from `specs/003-nav-bar/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add a top navigation bar to the website enabling users to navigate between three distinct pages: Home (introductory landing page), Browse Database (sortable/filterable/paginated Sources table), and Visualizations (interactive scatter plot of ra/dec coordinates). The navigation bar appears consistently on all pages, highlighting the active page. All Sources data loads client-side for fast table interactions, while the scatter plot displays actual coordinate data from the database.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: FastAPI ≥0.120.0, Jinja2 ≥3.1.0, Bokeh 3.8.0, Astrodbkit ≥2.4, DataTables (CDN)  
**Storage**: SQLite (SIMPLE.sqlite) via Astrodbkit  
**Testing**: pytest ≥8.0.0 (for integration tests)  
**Target Platform**: Web application (server-side FastAPI with client-side JavaScript)  
**Project Type**: web  
**Performance Goals**: Page loads <2s, table filtering/sorting <1s  
**Constraints**: Client-side processing for table controls using DataTables library, all Sources loaded once, excludes null coordinates from plots  
**Scale/Scope**: Small prototype handling hundreds to low thousands of Sources records

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. FastAPI-First**: ✅ YES - All three pages (/, /browse, /plots) will be FastAPI routes. Jinja2 templates render each page.  
**II. Astrodbkit Abstraction**: ✅ YES - Database queries via `src/database/sources.py` using Astrodbkit.  
**III. Bokeh Visualizations**: ✅ YES - Scatter plot on Visualizations page uses Bokeh with ra/dec from Sources.  
**IV. CSS Styling**: ✅ YES - Navigation bar and table controls styled via `src/static/style.css`. No inline styles.  
**V. Simplicity**: ⚠️ PARTIAL - Route handlers <50 lines. DataTables library used for table controls (justified: provides production-quality sorting, pagination, filtering with minimal code complexity).  
**VI. Prototype Reusability**: ✅ YES - Navigation structure and table patterns can be adapted to other astronomical databases.  
**VII. SQLite Compatibility**: ✅ YES - Uses SIMPLE.sqlite via Astrodbkit.

**GATE STATUS**: ✅ PASS - No violations detected.

**Any violations MUST be justified in Complexity Tracking section.**

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── main.py                    # FastAPI app with 3 routes: /, /browse, /plots
├── routes/
│   └── web.py                 # Route handlers: homepage(), browse(), plot()
├── templates/
│   ├── index.html             # Home page (introductory content)
│   ├── browse.html            # Browse page (Sources table with controls)
│   ├── plot.html              # Plot page (scatter plot)
│   └── 404.html               # 404 error page (existing)
├── static/
│   └── style.css              # CSS: navigation bar, table styling, controls
├── database/
│   └── sources.py             # get_sources_data(), get_all_sources()
└── visualizations/
    └── scatter.py             # create_scatter_plot() - updated for ra/dec

tests/
└── [integration tests for route handlers]
```

**Structure Decision**: Single web application with existing FastAPI structure. New routes in `src/routes/web.py`. New templates: `browse.html`, `plot.html`. Navigation bar extracted to shared template/partial. Client-side JavaScript using DataTables library (CDN) for table controls. Bokeh plot generated server-side, embedded in Plot page.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All decisions align with Constitution principles.

## Post-Design Constitution Re-Evaluation

**GATE STATUS**: ✅ PASS - Phase 1 design confirms compliance

**I. FastAPI-First**: ✅ All routes defined as FastAPI endpoints (`/`, `/browse`, `/plots`). All pages rendered via Jinja2 templates.  
**II. Astrodbkit Abstraction**: ✅ Database access via `src/database/sources.py` using Astrodbkit query interface. No direct SQL.  
**III. Bokeh Visualizations**: ✅ Scatter plot uses Bokeh for ra/dec visualization. Embedded as interactive component.  
**IV. CSS Styling**: ✅ Navigation bar and table controls styled via `style.css`. No inline styles or framework dependencies.  
**V. Simplicity**: ✅ Route handlers are straightforward (<50 lines). Client-side JavaScript uses DataTables library loaded via CDN (no framework or build step).  
**VI. Prototype Reusability**: ✅ Navigation structure and table patterns can be adapted to other astronomical databases. Clear separation of concerns.  
**VII. SQLite Compatibility**: ✅ Uses SIMPLE.sqlite via Astrodbkit interface.

## Phase 0 Output: research.md

✅ Generated with decisions for:
- Navigation bar integration (Jinja2 template inheritance)
- Client-side table controls (DataTables library via CDN)
- Bokeh plot data (Astrodbkit query)
- Active page indicator (server-side context + CSS)
- Table state management (ephemeral client-side)

## Phase 1 Output: design artifacts

✅ **data-model.md**: Navigation entities, Browse Database page entity, Visualizations page entity  
✅ **contracts/web-api.yaml**: OpenAPI specification for `/`, `/browse`, `/plots` endpoints  
✅ **quickstart.md**: Testing guide with 8 test scenarios  
✅ **agent context**: Updated Cursor IDE rules with project technology stack

**Generated files**:
- `specs/003-nav-bar/research.md` (Phase 0)
- `specs/003-nav-bar/data-model.md` (Phase 1, pre-existing, validated)
- `specs/003-nav-bar/contracts/web-api.yaml` (Phase 1, pre-existing, validated)
- `specs/003-nav-bar/quickstart.md` (Phase 1)
- `.cursor/rules/specify-rules.mdc` (agent context updated)

## Implementation Summary

**Next Step**: Run `/speckit.tasks` to generate `tasks.md` with concrete implementation steps

**Key Implementation Tasks** (to be detailed in tasks.md):
1. Create `src/templates/base.html` with navigation bar
2. Refactor `src/templates/index.html` to extend base
3. Create `src/templates/browse.html` with Sources table and client-side controls
4. Create `src/templates/plot.html` with Bokeh plot
5. Add routes to `src/routes/web.py`
6. Add `get_all_sources()` to `src/database/sources.py`
7. Update `src/visualizations/scatter.py` for ra/dec data
8. Add navigation CSS to `src/static/style.css`
