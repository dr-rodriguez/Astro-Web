# Phase 0: Research & Technical Decisions

**Feature**: Individual Source Inventory Page  
**Date**: 2025-01-27  
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Research Questions

### 1. Astrodbkit inventory() Method

**Question**: How does the astrodbkit `inventory()` method work? What parameters does it take and what does it return?

**Finding**: Based on astrodbkit documentation, the `inventory()` method retrieves all data for a specific source across multiple related tables:
- Method signature: `db.inventory(source_name)` where `source_name` is a string identifier
- Returns a dictionary with table names as keys (e.g., "Sources", "Photometry", "Spectra", "Parallaxes", "ProperMotions") and corresponding data as values
- Each value is typically a list of dictionaries or similar structure
- Empty results (no data for a table) will result in that key being absent
- Method automatically follows foreign key relationships to gather related data

**Decision**: Use `db.inventory(source_name)` to retrieve all data for a source. The result will be a dictionary where:
- Keys are table names (strings like "Sources", "Photometry", etc.)
- Values are list of dictionaries containing the related data

**Rationale**: The inventory method encapsulates all the complex JOIN operations needed to retrieve data from multiple related tables. This satisfies Constitution Principle II (Astrodbkit Abstraction) by using the existing Astrodbkit API rather than writing custom SQL queries.

**Alternatives Considered**:
- Manual JOIN queries for each table - Rejected (violates Astrodbkit Abstraction, more complex code)
- Direct SQLite queries - Rejected (violates Constitution Principle II)

---

### 2. URL Encoding/Decoding in FastAPI

**Question**: How do I handle URL-encoded source names in FastAPI path parameters? How do I encode for navigation links?

**Finding**: FastAPI handles URL decoding automatically for path parameters:
- Use `source_name: str` in path parameter definition
- FastAPI automatically decodes URL-encoded characters (e.g., "%20" becomes space)
- For encoding in templates: Use Python's `urllib.parse.quote()` or Jinja2's `urlencode` filter
- FastAPI's `Response` and `RedirectResponse` handle encoding internally

**Decision**: 
- Define route as `/source/{source_name}` where FastAPI handles URL decoding automatically
- For navigation links in templates, use `quote()` from `urllib.parse` to encode source names
- Test with special characters (spaces, commas, Unicode) to ensure proper encoding/decoding

**Rationale**: FastAPI's automatic URL decoding simplifies the implementation. The constraint from the spec (FR-005) requires handling special characters consistently, which FastAPI provides out-of-the-box.

**Alternatives Considered**:
- Manual URL encoding/decoding with base64 or custom encoding - Rejected (unnecessary complexity, FastAPI handles this)
- POST requests with source name in body - Rejected (violates REST principles for resource access)

---

### 3. Displaying Dynamic Data Tables in Jinja2

**Question**: How do I display multiple dynamically-generated data tables in a single Jinja2 template?

**Finding**: Jinja2 supports nested loops and conditional rendering:
- Use `{% for key, value in inventory_data.items() %}` to iterate over dictionary keys
- Check if table is empty using `{% if value and value|length > 0 %}`
- Use Jinja2's `|length` filter to check data availability
- Loop through columns dynamically using `.keys()` on first row of data
- Jinja2's table generation pattern: header row with `{% for column in columns %}`, then data rows with nested loops

**Decision**: 
- Template will iterate over inventory dictionary keys (table names)
- For each non-empty table, generate HTML table with:
  - Table header: table name (e.g., "Photometry", "Sources")
  - Column headers: dynamically generated from data keys
  - Data rows: iterate through records
- Use Jinja2 conditional `{% if table_data and table_data|length > 0 %}` to skip empty tables

**Rationale**: This approach handles the dynamic nature of inventory data - different sources will have data in different tables. The constraint from spec (FR-004) requires only showing tables with data, which Jinja2 conditionals handle naturally.

**Alternatives Considered**:
- Pre-generating all possible tables statically - Rejected (inefficient, violates YAGNI principle)
- Complex template macros - Rejected (violates Constitution Principle V, Simplicity)

---

### 4. Error Handling for Database Queries

**Question**: What error handling pattern should I use for inventory() method calls? How do I handle invalid source names or database connection failures?

**Finding**: Based on existing code patterns in `src/database/sources.py`:
- Use try-except blocks to catch exceptions during database operations
- Return `None` on error for route handlers to check
- Route handlers should provide user-friendly error messages and appropriate HTTP status codes
- Distinguish between "source not found" (empty inventory) vs database connection errors

**Decision**:
- Wrap `db.inventory(source_name)` in try-except block
- Return dictionary on success, return `None` on exception
- Route handler checks if result is None to indicate error
- Display appropriate error messages: "Source not found" for empty results, "Database unavailable" for exceptions
- Use HTTP 404 status for non-existent sources, HTTP 500 for database errors

**Rationale**: Follows existing patterns in the codebase (see `src/routes/web.py` browse() function). The constraints from spec (FR-008, FR-009) require graceful error handling, which this pattern provides.

**Alternatives Considered**:
- Returning empty dictionary instead of None - Rejected (ambiguous - can't distinguish between "no data" and "error")
- Custom exception classes - Rejected (violates Constitution Principle V, unnecessary complexity for this simple case)

---

## Summary of Technical Decisions

1. **Database Access**: Use `db.inventory(source_name)` to retrieve all source data as dictionary of table names to lists of dictionaries
2. **URL Handling**: FastAPI automatically decodes path parameters; use `quote()` for encoding in templates
3. **Template Rendering**: Iterate over inventory dictionary keys, check for non-empty data, generate tables dynamically
4. **Error Handling**: Return `None` on database errors; route handler displays appropriate error messages
5. **Data Display**: Display all data rows with native browser scrolling (no artificial row limits)

All decisions align with Constitution principles:
- ✅ Astrodbkit abstraction (Principle II)
- ✅ FastAPI-first architecture (Principle I)
- ✅ Jinja2 templates (Principle I)
- ✅ Simplicity - no complex abstractions (Principle V)
- ✅ CSS styling (Principle IV)

