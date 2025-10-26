# Data Model: Navigation Bar with Multi-Page Structure

**Feature**: Navigation Bar with Multi-Page Structure  
**Date**: 2025-01-27  
**Purpose**: Define data structures for navigation and multi-page content

## Entities

### Navigation Item Entity

**Description**: Represents a single item in the navigation bar with routing information.

**Fields**:

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `label` | string | Display text for navigation link | "Home" |
| `route` | string | URL path for the link | "/" |
| `is_active` | boolean | Whether this is the current page | true |

**State Transitions**:
- Inactive → Active (when user navigates to this page)
- Active → Inactive (when user navigates away)

---

### Home Page Content Entity

**Description**: Represents the content displayed on the Home page.

**Fields**:

| Field Name | Type | Description |
|------------|------|-------------|
| `introduction_text` | string | Brief text about the astronomical database |

**Content Structure**:
- 2-3 paragraphs explaining the database
- Information about astronomical sources
- Guidance to other sections

---

### Browse Database Page Entity

**Description**: Represents the table display with interactive controls for the Sources data.

**Fields**:

| Field Name | Type | Description |
|------------|------|-------------|
| `sources_data` | list[dict] | All Sources records from database |
| `sort_column` | string | Column name to sort by (null if no sort) |
| `sort_order` | string | "asc" or "desc" |
| `page_number` | int | Current page number (1-based) |
| `page_size` | int | Number of rows per page (10, 25, 50, or 100) |
| `filter_text` | string | Text to filter by (searches all columns) |
| `total_rows` | int | Total number of Sources records |
| `total_pages` | int | Calculated total pages based on page_size |

**Validation Rules**:
- Sort order toggles on repeated column clicks (asc → desc → none)
- Pagination shows appropriate controls for available pages
- Filter updates results dynamically
- Results update within 1 second of user interaction

---

### Visualizations Page Entity

**Description**: Represents the scatter plot visualization of astronomical coordinates.

**Fields**:

| Field Name | Type | Description |
|------------|------|-------------|
| `sources_with_coords` | list[dict] | Sources records with valid ra and dec |
| `plot_script` | string | Bokeh JavaScript script for rendering |
| `plot_div` | string | Bokeh HTML div container |
| `sources_plotted` | int | Count of sources displayed in plot |
| `sources_excluded` | int | Count of sources excluded (null coordinates) |

**Validation Rules**:
- Only Sources with non-null ra and dec are plotted
- Excluded count message shown in legend or note
- Plot uses actual coordinate values from database
- Interactive features: pan, zoom, reset, hover tooltips

---

### Navigation Context Entity

**Description**: Context passed to all pages for rendering navigation bar.

**Fields**:

| Field Name | Type | Description |
|------------|------|-------------|
| `current_page` | string | Route of current page ("/", "/browse", "/plots") |
| `nav_items` | list[NavigationItem] | List of all navigation items |

**Relationships**:
- Each page receives NavigationContext in template variables
- Template iterates over nav_items to render navigation links
- Current page's nav item has is_active=true

---

## Data Flow

### Navigation Flow

```
User clicks navigation link
    ↓
Route handler determines target page
    ↓
Sets current_page in NavigationContext
    ↓
Renders template with NavigationContext
    ↓
Template displays navigation bar with active state
```

### Browse Database Flow

```
User visits /browse
    ↓
Route handler retrieves all Sources from database
    ↓
Applies current sort, filter, pagination
    ↓
Passes filtered subset to template
    ↓
Template displays table with controls
```

### Visualizations Flow

```
User visits /plots
    ↓
Route handler retrieves all Sources from database
    ↓
Filters Sources to those with valid ra and dec
    ↓
Generates Bokeh plot with coordinates
    ↓
Passes plot components to template
    ↓
Template displays interactive visualization
```

---

## Error Handling

### Database Errors

**Error Case 1**: Database connection fails on Browse Database
- **Detection**: get_sources_data() returns None
- **Response**: has_error=True, error_message displayed in content area
- **Navigation**: Navigation bar remains visible and functional

**Error Case 2**: No Sources in database
- **Detection**: Empty list returned from database query
- **Response**: Table shows "No data available" message or empty table
- **Navigation**: All navigation links remain functional

**Error Case 3**: Database connection fails on Visualizations
- **Detection**: get_sources_data() returns None or empty
- **Response**: Plot area shows "Data unavailable" message
- **Navigation**: Users can navigate to other pages

---

## Database Schema Reference

**Table**: Sources

**Columns**:
- source (TEXT, PRIMARY KEY)
- ra (REAL)
- dec (REAL)
- epoch (REAL)
- equinox (TEXT)
- shortname (TEXT)
- reference (TEXT)
- other_references (TEXT)
- comments (TEXT)

**Query Pattern**:
- Browse Database: `db.query(db.Sources).all()`
- Visualizations: Filter results for non-null ra and dec


