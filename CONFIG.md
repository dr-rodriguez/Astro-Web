# Astro-Web Configuration

## Environment Variables

You can customize the application behavior by setting these environment variables:

### Database Configuration

- `ASTRO_WEB_DATABASE_URL`: Database connection string
  - Default: `sqlite:///SIMPLE.sqlite`
  - Examples:
    - SQLite: `sqlite:///path/to/database.db`
    - PostgreSQL: `postgresql://username:password@localhost:5432/astrodb`
    - MySQL: `mysql://username:password@localhost:3306/astrodb`

### Source URL Configuration

- `ASTRO_WEB_SOURCE_URL_BASE`: Base URL for source detail pages
  - Default: `/source/`
  - Example: `/astro/sources/` (for custom deployment)
- `ASTRO_WEB_SOURCE_COLUMN`: Column name for the source identifier
  - Default: `source`

## Usage

Set environment variables before running the application:

```bash
export ASTRO_WEB_DATABASE_URL="postgresql://user:pass@localhost:5432/astrodb"
export ASTRO_WEB_SOURCE_URL_BASE="/astro/sources/"
export ASTRO_WEB_SOURCE_COLUMN="source_id"
uvicorn src.main:app --reload --port 8000
```
