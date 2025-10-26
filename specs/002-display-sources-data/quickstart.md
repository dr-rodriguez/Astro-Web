# Quick Start: Display Sources Data

**Feature**: Display first 10 rows from Sources table on homepage  
**Branch**: `002-display-sources-data`

## Prerequisites

- Python 3.13+
- SIMPLE.sqlite database file in repository root
- Existing FastAPI application running from Feature 001

## Setup

### 1. Database File

Ensure `SIMPLE.sqlite` exists in repository root:

```bash
ls SIMPLE.sqlite  # Should see the file
```

### 2. Verify Dependencies

From repository root:

```bash
uv sync
```

Required packages (already in pyproject.toml):
- astrodbkit>=2.4
- fastapi>=0.120.0
- jinja2>=3.1.0
- uvicorn>=0.30.0

## Running the Application

### Start Development Server

```bash
uvicorn src.main:app --reload --port 8000
```

Or use the project script:

```bash
uv run serve
```

### Access Homepage

Open browser to: `http://localhost:8000`

**Expected Behavior**:
- First 10 rows from Sources table displayed in HTML table
- Table shows columns: source, ra, dec, epoch, equinox, shortname, reference, other_references, comments
- Data displayed at full precision (no rounding)
- Page loads within 3 seconds

## Testing

### Manual Testing

1. **Valid Database**:
   - Visit homepage
   - Verify Sources table displays with 10 rows
   - Check all columns are visible
   - Verify data matches database values

2. **Database Error Handling**:
   - Temporarily move SIMPLE.sqlite file
   - Visit homepage
   - Verify error message displays: "Sources data could not be loaded at this time."
   - Verify table is hidden

3. **Performance**:
   - Visit homepage
   - Check page loads within 3 seconds

### Integration Testing

Run tests from repository root:

```bash
pytest tests/integration/test_sources_display.py
```

## Code Structure

### New Files

```
src/database/
├── __init__.py          # Database module initialization
└── sources.py           # Sources table query functions

tests/
├── integration/
│   └── test_sources_display.py  # Integration tests
└── fixtures/
    └── test_data.py             # Test data fixtures
```

### Modified Files

```
src/routes/web.py              # Add Sources query to homepage route
src/templates/index.html       # Replace plot with Sources table
src/static/style.css           # Add Sources table styling
```

### Example Query

```python
# In src/database/sources.py

from astrodbkit.astrodb import Database
import pandas as pd

def get_sources_data(limit=10):
    """Retrieve first N rows from Sources table."""
    try:
        db = Database('sqlite:///SIMPLE.sqlite')
        # Query Sources table and convert to list of dictionaries
        df = db.query(db.Sources).limit(limit).pandas()
        return df.to_dict('records')  # Returns list of dicts
    except Exception:
        return None
```

## Troubleshooting

### Database Not Found

**Error**: "Sources data could not be loaded at this time."

**Fix**: Ensure SIMPLE.sqlite exists in repository root.

### Missing Columns

**Error**: Template shows fewer than 9 columns

**Fix**: Verify Sources table has all expected columns. Check database schema.

### Page Doesn't Load

**Error**: 500 Internal Server Error

**Fix**: Check server logs for traceback. Common issues:
- Astrodbkit not installed
- Database file path incorrect
- Table name mismatch (case-sensitive)

## Next Steps

After successful implementation:
1. Verify all functional requirements met (FR-001 through FR-007)
2. Run integration tests
3. Check constitution compliance (all principles satisfied)
4. Proceed to `/speckit.tasks` for implementation task breakdown

