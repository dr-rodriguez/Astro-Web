"""
Web page routes for Hello World website.

This module contains all HTML page routes including homepage and error pages.
"""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from src.visualizations.scatter import create_scatter_plot
from src.database.sources import get_sources_data

# Templates instance - will be imported from main
templates = None

def set_templates(templates_instance: Jinja2Templates):
    """Set the templates instance from main module."""
    global templates
    templates = templates_instance

async def homepage(request: Request):
    """Render the homepage with Sources table data."""
    # Get Sources data from database
    sources_data = get_sources_data(limit=10)

    # Generate scatter plot
    plot = create_scatter_plot()
    
    # Prepare context for template
    has_error = sources_data is None
    error_message = "Sources data could not be loaded at this time." if has_error else None
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sources_data": sources_data if not has_error else [],
            "has_error": has_error,
            "error_message": error_message,
            "plot_script": plot["script"],
            "plot_div": plot["div"],
        }
    )

async def not_found(request: Request, path: str):
    """Render 404 error page for non-existent routes."""
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "path": path},
        status_code=404
    )

