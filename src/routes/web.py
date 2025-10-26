"""
Web page routes for Hello World website.

This module contains all HTML page routes including homepage and error pages.
"""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from src.visualizations.scatter import create_scatter_plot

# Templates instance - will be imported from main
templates = None

def set_templates(templates_instance: Jinja2Templates):
    """Set the templates instance from main module."""
    global templates
    templates = templates_instance

async def homepage(request: Request):
    """Render the homepage with 'Hello World' content and visualization."""
    # Generate scatter plot
    plot = create_scatter_plot()
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "plot_script": plot["script"], "plot_div": plot["div"]}
    )

async def not_found(request: Request, path: str):
    """Render 404 error page for non-existent routes."""
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "path": path},
        status_code=404
    )

