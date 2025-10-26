# Quickstart Guide: Navigation Bar with Multi-Page Structure

**Feature**: `003-nav-bar`  
**Date**: 2025-01-27  
**Purpose**: Setup instructions and basic testing guide

---

## Prerequisites

- Python 3.13
- SIMPLE.sqlite database in project root
- Dependencies installed: `uv pip install -e .`

## Setup

1. **Ensure database is accessible**: Verify `SIMPLE.sqlite` exists in project root
2. **Start development server**: `uvicorn src.main:app --reload --port 8000`
3. **Access application**: Navigate to `http://localhost:8000`

## Testing Guide

### Test 1: Navigation Between Pages

**Steps**:
1. Open `http://localhost:8000`
2. Click "Browse Database" in navigation bar
3. Click "Visualizations" in navigation bar
4. Click "Home" in navigation bar

**Expected**: 
- Navigation bar visible at top of all pages
- Active page highlighted (different color/bold)
- Page content changes correctly (intro, table, plot)
- No JavaScript errors in browser console

### Test 2: Browse Database - Table Display

**Steps**:
1. Navigate to `/browse`
2. Observe Sources table with all columns
3. Verify pagination controls visible

**Expected**:
- Table displays all Sources records
- Columns: source, ra, dec, epoch, equinox, shortname, reference, other_references, comments
- Pagination shows page size selector (10, 25, 50, 100)
- First page displayed by default

### Test 3: Browse Database - Sorting

**Steps**:
1. Navigate to `/browse`
2. Click column header "RA"
3. Click again to toggle ascending/descending
4. Click different column header (e.g., "Dec")

**Expected**:
- Table sorts by clicked column
- Sort order toggles (asc ↔ desc)
- Previous sort cleared when clicking different column
- Results update within 1 second

### Test 4: Browse Database - Filtering

**Steps**:
1. Navigate to `/browse`
2. Enter text in search box (e.g., "GJ")
3. Observe table update
4. Clear search box

**Expected**:
- Table filters to show only rows matching search text
- Search matches across all columns
- Updates within 1 second
- Empty search shows all rows

### Test 5: Browse Database - Pagination

**Steps**:
1. Navigate to `/browse`
2. Change page size to 25
3. Navigate to next page
4. Navigate to previous page
5. Navigate away to Visualizations, then return to Browse

**Expected**:
- Page size changes work correctly
- Pagination controls enable/disable based on available pages
- Navigation between pages works
- **State resets** on return (default 10 rows, first page, no sort/filter)

### Test 6: Visualizations - Scatter Plot

**Steps**:
1. Navigate to `/plots`
2. Observe scatter plot with ra on x-axis, dec on y-axis
3. Hover over data points
4. Use zoom/pan controls
5. Click "reset" tool

**Expected**:
- All Sources with valid ra/dec displayed as points
- Hover shows tooltips with source info and coordinates
- Pan, zoom, reset tools work smoothly
- Points correspond to actual database coordinates

### Test 7: Error Handling

**Steps**:
1. Temporarily rename `SIMPLE.sqlite` to `SIMPLE.sqlite.bak`
2. Navigate to `/browse`
3. Navigate to `/plots`

**Expected**:
- Error message displayed: "Sources data could not be loaded"
- Navigation bar still visible and functional
- User can navigate to other pages

### Test 8: Empty Database Handling

**Steps**:
1. Backup existing database
2. Create empty SIMPLE.sqlite
3. Navigate through all pages

**Expected**:
- Home page displays (no database dependency)
- Browse page shows empty table or "No data" message
- Visualizations page shows empty plot or "No data" message
- No application crashes

## Performance Checks

- **Page Load Time**: All pages load within 2 seconds
- **Table Interactions**: Sorting, filtering, pagination updates within 1 second
- **Plot Interaction**: Hover tooltips appear within 100ms

## Browser Compatibility

Test in:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (latest)

## Troubleshooting

**Issue**: Table not displaying data  
**Solution**: Check browser console for JavaScript errors. Verify `SIMPLE.sqlite` exists and is accessible.

**Issue**: Plot not showing  
**Solution**: Verify Bokeh CDN scripts loaded (check Network tab). Ensure Sources have valid ra/dec values.

**Issue**: Navigation bar not highlighting active page  
**Solution**: Check CSS for `.nav-active` class. Verify `current_page` context passed to templates.

## Next Steps

After completing `/speckit.tasks`, implement the feature following the task breakdown in `tasks.md`.


