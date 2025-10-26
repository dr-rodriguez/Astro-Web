# Implementation Plan: Display Sources Data

**Branch**: `002-display-sources-data` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-display-sources-data/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Display the first 10 rows from the Sources table of the SIMPLE.sqlite database on the homepage. Uses Astrodbkit to query SQLite and render data in a Jinja2 template. Supports graceful error handling when database is unavailable.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: FastAPI 0.120.0+, Jinja2, Astrodbkit 2.4+  
**Storage**: SQLite (SIMPLE.sqlite file) via Astrodbkit abstraction  
**Testing**: pytest for integration tests  
**Target Platform**: Web browser via FastAPI development server (uvicorn)  
**Project Type**: web (FastAPI backend with Jinja2 frontend)  
**Performance Goals**: Page load <3 seconds, data retrieval <1 second (FR-004, SC-003)  
**Constraints**: Must display data at full precision, graceful error handling, maintain existing page structure  
**Scale/Scope**: Single database file with ~10 initial rows displayed on homepage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Pre-Phase 0 (Initial)**:

**I. FastAPI-First**: ✅ Yes - This feature extends the existing FastAPI app to serve Sources data, uses Jinja2 templates for HTML rendering  
**II. Astrodbkit Abstraction**: ✅ Yes - Must use Astrodbkit to query Sources table (direct SQL violates constitution)  
**III. Bokeh Visualizations**: ⚠️ Not Applicable - Feature displays tabular data, not visualizations  
**IV. CSS Styling**: ✅ Yes - Styling for table will be in CSS file, no inline styles allowed  
**V. Simplicity**: ✅ Yes - Feature requires simple query and table render, no complex patterns needed  
**VI. Prototype Reusability**: ✅ Yes - Querying Sources table via Astrodbkit is reusable pattern for other databases  
**VII. SQLite Compatibility**: ✅ Yes - Feature uses SIMPLE.sqlite via Astrodbkit abstraction

**Post-Phase 1 (After Design)**:

**I. FastAPI-First**: ✅ Confirmed - Homepage route uses FastAPI, Jinja2 TemplateResponse for HTML rendering  
**II. Astrodbkit Abstraction**: ✅ Confirmed - src/database/sources.py uses Database() with SQLAlchemy query methods exclusively (see research.md)  
**III. Bokeh Visualizations**: ⚠️ Not Applicable - Feature replaces plot with data table (no visualizations)  
**IV. CSS Styling**: ✅ Confirmed - Table styles in src/static/style.css, no inline styles in template  
**V. Simplicity**: ✅ Confirmed - Functions <50 lines, module-level DB connection, simple error handling (see research.md, data-model.md)  
**VI. Prototype Reusability**: ✅ Confirmed - Database connection pattern documented in quickstart.md, reusable for other astronomical databases  
**VII. SQLite Compatibility**: ✅ Confirmed - Uses SIMPLE.sqlite via Astrodbkit, file-based access documented

**Gate Status**: ✅ PASS - All applicable principles satisfied. No violations detected. Design completes Phase 1 planning.

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
├── main.py                    # FastAPI app initialization
├── routes/
│   └── web.py                 # Homepage and error routes
├── templates/
│   └── index.html             # Homepage template (to be modified)
├── static/
│   └── style.css              # CSS styling (to be extended)
├── database/                  # NEW - Astrodbkit database module
│   ├── __init__.py
│   └── sources.py             # Sources table query functions
└── visualizations/            # Existing Bokeh visualizations
    └── scatter.py

tests/                         # NEW - Test directory
├── integration/
│   └── test_sources_display.py
└── fixtures/
    └── test_data.py
```

**Structure Decision**: Single project with web architecture. New `src/database/` module for Astrodbkit queries. Tests in `tests/` directory following existing pattern (routes, database queries, error handling).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. Feature design maintains simplicity and follows all constitution principles.

---

## Phase 0 & Phase 1 Completion Summary

**Phase 0 (Research)**: ✅ Complete
- Resolved all technical unknowns via research.md
- Established Astrodbkit query patterns
- Defined database connection management
- Determined error handling approach
- Created data presentation format
- Designed template structure
- Styled with vanilla CSS

**Phase 1 (Design & Contracts)**: ✅ Complete
- Created data-model.md with Sources entities and error handling
- Generated contracts/web-api.yaml documenting homepage behavior
- Created quickstart.md with setup and testing instructions
- Updated agent context with new technology stack
- Re-evaluated Constitution Check post-design (all principles satisfied)

**Artifacts Generated**:
- `research.md` - Technical research and design decisions
- `data-model.md` - Data structures and error handling
- `contracts/web-api.yaml` - API documentation
- `quickstart.md` - Setup and testing guide
- `.cursor/rules/specify-rules.mdc` - Updated agent context

**Next Steps**:
- Run `/speckit.tasks` to generate implementation tasks
- Begin feature implementation following tasks.md

**Status**: ✅ Ready for Phase 2 (Task Generation)
