# Quickstart: Cone Search Implementation

**Feature**: Cone Search Form  
**Date**: 2024-12-19  
**Phase**: 1 - Design

## Overview

This quickstart guide provides step-by-step instructions for implementing cone search functionality on the existing Search page. The implementation adds spatial coordinate-based search using Astrodbkit's query_region method, allowing users to search for astronomical objects within a specified region of the sky.

## Prerequisites

- Astro-Web application running on development server
- Astrodbkit ≥2.4 installed with query_region support
- astropy installed for coordinate parsing (included with astrodbkit)
- FastAPI ≥0.120.0 with Jinja2 templates
- JavaScript DataTable library (already present from search page)

## Implementation Steps

### 1. Add Cone Search Form to Search Template

**File**: `src/templates/search.html`

Add cone search section below existing text search form:

```html
{% extends "base.html" %}

{% block content %}
<h1>Search Astronomical Objects</h1>

<!-- Existing text search form -->
<form method="post" action="/search/results" id="textSearchForm">
  <div class="form-group">
    <label for="query">Search by Name:</label>
    <input type="text" id="query" name="query" placeholder="Enter astronomical object name..." required>
  </div>
  <button type="submit">Search</button>
</form>

<!-- New cone search form -->
<h2 style="margin-top: 2rem;">Cone Search</h2>
<p>Search for objects within a specified region of the sky by coordinates.</p>

<form method="post" action="/search/cone-results" id="coneSearchForm">
  <div class="form-group">
    <label for="ra">Right Ascension (RA):</label>
    <input type="text" id="ra" name="ra" placeholder="e.g., 209.30 or 13h57m12s" required>
    <small>Enter as decimal degrees (209.30) or sexagesimal (13h57m12s)</small>
  </div>
  
  <div class="form-group">
    <label for="dec">Declination (Dec):</label>
    <input type="text" id="dec" name="dec" placeholder="e.g., 14.48 or +14d28m39s" required>
    <small>Enter as decimal degrees (14.48) or sexagesimal (+14d28m39s)</small>
  </div>
  
  <div class="form-group">
    <label for="radius">Search Radius:</label>
    <div style="display: flex; gap: 0.5rem; align-items: center;">
      <input type="number" id="radius" name="radius" step="0.001" min="0" required style="max-width: 150px;">
      <select id="radius_unit" name="radius_unit" required>
        <option value="arcseconds">Arcseconds</option>
        <option value="arcminutes" selected>Arcminutes</option>
        <option value="degrees">Degrees</option>
      </select>
    </div>
  </div>
  
  <button type="submit">Search</button>
</form>

<script>
document.getElementById('textSearchForm').addEventListener('submit', function(e) {
  const query = document.getElementById('query').value.trim();
  if (!query) {
    e.preventDefault();
    alert('Please enter a search term');
  }
});

document.getElementById('coneSearchForm').addEventListener('submit', function(e) {
  const ra = document.getElementById('ra').value.trim();
  const dec = document.getElementById('dec').value.trim();
  const radius = document.getElementById('radius').value.trim();
  
  if (!ra || !dec || !radius) {
    e.preventDefault();
    alert('Please fill in all required fields');
  }
});
</script>
{% endblock %}
```

### 2. Add Cone Search Query Function

**File**: `src/database/query.py`

Add new function for cone search queries:

```python
"""
Database query helper functions.

This module contains helper functions for executing database queries
with timing and error handling.
"""

import time
from astrodbkit.astrodb import Database

from src.database import CONNECTION_STRING


def search_objects(query: str):
    """
    Search for objects in the database using astrodbkit.
    
    Args:
        query (str): The search query string
        
    Returns:
        tuple: (results, execution_time) where results is a DataFrame
               and execution_time is the time taken in seconds
    """
    start_time = time.time()
    db = Database(CONNECTION_STRING)
    results = db.search_object(query.strip(), resolve_simbad=True, format="pandas")
    execution_time = time.time() - start_time
    
    return results, execution_time


def cone_search(ra, dec, radius_deg):
    """
    Perform a cone search for objects within a specified region of the sky.
    
    Args:
        ra (float): Right Ascension in decimal degrees (0-360)
        dec (float): Declination in decimal degrees (-90 to +90)
        radius_deg (float): Search radius in degrees
        
    Returns:
        tuple: (results, execution_time) where results is a DataFrame
               and execution_time is the time taken in seconds
    """
    start_time = time.time()
    db = Database(CONNECTION_STRING)
    results = db.query_region(ra, dec, radius_deg, coord_frame='icrs')
    execution_time = time.time() - start_time
    
    # Apply 10,000 result cap if needed
    if len(results) > 10000:
        results = results.head(10000)
    
    return results, execution_time
```

