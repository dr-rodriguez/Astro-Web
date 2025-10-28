# Quickstart: Spectra Display Implementation

**Feature**: Spectra Display Page  
**Date**: 2025-01-28  
**Phase**: 1 - Design

## Overview

This quickstart guide provides step-by-step instructions for implementing spectra display functionality. The implementation adds a new page accessible from source inventory that displays all spectra for a given source using an interactive Bokeh plot with a metadata table.

## Prerequisites

- Astro-Web application running on development server
- Astrodbkit ≥2.4 installed with database connection
- Bokeh ≥3.0 already present (used in existing visualizations)
- FastAPI ≥0.120.0 with Jinja2 templates

## Implementation Steps

### 1. Add Spectrum URL Column Configuration

**File**: `src/config.py`

Add new environment variable for configurable spectrum URL column name:

```python
# Spectrum URL column name (default: access_url)
SPECTRA_URL_COLUMN = os.getenv("ASTRO_WEB_SPECTRA_URL_COLUMN", "access_url")
```

### 2. Add Get Source Spectra Function

**File**: `src/database/sources.py`

Add new function to retrieve spectra for a source:

```python
from src.config import CONNECTION_STRING, SPECTRA_URL_COLUMN

def get_source_spectra(source_name):
    """
    Retrieve all spectra for a specific source.
    
    Args:
        source_name (str): Source identifier
        
    Returns:
        pandas.DataFrame: DataFrame containing spectrum records with columns:
            source, access_url (or configured column), observation_date,
            regime, telescope, instrument, and other metadata
    """
    try:
        db = Database(CONNECTION_STRING)
        
        # Query spectra for this source
        spectra_df = db.query(db.Spectra).filter(
            db.Spectra.source == source_name
        ).spectra(fmt='pandas')
        
        return spectra_df
    except Exception:
        return None
```

### 3. Create Spectrum Loading Function

**File**: `src/visualizations/spectra.py` (NEW FILE)

Create new module for spectrum loading and plot generation:

```python
"""
Spectrum visualization functions using Bokeh.

Note: astrodbkit returns spectra already formatted with wavelength and flux arrays 
accessible directly - no additional format conversion needed.
"""

import os
from typing import List, Dict, Tuple, Optional

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Category10_10
import pandas as pd

from src.config import SPECTRA_URL_COLUMN


def generate_spectra_plot(source_name: str, spectra_df: pd.DataFrame) -> Tuple[str, str, List[Dict]]:
    """
    Generate Bokeh plot and metadata for spectra visualization.
    
    Args:
        source_name (str): Source identifier
        spectra_df (pandas.DataFrame): DataFrame containing spectrum records
        
    Returns:
        tuple: (plot_script, plot_div, spectra_metadata)
    """
    # Create Bokeh figure
    p = figure(
        title=f"Spectra for {source_name}",
        x_axis_label="Wavelength (nm)",
        y_axis_label="Flux",
        width=900,
        height=600,
        tools="pan,box_zoom,wheel_zoom,reset",
        toolbar_location="above"
    )
    
    # Load spectra and plot
    spectra_metadata = []
    loaded_count = 0
    
    for idx, row in spectra_df.iterrows():
        # astrodbkit returns spectrum data already formatted
        # Access wavelength and flux arrays directly
        spectrum_data = row.get(SPECTRA_URL_COLUMN) # Pre-formatted by astrodbkit
        
        # Skip if no data
        if spectrum_data is None or isinstance(spectrum_data, str):
            continue
        
        # Extract metadata for legend and table
        observation_date = str(row.get('observation_date', '')).strip() if pd.notna(row.get('observation_date')) else "-"
        regime = str(row.get('regime', '')).strip() if pd.notna(row.get('regime')) else "-"
        telescope = str(row.get('telescope', '')).strip() if pd.notna(row.get('telescope')) else "-"
        instrument = str(row.get('instrument', '')).strip() if pd.notna(row.get('instrument')) else "-"
        
        # Format legend label
        legend_label = f"{observation_date} | {regime} | {telescope}/{instrument}"
        
        # Plot spectrum
        color = Category10_10[loaded_count % len(Category10_10)]
        p.line(
            spectrum_data['wavelength'],
            spectrum_data['flux'],
            legend_label=legend_label,
            color=color,
            line_width=2,
            alpha=0.7
        )
        
        # Store metadata for table
        spectra_metadata.append({
            'observation_date': observation_date if observation_date != 'nan' else '-',
            'regime': regime if regime != 'nan' else '-',
            'telescope': telescope if telescope != 'nan' else '-',
            'instrument': instrument if instrument != 'nan' else '-',
            'access_url': f'<a href="{spectrum_url}" target="_blank">{spectrum_url}</a>'
        })
        
        loaded_count += 1
    
    # Configure legend
    p.legend.click_policy = "hide"  # Click to hide/show spectra
    p.legend.location = "top_left"
    
    # Generate HTML components
    script, div = components(p)
    
    return script, div, spectra_metadata
```

