# Feature Specification: Individual Source Inventory Page

**Feature Branch**: `004-source-inventory`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: User description: "Let's create an inventory page for an individual source entry. This will use the inventory method from @https://astrodbkit.readthedocs.io/en/latest/  to gather relevant data for that source. Each key from the inventory result should be it's own DataTable. If a key is not present, it need not be displayed. If needed, @schema.yaml provides the database schema in yaml format as a reference. This inventory page should be accessible via a route using the url-encoded source name."

## Clarifications

### Session 2025-01-27
- Q: How should source inventory URLs be encoded? → A: Always URL-encode all source names before routing, regardless of special characters (Option D)
- Q: What happens while inventory data is loading? → A: Display loading indicator/skeleton with "Loading source inventory..." message (Option B)
- Q: How should large datasets with thousands of rows be displayed? → A: Use scrolling with a fixed display limit (e.g., show first 100-500 rows) - reasonable balance (Option C)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Comprehensive Source Inventory (Priority: P1)

A user navigates to an individual source's inventory page to view all data associated with that astronomical source. The page displays information from the Sources table plus all related data from other tables (Photometry, Spectra, Parallaxes, etc.) in organized data tables.

**Why this priority**: This provides the primary functionality for users to explore detailed information about a specific source. It's the core value proposition of the inventory page feature and cannot be partially implemented.

**Independent Test**: Can be fully tested by navigating to a specific source's inventory page (e.g., via URL-encoded source name) and verifying that multiple data tables are displayed, each representing a different data type from the inventory result. This delivers value by providing comprehensive source information in one place.

**Acceptance Scenarios**:

1. **Given** a user knows a source identifier, **When** they navigate to the inventory page using the URL-encoded source name, **Then** they see multiple data tables, each displaying data from a different key in the inventory result (e.g., Sources, Photometry, Spectra, Parallaxes, ProperMotions)
2. **Given** the inventory result contains data for a source, **When** a user views the inventory page, **Then** only tables for keys that have data are displayed
3. **Given** a source with limited data, **When** a user views the inventory page, **Then** only the relevant data tables (e.g., Sources and one other table) are displayed, with empty or non-existent keys not shown

---

### User Story 2 - Navigate to Source from Browse Page (Priority: P2)

A user is viewing the browse page with the Sources table, and clicks on a source to view its detailed inventory. The navigation maintains context and provides a clear path back.

**Why this priority**: This connects existing functionality (browse page) with the new inventory capability, making the inventory feature discoverable and accessible through the primary data navigation flow.

**Independent Test**: Can be fully tested by starting from the browse page, clicking on a source identifier, and arriving at the inventory page with all data displayed. This delivers value by providing intuitive navigation between listing and detail views.

**Acceptance Scenarios**:

1. **Given** a user is on the browse page viewing the Sources table, **When** they click on a source identifier, **Then** they are navigated to that source's inventory page
2. **Given** a user is viewing a source inventory page, **When** they use the navigation, **Then** they can return to the browse page or navigate to other sections
3. **Given** a user navigates between browse and inventory pages, **When** they perform this action multiple times, **Then** each navigation completes within 2 seconds

---

### User Story 3 - Handle Invalid or Missing Sources (Priority: P3)

A user attempts to access an inventory page for a source that doesn't exist or has a malformed identifier. The system provides clear feedback and handles the error gracefully.

**Why this priority**: This ensures a robust user experience when users enter invalid URLs or try to access sources that have been removed. It prevents confusing error states and provides clear guidance.

**Independent Test**: Can be fully tested by attempting to navigate to a non-existent source (using both invalid identifiers and valid-looking but missing identifiers) and verifying that an appropriate error message is displayed. This delivers value by preventing user confusion and maintaining application stability.

**Acceptance Scenarios**:

1. **Given** a user attempts to view inventory for a non-existent source, **When** they navigate to the inventory URL with an invalid source identifier, **Then** they see a clear error message indicating the source was not found
2. **Given** a user provides a URL-encoded source identifier with special characters, **When** the system processes the request, **Then** the identifier is correctly decoded and used to query the database
3. **Given** database connection fails during inventory retrieval, **When** a user attempts to access an inventory page, **Then** they receive a clear error message that data is temporarily unavailable

---

### Edge Cases

