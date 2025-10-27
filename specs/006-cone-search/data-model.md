# Data Model: Cone Search

**Feature**: Cone Search Form  
**Date**: 2024-12-19  
**Phase**: 1 - Design

## Overview

Cone search extends the existing search functionality with spatial/coordinate-based queries. The feature introduces new form inputs and query parameters but leverages existing database tables and result structures.

## Entities

### Cone Search Query (Input)

**Description**: User input representing a spatial search region in the sky

**Properties**:
- `ra` (str): Right Ascension in decimal degrees or sexagesimal format
  - Valid formats:
    - Decimal: "209.30", "0.5"
    - Sexagesimal RA: "13h57m12s", "13h 57m 12.37s"
  - Validation: Must parse to 0-360 degrees
  - Required: Yes

- `dec` (str): Declination in decimal degrees or sexagesimal format
  - Valid formats:
    - Decimal: "14.48", "-45.2"
    - Sexagesimal Dec: "+14d28m39s", "-45d30m"
  - Validation: Must parse to -90 to +90 degrees
  - Required: Yes

- `radius` (str): Search radius value
  - Validation: Must be positive numeric value
  - Required: Yes

- `radius_unit` (str): Unit for the search radius
  - Valid values: "degrees", "arcminutes", "arcseconds"
  - Validation: Must be one of the three allowed values
  - Required: Yes

**Relationships**:
- Maps to database query via `query_region()` method
- Converts to Target Coordinates (internal representation)

**Constraints**:
- All four properties must be provided
- Radius after conversion to degrees must be ≤ 10 degrees
- Coordinates must parse successfully to decimal degrees

### Target Coordinates (Internal)

**Description**: Parsed and validated coordinate values for database query

**Properties**:
- `ra_decimal` (float): Right Ascension in decimal degrees
  - Range: 0.0 to 360.0
  - Validation: Automatically validated during parsing

- `dec_decimal` (float): Declination in decimal degrees
  - Range: -90.0 to +90.0
  - Validation: Automatically validated during parsing

- `radius_degrees` (float): Search radius in degrees
  - Range: > 0.0 to ≤ 10.0
  - Derived: Converted from user input and radius_unit
  - Validation: Must not exceed 10 degrees

**Transformation**:
- Converted from Cone Search Query using astropy.coordinates
- Used as input to astrodbkit query_region()

### Search Results (Output)

**Description**: Astronomical objects found within the specified spatial region

**Structure**: Reuses existing search results structure

**Properties**:
- Inherits from Sources table columns:
  - `source` (str): Primary identifier
  - `ra` (float): Right Ascension in decimal degrees
  - `dec` (float): Declination in decimal degrees
  - `epoch` (float): Epoch of coordinates
  - `equinox` (str): Equinox reference
  - `shortname` (str): Short name for display
  - `reference` (str): Primary reference
  - `other_references` (str): Additional references
  - `comments` (str): Notes and comments

**Relationships**:
- Each result links to individual source inventory page via source name
- Results are displayed in DataTable format (same as text search)

**Constraints**:
- Maximum 10,000 results per query
- All objects within specified radius from target coordinates
- Spatially sorted by default (no explicit ordering requirement)

### Cone Search Response (API Output)

**Description**: Complete search results including metadata

**Properties**:
- `results` (list[dict]): List of astronomical objects found
  - Each dict contains all Sources table fields
- `total_count` (int): Number of results returned
  - Limited to 10,000 maximum
- `execution_time` (float): Query execution time in seconds
- `ra_input` (str): Original RA input for display
- `dec_input` (str): Original Dec input for display
- `radius_value` (str): Original radius value for display
- `radius_unit` (str): Original radius unit for display
- `warning` (str, optional): Warning message if results truncated
  - Format: "Results limited to 10,000 objects. Refine search to see all results."

**Display Context**:
- Rendered in search_results.html template
- Results displayed in JavaScript DataTable
- Form inputs preserved in template context

