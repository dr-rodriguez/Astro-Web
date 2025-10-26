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

```bash
# Start the development server
uvicorn src.main:app --reload --port 8000
```

Then open your browser to http://localhost:8000

## Project Structure

```
src/
├── main.py                  # FastAPI application entry point
├── routes/                   # API route definitions
│   └── web.py               # Web page routes (homepage, 404)
├── templates/               # Jinja2 HTML templates
│   ├── index.html          # Homepage template
│   └── 404.html            # Error page template
├── static/                  # CSS files and static assets
│   └── style.css           # Clean minimal theme CSS
└── visualizations/          # Bokeh plot generation functions
    └── scatter.py          # Scatter plot with sample data (temp vs magnitude)
```

## Features

- **Hello World Website**: Simple homepage demonstrating FastAPI + Jinja2 stack
- **Interactive Visualizations**: Bokeh scatter plots with hover tooltips
- **Clean Minimal Design**: Astronomy-inspired color palette with light background
- **Fast Development**: Hot-reload enabled for rapid development

## Technology Stack

- **FastAPI** ≥0.120.0 - Web framework
- **Jinja2** - Template engine
- **Bokeh** ≥3.0.0 - Interactive visualizations
- **uvicorn** - ASGI server

## Development

The application runs in development mode with auto-reload enabled:

```bash
uvicorn src.main:app --reload --port 8000
```

Changes to templates, routes, or visualizations will automatically reload.

## License

Copyright © 2025
