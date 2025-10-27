# Quickstart: Search Page Implementation

**Feature**: Search Page  
**Date**: 2025-01-27  
**Phase**: 1 - Design

## Overview

This quickstart guide provides step-by-step instructions for implementing the Search Page feature in the Astro-Web application. The implementation follows the Astro-Web Constitution principles and integrates with existing navigation and source inventory functionality.

## Prerequisites

- Astro-Web application running on development server
- Astrodbkit ≥2.4 installed and configured
- FastAPI ≥0.120.0 with Jinja2 templates
- JavaScript DataTable library available

## Implementation Steps

### 1. Add Search Route to Navigation

**File**: `src/templates/base.html`

Add search link to existing navigation bar:

```html
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/browse">Browse</a></li>
    <li><a href="/search">Search</a></li>  <!-- Add this line -->
    <li><a href="/plots">Plots</a></li>
  </ul>
</nav>
```

### 2. Create Search Form Template

**File**: `src/templates/search.html`

```html
{% extends "base.html" %}

{% block title %}Search Astronomical Objects{% endblock %}

{% block content %}
<h1>Search Astronomical Objects</h1>

<form method="post" action="/search/results" id="searchForm">
  <div class="form-group">
    <label for="query">Search Term:</label>
    <input type="text" id="query" name="query" placeholder="Enter astronomical object name..." required>
  </div>
  <button type="submit">Search</button>
</form>

<script>
document.getElementById('searchForm').addEventListener('submit', function(e) {
  const query = document.getElementById('query').value.trim();
  if (!query) {
    e.preventDefault();
    alert('Please enter a search term');
  }
});
</script>
{% endblock %}
```

### 3. Create Search Results Template

**File**: `src/templates/search_results.html`

```html
{% extends "base.html" %}

{% block title %}Search Results{% endblock %}

{% block content %}
<h1>Search Results for "{{ query_text }}"</h1>

{% if results %}
  <p>Found {{ total_count }} result(s) in {{ execution_time }} seconds</p>
  
  <table id="resultsTable" class="display">
    <thead>
      <tr>
        <th>Source</th>
        <th>RA</th>
        <th>Dec</th>
        <th>Epoch</th>
        <th>Equinox</th>
        <th>Shortname</th>
        <th>Reference</th>
        <th>Other References</th>
        <th>Comments</th>
      </tr>
    </thead>
    <tbody>
      {% for result in results %}
      <tr>
        <td><a href="/inventory/{{ result.source }}">{{ result.source }}</a></td>
        <td>{{ "%.2f"|format(result.ra) if result.ra else '' }}</td>
        <td>{{ "%.2f"|format(result.dec) if result.dec else '' }}</td>
        <td>{{ "%.1f"|format(result.epoch) if result.epoch else '' }}</td>
        <td>{{ result.equinox or '' }}</td>
        <td>{{ result.shortname or '' }}</td>
        <td>{{ result.reference or '' }}</td>
        <td>{{ result.other_references or '' }}</td>
        <td>{{ result.comments or '' }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
{% else %}
  <p>No results found for "{{ query_text }}"</p>
{% endif %}

<a href="/search">New Search</a>

<!-- DataTable CSS and JS -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css">
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.js"></script>

<script>
$(document).ready(function() {
  $('#resultsTable').DataTable({
    "pageLength": 25,
    "order": [[ 0, "asc" ]]
  });
});
</script>
{% endblock %}
```

### 4. Add Search Routes to FastAPI

**File**: `src/routes/web.py`

Add these routes to existing web routes:

