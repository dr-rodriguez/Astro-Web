# Tasks: Cone Search Form

**Feature**: Cone Search Form  
**Branch**: `006-cone-search`  
**Date**: 2024-12-19

## Overview

Add cone search functionality to the Search page, allowing users to search for astronomical objects within a specified spatial region using coordinates and a search radius. The feature adds a form section, coordinate parsing utilities, database query function, route handler, and styling while reusing existing search_results display infrastructure.

## Implementation Strategy

**MVP Scope**: User Story 1 (P1) - Core cone search functionality with decimal degree input  
**Incremental Delivery**:
1. Implement coordinate parsing and radius conversion (foundational)
2. Add cone search endpoint and database query (US1)
3. Enhance coordinate format support (US2)
4. Implement radius unit conversion (US3)
5. Integrate with existing results display (US4)

**Dependencies**: User Story 1 must be completed before Stories 2-4 can be tested. Stories 2-4 enhance the core functionality with flexible input formats and configurable radius.

**Parallel Opportunities**: Coordinate parsing functions, CSS styling, and API endpoint can be developed in parallel.

## Task Dependencies

### User Story Completion Order

```
US1 (P1) → US2 (P2) → US3 (P2) → US4 (P3)
```

**Rationale**: User Story 1 provides core cone search with decimal degree input. Stories 2-4 enhance format support and radius configuration. All stories ultimately integrate with the same results display (US4).

## Phase 1: Setup

No setup tasks required. Feature extends existing application infrastructure.

## Phase 2: Foundational Tasks

**Goal**: Implement coordinate parsing and radius conversion utilities required for all cone search operations.

### T001 [P] Add coordinate parsing utility function to src/database/query.py
Implement `parse_coordinate_to_decimal()` function that:
- Accepts coordinate string in sexagesimal or decimal format
- Accepts `is_ra` parameter to distinguish RA from Dec parsing
- Tries sexagesimal parsing first (per spec requirement)
- Falls back to decimal degrees if sexagesimal parsing fails
- Validates coordinate ranges (RA: 0-360°, Dec: -90 to +90°)
- Returns decimal degrees as float
- Raises ValueError with descriptive message on parsing failure

**File**: `src/database/query.py`

### T002 [P] Add radius unit conversion utility function to src/database/query.py
Implement `convert_radius_to_degrees()` function that:
- Accepts radius value (float) and radius_unit string
- Converts arcseconds to degrees (divide by 3600)
- Converts arcminutes to degrees (divide by 60)
- Leaves degrees unchanged
- Validates radius is positive
- Validates radius does not exceed 10 degrees after conversion
- Returns radius in degrees as float
- Raises ValueError with descriptive message on validation failure

**File**: `src/database/query.py`

### T003 [P] Add cone search query function to src/database/query.py
Implement `cone_search()` function that:
- Accepts ra (float), dec (float), radius_deg (float) parameters
- Connects to database using CONNECTION_STRING
- Calls astrodbkit `db.query_region(ra, dec, radius_deg, coord_frame='icrs')`
- Measures execution time
- Applies 10,000 result cap using `.head(10000)` if needed
- Returns tuple of (results DataFrame, execution_time float)
- Preserves existing search_objects() function unchanged

**File**: `src/database/query.py`

### T004 Add import statements for astropy.coordinates to src/database/query.py
Add `from astropy.coordinates import SkyCoord, Angle` import at top of file for coordinate parsing support.

**File**: `src/database/query.py`

## Phase 3: User Story 1 - Search by Sky Coordinates (P1)

**Goal**: Enable users to search for astronomical objects within a specified sky region using coordinates and radius.

**Independent Test**: Navigate to /search page, enter valid decimal degree coordinates (RA and Dec), specify radius in arcminutes, submit form, and verify results are returned in table format with clickable source links.

### T005 [P] [US1] Add cone search form section to src/templates/search.html
Add HTML form below existing text search form:
- Add `<h2>` heading: "Cone Search" with margin-top: 2rem styling
- Add descriptive paragraph about cone search functionality
- Create form with method="post", action="/search/cone-results", id="coneSearchForm"
- Add form-group div with label "Right Ascension (RA):" and text input
- Add placeholder and help text: "Enter as decimal degrees (209.30) or sexagesimal (13h57m12s)"
- Add form-group div with label "Declination (Dec):" and text input
- Add placeholder and help text: "Enter as decimal degrees (14.48) or sexagesimal (+14d28m39s)"
- Add form-group div with label "Search Radius:" and inline layout (display: flex)
- Add number input for radius with step="0.001", min="0", max-width: 150px
- Add dropdown select for radius_unit with options: arcseconds, arcminutes (selected), degrees
- Add submit button
- Preserve existing text search form and JavaScript unchanged

**File**: `src/templates/search.html`

