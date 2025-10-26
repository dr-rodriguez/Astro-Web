"""Sources table database queries."""

from astrodbkit.astrodb import Database


def get_sources_data(limit=10):
    """
    Retrieve first N rows from Sources table.

    Args:
        limit (int): Maximum number of rows to retrieve (default: 10)

    Returns:
        list: List of dictionaries representing Sources rows, or None on error
    """
    try:
        db = Database("sqlite:///SIMPLE.sqlite")
        df = db.query(db.Sources).limit(limit).pandas()
        return df.to_dict("records")
    except Exception:
        return None


def get_all_sources():
    """
    Retrieve all Sources records from database.

    Returns:
        list: List of dictionaries representing all Sources rows, or None on error
    """
    try:
        db = Database("sqlite:///SIMPLE.sqlite")
        df = db.query(db.Sources).pandas()
        return df.to_dict("records")
    except Exception:
        return None