### 3. Add Coordinate Parsing Utility

**File**: `src/database/query.py`

Add coordinate parsing functions:

```python
from astropy.coordinates import SkyCoord, Angle
import re

def parse_coordinate_to_decimal(coord_str, is_ra=False):
    """
    Parse coordinate string (sexagesimal or decimal) to decimal degrees.
    
    Args:
        coord_str (str): Coordinate string in sexagesimal or decimal format
        is_ra (bool): Whether this is a Right Ascension coordinate
        
    Returns:
        float: Coordinate in decimal degrees
        
    Raises:
        ValueError: If coordinate cannot be parsed or is out of range
    """
    coord_str = coord_str.strip()
    
    try:
        # Try to parse as sexagesimal first
        if is_ra:
            # RA format: "13h57m12.37s" or "13 57 12.37"
            if any(char in coord_str.lower() for char in ['h', 'm', 's', 'd']):
                # Parse as sexagesimal
                skycoord = SkyCoord(coord_str, frame='icrs', unit='deg')
                return skycoord.ra.deg
        else:
            # Dec format: "+14d28m39.8" or "+14 28 39.8"
            if any(char in coord_str for char in ['d', '°', 'm', "'", 's', '"']):
                # Parse as sexagesimal
                skycoord = SkyCoord(coord_str, frame='icrs', unit='deg')
                return skycoord.dec.deg
        
        # Fall back to decimal degrees
        coord_value = float(coord_str)
        
        if is_ra:
            if not (0 <= coord_value <= 360):
                raise ValueError(f"RA must be between 0 and 360 degrees, got {coord_value}")
        else:
            if not (-90 <= coord_value <= 90):
                raise ValueError(f"Dec must be between -90 and +90 degrees, got {coord_value}")
        
        return coord_value
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid coordinate format: {coord_str}") from e


def convert_radius_to_degrees(radius_value, radius_unit):
    """
    Convert radius from user-selected unit to degrees.
    
    Args:
        radius_value (float): Radius value as number
        radius_unit (str): Unit of radius ("degrees", "arcminutes", "arcseconds")
        
    Returns:
        float: Radius in degrees
        
    Raises:
        ValueError: If radius_unit is invalid or radius exceeds 10 degrees
    """
    if radius_unit == "degrees":
        radius_deg = float(radius_value)
    elif radius_unit == "arcminutes":
        radius_deg = float(radius_value) / 60.0
    elif radius_unit == "arcseconds":
        radius_deg = float(radius_value) / 3600.0
    else:
        raise ValueError(f"Invalid radius unit: {radius_unit}")
    
    if radius_value <= 0:
        raise ValueError("Radius must be a positive number")
    
    if radius_deg > 10.0:
        raise ValueError("Radius must not exceed 10 degrees after unit conversion")
    
    return radius_deg
```

### 4. Add Cone Search Routes

**File**: `src/routes/web.py`

Add new route for cone search results:

