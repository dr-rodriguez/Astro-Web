# Feature Specification: Spectra Display Page

**Feature Branch**: `007-spectra-display`  
**Created**: 2025-01-28  
**Status**: Draft  
**Input**: User description: "Let's create a spectra page that shows a Bokeh plot of all spectra for a given source. It should be accessible from the inventory page if any spectra are present and fetch them using astrodbkit, such as with db.query(db.Spectra).spectra(fmt='pandas'). Not all spectra are displayable, those that can't be displayed should be skipped. We should provide a small table with the spectra information and clickable links. We should have a single plot with all spectra displayed and a legend that allows us to identify which is which. The column for the spectra is access_url, which should be a configurable variable in case other databases have different column names."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Spectra Visualization from Inventory (Priority: P1)

A user is viewing a source's inventory page and notices there are spectra available. They click a link to view the spectra visualization page, which displays all spectra for that source in a single interactive plot with clear identification via a legend.

**Why this priority**: This is the primary access pathway and core functionality - providing visual representation of all spectra for a source. This delivers the main value proposition of the feature and cannot be partially implemented.

**Independent Test**: Can be fully tested by navigating from the inventory page to the spectra visualization page and verifying that all spectra are displayed in an interactive plot with a visible legend. This delivers value by enabling users to visually compare multiple spectra for the same source in one view.

**Acceptance Scenarios**:

1. **Given** a user is viewing the inventory page for a source with spectra data, **When** they click the link to view spectra, **Then** they are navigated to a page displaying all spectra for that source in a single interactive plot with axis labels (wavelength on x-axis, flux on y-axis)
2. **Given** a user views the spectra page with multiple spectra, **When** they examine the plot, **Then** a legend is displayed that clearly identifies each spectrum with a unique identifier (e.g., observation date, telescope, regime)
3. **Given** the spectra plot contains multiple spectra, **When** a user interacts with the plot (zoom, pan), **Then** all spectra remain visible and identifiable through the legend

---

### User Story 2 - Access Spectra Metadata Table (Priority: P2)

A user views the spectra page and wants to understand the details and context of each spectrum being displayed. The page provides a metadata table showing spectrum information including observation details, telescope/instrument, and links to access the original data.

**Why this priority**: This provides essential context about the spectra being visualized, enabling users to understand what they're looking at and access the original data sources. This complements the visualization with detailed information.

**Independent Test**: Can be fully tested by navigating to the spectra page for any source with spectra and verifying that a metadata table is displayed with key spectrum information (observation date, regime, telescope, instrument) including clickable links to access spectrum URLs. This delivers value by providing detailed context and data access.

**Acceptance Scenarios**:

1. **Given** a user views the spectra page, **When** they examine the metadata table, **Then** they see key information for each spectrum including observation date, regime, telescope, and instrument
2. **Given** a user views the spectra page, **When** they click a link in the metadata table, **Then** they can access the original spectrum data (via the access_url)
3. **Given** a user views the spectra page with multiple spectra, **When** they examine the metadata table, **Then** each row corresponds to a spectrum visible in the plot, allowing them to identify which metadata matches which plot line

---

### User Story 3 - Handle Non-Displayable Spectra Gracefully (Priority: P3)

A user attempts to view spectra for a source, but some spectra in the database cannot be loaded or displayed. The system gracefully skips unreadable spectra while displaying the rest, providing clear feedback.

**Why this priority**: This ensures robust handling of real-world data issues like corrupt files, unsupported formats, or inaccessible URLs. This prevents user confusion and maintains application stability when data quality varies.

**Independent Test**: Can be fully tested by accessing spectra for a source where some spectra are invalid or unreadable (e.g., invalid URL format, corrupt data) and verifying that valid spectra are displayed while invalid ones are silently skipped. This delivers value by preventing errors and providing the best available visualization.

**Acceptance Scenarios**:

1. **Given** a source has multiple spectra in the database but some cannot be loaded, **When** a user views the spectra page, **Then** only the loadable spectra are displayed in the plot, with no error messages for skipped spectra
2. **Given** a source has at least one valid spectrum, **When** a user views the spectra page, **Then** the page loads successfully displaying the valid spectra even if other spectra failed to load
3. **Given** a source has no valid spectra or all spectra failed to load, **When** a user views the spectra page, **Then** a clear message is displayed indicating no spectra are available for display

