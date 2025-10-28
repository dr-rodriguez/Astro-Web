# Implementation Plan: Spectra Display Page

**Branch**: `007-spectra-display` | **Date**: 2025-01-28 | **Spec**: specs/007-spectra-display/spec.md
**Input**: Feature specification from `/specs/007-spectra-display/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add a spectra display page accessible from source inventory pages that visualizes all spectra for a given source using an interactive Bokeh plot. The implementation includes:
1. A new route `/source/{source_name}/spectra` accessible from inventory pages when spectra exist
2. Database query using astrodbkit to retrieve spectrum data with configurable column name (default: `access_url`)
3. Spectrum data is already formatted by astrodbkit - wavelength and flux arrays are accessible directly
4. Interactive Bokeh plot displaying all spectra with legend showing observation details
5. Metadata table showing spectrum information with clickable links to original data
6. Graceful handling of non-displayable spectra by skipping invalid entries
7. Configuration support for custom spectrum URL column names

## Technical Context

**Language/Version**: Python ≥3.13  
**Primary Dependencies**: FastAPI ≥0.120.0, Astrodbkit ≥2.4, Bokeh ≥3.0, requests ≥2.0  
**Note**: specutils is not needed separately - astrodbkit returns spectra already formatted  
**Storage**: SQLite database with Spectra table accessed via astrodbkit  
**Testing**: pytest for integration tests, manual testing for UI flows  
**Target Platform**: Web application (development server with uvicorn)  
**Project Type**: Web application (FastAPI backend with Jinja2 templates)  
**Performance Goals**: Page loads and spectrum retrieval within 10 seconds for sources with up to 15 spectra; loading indicator displayed during data fetching  
**Constraints**: Must maintain simplicity for astronomer maintainability, handle corrupt/missing spectrum files gracefully, skip unreadable spectra without error messages  
**Scale/Scope**: Single feature addition to existing web application; reusable pattern for displaying spectra from any astronomical database using astrodbkit

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. FastAPI-First**: ✅ YES - Feature adds new FastAPI endpoint for spectra display and renders results using Jinja2 template  
**II. Astrodbkit Abstraction**: ✅ YES - All database queries use astrodbkit's `db.query(db.Spectra)` method, no direct SQL  
**III. Bokeh Visualizations**: ✅ YES - Feature uses Bokeh for interactive spectrum plots with legend  
**IV. CSS Styling**: ✅ YES - Styling will be added to src/static/style.css, no inline styles or frameworks  
**V. Simplicity**: ✅ YES - Functions kept under 50 lines where possible, straightforward spectrum loading logic  
**VI. Prototype Reusability**: ✅ YES - Design works for other astronomical databases with spectra, clear API separation  
**VII. SQLite Compatibility**: ✅ YES - Feature works with SQLite as primary storage via Astrodbkit

**Any violations MUST be justified in Complexity Tracking section.**

## Project Structure

### Documentation (this feature)

```text
specs/007-spectra-display/
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
│   └── web.py                    # Add new spectra_display endpoint
├── templates/
│   ├── inventory.html            # Add spectra link when spectra exist
│   └── spectra.html              # New template for spectra visualization
├── static/
│   └── style.css                 # Add styling for spectra page
├── database/
│   └── sources.py                # Add get_source_spectra function
├── visualizations/
│   └── spectra.py                # New module for Bokeh spectrum plot generation
└── config.py                     # Add SPECTRA_URL_COLUMN configuration
```

**Structure Decision**: Single web application (FastAPI backend with Jinja2 templates). Feature extends existing inventory page with link to new spectra display page, reuses existing database and visualization infrastructure.

## Phase 0: Research Complete

**Status**: ✅ Complete  
**Output**: `research.md`

**Decisions Made**:
- Use astrodbkit's `db.query(db.Spectra).filter(...).spectra(fmt='pandas')` for spectrum retrieval
- Configure spectrum URL column name via environment variable (default: `access_url`)
- Use Bokeh for interactive multi-spectrum plots with legend
- Skip invalid/undisplayable spectra gracefully without error messages
- Display loading indicator during spectrum data retrieval

**Research Findings**:
- astrodbkit provides `spectra()` method that returns pandas DataFrame with wavelength and flux arrays already formatted
- astrodbkit handles spectrum format detection and conversion automatically (no need for separate specutils installation)
- Bokeh supports overlay plots with legends
- Configuration pattern consistent with existing ASTRO_WEB environment variables
- No database schema changes needed

## Phase 1: Design Complete

**Status**: ✅ Complete  
**Output**: `data-model.md`, `contracts/web-api.yaml`, `quickstart.md`

**Design Artifacts**:
- Data model defines input (Source Name) and output (Spectra Visualization) entities
- API contracts specify web endpoint for spectra display
- Quickstart provides step-by-step implementation guide

**Key Design Decisions**:
- Extract spectrum metadata from astrodbkit query results
- astrodbkit returns spectra already formatted - access wavelength and flux arrays directly (no specutils needed)
- Generate Bokeh plot with multiple spectrum lines and legend
- Display metadata table alongside plot
- Configure spectrum URL column via environment variable

## Constitution Check Re-Evaluation (Post Phase 1 Design)

**Status**: ✅ All principles still compliant

**Re-check Results**:
- **I. FastAPI-First**: ✅ Confirmed - Uses FastAPI endpoint and Jinja2 template
- **II. Astrodbkit Abstraction**: ✅ Confirmed - Uses query/filter methods, no direct SQL
- **III. Bokeh Visualizations**: ✅ Confirmed - Uses Bokeh for interactive spectrum plots
- **IV. CSS Styling**: ✅ Confirmed - CSS in separate file, no inline styles
- **V. Simplicity**: ✅ Confirmed - Functions under 50 lines where possible
- **VI. Prototype Reusability**: ✅ Confirmed - Standard pattern for any astro database with spectra
- **VII. SQLite Compatibility**: ✅ Confirmed - Uses existing SQLite via Astrodbkit

No design changes affect constitution compliance.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. Feature fully complies with constitution principles.

