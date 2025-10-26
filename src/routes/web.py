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


def create_navigation_context(current_page="/"):
    """
    Generate navigation items with active state for the navigation bar.

    Args:
        current_page (str): Route of the current page (e.g., "/", "/browse", "/plots")

    Returns:
        dict: Navigation context with list of navigation items
    """
    nav_items = [
        {"label": "Home", "route": "/", "is_active": current_page == "/"},
        {
            "label": "Browse Database",
            "route": "/browse",
            "is_active": current_page == "/browse",
        },
        {"label": "Plots", "route": "/plots", "is_active": current_page == "/plots"},
    ]
    return {"nav_items": nav_items}


async def homepage(request: Request):
    """Render the homepage"""

    # Create navigation context with active page
    nav_context = create_navigation_context(current_page="/")

    return templates.TemplateResponse("index.html", {"request": request, **nav_context})


async def browse(request: Request):
    """Render the browse database page with Sources table."""
    from src.database.sources import get_all_sources

    # Get all Sources from database
    sources_data = get_all_sources()

    # Handle errors
    has_error = sources_data is None
    error_message = (
        "Sources data could not be loaded at this time." if has_error else None
    )

    # Create navigation context with active page
    nav_context = create_navigation_context(current_page="/browse")

    return templates.TemplateResponse(
        "browse.html",
        {
            "request": request,
            "sources_data": sources_data if not has_error else [],
            "has_error": has_error,
            "error_message": error_message,
            **nav_context,
        },
    )


async def plot(request: Request):
    """Render the plots page with scatter visualization."""
    # Generate scatter plot
    plot = create_scatter_plot()

    # Create navigation context with active page
    nav_context = create_navigation_context(current_page="/plots")

    return templates.TemplateResponse(
        "plot.html",
        {
            "request": request,
            "plot_script": plot["script"],
            "plot_div": plot["div"],
            **nav_context,
        },
    )


async def not_found(request: Request, path: str):
    """Render 404 error page for non-existent routes."""
    return templates.TemplateResponse(
        "404.html", {"request": request, "path": path}, status_code=404
    )