---

### User Story 4 - Navigate Back to Inventory Page (Priority: P3)

A user is viewing a spectrum visualization and wants to return to the full source inventory to see other data types. Clear navigation allows them to move between inventory and spectra views seamlessly.

**Why this priority**: This connects the spectra visualization with the broader source inventory, enabling users to explore all data types. This maintains context and supports comprehensive data exploration workflows.

**Independent Test**: Can be fully tested by starting from an inventory page, navigating to the spectra page, then navigating back to the inventory page. This delivers value by providing seamless navigation between related views.

**Acceptance Scenarios**:

1. **Given** a user is viewing a spectra page, **When** they click the back to inventory link or use browser navigation, **Then** they return to the source inventory page with all data tables displayed
2. **Given** a user navigates between inventory and spectra pages multiple times, **When** they perform this action, **Then** each transition completes within 2 seconds

---

### Edge Cases

- What happens when a source has a single spectrum? The visualization displays the single spectrum with appropriate labels
- How does system handle spectra with missing observation dates or other metadata? Missing metadata fields are displayed as "N/A" in both the table and legend
- What happens when all spectra for a source fail to load or are invalid? The page displays a message indicating no spectra are available for display
- How does system handle very large spectrum files that take time to load? System displays a loading indicator while retrieving spectrum data, with loading completing within 10 seconds
- What happens when access_url column contains invalid URLs or broken links? Invalid URLs are skipped silently, and clickable links in the table may not work for broken URLs
- How does system handle sources with 10+ spectra? All spectra are displayed on the plot with a legend that can be toggled to show/hide individual spectra
- What happens when a spectrum URL points to an unsupported file format? The system skips that spectrum and displays others that are supported
- How does system handle network timeouts when fetching spectrum URLs? Network errors are handled gracefully, with loading indicator timing out after 10 seconds and showing an error message if no spectra could be loaded
- What is shown when the spectra page is first accessed? A loading indicator is displayed while spectrum data is being retrieved and the plot is being generated

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a route accessible from the inventory page to display spectra visualization (e.g., `/source/{source_name}/spectra`)
- **FR-002**: System MUST retrieve all spectra for a given source using astrodbkit query methods (e.g., `db.query(db.Spectra).filter(Source.source == source_name).spectra(fmt='pandas')`)
- **FR-003**: System MUST generate a single interactive Bokeh plot displaying all spectra for the source on one plot
- **FR-004**: System MUST display a legend on the plot with each spectrum labeled as "Observation_Date | Regime | Telescope/Instrument" (e.g., "2020-03-15 | NIR | JWST/NIRSpec")
- **FR-005**: System MUST display a metadata table showing observation_date, regime, telescope, instrument, and access_url (as clickable link) for each spectrum
- **FR-006**: System MUST provide clickable links in the metadata table to access the original spectrum data (via the access_url or configured column)
- **FR-007**: System MUST skip spectra that cannot be loaded or displayed without showing error messages to users
- **FR-008**: System MUST only display the spectra link on the inventory page when spectra data exists for that source
- **FR-009**: System MUST make the spectrum URL column name configurable (default: `access_url`) to support different database schemas
- **FR-010**: System MUST handle spectrum loading failures gracefully, displaying valid spectra while silently skipping invalid ones
- **FR-011**: System MUST retrieve and display all valid spectra within 10 seconds of page load
- **FR-012**: System MUST display a loading indicator while spectrum data is being retrieved and the plot is being generated
- **FR-013**: System MUST include navigation to return to the source inventory page from the spectra view
- **FR-014**: System MUST provide axis labels on the plot (wavelength on x-axis, flux on y-axis)
- **FR-015**: System MUST enable interactive plot features (zoom, pan, reset) for exploring the spectra
- **FR-016**: System MUST maintain the same navigation structure (header, footer, navigation bar) on the spectra page
- **FR-017**: System MUST display "-" for any missing metadata fields (observation_date, regime, telescope, instrument) in both the metadata table and legend

