# Phase 0: Research & Technical Decisions

**Feature**: Display Sources Data  
**Date**: 2025-01-27  
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Research Questions

### 1. Astrodbkit Query Patterns for SQLite

**Question**: How do I query the Sources table using Astrodbkit?

**Finding**: Based on [Astrodbkit documentation](https://astrodbkit.readthedocs.io/en/latest/), Astrodbkit uses SQLAlchemy ORM with a `Database` class:
- `Database(connection_string)` - Initialize database connection using SQLAlchemy connection string
- For SQLite: `connection_string = 'sqlite:///SIMPLE.sqlite'`
- Database creates methods for each table (e.g., `db.Sources`, `db.Photometry`)
- Query using SQLAlchemy methods: `db.query(db.Sources).limit(10).pandas()` or `.table()`
- Convert results to pandas DataFrame with `.pandas()` or Astropy Table with `.table()`

**Decision**: Use `Database('sqlite:///SIMPLE.sqlite')` to connect, then query with `db.query(db.Sources).limit(10).pandas()` to get a pandas DataFrame. Convert DataFrame to list of dictionaries for Jinja2 templates.

**Rationale**: Astrodbkit maintains database abstraction via SQLAlchemy while providing SQLite compatibility. Using `.pandas()` provides clean DataFrame conversion. This satisfies Constitution Principle II (Astrodbkit Abstraction).

**Alternatives Considered**: 
- Direct SQL via sqlite3 - Rejected (violates Constitution Principle II)
- pandas read_sql - Rejected (adds unnecessary dependency, bypasses Astrodbkit)

---

### 2. Database Connection Management

**Question**: Where should database connections live and how should they be initialized?

**Finding**: Based on [Astrodbkit documentation](https://astrodbkit.readthedocs.io/en/latest/):
- Initialize with `Database(connection_string)` where `connection_string = 'sqlite:///SIMPLE.sqlite'`
- Database object exposes table classes (e.g., `db.Sources`, `db.Photometry`)
- Best practice for FastAPI: Initialize once, store as module-level variable

**Decision**: Create `src/database/sources.py` module with a `get_db()` function that initializes `Database('sqlite:///SIMPLE.sqlite')` connection. Store connection as module-level variable, initialized on first access (lazy initialization).

**Rationale**: Lazy initialization avoids startup errors if database file is missing. Module-level storage is simple and sufficient for development prototype. Follows Astrodbkit initialization pattern.

**Alternatives Considered**:
- Database per-request via FastAPI dependency - Rejected (overkill for single read-only query)
- Global connection in main.py - Rejected (violates separation of concerns)

---

### 3. Error Handling with Astrodbkit

**Question**: What exceptions can Astrodbkit raise and how should they be handled?

**Finding**: Based on [Astrodbkit documentation](https://astrodbkit.readthedocs.io/en/latest/) and SQLAlchemy patterns:
- Missing database file: `OperationalError` or `sqlalchemy.exc.NoSuchTableError`
- Corrupted database: `sqlite3.DatabaseError` or SQLAlchemy connection errors
- Missing table or schema issues: `NoSuchTableError` or attribute errors
- Connection errors: SQLAlchemy `OperationalError`, `DatabaseError`

**Decision**: Wrap Astrodbkit queries in try/except block catching `Exception` for broad coverage (catches SQLAlchemy errors). Return None or empty list on any error. Route handler checks for None and renders error message accordingly.

**Rationale**: Catching all exceptions provides comprehensive error handling. Graceful degradation aligns with FR-005 (database errors must be handled gracefully). Simple error handling maintains Constitution Principle V (Simplicity).

**Alternatives Considered**:
- Detailed error messages per exception type - Rejected (adds complexity, violates FR-005 requirement for simple message)
- Retry logic - Rejected (unnecessary for file-based SQLite, adds complexity)

---

### 4. Data Presentation Format

**Question**: How should table data be passed to Jinja2 templates?

**Finding**: Jinja2 best practices:
- Pass data as dictionaries or lists of dictionaries
- Use Jinja2 template variables to iterate over rows
- Keep template logic simple (no complex transformations in template)

**Decision**: Convert Astrodbkit query results to list of dictionaries. Each dictionary represents one row with column names as keys. Pass list to template via TemplateResponse context.

**Rationale**: Dictionary format is native to Python and Jinja2. Column names as keys allow easy template access (`{{ row.source }}`). Simple structure satisfies Constitution Principle V.

**Alternatives Considered**:
- Pass raw Astrodbkit objects - Rejected (template would need to know Astrodbkit API)
- Use pandas DataFrame - Rejected (unnecessary dependency)

---

### 5. Template Structure for Sources Table

**Question**: How should the Sources table be displayed in the HTML template?

**Finding**: HTML table best practices:
- Use semantic `<table>`, `<thead>`, `<tbody>` structure
- Include column headers matching database column names
- Support conditional rendering (show table only if data exists)

**Decision**: Replace Bokeh plot in index.html with Sources table. Use Jinja2 if/else to conditionally render table or error message. Table headers match database columns: source, ra, dec, epoch, equinox, shortname, reference, other_references, comments.

**Rationale**: Sematic HTML improves accessibility and maintainability. Conditional rendering handles FR-005 error case cleanly.

**Alternatives Considered**:
- Keep both plot and table - Rejected (out of scope, violates SC-004 requirement for immediate visibility)
- Separate route for Sources data - Rejected (FR-007 requires homepage display)

---

### 6. CSS Styling for Data Table

**Question**: How should the Sources table be styled?

**Finding**: CSS table styling best practices:
- Use border-collapse for clean grid appearance
- Add padding to cells for readability
- Use alternating row colors for visual separation
- Center-align numeric columns (ra, dec, epoch, equinox)
- Left-align text columns

**Decision**: Extend existing `src/static/style.css` with `.sources-table` styles. Add border, cell padding, and alternating row backgrounds. No framework required (vanilla CSS).

**Rationale**: Extends existing CSS file maintains consistency. Simple styling aligns with Constitution Principle IV (CSS Styling). No compilation needed.

**Alternatives Considered**:
- Bootstrap table styling - Rejected (requires CDN or framework, violates Constitution Principle IV)
- Inline styles - Rejected (violates Constitution Principle IV)

---

## Summary of Decisions

| Decision | Rationale | Constitution Alignment |
|----------|-----------|------------------------|
| Use `Database('sqlite:///SIMPLE.sqlite')` with SQLAlchemy query methods | Database abstraction required, follows Astrodbkit API | Principle II ✅ |
| Module-level DB connection with lazy initialization | Simple initialization avoids startup errors | Principle V ✅ |
| Catch all exceptions → simple error message | Graceful error handling for any SQLAlchemy/Astrodbkit error | Principles V, FR-005 ✅ |
| Pass list of dicts to template (convert from pandas DataFrame) | Simple Jinja2 rendering, leverages `.pandas()` output | Principle V ✅ |
| Replace plot with table on homepage | Requirement for immediate data display | FR-002, SC-004 ✅ |
| Extend existing CSS with vanilla styles | Keep styling simple and maintainable | Principle IV ✅ |

## Implementation Readiness

All research questions resolved. No NEEDS CLARIFICATION markers remain. Ready to proceed to Phase 1 (Design & Contracts).

