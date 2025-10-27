"""
Database query helper functions.

This module contains helper functions for executing database queries
with timing and error handling.
"""

import time
from astrodbkit.astrodb import Database

from src.database import CONNECTION_STRING


def search_objects(query: str):
    """
    Search for objects in the database using astrodbkit.

    Args:
        query (str): The search query string
        db_path (str): Path to the database file

    Returns:
        tuple: (results, execution_time) where results is a list of search results
               and execution_time is the time taken in seconds
    """
    start_time = time.time()
    db = Database(CONNECTION_STRING)
    results = db.search_object(query.strip(), resolve_simbad=True, format="pandas")
    execution_time = time.time() - start_time

    return results, execution_time