```python
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import astrodbkit
from datetime import datetime
import time

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/search", response_class=HTMLResponse)
async def search_form(request: Request):
    """Display search form page"""
    return templates.TemplateResponse("search.html", {"request": request})

@router.post("/search/results", response_class=HTMLResponse)
async def search_results(
    request: Request,
    query: str = Form(...)
):
    """Process search query and display results"""
    try:
        # Validate query
        if not query.strip():
            return templates.TemplateResponse("search.html", {
                "request": request,
                "error": "Please enter a search term"
            })
        
        # Execute search using astrodbkit
        start_time = time.time()
        results = astrodbkit.search_object(query.strip())
        execution_time = time.time() - start_time
        
        # Format results for display
        formatted_results = []
        for result in results:
            formatted_results.append({
                "source": result.get("source", ""),
                "ra": result.get("ra", 0.0),
                "dec": result.get("dec", 0.0),
                "epoch": result.get("epoch"),
                "equinox": result.get("equinox", ""),
                "shortname": result.get("shortname", ""),
                "reference": result.get("reference", ""),
                "other_references": result.get("other_references", ""),
                "comments": result.get("comments", "")
            })
        
        return templates.TemplateResponse("search_results.html", {
            "request": request,
            "query_text": query.strip(),
            "results": formatted_results,
            "total_count": len(formatted_results),
            "execution_time": f"{execution_time:.3f}"
        })
        
    except Exception as e:
        # Handle astrodbkit errors
        return templates.TemplateResponse("search_results.html", {
            "request": request,
            "query_text": query.strip(),
            "error": "An error occurred during search",
            "results": [],
            "total_count": 0,
            "execution_time": "0.000"
        })

@router.post("/api/search")
async def search_api(query: str = Form(...)):
    """API endpoint for programmatic search access"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query parameter is required")
        
        start_time = time.time()
        results = astrodbkit.search_object(query.strip())
        execution_time = time.time() - start_time
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "source": result.get("source", ""),
                "ra": result.get("ra", 0.0),
                "dec": result.get("dec", 0.0),
                "epoch": result.get("epoch"),
                "equinox": result.get("equinox", ""),
                "shortname": result.get("shortname", ""),
                "reference": result.get("reference", ""),
                "other_references": result.get("other_references", ""),
                "comments": result.get("comments", "")
            })
        
        return {
            "results": formatted_results,
            "total_count": len(formatted_results),
            "query_text": query.strip(),
            "search_time": datetime.now().isoformat(),
            "execution_time": execution_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during search")
```

### 5. Add CSS Styling

**File**: `src/static/style.css`

Add search-specific styles to existing CSS:

```css
/* Search form styling */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input[type="text"] {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

/* Search results styling */
#resultsTable {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

#resultsTable th,
#resultsTable td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

#resultsTable th {
  background-color: #f8f9fa;
  font-weight: bold;
}

#resultsTable a {
  color: #007bff;
  text-decoration: none;
}

#resultsTable a:hover {
  text-decoration: underline;
}

/* Responsive table for many columns */
@media (max-width: 768px) {
  #resultsTable {
    font-size: 0.9rem;
  }
  
  #resultsTable th,
  #resultsTable td {
    padding: 0.3rem;
  }
}
```

## Testing

### Manual Testing Steps

1. **Start the development server**:
   ```bash
   cd /Users/drodriguez/Projects/Astro-Web
   uvicorn src.main:app --reload
   ```

2. **Test search form access**:
   - Navigate to `http://localhost:8000/search`
   - Verify search form displays correctly
   - Verify navigation includes Search link

3. **Test search functionality**:
   - Enter a valid astronomical object name (e.g., "NGC 1234")
   - Submit the form
   - Verify results page displays with DataTable
   - Verify results link to inventory pages

4. **Test error handling**:
   - Submit empty search form
   - Verify validation error message
   - Test with non-existent object names

5. **Test API endpoint**:
   ```bash
   curl -X POST "http://localhost:8000/api/search" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "query=NGC 1234"
   ```

### Integration Testing

Create test file `tests/test_search.py`:

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_search_form():
    response = client.get("/search")
    assert response.status_code == 200
    assert "Search Astronomical Objects" in response.text

def test_search_results():
    response = client.post("/search/results", data={"query": "NGC 1234"})
    assert response.status_code == 200
    assert "Search Results" in response.text

def test_search_api():
    response = client.post("/api/search", data={"query": "NGC 1234"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_count" in data
    assert "query_text" in data

def test_empty_search():
    response = client.post("/search/results", data={"query": ""})
    assert response.status_code == 200
    # Should show validation error or empty results
```

## Deployment Notes

- Ensure astrodbkit is properly configured with database connection
- Verify JavaScript DataTable CDN links are accessible
- Test search performance with large datasets
- Consider adding search result caching for frequently searched terms

## Troubleshooting

### Common Issues

1. **Search returns no results**: Verify astrodbkit database connection and data availability
2. **DataTable not loading**: Check CDN links and JavaScript console for errors
3. **Navigation link missing**: Verify base.html template includes Search link
4. **Styling issues**: Ensure CSS file is properly linked and styles are applied

### Performance Optimization

- Monitor search execution times
- Consider adding database indexes for frequently searched fields
- Implement result caching for repeated queries
- Optimize astrodbkit search_object parameters if needed
