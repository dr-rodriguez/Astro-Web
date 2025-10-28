# Research: Spectra Display Implementation

**Feature**: Spectra Display Page  
**Date**: 2025-01-28  
**Phase**: 0 - Research & Technical Decisions

## Technology Decisions

### Astrodbkit for Spectrum Database Access

**Decision**: Use Astrodbkit's `db.query(db.Spectra)` method to retrieve spectrum data  
**Rationale**:
- Maintains constitution compliance (Principle II: Astrodbkit Database Abstraction)
- Provides standardized access to spectrum data through astrodbkit API
- Returns pandas DataFrame for consistency with existing codebase patterns
- Filters spectra by source name automatically
- Requires no database schema knowledge or direct SQL access

**API Usage**: 
```python
db = Database(CONNECTION_STRING)
spectra_df = db.query(db.Spectra).filter(db.Spectra.source == source_name).spectra(fmt='pandas')
```

**Parameters**:
- `source_name` (str): Source identifier from inventory page
- `fmt='pandas'`: Return results as pandas DataFrame

**Alternative Methods Considered**:
- Direct SQL queries: ❌ Violates constitution principle
- Custom query methods: ❌ Unnecessary complexity, reimplements astrodbkit functionality

### Spectrum URL Configuration via Environment Variable

**Decision**: Make spectrum URL column name configurable via `ASTRO_WEB_SPECTRA_URL_COLUMN` environment variable (default: `access_url`)  
**Rationale**:
- Different databases may use different column names for spectrum URLs
- Allows deployment flexibility without code changes
- Consistent with existing configuration pattern (`ASTRO_WEB_SOURCE_COLUMN`, `ASTRO_WEB_RA_COLUMN`, etc.)
- Default `access_url` matches spec requirements

**Implementation**:
```python
# In src/config.py
SPECTRA_URL_COLUMN = os.getenv("ASTRO_WEB_SPECTRA_URL_COLUMN", "access_url")

# Usage in database queries
spectra_df = db.query(db.Spectra).filter(db.Spectra.source == source_name).spectra(fmt='pandas')
url_column = SPECTRA_URL_COLUMN
spectrum_urls = spectra_df[url_column].tolist()
```

**Alternatives Considered**:
- Hardcoded column name: ❌ Reduces flexibility across database schemas
- Database-specific configuration files: ❌ Over-engineered for single column name

### Spectrum Data Format from astrodbkit

**Decision**: Use spectrum data directly from astrodbkit - it returns spectra already formatted  
**Rationale**:
- astrodbkit handles spectrum format detection and conversion automatically
- Returns wavelength and flux arrays directly accessible
- No need to install or use specutils separately
- Handles common astronomical spectrum formats transparently (FITS, ASCII, etc.)
- Standardized access to spectrum data through astrodbkit API

**API Usage**:
```python
# astrodbkit returns spectra already formatted with wavelength and flux arrays
spectra_df = db.query(db.Spectra).filter(db.Spectra.source == source_name).spectra(fmt='pandas')
# Access wavelength and flux from the DataFrame directly
# Format varies by spectrum, but arrays are accessible as spec.wavelength, spec.flux, etc.
```

**Supported Formats**: FITS files (.fits), ASCII text files (.txt, .dat, .csv), automatically handled by astrodbkit

**Error Handling**: Gracefully skip spectra that cannot be loaded (invalid URL, unsupported format, corrupt data) without showing error messages to users

**Alternatives Considered**:
- Manual format conversion with specutils: ❌ Unnecessary - astrodbkit already handles this
- Direct FITS file reading with `astropy.io.fits`: ❌ Limited to FITS only, astrodbkit is more flexible
- Manual ASCII parsing: ❌ Reimplements functionality already in astrodbkit
- Raw URL reading: ❌ No format abstraction or standardization

### Bokeh for Interactive Spectrum Visualization

**Decision**: Use Bokeh to generate interactive multi-spectrum plots with legends  
**Rationale**:
- Required by constitution (Principle III: Bokeh Visualizations)
- Supports overlay plots with multiple data series
- Interactive features (zoom, pan, reset) built-in
- Legend support for identifying multiple spectra
- Integrates with existing codebase (already used in scatter plot visualizations)
- Embeddable as HTML/JavaScript in Jinja2 templates

**API Usage**:
```python
from bokeh.plotting import figure
from bokeh.embed import components

# Create figure with axis labels
p = figure(
    title="Spectra for {source_name}",
    x_axis_label="Wavelength (nm)",
    y_axis_label="Flux",
    width=800,
    height=600,
    tools="pan,box_zoom,wheel_zoom,reset",
    toolbar_location="above"
)

# Plot multiple spectra with different colors
for i, (spec, label) in enumerate(spectra):
    p.line(
        spec['wavelength'],
        spec['flux'],
        legend_label=label,
        color=palette[i % len(palette)],
        line_width=2
    )

p.legend.click_policy = "hide"  # Click to hide/show spectra
script, div = components(p)
```

**Legend Format**: "Observation_Date | Regime | Telescope/Instrument" or "-" for missing metadata fields

**Alternatives Considered**:
- Matplotlib: ❌ Not interactive, violates constitution
- Plotly: ❌ Not required by constitution, adds unnecessary dependency

### Spectrum Metadata Display in Table

