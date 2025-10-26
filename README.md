# Astro Web

A dynamic web application for exploring astronomical databases, built with FastAPI, Jinja2, and Bokeh.

## Quickstart

### Prerequisites

- Python 3.13+
- `uv` package manager (or pip)

### Installation

```bash
# Install dependencies
uv sync
```

### Running the Application

Grab a copy of the database at https://github.com/SIMPLE-AstroDB/SIMPLE-binary

```bash
# Start the development server
uvicorn src.main:app --reload --port 8000
```

Then open your browser to http://localhost:8000

## Project Structure

```
src/
├── main.py                  # FastAPI application entry point
├── database/                # Database interaction modules
│   └── sources.py          # Source data database operations
├── routes/                   # API route definitions
│   └── web.py               # Web page routes (homepage, browse, inventory, plot, 404)
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Homepage template
│   ├── browse.html         # Browse sources page
│   ├── inventory.html      # Source inventory page
│   ├── plot.html           # Interactive plot page
│   └── 404.html            # Error page template
├── static/                  # CSS files and static assets
│   ├── style.css           # Clean minimal theme CSS
│   └── schema.yaml         # Schema definitions
└── visualizations/          # Bokeh plot generation functions
    └── scatter.py          # Scatter plot from source data
```

## Features

- **Navigation Bar**: Persistent navigation across all pages
- **Browse Sources**: Explore astronomical sources with DataTables-powered search, filtering, and pagination
- **Source Inventory**: View detailed inventory of astronomical data sources
- **Interactive Visualizations**: Bokeh scatter plots with hover tooltips
- **Database Integration**: SQLite database for source data management
- **Clean Minimal Design**: Astronomy-inspired color palette with light background
- **Fast Development**: Hot-reload enabled for rapid development

## Technology Stack

- **FastAPI** ≥0.120.0 - Web framework
- **Jinja2** - Template engine
- **Bokeh** =3.8.0 - Interactive visualizations
- **DataTables** =1.13.7 - Interactive data tables with jQuery
- **uvicorn** - ASGI server

## Development

The application runs in development mode with auto-reload enabled:

```bash
uvicorn src.main:app --reload --port 8000
```

Changes to templates, routes, or visualizations will automatically reload.

## License

Copyright © 2025 David Rodriguez
