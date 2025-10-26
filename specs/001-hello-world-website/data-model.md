# Data Model: Hello World Website

**Feature**: Hello World Website  
**Branch**: 001-hello-world-website  
**Date**: 2025-01-27

## Entities

This feature uses **no database entities** as database connectivity is explicitly out of scope. The following describe logical entities for the UI and application flow.

### 1. Web Page

**Description**: Represents a single HTML page rendered by the application.

**Structure**:
- Header section: Displays "Astro Web" title
- Content area: Contains main page content and visualization
- Footer section: Displays copyright "© 2025"

**Fields/Properties**:
- `title` (string): Page title, e.g., "Astro Web"
- `header_text` (string): Header text to display ("Astro Web")
- `footer_text` (string): Footer text to display ("© 2025")
- `content` (string/HTML): Main content area including visualization

**Validation Rules**:
- Title must be non-empty
- Header and footer must render correctly

**State Transitions**: None (static page rendering)

**Relationships**: None (no database)

### 2. Visualization (Scatter Plot)

**Description**: Represents an interactive scatter plot displaying sample astronomical data.

**Structure**:
- Data points: ~20 (temperature, magnitude) coordinates
- Interactive features: Hover tooltips
- Visual properties: Temperature vs Magnitude axes

**Fields/Properties**:
- `temperature` (float): Temperature value (range: 3000-10000, sample range)
- `magnitude` (float): Magnitude value (range: 0-10, sample range)
- `hover_tooltip` (string): Text to display on mouse hover

**Validation Rules**:
- Temperature must be within reasonable astronomical range
- Magnitude must be within reasonable range
- Must respond to hover interactions within 100ms

**State Transitions**: None (static visualization, interactive hover state)

**Relationships**: None (no database relationships)

## Sample Data

**Source**: Hard-coded in application (no external files or database)

**Data Points**: Approximately 20 random data points
- Format: `(temperature, magnitude)` pairs
- Example ranges:
  - Temperature: 3000-10000 (arbitrary units)
  - Magnitude: 0-10 (arbitrary units)

**Implementation**:
```python
def get_sample_data():
    """Generate ~20 random astronomical data points"""
    import random
    return [
        {"temperature": random.uniform(3000, 10000), 
         "magnitude": random.uniform(0, 10)}
        for _ in range(20)
    ]
```

## Static Assets

### 1. CSS File

**Description**: Stylesheet for clean minimal theme with astronomy-inspired palette.

**Purpose**: Separate styling from HTML templates per Constitution principle IV.

**Properties**:
- Light background color
- Dark text color
- Astronomy-inspired color palette
- Proper fonts and spacing
- Clean minimal design

**Location**: `/src/static/style.css`

## Notes

- **No Database**: This feature explicitly excludes database connectivity
- **No Persistence**: All data is generated on-the-fly or hard-coded
- **No State Management**: Static page rendering, no user sessions
- **No Data Validation**: Sample data generation only, no input validation needed
- **Next Features**: Future features will add database entities and relationships

