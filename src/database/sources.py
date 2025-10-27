"""Sources table database queries."""

from astrodbkit.astrodb import Database

from src.database import CONNECTION_STRING


def get_all_sources():
    """
    Retrieve all Sources records from database.

    Returns:
        list: List of dictionaries representing all Sources rows, or None on error
    """
    try:
        db = Database(CONNECTION_STRING)
        df = db.query(db.Sources).pandas()
        return df.to_dict("records")
    except Exception:
        return None


def get_source_inventory(source_name):
    """
    Retrieve all data for a specific source using inventory method.

    Args:
        source_name (str): Source identifier (will be automatically decoded by FastAPI)

    Returns:
        dict: Dictionary of table names to lists of dictionaries, or None on error.
              Only tables with data are returned. Empty tables are filtered out.
    """
    try:
        # Connect to database
        db = Database(CONNECTION_STRING)

        # Get inventory (returns dict of table name -> list of dicts)
        inventory = db.inventory(source_name)

        # Filter out empty tables - only return tables that have data
        result = {}
        for table_name, table_data in inventory.items():
            if table_data is not None and len(table_data) > 0:
                result[table_name] = table_data

        return result if result else None
    except Exception:
        return None