```python
from astropy.coordinates import SkyCoord
from src.database.query import cone_search, parse_coordinate_to_decimal, convert_radius_to_degrees

async def cone_search_results(
    request: Request,
    ra: str = Form(...),
    dec: str = Form(...),
    radius: str = Form(...),
    radius_unit: str = Form(...)
):
    """Process cone search query and display results"""
    try:
        # Parse coordinates
        ra_decimal = parse_coordinate_to_decimal(ra, is_ra=True)
        dec_decimal = parse_coordinate_to_decimal(dec, is_ra=False)
        
        # Convert and validate radius
        radius_degrees = convert_radius_to_degrees(radius, radius_unit)
        
        # Execute cone search
        results, execution_time = cone_search(ra_decimal, dec_decimal, radius_degrees)
        
        # Check if results were truncated
        warning = None
        if len(results) >= 10000:
            warning = "Results limited to 10,000 objects. Refine search to see all results."
        
        # Format results for display
        formatted_results = results.to_dict('records')
        
        # Apply source URL conversion
        formatted_results = get_source_url(formatted_results)
        
        # Create navigation context
        nav_context = create_navigation_context(current_page="/search")
        
        return templates.TemplateResponse("search_results.html", {
            "request": request,
            "query_text": f"RA={ra}, Dec={dec}, Radius={radius} {radius_unit}",
            "results": formatted_results,
            "total_count": len(formatted_results),
            "execution_time": f"{execution_time:.3f}",
            "warning": warning,
            "ra_input": ra,
            "dec_input": dec,
            "radius_value": radius,
            "radius_unit": radius_unit,
            **nav_context
        })
        
    except ValueError as e:
        # Validation errors
        nav_context = create_navigation_context(current_page="/search")
        return templates.TemplateResponse("search.html", {
            "request": request,
            "error": str(e),
            **nav_context
        })
    except Exception as e:
        # Database errors
        nav_context = create_navigation_context(current_page="/search")
        return templates.TemplateResponse("search_results.html", {
            "request": request,
            "query_text": f"RA={ra}, Dec={dec}",
            "error": f"An error occurred during search: {e}",
            "results": [],
            "total_count": 0,
            "execution_time": "0.000",
            **nav_context
        })
```

### 5. Add Cone Search API Endpoint

**File**: `src/routes/web.py`

Add API endpoint for programmatic access:

```python
async def cone_search_api(
    ra: str = Form(...),
    dec: str = Form(...),
    radius: str = Form(...),
    radius_unit: str = Form(...)
):
    """API endpoint for programmatic cone search access"""
    try:
        # Parse and validate inputs
        ra_decimal = parse_coordinate_to_decimal(ra, is_ra=True)
        dec_decimal = parse_coordinate_to_decimal(dec, is_ra=False)
        radius_degrees = convert_radius_to_degrees(radius, radius_unit)
        
        # Execute search
        results, execution_time = cone_search(ra_decimal, dec_decimal, radius_degrees)
        
        # Check for truncation
        warning = None
        if len(results) >= 10000:
            warning = "Results limited to 10,000 objects. Refine search to see all results."
        
        # Format results
        formatted_results = results.to_dict('records')
        
        return {
            "results": formatted_results,
            "total_count": len(formatted_results),
            "ra_input": ra,
            "dec_input": dec,
            "radius_value": radius,
            "radius_unit": radius_unit,
            "search_time": datetime.now().isoformat(),
            "execution_time": execution_time,
            "warning": warning
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during search: {e}")
```

### 6. Update Routes in main.py

**File**: `src/main.py`

Add cone search routes to FastAPI application:

```python
from src.routes.web import (
    homepage, browse, plot, inventory,
    search_form, search_results, search_api,
    cone_search_results, cone_search_api,  # Add these
    not_found
)

# ... existing routes ...

# Add cone search routes
app.add_api_route("/search", search_form, methods=["GET"], name="search_form")
app.add_api_route("/search/results", search_results, methods=["POST"], name="search_results")
app.add_api_route("/api/search", search_api, methods=["POST"], name="search_api")
app.add_api_route("/api/search/cone", cone_search_api, methods=["POST"], name="cone_search_api")
```

### 7. Update Search Results Template

**File**: `src/templates/search_results.html`

Add support for cone search warning messages:

```html
{% extends "base.html" %}

{% block content %}
<h1>Search Results</h1>
<p>Query: {{ query_text }}</p>

{% if warning %}
<div class="warning-message">
  <p>{{ warning }}</p>
</div>
{% endif %}

{% if results %}
  <p>Found {{ total_count }} result(s) in {{ execution_time }} seconds</p>
  
  <table id="resultsTable" class="display">
    <!-- existing table structure -->
  </table>
{% else %}
  <p>No results found</p>
{% endif %}

<!-- existing DataTable scripts -->
{% endblock %}
```

### 8. Add CSS Styling for Cone Search Form

**File**: `src/static/style.css`

Add cone search form specific styles:

```css
/* Cone search form specific styles */
h2 {
  margin-top: 2rem;
  border-top: 2px solid #ddd;
  padding-top: 1rem;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.875rem;
}

.warning-message {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  color: #856404;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.error-message {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}
```

## Testing

### Manual Testing Steps

1. **Start development server**:
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Test coordinate parsing**:
   - Navigate to `http://localhost:8000/search`
   - Test decimal: RA=209.30, Dec=14.48, Radius=0.5 arcminutes
   - Test sexagesimal: RA=13h57m12s, Dec=+14d28m39s, Radius=0.5 arcminutes
   - Verify both return same results

3. **Test validation**:
   - Empty fields → validation error
   - Invalid coordinates → format error
   - RA > 360 → range error
   - Dec > 90 → range error
   - Radius > 10 degrees → max radius error

4. **Test result display**:
   - Perform valid search
   - Verify results in DataTable
   - Click source links
   - Check execution time display

5. **Test result capping**:
   - Search with very large radius (max 10 degrees)
   - Verify results limited to 10,000 with warning

6. **Test API endpoint**:
   ```bash
   curl -X POST "http://localhost:8000/api/search/cone" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "ra=209.30&dec=14.48&radius=0.5&radius_unit=arcminutes"
   ```

### Integration Tests

Create `tests/test_cone_search.py`:

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.query import parse_coordinate_to_decimal, convert_radius_to_degrees

client = TestClient(app)

def test_parse_decimal_coordinate():
    assert parse_coordinate_to_decimal("209.30", is_ra=True) == 209.30
    assert parse_coordinate_to_decimal("14.48", is_ra=False) == 14.48

def test_parse_sexagesimal_coordinate():
    ra = parse_coordinate_to_decimal("13h57m12s", is_ra=True)
    assert 209.0 < ra < 210.0  # Approximate
    
    dec = parse_coordinate_to_decimal("+14d28m39s", is_ra=False)
    assert 14.0 < dec < 15.0  # Approximate

def test_convert_radius():
    assert convert_radius_to_degrees(60, "arcminutes") == 1.0
    assert convert_radius_to_degrees(3600, "arcseconds") == 1.0
    assert convert_radius_to_degrees(5, "degrees") == 5.0

def test_cone_search_endpoint():
    response = client.post("/search/cone-results", data={
        "ra": "209.30",
        "dec": "14.48",
        "radius": "0.5",
        "radius_unit": "arcminutes"
    })
    assert response.status_code == 200
    assert "Search Results" in response.text

def test_cone_search_api():
    response = client.post("/api/search/cone", data={
        "ra": "209.30",
        "dec": "14.48",
        "radius": "0.5",
        "radius_unit": "arcminutes"
    })
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_count" in data
```

## Deployment Notes

- No database schema changes required
- Ensure astropy is available in production environment
- Test with production database for performance
- Consider adding coordinate format help text in UI
- Monitor search performance for large radius values

## Troubleshooting

### Common Issues

1. **"Invalid coordinate format"**: Check astropy parsing, verify input format
2. **Results not matching expected region**: Verify coordinate system (ICRS) and radius conversion
3. **Performance issues with large radius**: Consider radius limiting and database indexing
4. **Sexagesimal parsing fails**: Check for typos in separator characters (h, m, s, d, °, ', ")

### Performance Optimization

- Astrodbkit's query_region uses spatial indexing
- Results capped at 10,000 to prevent UI issues
- Consider radius limits based on database size
- Monitor coordinate parsing overhead