### 4. Create Spectra Template

**File**: `src/templates/spectra.html` (NEW FILE)

Create template for spectra visualization page:

```html
{% extends "base.html" %}

{% block content %}
<div class="spectra-container">
    <h1>Spectra for {{ source_name }}{% if spectra_count > 0 %} ({{ spectra_count }}){% endif %}</h1>
    
    <div class="navigation-link">
        <a href="/source/{{ source_name }}">← Back to Inventory</a>
    </div>
    
    {% if has_spectra %}
    <div class="spectra-plot-section">
        {{ plot_div|safe }}
        {{ plot_script|safe }}
    </div>
    
    <div class="spectra-metadata-section">
        <h2>Spectrum Details</h2>
        <table class="spectra-metadata-table">
            <thead>
                <tr>
                    <th>Observation Date</th>
                    <th>Regime</th>
                    <th>Telescope</th>
                    <th>Instrument</th>
                    <th>Access URL</th>
                </tr>
            </thead>
            <tbody>
                {% for spectrum in spectra_metadata %}
                <tr>
                    <td>{{ spectrum.observation_date }}</td>
                    <td>{{ spectrum.regime }}</td>
                    <td>{{ spectrum.telescope }}</td>
                    <td>{{ spectrum.instrument }}</td>
                    <td>{{ spectrum.access_url|safe }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="no-spectra-message">
        <p>No spectra available for display for this source.</p>
    </div>
    {% endif %}
</div>
{% endblock %}
```

### 5. Add Spectra Display Route

**File**: `src/routes/web.py`

Add import and new route function:

```python
from src.visualizations.spectra import generate_spectra_plot
from src.database.sources import get_source_spectra

async def spectra_display(request: Request, source_name: str):
    """Render the spectra visualization page for a source."""
    
    # Get decoded source name for display
    decoded_source_name = unquote(source_name)
    
    # Get spectra data
    spectra_df = get_source_spectra(source_name)
    
    # Check if source has spectra
    if spectra_df is None or spectra_df.empty:
        has_error = True
        error_message = f"No spectra found for source: {decoded_source_name}"
        nav_context = create_navigation_context(current_page=f"/source/{source_name}")
        
        return templates.TemplateResponse(
            "spectra.html",
            {
                "request": request,
                "source_name": decoded_source_name,
                "has_spectra": False,
                "spectra_count": 0,
                "has_error": True,
                "error_message": error_message,
                **nav_context
            },
            status_code=404 if spectra_df is None else 200
        )
    
    # Generate plot and metadata
    plot_script, plot_div, spectra_metadata = generate_spectra_plot(
        decoded_source_name,
        spectra_df
    )
    
    has_spectra = len(spectra_metadata) > 0
    spectra_count = len(spectra_metadata)
    
    # Create navigation context
    nav_context = create_navigation_context(current_page=f"/source/{source_name}")
    
    return templates.TemplateResponse(
        "spectra.html",
        {
            "request": request,
            "source_name": decoded_source_name,
            "plot_script": plot_script,
            "plot_div": plot_div,
            "spectra_metadata": spectra_metadata,
            "spectra_count": spectra_count,
            "has_spectra": has_spectra,
            "has_error": False,
            **nav_context
        }
    )
```

