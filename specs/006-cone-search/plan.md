# Implementation Plan: Cone Search Form

**Branch**: `006-cone-search` | **Date**: 2024-12-19 | **Spec**: specs/006-cone-search/spec.md
**Input**: Feature specification from `/specs/006-cone-search/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add a cone search form to the existing Search page that allows users to search for astronomical objects within a specified spatial region. The form accepts Right Ascension (RA) and Declination (Dec) coordinates in either decimal degrees or sexagesimal format, along with a search radius that can be specified in degrees, arcminutes, or arcseconds. Results are displayed on the same search_results page used by text search, maintaining consistency in the user experience. Implementation uses Astrodbkit's query_region method for spatial queries and reuses existing result display infrastructure.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: FastAPI ≥0.120.0, Astrodbkit ≥2.4  
**Storage**: SQLite database with Sources table  
**Testing**: pytest for integration tests  
**Target Platform**: Web application (development server with uvicorn)  
**Project Type**: Web application (FastAPI backend with Jinja2 templates)  
**Performance Goals**: 95% of queries return results within 5 seconds for radius ≤ 1 degree; <30 second end-to-end for typical queries  
**Constraints**: Results capped at 10,000 objects with warning; radius validation limited to ≤10 degrees; coordinate validation required for RA (0-360) and Dec (-90 to +90)  
**Scale/Scope**: Single web application with form enhancement; extends existing Search page and search_results page

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. FastAPI-First**: ✅ YES - Feature adds new FastAPI endpoint for cone search and renders results using existing Jinja2 search_results.html template  
**II. Astrodbkit Abstraction**: ✅ YES - All spatial queries use Astrodbkit's query_region method for database access  
**III. Bokeh Visualizations**: ❌ NO - Feature displays search results in existing DataTable format, no new visualizations required  
**IV. CSS Styling**: ✅ YES - Form styling will be added to src/static/style.css, no inline styles or frameworks  
**V. Simplicity**: ✅ YES - Form handling and coordinate parsing will be straightforward functions under 50 lines  
**VI. Prototype Reusability**: ✅ YES - Cone search is standard functionality that will work with any astronomical database using Astrodbkit  
**VII. SQLite Compatibility**: ✅ YES - Uses existing SQLite database with Sources table, fully compatible

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
├── routes/
│   └── web.py                    # Add new cone_search endpoint and update search endpoint
├── templates/
│   ├── search.html               # Add cone search form section below text search
│   └── search_results.html       # Reuse existing for displaying cone search results
├── static/
│   └── style.css                 # Add styling for cone search form
└── database/
    ├── query.py                  # Add cone search query function using Astrodbkit
    └── sources.py                # Existing - no changes
```

**Structure Decision**: Single web application (FastAPI backend with Jinja2 templates). Feature extends existing Search page by adding cone search form section and new database query function. Reuses existing search_results page infrastructure for displaying results.

## Phase 0: Research Complete

**Status**: ✅ Complete  
**Output**: `research.md`

**Decisions Made**:
- Use Astrodbkit's query_region method for spatial searches
- Use astropy.coordinates for coordinate parsing and conversion
- Convert all radius units to degrees before database query
- Reuse existing search_results.html template
- Implement comprehensive validation with error messages
- Cap results at 10,000 objects with warning

**Research Findings**:
- Astrodbkit query_region signature: `db.query_region(ra, dec, radius_deg, coord_frame='icrs')`
- astropy provides robust sexagesimal and decimal parsing
- No database schema changes needed
- Consistent with existing architecture

## Phase 1: Design Complete

**Status**: ✅ Complete  
**Output**: `data-model.md`, `contracts/web-api.yaml`, `quickstart.md`

**Design Artifacts**:
- Data model defines input entities (Cone Search Query) and output (Search Results)
- API contracts specify web endpoints and JSON response formats
- Quickstart provides step-by-step implementation guide

**Key Design Decisions**:
- Parse coordinates to decimal degrees before query execution
- Convert radius to degrees and validate ≤ 10 degrees maximum
- Apply 10,000 result cap with user warning
- Preserve form input values in results page

## Constitution Check Re-Evaluation (Post Phase 1 Design)

**Status**: ✅ All principles still compliant

**Re-check Results**:
- **I. FastAPI-First**: ✅ Confirmed - Uses FastAPI endpoints and Jinja2 templates
- **II. Astrodbkit Abstraction**: ✅ Confirmed - Uses query_region method, no direct SQL
- **III. Bokeh Visualizations**: ✅ N/A - Feature doesn't require visualizations
- **IV. CSS Styling**: ✅ Confirmed - CSS in separate file, no inline styles
- **V. Simplicity**: ✅ Confirmed - Functions under 50 lines, straightforward logic
- **VI. Prototype Reusability**: ✅ Confirmed - Standard cone search for any astro database
- **VII. SQLite Compatibility**: ✅ Confirmed - Uses existing SQLite with Sources table

No design changes affect constitution compliance.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. Feature fully complies with constitution principles.
