# Data Model: Individual Source Inventory

**Feature**: Individual Source Inventory Page  
**Date**: 2025-01-27  
**Status**: Phase 1 Design

## Overview

This feature displays data from existing database tables for a single astronomical source. No new database tables are created - the feature reads and displays data from existing related tables.

## Entities

### Source Inventory (Runtime Entity)

**Description**: Represents the complete data collection for a single astronomical source, aggregated from multiple database tables.

**Source**: Retrieved via `db.inventory(source_name)` method from astrodbkit, returns dictionary of table names to lists of dictionaries.

**Fields** (dynamically determined by inventory method):
- `Sources`: List of dictionaries with single source record (source, ra, dec, epoch, equinox, reference, etc.)
- `Photometry`: List of dictionaries with photometry measurements (source, band, magnitude, magnitude_error, telescope, epoch, reference)
- `Spectra`: List of dictionaries with spectrum records (source, regime, observation_date, telescope, instrument, reference, access_url)
- `Parallaxes`: List of dictionaries with parallax measurements (source, parallax, parallax_error, reference)
- `ProperMotions`: List of dictionaries with proper motion data (source, mu_ra, mu_dec, reference)
- `RadialVelocities`: List of dictionaries with radial velocity measurements (source, radial_velocity_km_s, reference)
- `SpectralTypes`: List of dictionaries with spectral type classifications (source, spectral_type_string, spectral_type_code, regime, reference)
- `Gravities`: List of dictionaries with gravity measurements (source, gravity, regime, reference)
- `ModeledParameters`: List of dictionaries with modeled parameters (source, model, parameter, value, unit, reference)
- `CompanionRelationships`: List of dictionaries with companion data (source, companion_name, relationship)
- `CompanionParameters`: List of dictionaries with companion parameter measurements
- `RotationalParameters`: List of dictionaries with rotational data (source, period, v_sin_i, inclination)

**Relationships**:
- All tables have foreign key relationship to `Sources.source` (primary identifier)
- Each table in inventory represents a different data type for the same source
- Not all sources will have data in all tables - some keys may be missing or contain empty lists

**Constraints**:
- Source identifier must exist in Sources table
- If source doesn't exist, inventory method returns empty or raises exception
- Source names may contain special characters, spaces, Unicode that require URL encoding

### Inventory Data Table (Display Entity)

**Description**: Represents a single HTML table displayed on the inventory page, corresponding to one key from the inventory result.

**Fields**:
- `table_name` (str): Name of the database table (e.g., "Photometry", "Spectra")
- `columns` (list): List of column names from the data
- `rows` (list): List of dictionaries, each representing one data record
- `row_count` (int): Number of rows in the table

**Relationships**:
- Each Inventory Data Table corresponds to one key-value pair from the inventory dictionary
- Multiple tables displayed on single inventory page for one source
- Empty or non-existent tables are not displayed (spec requirement FR-004)

**Validation Rules**:
- Table must have data (at least 1 row) to be displayed
- Table names should be readable (e.g., "Photometry" not "db_photometry")
- Column names should preserve database schema names for user reference

### URL-Encoded Source Identifier (Routing Entity)

**Description**: Represents the source name encoded for safe transmission in URL path.

**Fields**:
- `raw_identifier` (str): Original source name from database (e.g., "2MASS J12345678+0123456")
- `url_encoded` (str): URL-encoded version using urllib.parse.quote() (e.g., "2MASS%20J12345678%2B0123456")
- `url_path` (str): Full URL path (e.g., "/source/2MASS%20J12345678%2B0123456")

**Relationships**:
- Maps one-to-one with Sources.source identifier
- Used in URL routing, navigation links from browse page
- Must be decoded by FastAPI before database query

**Constraints**:
- All special characters must be URL-encoded before routing (spec requirement FR-005)
- Decoding must handle: spaces, commas, plus signs, Unicode characters
- FastAPI automatically decodes path parameters
- Encoding must be consistent across navigation (browse page links)

## Data Flow

1. **User navigates** to `/source/{source_name}` where `source_name` is URL-encoded
2. **FastAPI receives** request and decodes `source_name` automatically
3. **Route handler** calls `get_source_inventory(decoded_source_name)`
4. **Database function** executes `db.inventory(decoded_source_name)` 
5. **Inventory method** returns dictionary of lists of dictionaries (table name → list of dicts)
6. **Function filters** out empty tables
7. **Returns** dictionary of inventory data or None on error
9. **Template** receives inventory dictionary, iterates over keys
10. **Template** generates HTML table for each non-empty inventory key
11. **Template** displays source identifier prominently at top
12. **User views** complete inventory page with multiple data tables

## State Transitions

### Source Inventory Retrieval States

**State 1: Valid Source Found**
- Database query succeeds
- Inventory dictionary contains data in one or more tables
- Display all non-empty tables on page

**State 2: Invalid Source**
- Source name doesn't exist in database
- Inventory method returns empty dictionary or raises exception
- Display "Source not found" error message

**State 3: Database Connection Error**
- Database connection fails or query times out
- Exception caught in function
- Display "Database temporarily unavailable" error message

**State 4: Partial Data (Edge Case)**
- Source exists but all related table queries return empty
- Only Sources table has data
- Display only Sources table (spec requirement: empty tables not shown)

## Data Validation

### Input Validation
- Source name must be string
- Source name must not be empty
- URL-decoded source name must match database identifier format

### Output Validation  
- Inventory dictionary keys must be valid table names
- Each table's data must be list of dictionaries
- Empty tables are filtered out (not displayed)
- Tables with data must have consistent column names across all rows

## Notes

- No database schema modifications required
- All data entities already exist in database
- This feature is read-only (displays existing data)
- Inventory method handles all JOIN operations automatically
- All data rows are displayed with native browser scrolling