**Decision**: Display spectrum metadata in HTML table alongside plot  
**Rationale**:
- Provides context for each spectrum being visualized
- Shows observation details, telescope/instrument information
- Includes clickable links to original spectrum data
- Maintains consistency with existing inventory page design
- Enables users to identify which plot line corresponds to which metadata entry

**Table Columns**: observation_date, regime, telescope, instrument, access_url (clickable link)

**Display Format**: Missing metadata fields shown as "-" for consistency

### Inventory Page Integration

**Decision**: Add spectra link to inventory page that only displays when spectra exist  
**Rationale**:
- Seamless integration with existing source inventory workflow
- Discovery of spectra availability without extra queries
- Conditional display based on inventory data prevents empty links
- Maintains user experience consistency

**Implementation**:
```python
# In get_source_inventory or inventory route
if 'Spectra' in inventory_data:
    spectra_count = len(inventory_data['Spectra'])
    has_spectra = spectra_count > 0
```

**Link Display Logic**:
```html
{% if has_spectra %}
<a href="/source/{{ source_name }}/spectra">View Spectra ({{ spectra_count }})</a>
{% endif %}
```

### Error Handling Strategy

**Decision**: Skip unreadable spectra silently and continue processing remaining spectra  
**Rationale**:
- Prevents entire page failure when only some spectra are problematic
- Maximizes value delivery by showing all displayable spectra
- Reduces user confusion by avoiding error messages
- Handles real-world data quality issues gracefully

**Error Conditions Handled**:
1. Invalid URL (404, timeout, network error)
2. Unsupported file format
3. Corrupt or unreadable spectrum data
4. Missing or empty spectrum files
5. Invalid wavelength/flux arrays

**Fallback Behavior**:
- If no spectra can be loaded: Display message "No spectra available for display"
- If some spectra load successfully: Display only valid spectra
- If all spectra load successfully: Display all spectra as normal

### Loading Indicator

**Decision**: Display loading indicator during spectrum data retrieval  
**Rationale**:
- Spectrum loading may take several seconds (network requests, file parsing)
- Provides user feedback that page is processing
- Prevents user confusion during loading delay
- Improves perceived performance with visual feedback

**Implementation**: Use CSS/JavaScript loading spinner or message in template

**Timing**: Display loading indicator until:
1. All spectrum URLs have been fetched (or timed out)
2. All loadable spectra have been processed
3. Bokeh plot has been generated
4. Page is ready to display

### Configuration Pattern

**Decision**: Add `ASTRO_WEB_SPECTRA_URL_COLUMN` to src/config.py following existing patterns  
**Rationale**:
- Consistent with existing configuration system (`ASTRO_WEB_SOURCE_COLUMN`, etc.)
- Follows established patterns for database column customization
- Enables deployment across different database schemas
- Leverages existing environment variable loading infrastructure

**Configuration Location**: `src/config.py`

**Environment Variable**: `ASTRO_WEB_SPECTRA_URL_COLUMN` (default: `access_url`)

## Integration with Existing Infrastructure

### Database Layer
- **New Function**: `get_source_spectra(source_name)` in `src/database/sources.py`
- Queries astrodbkit for spectra, returns pandas DataFrame
- Uses configurable column name for spectrum URLs
- Filters by source name automatically

### Route Layer
- **New Function**: `spectra_display(request, source_name)` in `src/routes/web.py`
- Handles source name decoding and spectrum retrieval
- Calls spectrum loading and visualization functions
- Renders spectra.html template with plot components

### Template Layer
- **New File**: `src/templates/spectra.html`
- Extends base.html for consistent navigation
- Displays Bokeh plot with embedded JavaScript
- Includes spectrum metadata table
- Shows loading indicator during data retrieval

### Visualization Layer
- **New File**: `src/visualizations/spectra.py`
- Creates Bokeh plot with multiple spectrum lines
- Formats legend with observation metadata
- Handles error cases (no spectra, all failed to load)

### Configuration Layer
- **Modify**: `src/config.py` to add `SPECTRA_URL_COLUMN` environment variable
- Follows existing pattern for configurable columns
- Provides default value compatible with spec requirements

## Dependencies

**Dependencies already available**:
- `bokeh ≥3.0`: Interactive plot generation (already in use)
- `astrodbkit ≥2.4`: Database access and spectrum format handling (already in use)
- `pandas`: Data manipulation (already in use)

**Note**: No need for separate specutils installation - astrodbkit returns spectra already formatted

## Performance Considerations

- **Spectrum Loading**: Individual spectrum files typically <1MB, load in <1 second each
- **Network Requests**: Parallel fetching of spectrum URLs recommended
- **Plot Generation**: Bokeh plots with 10-15 spectra render efficiently (<1 second)
- **Page Load Time**: Total page load within 10 seconds for sources with up to 15 spectra
- **Optimization**: Display loading indicator during spectrum retrieval and processing
- **Timeout**: Network requests timeout after 10 seconds to prevent indefinite hanging

## Testing Strategy

**Unit Tests**:
- Spectrum URL configuration reading
- Spectrum metadata extraction from DataFrame
- Legend formatting with various metadata combinations
- Missing metadata handling ("-" display)

**Integration Tests**:
- Full spectrum loading from URL to plot
- Multiple spectrum overlay in single plot
- Error handling for invalid spectrum URLs
- Graceful degradation when no valid spectra load

**Manual Testing**:
- UI display of plot with legend
- Metadata table rendering and link functionality
- Navigation from inventory to spectra page
- Loading indicator visibility and timing
- Interactive plot features (zoom, pan, reset)

