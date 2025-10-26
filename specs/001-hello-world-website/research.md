# Research: Hello World Website

**Feature**: Hello World Website  
**Branch**: 001-hello-world-website  
**Date**: 2025-01-27  
**Purpose**: Document technical decisions and patterns for building the initial FastAPI web application

## Decisions

### Decision 1: FastAPI Web Server

**Decision**: Use FastAPI as the web server and routing framework.

**Rationale**:
- Constitution principle I mandates FastAPI for all web endpoints
- FastAPI provides built-in Jinja2 template support via Jinja2Templates
- FastAPI's dependency injection supports clean separation of concerns
- Well-documented and compatible with uvicorn ASGI server

**Alternatives considered**:
- Django: Rejected - More complex, heavyweight framework beyond needs
- Flask: Rejected - Constitution explicitly requires FastAPI
- Raw ASGI: Rejected - Too low-level, FastAPI provides better ergonomics

### Decision 2: Jinja2 Template Engine

**Decision**: Use Jinja2 for HTML template rendering.

**Rationale**:
- Constitution principle I mandates Jinja2 templates
- FastAPI has native Jinja2 support via Jinja2Templates class
- Jinja2 is simple and well-suited for basic HTML generation
- Templates separate presentation from logic (API layer separation)

**Alternatives considered**:
- Pydantic HTML rendering: Rejected - Not suitable for complex HTML layouts
- Manual string concatenation: Rejected - No template benefits, maintenance issues

### Decision 3: Bokeh for Visualizations

**Decision**: Use Bokeh library to generate interactive scatter plot visualization.

**Rationale**:
- Constitution principle III mandates Bokeh for all visualizations
- Bokeh supports interactive elements (hover tooltips, pan, zoom)
- Embedded visualizations integrate well with Jinja2 templates
- Bokeh's server-based rendering works with FastAPI backend
- Export capabilities (PNG, HTML) for documentation

**Alternatives considered**:
- Matplotlib: Rejected - Not designed for web interactivity
- Plotly: Rejected - Constitution requires Bokeh, would violate principles
- D3.js: Rejected - JavaScript-based, violates "CSS only" styling approach

### Decision 4: CSS Styling Approach

**Decision**: Use vanilla CSS files separate from HTML templates.

**Rationale**:
- Constitution principle IV mandates separate CSS files, no inline styles
- Simple enough to maintain with intermediate Python skills
- Clean minimal theme aligns with project needs (light background, dark text)
- Avoids compilation step that would add complexity

**Alternatives considered**:
- Tailwind CSS: Rejected - Requires build step, violates simplicity principle
- Bootstrap: Rejected - Complex framework, not minimal as required
- Inline styles: Rejected - Violates constitution principle IV
- CSS-in-JS: Rejected - Not applicable to Python backend

### Decision 5: No Database for This Feature

**Decision**: Use hard-coded sample data (approximately 20 data points) without database connectivity.

**Rationale**:
- Explicitly specified in feature requirements and out-of-scope section
- Simplifies initial prototype to focus on web stack integration
- Allows validation of FastAPI + Jinja2 + Bokeh workflow before adding database complexity
- Sample data sufficient for demonstrating visualization capability

**Alternatives considered**:
- SQLite database: Rejected - Explicitly out of scope for this feature
- JSON file: Rejected - Unnecessary complexity for 20 static data points
- External API: Rejected - Violates "no external dependencies" goal

### Decision 6: Port 8000 Development Server

**Decision**: Run development server on http://localhost:8000 using uvicorn.

**Rationale**:
- Explicitly specified in requirements (FR-001)
- Standard development port that doesn't conflict with common services
- uvicorn is the recommended ASGI server for FastAPI
- Development-only deployment matches project phase

**Alternatives considered**:
- Port 3000: Rejected - Typically used for Node.js, not Python
- Port 5000: Rejected - Conflicts with macOS AirPlay
- Production ports (80/443): Rejected - Development environment only

### Decision 7: Directory Structure

**Decision**: Follow constitution code organization: `/src/main.py`, `/src/routes/`, `/src/templates/`, `/src/static/`, `/src/visualizations/`

**Rationale**:
- Constitution section "Code Organization" specifies exact structure
- Clear separation of concerns (routes, templates, static files, visualizations)
- Aligns with FastAPI best practices for web applications
- No database directory needed since this feature has no database access

**Alternatives considered**:
- Flat structure: Rejected - Violates constitution, poor organization
- Flask-style app.py approach: Rejected - Not aligned with structure requirements
- Monolithic single file: Rejected - Violates simplicity and maintainability

## Implementation Patterns

### Pattern: Template Rendering

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    # Generate visualization
    plot_html = generate_scatter_plot()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "plot": plot_html
    })
```

### Pattern: Bokeh Embedding

```python
from bokeh.embed import components
from bokeh.plotting import figure

def generate_scatter_plot():
    # Create plot
    p = figure(plot_width=800, plot_height=400)
    # Add data and styling
    # Return script and div for Jinja2 embedding
    script, div = components(p)
    return {"script": script, "div": div}
```

### Pattern: Sample Data

```python
import random

def get_sample_data():
    """Generate ~20 random astronomical data points (temperature vs magnitude)"""
    return [
        {"temperature": random.uniform(3000, 10000), "magnitude": random.uniform(0, 10)}
        for _ in range(20)
    ]
```

## Research Status

✅ **NO CLARIFICATIONS NEEDED** - All technical decisions are documented above. The feature specification, constitution requirements, and research provide complete guidance for implementation.