### T006 [US1] Implement cone_search_results route handler in src/routes/web.py
Add async function `cone_search_results()` that:
- Accepts Request and form parameters: ra, dec, radius, radius_unit (all str)
- Parses coordinates using parse_coordinate_to_decimal(ra, is_ra=True) and parse_coordinate_to_decimal(dec, is_ra=False)
- Converts radius using convert_radius_to_degrees(radius, radius_unit)
- Executes cone_search(ra_decimal, dec_decimal, radius_degrees)
- Checks if results truncated (len >= 10000) and creates warning message
- Converts DataFrame to list of dicts using .to_dict('records')
- Applies get_source_url() to results for clickable links
- Creates navigation context using create_navigation_context(current_page="/search")
- Returns TemplateResponse for "search_results.html" with: request, query_text (formatted search params), results, total_count, execution_time, warning (if truncated), ra_input, dec_input, radius_value, radius_unit, nav_context
- Catches ValueError for validation errors and returns search.html with error message
- Catches Exception for database errors and returns search_results.html with error message and empty results

**File**: `src/routes/web.py`

### T007 [US1] Add cone_search_results route to src/main.py
Import cone_search_results from src.routes.web  
Add route decorator: @app.post("/search/cone-results", response_class=HTMLResponse)  
Add route function: async def cone_search_results_page() that calls web.cone_search_results()

**File**: `src/main.py`

### T008 [P] [US1] Add import statements for coordinate parsing functions in src/routes/web.py
Add imports: parse_coordinate_to_decimal, convert_radius_to_degrees, cone_search from src.database.query

**File**: `src/routes/web.py`

### T009 [P] [US1] Add CSS styling for cone search form section to src/static/style.css
Add CSS rules for:
- h2 with margin-top: 2rem, border-top: 2px solid #ddd, padding-top: 1rem
- .form-group small with display: block, margin-top: 0.25rem, color: #666, font-size: 0.875rem
- .warning-message with background-color: #fff3cd, border: 1px solid #ffc107, color: #856404, padding: 1rem, border-radius: 4px, margin: 1rem 0
- .error-message with background-color: #f8d7da, border: 1px solid #f5c6cb, color: #721c24, padding: 1rem, border-radius: 4px, margin: 1rem 0
- Form field inline layout: display: flex, gap: 0.5rem, align-items: center for number input and select

**File**: `src/static/style.css`

### T010 [US1] Add client-side form validation JavaScript to src/templates/search.html
Add event listener for coneSearchForm submit:
- Get ra, dec, radius values and trim whitespace
- Check all three fields are non-empty
- If validation fails, prevent default and show alert: "Please fill in all required fields"
- Place after existing textSearchForm validation code

**File**: `src/templates/search.html`

## Phase 4: User Story 2 - Flexible Coordinate Input (P2)

**Goal**: Support both decimal degrees and sexagesimal coordinate formats for flexible user input.

**Independent Test**: Enter same coordinates in decimal (209.30, 14.48) and sexagesimal (13h57m12s, +14d28m39s) formats for same radius and verify identical results.

### T011 [P] [US2] Enhance parse_coordinate_to_decimal to support sexagesimal RA format in src/database/query.py
Modify parse_coordinate_to_decimal() to detect and parse sexagesimal RA:
- Check for presence of 'h', 'm', 's', 'd' characters in coord_str
- If found and is_ra=True, use SkyCoord to parse sexagesimal format
- Support formats like "13h57m12.37s", "13h 57m 12s", "13 57 12.37"
- Return skycoord.ra.deg for RA extraction
- Maintain fallback to decimal degrees if parsing fails

**File**: `src/database/query.py`

### T012 [P] [US2] Enhance parse_coordinate_to_decimal to support sexagesimal Dec format in src/database/query.py
Modify parse_coordinate_to_decimal() to detect and parse sexagesimal Dec:
- Check for presence of 'd', '°', 'm', "'", 's', '"' characters in coord_str
- If found and is_ra=False, use SkyCoord to parse sexagesimal format
- Support formats like "+14d28m39.8", "-45d30m", "+14° 28' 39"", "-90°"
- Return skycoord.dec.deg for Dec extraction
- Maintain fallback to decimal degrees if parsing fails

**File**: `src/database/query.py`

### T013 [US2] Update parse_coordinate_to_decimal error handling in src/database/query.py
Enhance exception handling in parse_coordinate_to_decimal():
- Wrap try-except block around all coordinate parsing logic
- Catch ValueError and TypeError exceptions
- Raise ValueError with message: "Invalid coordinate format: {coord_str}"
- Preserve exception chain with "from e" syntax
- Ensure coordinate range validation occurs for decimal fallback

**File**: `src/database/query.py`

## Phase 5: User Story 3 - Configurable Search Radius (P2)

**Goal**: Allow users to select appropriate radius unit (degrees, arcminutes, arcseconds) for searches at different angular scales.

**Independent Test**: Enter same numeric radius value with different units (arcseconds, arcminutes, degrees) and verify results scale appropriately with selected unit.

