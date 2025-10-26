# Quickstart Guide: Hello World Website

**Feature**: Hello World Website  
**Branch**: 001-hello-world-website  
**Date**: 2025-01-27

## Prerequisites

- Python 3.13+ installed
- `uv` package manager installed (or pip)

## Setup

### 1. Install Dependencies

```bash
# Install project dependencies
uv sync
# OR
pip install -r requirements.txt
```

**Required packages**:
- FastAPI ≥0.120.0
- Jinja2
- Bokeh
- uvicorn

### 2. Project Structure

```
src/
├── main.py                  # FastAPI application entry point
├── routes/                   # API route definitions
│   └── web.py               # Web page routes
├── templates/               # Jinja2 HTML templates
│   └── index.html           # Homepage template
├── static/                  # CSS files
│   └── style.css            # Styling
└── visualizations/          # Bokeh plots
    └── scatter.py           # Scatter plot generation
```

### 3. Start the Server

```bash
# From project root
uvicorn src.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 4. View the Website

Open your browser and navigate to:
- **Homepage**: http://localhost:8000/

## What You Should See

### Homepage (`/`)

- **Header**: "Astro Web" title
- **Content**: "Hello World" welcome message
- **Visualization**: Interactive scatter plot with ~20 data points (temperature vs magnitude)
- **Footer**: "© 2025" copyright notice
- **Styling**: Clean minimal theme with light background, dark text, astronomy-inspired colors

### Interactive Features

- **Hover tooltips**: Mouse over data points in the scatter plot to see values
- **Plot interactions**: Pan, zoom, and tool interactions (Bokeh default features)

### 404 Error Page

Navigate to any non-existent URL (e.g., http://localhost:8000/test) to see the 404 error page.

## Development Workflow

### Running in Development Mode

The `--reload` flag enables auto-reload on code changes:

```bash
uvicorn src.main:app --reload --port 8000
```

### Making Changes

1. **Templates**: Edit files in `src/templates/`
2. **Styling**: Edit `src/static/style.css`
3. **Routes**: Edit `src/routes/web.py`
4. **Visualizations**: Edit `src/visualizations/scatter.py`

Changes will automatically reload (when using `--reload`).

### Sample Data Customization

Edit `src/visualizations/scatter.py` to modify:
- Number of data points
- Data ranges (temperature, magnitude)
- Plot appearance
- Tooltip content

## Testing

### Manual Testing

1. **Homepage loads**: Open http://localhost:8000 - should display within 2 seconds
2. **Visualization interactive**: Hover over scatter plot - tooltip should appear within 100ms
3. **404 handling**: Navigate to http://localhost:8000/nonexistent - should show 404 page
4. **Styling applied**: Verify light background, dark text, astronomy colors
5. **Server startup**: Server should start within 5 seconds

### Browser Compatibility

Test in modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Troubleshooting

### Port Already in Use

If port 8000 is occupied:

```bash
# Option 1: Kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 2: Use different port
uvicorn src.main:app --reload --port 8001
```

### Import Errors

```bash
# Ensure you're in the project root
cd C:\Users\strak\Projects\astro-web

# Verify dependencies
uv pip list
# OR
pip list
```

### Visualization Not Rendering

- Check browser console for JavaScript errors
- Verify Bokeh CDN/resources are accessible
- Ensure static files are being served correctly

## Next Steps

- Review [spec.md](./spec.md) for full requirements
- Review [data-model.md](./data-model.md) for entity structure
- Review [contracts/web-api.yaml](./contracts/web-api.yaml) for API endpoints
- Implement according to [tasks.md](./tasks.md) (after running `/speckit.tasks`)

## Support

- **Constitution**: See `.specify/memory/constitution.md` for project principles
- **Quickstart Issues**: Check that all dependencies are installed and paths are correct
- **Development**: Use `--reload` flag for hot-reloading during development

