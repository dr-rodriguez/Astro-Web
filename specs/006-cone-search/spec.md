# Feature Specification: Cone Search Form

**Feature Branch**: `006-cone-search`  
**Created**: 2024-12-19  
**Status**: Draft  
**Input**: User description: "Add a cone search form to the search page. This should take RA and Dec in either degree or sexagesimal and a search radius with a selectable unit dropdown (degrees, arcminutes, arcseconds). The results should show up in the search_results page. We should use Astrodbkit's query_region method as described in @https://astrodbkit.readthedocs.io/en/latest/#region-spatial-search"

## Clarifications

### Session 2024-12-19

- Q: How should the system handle result volume limits for cone searches? → A: System must cap results at 10,000 records with warning message to user
- Q: What specific sexagesimal format variants should be supported for parsing? → A: Flexible parsing with spaces optional, symbol variations accepted (°, ', ", or d, m, s)
- Q: How should the system automatically detect whether input is decimal degrees or sexagesimal format? → A: Always try sexagesimal first, fall back to degrees if it fails
- Q: How should the system handle very large radius values (e.g., > 90 degrees)? → A: Block submission and display validation error for radius > 10 degrees
- Q: How should the cone search form be laid out on the Search page with the existing text search? → A: Cone search displayed as separate section below text search on same page

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Search by Sky Coordinates (Priority: P1)

A user wants to find all astronomical objects within a specific region of the sky by entering coordinates (Right Ascension and Declination) and a search radius. They navigate to the Search page, fill in the cone search form with coordinates, select a radius unit, and receive a table of matching objects that fall within the specified region.

**Why this priority**: This is the core functionality that enables spatial/coordinate-based searches, which is a fundamental operation in astronomical databases. Users who know object coordinates need an efficient way to discover objects near those coordinates.

**Independent Test**: Can be fully tested by accessing the Search page with cone search form visible, entering valid RA/Dec coordinates and radius values, and verifying that results are returned in a table format with clickable links to individual source pages.

**Acceptance Scenarios**:

1. **Given** a user is on the Search page, **When** they see a cone search form with RA, Dec, radius, and unit dropdown fields, **Then** they can enter coordinate values and submit the search
2. **Given** a user enters valid RA and Dec in decimal degrees format (e.g., 209.301675, 14.477722), **When** they select a radius (e.g., 0.5) and unit (e.g., arcminutes), **Then** they are redirected to search results page showing objects within that search region
3. **Given** a user enters valid RA and Dec in sexagesimal format (e.g., 13h 57m 12.37s, +14° 28' 39.8"), **When** they submit the form, **Then** the system converts these to decimal degrees and performs the cone search
4. **Given** a user views cone search results, **When** they see astronomical objects in the results table, **Then** each result is within the specified radius of the target coordinates

---

### User Story 2 - Flexible Coordinate Input (Priority: P2)

A user wants flexibility in how they enter coordinates - they may have coordinates in different formats from different sources. They need to be able to enter coordinates in either decimal degrees or sexagesimal format without needing to pre-convert values.

**Why this priority**: Different astronomical data sources provide coordinates in different formats, and requiring manual conversion creates friction for users. Supporting both formats makes the system more accessible.

**Independent Test**: Can be fully tested by entering the same coordinates in both decimal degrees and sexagesimal formats and verifying that both return the same search results for the same radius.

**Acceptance Scenarios**:

1. **Given** a user has coordinates in decimal degrees format (e.g., 209.30, 14.48), **When** they enter these values into the RA and Dec fields, **Then** the system accepts them as decimal degrees and performs the search
2. **Given** a user has coordinates in sexagesimal format (e.g., 13h 57m 12s, +14° 28' 39"), **When** they enter these values into the RA and Dec fields, **Then** the system automatically detects the format, converts to decimal degrees, and performs the search
3. **Given** a user enters a mix of decimal degrees and sexagesimal (e.g., decimal RA but sexagesimal Dec), **When** they submit the form, **Then** the system handles both formats correctly in a single search

---

### User Story 3 - Configurable Search Radius (Priority: P2)

A user wants to control the size of their search region to find objects at different scales - from a small region around a known object to larger sky surveys. They need to select an appropriate radius unit (degrees, arcminutes, or arcseconds) to match their search intent.

**Why this priority**: Astronomical searches operate across vastly different angular scales. Being able to search within arcseconds around a target versus degrees for a survey is essential for different use cases.

**Independent Test**: Can be fully tested by performing searches with the same numeric radius value but different units (degrees, arcminutes, arcseconds) and verifying that results appropriately scale with the selected unit.

**Acceptance Scenarios**:

1. **Given** a user wants to find objects very close to a specific location (within 1 arcminute), **When** they set radius=1 and select unit="arcminutes", **Then** the search returns objects within 1 arcminute of the target
2. **Given** a user wants to perform a wide-field survey around coordinates, **When** they set radius=5 and select unit="degrees", **Then** the search returns objects within 5 degrees of the target (within maximum of 10 degrees)
3. **Given** a user performs a cone search with radius unit in arcseconds, **When** they submit the form, **Then** the system correctly converts arcseconds to degrees for the database query
4. **Given** a user performs a cone search with radius unit in arcminutes, **When** they submit the form, **Then** the system correctly converts arcminutes to degrees for the database query

---

### User Story 4 - Display Spatial Search Results (Priority: P3)

A user wants to see the results of their cone search in the same results table format as text-based searches, with clear indication of which objects were found within their specified region.

**Why this priority**: Consistent presentation of results across different search types improves user experience and allows users to navigate to individual object pages regardless of search method used.

**Independent Test**: Can be fully tested by performing a cone search and verifying that results are displayed in the same table format with clickable source links as text-based search results.

**Acceptance Scenarios**:

1. **Given** a cone search finds multiple objects, **When** results are displayed, **Then** the results table shows all found objects in the same format as text search results
2. **Given** a user views cone search results, **When** they click on a source name in the results table, **Then** they are taken to the individual source inventory page for that object
3. **Given** a cone search returns no results, **When** the results page loads, **Then** a clear message indicates no objects were found within the specified region
4. **Given** a cone search completes successfully, **When** results are displayed, **Then** users can see the total count of objects found and the execution time

---

### Edge Cases

- What happens when users enter invalid RA/Dec coordinates (e.g., RA > 360 or Dec > 90)? → Display validation error prompting correction
- What happens when users enter sexagesimal RA with hours > 24 or invalid sexagesimal format? → Display validation error with format guidance
- How does the system handle negative Dec values in both decimal and sexagesimal formats? → System accepts negative Dec values as coordinates are in southern hemisphere
- What happens when users enter a radius of 0 or negative radius? → Display validation error requiring positive radius
- What happens when users don't fill in all required fields (RA, Dec, or radius)? → Display validation error listing missing fields
- How does the system handle RA values that wrap around the 360-degree boundary? → Database handles coordinate wraparound using proper angular distance calculations
- What happens when users enter coordinates but no objects exist within the specified radius? → Display "No objects found within specified region" message
- How does the system handle very large radius values (e.g., > 10 degrees)? → Block submission and display validation error with message "Radius must not exceed 10 degrees"
- What happens when users switch between text search and cone search on the same page? → Both search forms are accessible and operate independently
- What happens when a cone search finds more than 10,000 objects? → System returns first 10,000 objects and displays warning message about result truncation

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a cone search form on the Search page with input fields for RA, Dec, radius value, and radius unit selection
- **FR-002**: System MUST accept RA and Dec in decimal degrees format (e.g., 209.30, 14.48) and automatically detect this format by checking for absence of sexagesimal separators (h/m/s or °, ', ")
- **FR-003**: System MUST accept RA and Dec in sexagesimal format with flexible parsing supporting: spaces optional (e.g., "13h57m12s" or "13h 57m 12s"), symbol variations for degrees/minutes/seconds (h/d for hours/degrees, m for minutes, s for seconds, or °, ', " for RA/Dec), and case-insensitive input
- **FR-004**: System MUST provide a radius unit dropdown with three options: degrees, arcminutes, arcseconds
- **FR-005**: System MUST convert the user-specified radius to degrees before calling Astrodbkit's query_region method
- **FR-006**: System MUST call Astrodbkit's query_region method with the target coordinates and search radius in degrees
- **FR-007**: System MUST display cone search results in the same JavaScript DataTable format as text search results
- **FR-008**: System MUST show all columns from the Sources table in the results (source, ra, dec, epoch, equinox, shortname, reference, other_references, comments)
- **FR-009**: System MUST make the source column in results clickable to navigate to individual source inventory pages
- **FR-010**: System MUST display results count and execution time for cone searches
- **FR-011**: System MUST handle cases where no objects are found within the specified region
- **FR-012**: System MUST validate that all required fields (RA, Dec, radius) are provided before submitting the search
- **FR-013**: System MUST validate coordinate ranges (RA: 0-360 degrees or 0h-24h, Dec: -90 to +90 degrees)
- **FR-014**: System MUST validate that radius values are positive numbers
- **FR-023**: System MUST validate that radius values do not exceed 10 degrees (after unit conversion) and block submission with error message "Radius must not exceed 10 degrees"
- **FR-015**: System MUST display appropriate error messages when validation fails
- **FR-016**: System MUST handle conversion errors when invalid sexagesimal coordinates are entered
- **FR-017**: System MUST handle Astrodbkit query_region errors gracefully with user-friendly error messages
- **FR-018**: System MUST preserve form input values (RA, Dec, radius, unit) when displaying search results
- **FR-019**: System MUST allow users to perform both text search and cone search on the same Search page
- **FR-020**: System MUST display cone search form as a separate section below the text search form on the Search page
- **FR-024**: System MUST display cone search results on the search_results page, integrating with existing results display functionality
- **FR-021**: System MUST cap cone search results at 10,000 objects with warning message indicating truncation
- **FR-022**: System MUST display warning message when result cap is reached (e.g., "Results limited to 10,000 objects. Refine search to see all results.")

### Key Entities *(include if feature involves data)*

- **Cone Search Query**: User input containing target coordinates (RA, Dec), search radius value, and radius unit; represents a spatial region in the sky
- **Target Coordinates**: RA and Dec values specified by the user, in either decimal degrees or sexagesimal format, defining the center of the search region
- **Search Radius**: Distance from the target coordinates defining the circular search region, with user-selected unit (degrees, arcminutes, arcseconds) that must be converted to degrees
- **Cone Search Results**: Collection of astronomical objects returned by Astrodbkit's query_region method that fall within the specified spatial region
- **Astronomical Objects**: Individual sources with coordinate information that can be spatially queried using cone search functionality

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete a cone search from Search page to results page in under 30 seconds for typical queries (radius ≤ 1 degree, < 1000 results)
- **SC-002**: 95% of valid cone search queries return results successfully within 5 seconds
- **SC-003**: Users can enter coordinates in both decimal degrees and sexagesimal formats with 90% successful format detection
- **SC-004**: Cone search results are displayed on the search_results page with the same functionality as text search results
- **SC-005**: Users can navigate from cone search results to individual source pages with one click on the source name
- **SC-006**: All cone searches for radius ≤ 1 arcminute return results within 3 seconds for databases with 10,000+ sources
- **SC-007**: Cone search results accurately include objects within the specified radius and exclude objects outside the radius with 100% spatial accuracy
- **SC-008**: Users receive clear validation error messages for invalid inputs (invalid coordinates, missing fields, negative radius) in under 1 second