## State Transitions

### Form Input → Validation → Query Execution → Results Display

1. **User Input**:
   - User enters RA, Dec, radius, selects unit
   - Submits cone search form

2. **Validation**:
   - Check all required fields present
   - Validate coordinate formats (try sexagesimal, fall back to decimal)
   - Validate coordinate ranges (RA: 0-360°, Dec: -90 to +90°)
   - Convert and validate radius (must be >0 and ≤10°)

3. **Query Execution**:
   - Parse coordinates to decimal degrees using astropy
   - Convert radius to degrees
   - Call astrodbkit query_region(ra_decimal, dec_decimal, radius_degrees)
   - Apply 10,000 result cap if needed

4. **Results Display**:
   - Render search_results.html with results
   - Display execution time and count
   - Show warning if results truncated
   - Preserve form input values for display

## Validation Rules

### Format Detection

1. **Try sexagesimal first** (as per spec clarification):
   - RA: Look for 'h', 'm', 's' or 'd', 'm', 's' separators
   - Dec: Look for 'd', '°', 'm', "'", 's', '"' separators
2. **Fall back to decimal** if sexagesimal parsing fails
3. **Return parsing error** if both methods fail

### Range Validation

- **RA**: 0 to 360 degrees (decimal) or 0h to 24h (sexagesimal)
- **Dec**: -90 to +90 degrees (decimal) or -90° to +90° (sexagesimal)
- **Radius**: > 0 and ≤ 10 degrees (after unit conversion)

### Unit Conversion

- **arcseconds**: radius_degrees = radius_input / 3600.0
- **arcminutes**: radius_degrees = radius_input / 60.0
- **degrees**: radius_degrees = radius_input

## Error Handling

### Validation Errors

**Missing Fields**:
- Error: "All fields (RA, Dec, radius) are required"
- Action: Display error on search.html form

**Invalid Coordinates**:
- Error: "Invalid RA format" or "Invalid Dec format"
- Action: Display error with format guidance

**Coordinate Out of Range**:
- Error: "RA must be between 0 and 360 degrees" or "Dec must be between -90 and +90 degrees"
- Action: Display error with range guidance

**Invalid Radius**:
- Error: "Radius must be a positive number"
- Action: Display error requiring positive value

**Radius Too Large**:
- Error: "Radius must not exceed 10 degrees"
- Action: Display error suggesting smaller radius

### Query Errors

**No Objects Found**:
- Response: Empty results list, total_count=0
- Message: "No objects found within the specified region"
- Action: Display message in search_results.html

**Database Error**:
- Exception: Catch astrodbkit query exceptions
- Error: "An error occurred during search: {error_message}"
- Action: Display error in search_results.html

## Database Schema

**No schema changes required**:
- Uses existing Sources table
- query_region() reads from existing ra/dec columns
- No new tables or columns needed

**Existing Source Columns Used**:
- ra: float - Right Ascension in degrees
- dec: float - Declination in degrees
- source: str - Primary identifier
- All other source fields displayed in results

## Performance Considerations

### Query Optimization

- Astrodbkit query_region() uses spatial indexing on ra/dec
- Results limited to 10,000 to prevent UI performance issues
- Coordinate parsing adds minimal overhead (<1ms)

### Result Processing

- pandas DataFrame to dict conversion for template
- DataTable pagination handles large result sets efficiently
- Source URL conversion applied to results

## Testing Strategy

### Unit Tests
- Coordinate parsing (sexagesimal and decimal)
- Radius unit conversion
- Validation logic
- Error message generation

### Integration Tests
- Full search flow from form to results
- Result count and execution time accuracy
- Result truncation at 10,000 limit
- Error handling for invalid inputs

### Manual Testing
- UI form layout and styling
- DataTable rendering and interaction
- Source link navigation
- Cross-browser compatibility

