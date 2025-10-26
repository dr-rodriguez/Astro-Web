# Quick Start: Individual Source Inventory Page

**Feature**: Individual Source Inventory Page  
**Date**: 2025-01-27  
**Status**: Phase 1 Design Complete

## Overview

This feature adds an inventory page that displays all data for a single astronomical source across multiple related tables. Users access the page via a URL containing the URL-encoded source name.

## Key Concepts

### Astrodbkit inventory() Method
The inventory method retrieves all related data for a source in one call:
```python
from astrodbkit.astrodb import Database
db = Database("sqlite:///SIMPLE.sqlite")
inventory = db.inventory("2MASS J12345678+0123456")
# Returns: {'Sources': DataFrame, 'Photometry': DataFrame, 'Spectra': DataFrame, ...}
```

### URL Encoding
Source names must be URL-encoded for routing:
- Original: "2MASS J12345678+0123456"  
- Encoded: "2MASS%20J12345678%2B0123456"
- URL: `/source/2MASS%20J12345678%2B0123456`

FastAPI automatically decodes path parameters.

## Implementation Steps

### 1. Add Database Query Function

**File**: `src/database/sources.py`

```python
def get_source_inventory(source_name):
    """
    Retrieve all data for a specific source using inventory method.
    
    Args:
        source_name (str): Source identifier
        
    Returns:
        dict: Dictionary of table names to lists of dictionaries, or None on error
    """
    try:
        from astrodbkit.astrodb import Database
        from urllib.parse import unquote
        
        # Decode URL-encoded source name
        decoded_name = unquote(source_name)
        
        # Connect to database
        db = Database("sqlite:///SIMPLE.sqlite")
        
        # Get inventory (returns dict of table name -> list of dicts)
        inventory = db.inventory(decoded_name)
        
        # Filter out empty tables
        result = {}
        for table_name, table_data in inventory.items():
            if table_data and len(table_data) > 0:
                result[table_name] = table_data
        
        return result if result else None
    except Exception:
        return None
```

### 2. Add Route Handler

**File**: `src/routes/web.py`

```python
async def inventory(request: Request, source_name: str):
    """Render the source inventory page."""
    from src.database.sources import get_source_inventory
    from urllib.parse import unquote
    
    # Get inventory data
    inventory_data = get_source_inventory(source_name)
    
    # Handle errors
    has_error = inventory_data is None
    error_message = (
        "Source not found or database temporarily unavailable." 
        if has_error else None
    )
    
    # Get decoded source name for display
    decoded_source_name = unquote(source_name)
    
    # Create navigation context
    nav_context = create_navigation_context(current_page=f"/source/{source_name}")
    
    return templates.TemplateResponse(
        "inventory.html",
        {
            "request": request,
            "source_name": decoded_source_name,
            "inventory_data": inventory_data if not has_error else {},
            "has_error": has_error,
            "error_message": error_message,
            **nav_context,
        },
    )
```

### 3. Register Route in Main App

**File**: `src/main.py`

```python
from fastapi import FastAPI
from src.routes import web

app = FastAPI()

# ... existing routes ...

# Add inventory route
@app.get("/source/{source_name}")
async def inventory_page(request: Request, source_name: str):
    return await web.inventory(request, source_name)
```

### 4. Create Inventory Template

**File**: `src/templates/inventory.html`

```html
{% extends "base.html" %}

{% block content %}
<div class="inventory-container">
    <h1>Source Inventory: {{ source_name }}</h1>
    
    {% if has_error %}
    <div class="error-message">
        <p>{{ error_message }}</p>
        <a href="/browse">Return to Browse</a>
    </div>
    {% else %}
        {% for table_name, table_data in inventory_data.items() %}
        {% if table_data and table_data|length > 0 %}
        <div class="inventory-table-section">
            <h2>{{ table_name }}</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        {% for column in table_data[0].keys() %}
                        <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in table_data %}
                    <tr>
                        {% for value in row.values() %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        {% endfor %}
    {% endif %}
</div>
{% endblock %}
```

### 5. Add Table Styles to CSS

**File**: `src/static/style.css`

```css
/* Inventory Page Styles */
.inventory-container {
    padding: 2rem;
}

.inventory-container h1 {
    margin-bottom: 2rem;
    font-size: 1.8rem;
}

.inventory-table-section {
    margin-bottom: 3rem;
}

.inventory-table-section h2 {
    margin-bottom: 1rem;
    font-size: 1.4rem;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}

.data-table th,
.data-table td {
    padding: 0.5rem;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.data-table th {
    background-color: #f5f5f5;
    font-weight: 600;
}

.data-table tr:hover {
    background-color: #f9f9f9;
}

.error-message {
    padding: 2rem;
    background-color: #fee;
    border: 1px solid #fcc;
    border-radius: 4px;
}
```

### 6. Add Link to Browse Page (Optional)

**File**: `src/templates/browse.html`

Update to make source identifiers clickable:

```html
<!-- In the table rendering section -->
<td>
    <a href="/source/{{ urlquote(row.source) }}">{{ row.source }}</a>
</td>
```

Add `urlquote` filter import in base.html or create custom filter.

## Testing the Implementation

### 1. Start Development Server
```bash
uvicorn src.main:app --reload
```

### 2. Navigate to Inventory Page
Open browser to: `http://localhost:8000/source/{source_name}`

Replace `{source_name}` with a URL-encoded source name from your database.

### 3. Verify Display
- Source name displayed at top
- Multiple data tables shown (Sources, Photometry, etc.)
- Navigation bar visible
- Only tables with data are displayed
- Tables without data are hidden

### 4. Test Error Cases
- Invalid source name → "Source not found" message
- Network interruption → Database error message

## Key Implementation Details

### URL Encoding/Decoding
- FastAPI automatically decodes path parameters
- Use `urllib.parse.quote()` to encode in Python
- Use `urllib.parse.unquote()` to decode
- Template filter: `{{ source_name|urlencode }}`

### Data Display
- All data rows are displayed with native browser scrolling
- No artificial row limits applied
- Inventory method returns data as lists of dictionaries ready for template rendering

### Error Handling
- Database exceptions caught, return `None`
- Route handler checks `None`, displays error message
- HTTP 404 for not found, HTTP 500 for database errors

### Template Logic
- Iterate over inventory dictionary with `{% for key, value in data.items() %}`
- Check for non-empty data: `{% if value and value|length > 0 %}`
- Generate tables dynamically from data structure

## Next Steps

After implementing these changes:
1. Test with various source names (including special characters)
2. Verify data tables display correctly
3. Check error handling for invalid sources
4. Ensure navigation bar works correctly
5. Test with sources that have data in different table combinations

