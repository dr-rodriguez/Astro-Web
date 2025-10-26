"""
Main FastAPI application entry point for Hello World website.

This module initializes the FastAPI app with basic configuration.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
from src.routes import web

app = FastAPI(
    title="Astro Web",
    description="Multi-page astronomy database web application with navigation bar",
    version="0.1.0",
)

# Configure Jinja2 templates
templates = Jinja2Templates(directory="src/templates")
# Add urlencode filter for URL encoding source names
templates.env.filters['urlencode'] = lambda u: quote(str(u), safe='')
web.set_templates(templates)

# Configure static file serving
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Homepage route rendering 'Hello World' content."""
    return await web.homepage(request)


@app.get("/browse", response_class=HTMLResponse)
async def browse(request: Request):
    """Browse database page rendering Sources table."""
    return await web.browse(request)


@app.get("/plots", response_class=HTMLResponse)
async def plot(request: Request):
    """Plots page rendering scatter visualization."""
    return await web.plot(request)


@app.get("/source/{source_name}", response_class=HTMLResponse)
async def inventory_page(request: Request, source_name: str):
    """Source inventory page rendering all data for a specific source."""
    return await web.inventory(request, source_name)


@app.get("/{path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str):
    """404 handler for non-existent pages."""
    return await web.not_found(request, path)