### Key Entities *(include if feature involves data)*

- **Spectrum Record**: Represents a single spectrum entry from the database, containing source identifier, access_url, regime, observation date, telescope/instrument details, and metadata
- **Spectrum Visualization**: Represents the interactive Bokeh plot displaying multiple spectra, each as a separate line on the plot with distinct colors and legend entries
- **Spectrum Metadata Table**: Represents the tabular data displayed alongside the plot, showing observation details, telescope/instrument, regime, and clickable links to access spectra

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can navigate from an inventory page to the spectra visualization page within 2 seconds of clicking the spectra link
- **SC-002**: Spectrum data is retrieved and the visualization is displayed within 10 seconds of accessing the spectra page
- **SC-003**: All valid spectra for a source are displayed in a single plot with a legend that clearly identifies each spectrum
- **SC-004**: Users can click links in the metadata table to access at least 95% of valid spectrum URLs successfully
- **SC-005**: System gracefully handles at least 3 consecutive requests to view spectra for different sources without performance degradation
- **SC-006**: Users can navigate between inventory and spectra pages seamlessly, with page transitions completing within 2 seconds
- **SC-007**: The spectra link only appears on inventory pages when spectra data exists for that source

## Dependencies

- Existing source inventory page functionality
- Existing navigation system (header, footer, navigation bar)
- Existing astrodbkit integration for database access
- Existing web server infrastructure and route handling
- Bokeh library for plot generation
- Configuration system for customizable column names

## Clarifications

### Session 2025-01-28

- Q: Which metadata columns should the spectra table display? → A: Observation Date, Regime, Telescope, Instrument, Access URL (link)
- Q: How should spectrum data be loaded from access_url? → A: astrodbkit returns spectrum data already formatted with wavelength and flux arrays accessible directly - no need to use specutils separately
- Q: Which spectrum file formats should the system support? → A: FITS files and ASCII text files (astrodbkit handles format detection automatically)
- Q: What should the legend identify for each spectrum? → A: Observation date, regime, telescope/instrument combined (e.g., "2020-03-15 | NIR | JWST/NIRSpec")
- Q: How should missing metadata be displayed? → A: Display "-" for any missing metadata fields (observation_date, regime, telescope, instrument)

## Assumptions

- Spectra data will be accessed via the `access_url` column (or configured equivalent) which contains URLs or file paths
- astrodbkit returns spectrum data already formatted with wavelength and flux arrays accessible directly - no manual format conversion needed
- Supported spectrum file formats are FITS and ASCII text files (astrodbkit handles format detection automatically)
- The database query `db.query(db.Spectra).filter(db.Spectra.source == source_name).spectra(fmt='pandas')` will return all spectra for a given source with data already formatted
- Invalid or unreadable spectra will be a small minority (less than 20% of spectra)
- Users will typically view spectra for sources with 1-10 spectra at a time
- The configured column name (default: `access_url`) will contain valid URLs or file paths to spectrum data
- Network access to spectrum URLs will generally be available for remote spectra
- Bokeh plot generation will handle moderate numbers of spectra (up to 15) without significant performance issues
- Metadata table will display observation_date, regime, telescope, instrument, and access_url as clickable link
- Legend entries will be formatted as "Observation_Date | Regime | Telescope/Instrument" with "-" for missing fields

## Out of Scope

This feature explicitly does NOT include:

- Ability to download spectrum files directly from the page
- Ability to edit or modify spectrum data through the page
- Comparison of spectra across different sources
- Ability to overlay model spectra or templates on the observed spectra
- Full-text search within spectrum metadata
- Ability to filter which spectra are displayed on the plot
- Interactive spectrum fitting or analysis tools
- Ability to export the plot as an image file
- Support for spectrum file formats that require specialized software beyond standard astronomy libraries
- Real-time updates when underlying spectrum data changes in the database
- User authentication or authorization for accessing spectrum visualizations
- Ability to bookmark or favorite specific spectra
- Support for displaying spectrum error bars or uncertainty
- Ability to customize plot appearance (colors, styles) by user preference
