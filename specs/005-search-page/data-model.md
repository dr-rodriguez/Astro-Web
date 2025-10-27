# Data Model: Search Page

**Feature**: Search Page  
**Date**: 2025-01-27  
**Phase**: 1 - Design

## Entities

### Search Query

**Purpose**: Represents user input for astronomical object search  
**Fields**:
- `query_text` (string, required): The search term entered by the user
- `timestamp` (datetime, optional): When the search was performed
- `user_session` (string, optional): Session identifier for tracking

**Validation Rules**:
- `query_text` must not be empty (validated client-side and server-side)
- `query_text` length should be reasonable (< 1000 characters)
- No special sanitization required (passed directly to astrodbkit)

**State Transitions**: None (stateless entity)

### Search Results

**Purpose**: Collection of astronomical objects returned by astrodbkit search_object function  
**Fields**:
- `results` (list of AstronomicalObject): Array of matching objects
- `total_count` (integer): Total number of matching objects found
- `query_text` (string): Original search query for display
- `search_time` (datetime): When the search was performed
- `execution_time` (float): Time taken to execute search in seconds

**Validation Rules**:
- `results` can be empty (no matches found)
- `total_count` must match length of `results` array
- `execution_time` must be positive

**State Transitions**: None (read-only result set)

### Astronomical Object (from astrodbkit)

**Purpose**: Individual source returned by search_object function  
**Fields**:
- `source` (string): Primary identifier/name of the astronomical object (hyperlinked column)
- `ra` (float): Right Ascension coordinate in degrees
- `dec` (float): Declination coordinate in degrees  
- `epoch` (float): Decimal year for coordinates (e.g., 2015.5)
- `equinox` (string): Equinox reference frame year (e.g., J2000)
- `shortname` (string): Short name for the source (marked for deletion in schema)
- `reference` (string): Discovery reference for the source
- `other_references` (string): Additional references, comma-separated
- `comments` (string): Free form comments about the object

**Validation Rules**:
- `source` is required for display and linking
- `ra` must be between 0 and 360 degrees
- `dec` must be between -90 and 90 degrees
- `epoch` can be null if using ICRS coordinates
- `equinox`, `shortname`, `reference`, `other_references`, and `comments` can be empty/null

**Relationships**:
- Links to individual source inventory pages via `source` field
- Part of Search Results collection

## Data Flow

### Search Process Flow

1. **User Input**: Search query submitted via form
2. **Validation**: Client-side validation for empty queries
3. **API Call**: FastAPI endpoint receives search request
4. **Database Query**: astrodbkit search_object function called
5. **Result Processing**: Results formatted for display
6. **Template Rendering**: Jinja2 template renders results page
7. **Client Display**: JavaScript DataTable processes results for pagination

### Error Handling Flow

1. **Empty Query**: Client-side validation shows "Please enter a search term"
2. **Astrodbkit Error**: Server catches exception, shows "An error occurred during search"
3. **No Results**: Empty results array displayed with appropriate message

## Database Schema Integration

The search functionality integrates with the existing SQLite database through astrodbkit's search_object function. No new database tables are required as the search operates on existing astronomical object data.

### Existing Tables Used
- Sources table (via astrodbkit search_object)
- Any related tables that astrodbkit searches across

### No Schema Changes Required
- Search functionality uses existing data structures
- No new tables, indexes, or constraints needed
- Leverages astrodbkit's built-in search capabilities

## API Data Contracts

### Request Format
```json
{
  "query": "string",
  "session_id": "string (optional)"
}
```

### Response Format
```json
{
  "results": [
    {
      "source": "string",
      "ra": "float",
      "dec": "float",
      "epoch": "float",
      "equinox": "string",
      "shortname": "string",
      "reference": "string",
      "other_references": "string",
      "comments": "string"
    }
  ],
  "total_count": "integer",
  "query_text": "string",
  "search_time": "datetime",
  "execution_time": "float"
}
```

### Error Response Format
```json
{
  "error": "string",
  "message": "string",
  "query_text": "string"
}
```