- What happens when URL-encoded source names contain special characters (spaces, commas, special Unicode)? System correctly decodes the URL-encoded identifier before database query
- How does system handle sources with no related data (only Sources table data exists)? Only the Sources table is displayed; other data tables are not shown
- What happens when inventory method returns an unexpected key structure? System handles gracefully by displaying known tables and ignoring unknown keys
- How does system handle very long source identifiers in URLs? URL encoding ensures all characters are properly encoded and decoded
- What happens when user provides source identifier in wrong case (if database is case-sensitive)? System matches source identifiers based on database's actual comparison rules
- How does system handle database timeout during inventory retrieval? Error is displayed to user indicating temporary unavailability
- What happens when a source exists but all related table queries return empty results? Only the Sources table with basic information is displayed
- What is shown to user during the 5-second inventory retrieval? A loading indicator or skeleton screen with "Loading source inventory..." message is displayed while data is fetched
- How are data tables with thousands of rows displayed? System uses scrolling with a fixed display limit (e.g., first 100-500 rows), allowing users to scroll through all data while maintaining reasonable page performance

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a route accessible via URL-encoded source name (e.g., `/source/{source_name}`) to display individual source inventory
- **FR-002**: System MUST use the inventory method from astrodbkit to retrieve all data for a specific source
- **FR-003**: System MUST display each key from the inventory result as a separate data table on the page
- **FR-004**: System MUST only display data tables for keys that have data (empty results should not show empty tables)
- **FR-005**: System MUST always URL-encode all source names before routing and correctly decode them for database queries (handles special characters, spaces, Unicode characters consistently)
- **FR-006**: System MUST display the source identifier prominently at the top of the inventory page
- **FR-007**: System MUST include navigation to allow users to return to browse page or navigate to other sections
- **FR-008**: System MUST handle errors gracefully when source doesn't exist, displaying a clear "source not found" message
- **FR-009**: System MUST handle database connection errors gracefully, displaying an appropriate error message
- **FR-010**: System MUST retrieve and display inventory data within 5 seconds of page request
- **FR-011**: System MUST maintain existing navigation structure (header, footer, navigation bar) on inventory pages
- **FR-012**: System MUST display a loading indicator (e.g., "Loading source inventory...") while retrieving inventory data from the database
- **FR-013**: System MUST use scrolling with a fixed display limit (e.g., first 100-500 rows) for data tables with large numbers of rows to maintain reasonable page load performance

### Key Entities *(include if feature involves data)*

- **Source Inventory**: Represents the complete data collection for a single astronomical source, including base information from Sources table and all related data from other tables (Photometry, Spectra, Parallaxes, ProperMotions, RadialVelocities, SpectralTypes, Gravities, etc.)
- **Inventory Data Table**: Represents a single data table displayed on the inventory page, corresponding to one key from the inventory result (e.g., a table for Photometry data, a table for Spectra data)
- **URL-Encoded Source Identifier**: Represents the source name encoded for safe transmission in URL path, supporting special characters and spaces

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can navigate to any source's inventory page using the URL-encoded source name within 2 seconds of accessing the URL
- **SC-002**: Inventory page displays at least 2 data tables for sources with related data (Sources table plus at least one other table) within 5 seconds of page load
- **SC-003**: System correctly handles URL-encoded identifiers with special characters (spaces, commas, Unicode) and successfully displays inventory data
- **SC-004**: When a source has data in different tables (e.g., Sources, Photometry, Spectra, Parallaxes, ProperMotions), all tables are displayed on the inventory page
- **SC-005**: System provides clear error messages within 2 seconds when users attempt to access non-existent sources
- **SC-006**: Users can navigate between browse page and inventory pages seamlessly, with page transitions completing within 2 seconds

## Dependencies

- Existing astrodbkit integration for database access
- Existing database structure (SIMPLE.sqlite) with Sources table and related tables
- Existing web server infrastructure and route handling
- Existing navigation system (header, footer, navigation bar)
- URL encoding/decoding capability for handling special characters in source names

## Assumptions

- Source identifiers in the database are unique and match exactly with what users will provide in URLs
- The inventory method from astrodbkit returns data in a dictionary structure with table names as keys
- Users will navigate to inventory pages either by clicking from the browse page or by typing URLs directly
- URL encoding will handle all special characters that may appear in source identifiers
- The database connection and inventory retrieval will typically complete within 5 seconds for sources with moderate amounts of data
- Data tables will use scrolling with a fixed display limit (e.g., first 100-500 rows visible) for very large datasets to balance full data access with page performance
- Only sources that exist in the Sources table will have accessible inventory pages

## Out of Scope

This feature explicitly does NOT include:

- Ability to edit or modify source data through the inventory page
- Ability to add new data entries for a source through the page
- Export functionality for individual tables or the entire inventory
- Ability to compare multiple sources side-by-side
- Visualizations or charts of the inventory data (e.g., plotting photometry over time)
- Full-text search within the inventory data
- Bulk operations on multiple sources
- Downloading individual spectrum files or other data files
- Real-time updates when underlying database data changes
- User authentication or authorization for accessing inventory data
- Ability to flag or bookmark sources
- Support for printing or PDF generation of inventory pages
