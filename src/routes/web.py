"""
Web page routes for Hello World website.

This module contains all HTML page routes including homepage and error pages.
"""

from urllib.parse import unquote
import time
from datetime import datetime

from fastapi import Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from astrodbkit.astrodb import Database

from src.database.sources import get_all_sources, get_source_inventory
from src.visualizations.scatter import create_scatter_plot

# Templates instance - will be imported from main
templates = None


def set_templates(templates_instance: Jinja2Templates):
    """Set the templates instance from main module."""
    global templates  # noqa: PLW0603
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
        {"label": "Search", "route": "/search", "is_active": current_page == "/search"},
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


async def inventory(request: Request, source_name: str):
    """Render the source inventory page."""
    
    # Get decoded source name for display
    decoded_source_name = unquote(source_name)
    
    # Get inventory data
    inventory_data = get_source_inventory(source_name)
    
    # Handle errors
    if inventory_data is None:
        # Source not found
        has_error = True
        error_message = f"Source not found: {decoded_source_name}"
    else:
        has_error = False
        error_message = None
    
    # Create navigation context with active page
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
        status_code=404 if has_error else 200,
    )


async def search_form(request: Request):
    """Display search form page"""
    # Create navigation context with active page
    nav_context = create_navigation_context(current_page="/search")
    
    return templates.TemplateResponse("search.html", {
        "request": request, 
        **nav_context
    })


async def search_results(request: Request, query: str = Form(...)):
    """Process search query and display results"""
    try:
        # Validate query
        if not query.strip():
            nav_context = create_navigation_context(current_page="/search")
            return templates.TemplateResponse("search.html", {
                "request": request,
                "error": "Please enter a search term",
                **nav_context
            })
        
        # Execute search using astrodbkit
        start_time = time.time()
        db = Database("sqlite:///SIMPLE.sqlite")
        results = db.search_object(query.strip())
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
        
        # Create navigation context with active page
        nav_context = create_navigation_context(current_page="/search")
        
        return templates.TemplateResponse("search_results.html", {
            "request": request,
            "query_text": query.strip(),
            "results": formatted_results,
            "total_count": len(formatted_results),
            "execution_time": f"{execution_time:.3f}",
            **nav_context
        })
        
    except Exception as e:
        # Handle astrodbkit errors
        nav_context = create_navigation_context(current_page="/search")
        return templates.TemplateResponse("search_results.html", {
            "request": request,
            "query_text": query.strip() if query else "",
            "error": f"An error occurred during search: {e}",
            "results": [],
            "total_count": 0,
            "execution_time": "0.000",
            **nav_context
        })


async def search_api(query: str = Form(...)):
    """API endpoint for programmatic search access"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query parameter is required")
        
        start_time = time.time()
        db = Database("sqlite:///SIMPLE.sqlite")
        results = db.search_object(query.strip())
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
        raise HTTPException(status_code=500, detail=f"An error occurred during search: {e}")


async def not_found(request: Request, path: str):
    """Render 404 error page for non-existent routes."""
    return templates.TemplateResponse(
        "404.html", {"request": request, "path": path}, status_code=404
    )