### 6. Update Inventory Template to Add Spectra Link

**File**: `src/templates/inventory.html`

Add conditional spectra link in inventory template:

```html
{% extends "base.html" %}

{% block content %}
<div class="inventory-container">
    <h1>Source Inventory: {{ source_name }}</h1>
    
    <!-- Add spectra link if spectra exist -->
    {% if inventory_data.Spectra and inventory_data.Spectra|length > 0 %}
    <div class="spectra-link-section">
        <a href="/source/{{ source_name }}/spectra" class="spectra-link">
            View Spectra ({{ inventory_data.Spectra|length }})
        </a>
    </div>
    {% endif %}
    
    {% if has_error %}
    <!-- existing error handling -->
    {% else %}
        {% for table_name, table_data in inventory_data.items() %}
        <!-- existing table rendering -->
        {% endfor %}
    {% endif %}
</div>
{% endblock %}
```

### 7. Add Spectra Route to Main Application

**File**: `src/main.py`

Add spectra route to FastAPI application:

```python
from src.routes.web import (
    homepage, browse, plot, inventory,
    search_form, search_results, search_api,
    cone_search_results, cone_search_api,
    spectra_display,  # Add this
    not_found
)

# ... existing routes ...

# Add spectra route
app.add_api_route(
    "/source/{source_name}/spectra",
    spectra_display,
    methods=["GET"],
    name="spectra_display"
)
```

### 8. Add CSS Styling

**File**: `src/static/style.css`

Add styles for spectra page:

```css
/* Spectra page styles */
.spectra-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.navigation-link {
    margin-bottom: 2rem;
}

.navigation-link a {
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
}

.navigation-link a:hover {
    text-decoration: underline;
}

.spectra-plot-section {
    margin: 2rem 0;
}

.spectra-metadata-section {
    margin-top: 2rem;
}

.spectra-metadata-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.spectra-metadata-table th,
.spectra-metadata-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.spectra-metadata-table th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.no-spectra-message {
    padding: 2rem;
    text-align: center;
    background-color: #f8f9fa;
    border-radius: 4px;
}

.spectra-link-section {
    margin: 1rem 0;
}

.spectra-link {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}

.spectra-link:hover {
    background-color: #0056b3;
}
```

## Testing

### Manual Testing Steps

1. **Start development server**:
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Test spectrum retrieval**:
   - Navigate to a source inventory page with spectra
   - Verify "View Spectra" link appears
   - Click link to view spectra page

3. **Test plot display**:
   - Verify Bokeh plot displays with all spectra
   - Check legend labels format correctly
   - Verify interactive features (zoom, pan, reset)
   - Test legend click-to-hide functionality

4. **Test metadata table**:
   - Verify table displays all spectrum metadata
   - Check missing values display as "-"
   - Test clickable URL links

5. **Test error handling**:
   - Navigate to source with no spectra
   - Verify appropriate message displayed
   - Test with source that has invalid spectrum URLs (should skip gracefully)

6. **Test navigation**:
   - Verify "Back to Inventory" link works
   - Check browser back button functionality
   - Test inventory link conditional display

## Deployment Notes

- Test with production database for spectrum file access
- Verify spectrum URLs are accessible from production server
- Monitor spectrum loading performance for large files
- Consider timeout adjustments based on network conditions

## Troubleshooting

### Common Issues

1. **Spectrum files not loading**: Check URL accessibility and format support
2. **Plot not displaying**: Verify Bokeh JavaScript libraries loading
3. **Missing spectra**: Check database query filtering and column names
4. **Legend formatting issues**: Verify metadata extraction and formatting logic
5. **Performance slow**: Consider parallel spectrum loading with asyncio

### Performance Optimization

- Use parallel requests for spectrum file fetching (asyncio or threading)
- Cache spectrum files locally if frequently accessed
- Consider lazy loading for sources with many spectra
- Monitor network timeouts based on spectrum file sizes