### T014 [P] [US3] Verify convert_radius_to_degrees handles all three unit types in src/database/query.py
Ensure convert_radius_to_degrees() implements all unit conversions correctly:
- Verify arcseconds conversion: divide by 3600.0
- Verify arcminutes conversion: divide by 60.0
- Verify degrees conversion: no division (multiply by 1.0)
- Validate all conversions respect 10-degree maximum limit
- Test with common values: 3600 arcseconds = 1 degree, 60 arcminutes = 1 degree

**File**: `src/database/query.py`

### T015 [US3] Verify cone_search applies result cap correctly in src/database/query.py
Verify cone_search() properly handles 10,000 object cap:
- Apply .head(10000) to results DataFrame when len(results) > 10000
- Return truncated DataFrame with execution time
- Document that caller must detect truncation by checking original length
- Ensure performance is not impacted by applying cap

**File**: `src/database/query.py`

## Phase 6: User Story 4 - Display Spatial Search Results (P3)

**Goal**: Display cone search results in same table format as text search with consistent functionality.

**Independent Test**: Perform cone search and verify results display in DataTable format with clickable source links, execution time, and result count matching text search behavior.

### T016 [US4] Update search_results.html to support cone search warning messages
Modify search_results.html template to:
- Add conditional block checking if warning variable exists
- Display warning-message div with warning text if warning is set
- Place warning message block before results count display
- Ensure warning styling from CSS is applied (background #fff3cd, border #ffc107)
- Maintain compatibility with text search results (warning is optional)

**File**: `src/templates/search_results.html`

### T017 [US4] Verify search_results.html handles both text and cone search results
Ensure search_results.html works for both search types:
- Check query_text variable displays appropriately for both search types
- Verify results table structure supports both search result formats
- Ensure execution_time displays correctly for both
- Confirm total_count works for both
- Test DataTable initialization works identically for both search types

**File**: `src/templates/search_results.html`

### T018 [US4] Add API endpoint for cone search in src/routes/web.py
Implement cone_search_api() function that:
- Accepts form parameters: ra, dec, radius, radius_unit (all str)
- Performs same parsing, validation, and query execution as cone_search_results
- Returns JSON response with: results, total_count, ra_input, dec_input, radius_value, radius_unit, execution_time, search_time (datetime.now().isoformat()), warning (if truncated)
- Catches ValueError and raises HTTPException(status_code=400, detail=str(e))
- Catches Exception and raises HTTPException(status_code=500, detail=f"An error occurred during search: {e}")

**File**: `src/routes/web.py`

### T019 [US4] Add cone search API route to src/main.py
Import cone_search_api from src.routes.web  
Add route decorator: @app.post("/api/search/cone")  
Add route function: async def cone_search_api_endpoint() that calls web.cone_search_api()  
Ensure API route comes before catch-all 404 route

**File**: `src/main.py`

## Phase 7: Polish & Cross-Cutting Concerns

### T020 Add coordinate format help text to cone search form in src/templates/search.html
Enhance form usability by:
- Adding more detailed placeholder examples (e.g., "e.g., 13h57m12s or 209.30")
- Adding format help text explaining both supported formats
- Adding unit conversion reference (arcseconds to degrees, etc.)
- Ensuring help text is visible and informative without cluttering UI

**File**: `src/templates/search.html`

### T021 Verify error handling displays user-friendly messages in all error scenarios
Test and verify error messages:
- Missing RA/Dec/radius fields: "All fields (RA, Dec, radius) are required"
- Invalid sexagesimal format: "Invalid coordinate format: {value}. Supported formats: decimal degrees or sexagesimal"
- RA out of range: "RA must be between 0 and 360 degrees"
- Dec out of range: "Dec must be between -90 and +90 degrees"
- Radius too large: "Radius must not exceed 10 degrees"
- Negative radius: "Radius must be a positive number"
- Database errors: "An error occurred during search: {error_message}"

**Files**: `src/routes/web.py`, `src/database/query.py`

### T022 Verify form input values are preserved in search results page
Test that cone search form values are preserved:
- ra_input, dec_input, radius_value, radius_unit are passed to template
- Values display correctly if user wants to refine search
- Values can be copy-pasted for new searches
- Integration with text search doesn't interfere with value preservation

**File**: `src/routes/web.py`, `src/templates/search_results.html`

## Task Summary

**Total Tasks**: 22  
**Parallelizable**: 11 tasks  
**Sequential**: 11 tasks

**Tasks by User Story**:
- Foundational: 4 tasks
- US1 (P1): 6 tasks
- US2 (P2): 3 tasks  
- US3 (P2): 2 tasks
- US4 (P3): 4 tasks
- Polish: 3 tasks

**MVP Scope (User Story 1)**: T001-T010 (10 tasks)  
**Completion Order**: Foundational → US1 → US2 → US3 → US4 → Polish

**Independent Test Criteria**:
- US1: Submit cone search form with valid decimal coordinates and verify results table appears
- US2: Submit same coordinates in different formats and verify same results
- US3: Submit same numeric radius with different units and verify appropriate scaling
- US4: Verify cone search results display with same functionality as text search results

