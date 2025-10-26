# Data Model: Display Sources Data

**Feature**: Display Sources Data  
**Date**: 2025-01-27  
**Purpose**: Define data structures for Sources table display

## Entities

### Sources Display Entity

**Description**: Represents a single row from the Sources table displayed on the homepage.

**Fields**:

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `source` | string | Unique source identifier | "2MASS J12345678-0123456" |
| `ra` | float | Right ascension (degrees) | 123.456789 |
| `dec` | float | Declination (degrees) | -12.345678 |
| `epoch` | float | Epoch of coordinates | 2000.0 |
| `equinox` | string | Equinox reference | "J2000.0" |
| `shortname` | string | Short catalog name | "J1234-0123" |
| `reference` | string | Primary reference | "2019ApJ...123..456A" |
| `other_references` | string | Additional references | "2010MNRAS..987..321B, 2020AJ....456..789C" |
| `comments` | string | Additional notes | "High proper motion source" |

**Relationships**: None (feature displays tabular data only, no joins required)

**Validation Rules**:
- All fields are optional (can be NULL in database)
- Display data at full precision (no rounding, no formatting)
- Column order: source, ra, dec, epoch, equinox, shortname, reference, other_references, comments

---

### Database Connection Entity

**Description**: Represents the connection to SIMPLE.sqlite database.

**Fields**:

| Field Name | Type | Description |
|------------|------|-------------|
| `db_path` | string | Path to SIMPLE.sqlite file | "SIMPLE.sqlite" |
| `connection` | Database object | Astrodbkit connection instance |

**State Transitions**:
- Uninitialized → Initialized (on first query)
- Initialized → Error (database file not found or corrupted)
- Error → Initialized (if database becomes available)

**Error States**:
- FileNotFoundError: SIMPLE.sqlite file missing
- sqlite3.DatabaseError: Corrupted database file
- Astrodbkit errors: Table schema issues or connection failures

---

### Sources Query Result

**Description**: Container for query results passed to Jinja2 template.

**Fields**:

| Field Name | Type | Description |
|------------|------|-------------|
| `rows` | list[dict] | List of Sources records (up to 10 rows) |
| `row_count` | int | Number of rows returned (0-10) |
| `has_error` | bool | True if query failed |
| `error_message` | string | Error message (only if has_error=True) |

**Validation Rules**:
- `has_error=True` if database connection or query fails
- `row_count` is exact number of rows in `rows` list
- If `has_error=True`, `rows` should be empty list
- If `has_error=True`, `error_message` must be present

---

## Data Flow

```
SIMPLE.sqlite (Database)
    ↓
Database('sqlite:///SIMPLE.sqlite')
    ↓
db.query(db.Sources).limit(10).pandas()
    ↓
DataFrame.to_dict('records') → List of row dictionaries
    ↓
sources_query_result (container)
    ↓
Jinja2 template context
    ↓
index.html (rendered HTML)
```

## Database Schema Reference

**Table**: Sources

**Columns** (from database schema):
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
```python
db = Database("sqlite:///SIMPLE.sqlite")
results = db.query(db.Sources).limit(10).pandas()
```

## Error Handling

**Error Case 1**: Database file missing
- **Detection**: FileNotFoundError or Astrodbkit connection error
- **Response**: has_error=True, error_message="Sources data could not be loaded at this time."
- **Template Behavior**: Render error message, hide table

**Error Case 2**: Fewer than 10 rows
- **Detection**: row_count < 10
- **Response**: has_error=False, rows contains available rows (<10)
- **Template Behavior**: Render all available rows

**Error Case 3**: Database corruption or SQLite errors
- **Detection**: sqlite3.DatabaseError or generic exception
- **Response**: has_error=True, error_message="Sources data could not be loaded at this time."
- **Template Behavior**: Render error message, hide table

