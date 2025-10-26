# Implementation Plan: Individual Source Inventory Page

**Branch**: `004-source-inventory` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-source-inventory/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an inventory page for individual astronomical sources using the astrodbkit inventory method. The page displays all data associated with a source from multiple tables (Sources, Photometry, Spectra, Parallaxes, ProperMotions, etc.) in organized data tables. Accessible via URL-encoded source name route (e.g., `/source/{source_name}`). Each key from the inventory result becomes its own data table. Tables with no data are not displayed. Includes loading states, error handling, and maintains existing navigation structure.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: FastAPI ≥0.120.0, Astrodbkit ≥2.4, Jinja2, pandas  
**Storage**: SQLite (SIMPLE.sqlite database file)  
**Testing**: pytest for integration tests, manual testing for UI flows  
**Target Platform**: Linux server (development with uvicorn, local SQLite database)  
**Project Type**: Web application (FastAPI backend, Jinja2 templates)  
**Performance Goals**: Inventory page loads within 5 seconds for sources with moderate data. Page navigation transitions complete within 2 seconds.  
**Constraints**: <5s inventory retrieval time, <2s response time for error cases (invalid source), handle special characters and Unicode in source identifiers via URL encoding, display all data rows with native browser scrolling  
**Scale/Scope**: Single-page route addition to existing FastAPI application, one new template, one new database query function, displays data from up to 10+ related database tables

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. FastAPI-First**: ✅ YES - New route handler added to FastAPI app, uses Jinja2 template for inventory page  
**II. Astrodbkit Abstraction**: ✅ YES - Uses `db.inventory()` method from astrodbkit to retrieve all related data for a source  
**III. Bokeh Visualizations**: ✅ N/A - This feature displays data tables only, no visualizations required  
**IV. CSS Styling**: ✅ YES - Will extend existing `style.css` with table styling, no inline styles or complex frameworks  
**V. Simplicity**: ✅ YES - Function will be under 50 lines, no complex abstractions or design patterns needed  
**VI. Prototype Reusability**: ✅ YES - Inventory page design uses standard astrodbkit patterns that work with any astronomical database following the same schema structure  
**VII. SQLite Compatibility**: ✅ YES - Uses SQLite database (SIMPLE.sqlite) via astrodbkit which provides compatibility layer

**Any violations MUST be justified in Complexity Tracking section.**

✅ **ALL CHECKS PASSED (Pre-Phase 0)** - No violations detected, proceeded to Phase 0 research.

**Post-Phase 1 Re-Evaluation**: ✅ **ALL CHECKS PASSED** - Design confirms compliance with all constitution principles. Implementation uses astrodbkit inventory method, FastAPI routes, Jinja2 templates, and CSS styling - all within framework constraints.

## Project Structure

### Documentation (this feature)

```text
specs/004-source-inventory/
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
├── main.py                      # FastAPI app - add new inventory route
├── routes/
│   └── web.py                   # Add inventory() route handler function
├── database/
│   └── sources.py               # Add get_source_inventory() function
├── templates/
│   ├── base.html                # Existing base template
│   ├── browse.html              # Existing browse page
│   ├── index.html                # Existing homepage
│   ├── plot.html                 # Existing plots page
│   ├── 404.html                  # Existing error page
│   └── inventory.html            # NEW - Inventory page template
└── static/
    ├── style.css                 # Extend with inventory table styles
    └── schema.yaml               # Database schema reference

SIMPLE.sqlite                     # SQLite database (existing)

tests/                            # (future integration tests)
```

**Structure Decision**: This is a single FastAPI web application. The feature adds:
- 1 new route handler in `src/routes/web.py`
- 1 new database query function in `src/database/sources.py`
- 1 new Jinja2 template in `src/templates/inventory.html`
- Extensions to existing `src/static/style.css` for table styling

## Complexity Tracking

> **No violations detected.** All constitution principles are followed. The implementation will be straightforward with no complex abstractions needed.

---

## Phase 0 & Phase 1 Completion Summary

**Phase 0 (Research)**: ✅ **COMPLETE**
- Research questions resolved in `research.md`
- Technical decisions documented for: astrodbkit inventory method, URL encoding/decoding, dynamic table rendering, error handling
- All unknowns clarified

**Phase 1 (Design)**: ✅ **COMPLETE**
- Data model documented in `data-model.md` (inventory entities, data flow, state transitions)
- API contract created in `contracts/web-api.yaml` (OpenAPI specification)
- Quick start guide created in `quickstart.md` (implementation steps, code examples)
- Agent context updated via `update-agent-context.ps1`
- **Updated**: Removed 500-row display limit - all data will be displayed with native browser scrolling

**Constitution Compliance**: ✅ **VERIFIED**
- Re-checked after Phase 1 design
- All principles (I-VII) remain compliant
- No violations identified
- Implementation will use FastAPI routes, Jinja2 templates, CSS styling, Astrodbkit queries

**Generated Artifacts**:
- `specs/004-source-inventory/research.md` (Phase 0)
- `specs/004-source-inventory/data-model.md` (Phase 1)
- `specs/004-source-inventory/quickstart.md` (Phase 1)
- `specs/004-source-inventory/contracts/web-api.yaml` (Phase 1)
- `specs/004-source-inventory/plan.md` (this file)

**Next Steps**: Run `/speckit.tasks` to generate implementation tasks in `tasks.md` (Phase 2)
