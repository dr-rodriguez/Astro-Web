# Research: Cone Search Implementation

**Feature**: Cone Search Form  
**Date**: 2024-12-19  
**Phase**: 0 - Research & Technical Decisions

## Technology Decisions

### Astrodbkit query_region for Spatial Searches

**Decision**: Use Astrodbkit's query_region method for cone search functionality  
**Rationale**:
- Maintains constitution compliance (Principle II: Astrodbkit Database Abstraction)
- Provides efficient spatial search over astronomical databases
- Properly handles angular distance calculations and coordinate wraparound
- Returns results as pandas DataFrame for consistency with existing search_object results
- Specifically designed for astronomical coordinate systems and sky regions

**API Usage**: `db.query_region(ra, dec, radius_deg, coord_frame='icrs')` where ra and dec are in decimal degrees and radius_deg is in degrees.

**Parameters**:
- `ra`: Right Ascension in decimal degrees (0-360)
- `dec`: Declination in decimal degrees (-90 to +90)
- `radius_deg`: Search radius in degrees (will convert from user-selected units)
- `coord_frame`: Optional, defaults to 'icrs' which is appropriate for modern astronomical coordinates

**Alternatives considered**:
- Direct SQL with spherical geometry: Violates constitution and increases complexity
- Custom spatial search implementation: Unnecessary complexity, astrodbkit provides robust spatial queries

### Coordinate Format Parsing Strategy

**Decision**: Use astropy.coordinates for all coordinate conversions  
**Rationale**:
- Standard astronomy library for coordinate handling
- Built-in support for both sexagesimal and decimal degree formats
- Handles RA (hours/minutes/seconds) and Dec (degrees/arcminutes/arcseconds) parsing
- Robust validation and error handling
- Provides conversion utilities for all needed formats

**API Usage**:
```python
from astropy.coordinates import SkyCoord, Angle
# Parse sexagesimal RA: "13h57m12.37s"
# Parse sexagesimal Dec: "+14d28m39.8"
# Parse decimal: "209.30", "14.48"
```

**Detection Strategy**: Try sexagesimal parsing first (spec requirement), fall back to decimal degrees. Astropy automatically handles format detection based on separators (h/m/s, d/m/s, or decimal).

**Alternatives considered**:
- Regex parsing: More error-prone and complex
- Manual parsing functions: Reimplements existing astropy functionality
- Multiple parsing libraries: Adds unnecessary dependencies

### Radius Unit Conversion

**Decision**: Convert all radius units to degrees before passing to query_region  
**Rationale**:
- query_region requires radius in degrees
- Standard astronomy convention for angular distances
- Simplifies database query interface
- Allows validation of maximum radius (10 degrees) regardless of user-selected unit

**Conversion factors**:
- arcseconds: divide by 3600
- arcminutes: divide by 60
- degrees: no conversion needed

**Validation**: All radii must be ≤ 10 degrees after conversion, per spec FR-023.

### Search Form Layout

**Decision**: Add cone search as separate section below text search on same page  
**Rationale**:
- Maintains existing page layout and user expectations
- Both search types remain accessible on one page
- Reuses existing search_results.html template for consistency
- Aligns with spec requirement FR-019 and FR-020

**Form Fields**:
- `ra`: Text input for Right Ascension (decimal degrees or sexagesimal)
- `dec`: Text input for Declination (decimal degrees or sexagesimal)
- `radius`: Number input for search radius
- `radius_unit`: Dropdown with options: degrees, arcminutes, arcseconds

### Results Display Integration

**Decision**: Reuse existing search_results.html template and DataTable implementation  
**Rationale**:
- Maintains consistency with text search results
- No new JavaScript dependencies or template code needed
- Provides same pagination, sorting, and browsing functionality
- Clickable source names already implemented

**Modification Required**: Add CSS styling for cone search form section to maintain visual separation from text search.

### Error Handling

**Decision**: Implement comprehensive validation with clear user-facing error messages  
**Rationale**:
- Prevents invalid database queries
- Improves user experience with immediate feedback
- Catches coordinate format errors before database query
- Validates spatial constraints (RA: 0-360°, Dec: -90 to +90°, radius: >0 to ≤10°)

**Validation Points**:
1. Required fields presence (RA, Dec, radius)
2. Coordinate range validity
3. Radius range and unit conversion
4. Sexagesimal format parsing errors
5. Database query errors (no objects found, etc.)

### Result Capping Strategy

**Decision**: Implement 10,000 object cap with warning message in template  
**Rationale**:
- Prevents UI performance issues with very large result sets
- Provides clear user feedback about result truncation
- Allows users to refine search for targeted results
- Maintains reasonable execution times per spec SC-002

**Implementation**: Apply `.head(10000)` to pandas DataFrame before conversion to dict list, check if original length > 10000 and pass warning flag to template.

## Integration with Existing Infrastructure

### Database Layer
- **New Function**: `cone_search(ra, dec, radius_deg)` in `src/database/query.py`
- Returns pandas DataFrame with same structure as `search_objects()`
- Uses `db.query_region()` method from astrodbkit

### Route Layer
- **New Function**: `cone_search_results()` in `src/routes/web.py`
- Handles form submission, validation, and result rendering
- Follows same pattern as existing `search_results()` function

### Template Layer
- **Modify**: `src/templates/search.html` to add cone search form section
- **Reuse**: `src/templates/search_results.html` with minimal modifications
- **Modify**: `src/static/style.css` to add form styling

## Dependencies

**No new dependencies required**:
- `astropy` already available in astronomy Python ecosystem
- `astropy.coordinates.SkyCoord` for coordinate parsing
- `astropy.coordinates.Angle` for sexagesimal conversion

## Performance Considerations

- Expect sub-second queries for typical searches (radius ≤ 1 degree)
- Astrodbkit's query_region optimized for spatial queries
- Result capping limits memory usage and UI rendering time
- Coordinate parsing overhead minimal compared to database query time

