"""
Main FastAPI application entry point for Hello World website.

This module initializes the FastAPI app with basic configuration.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.routes import web

app = FastAPI(
    title="Astro Web - Hello World",
    description="Hello World website demonstrating FastAPI + Jinja2 + Bokeh stack",
    version="0.1.0"
)

# Configure Jinja2 templates
templates = Jinja2Templates(directory="src/templates")
web.set_templates(templates)

# Configure static file serving
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Homepage route rendering 'Hello World' content."""
    return await web.homepage(request)

@app.get("/{path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str):
    """404 handler for non-existent pages."""
    return await web.not_found(request, path)

