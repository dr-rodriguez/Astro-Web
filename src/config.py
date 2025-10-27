"""
Configuration settings for the Astro-Web application.

This module contains all configurable settings including database connection
and URL generation parameters.
"""

import os
import pandas as pd
from urllib.parse import quote

# Database Configuration
# Default to SQLite database in project root
DATABASE_CONNECTION_STRING = os.getenv("ASTRO_WEB_DATABASE_URL", "sqlite:///SIMPLE.sqlite")

# Source URL Configuration
# Base URL for source detail pages - can be customized for different deployments
ASTRO_WEB_SOURCE_URL_BASE = os.getenv("ASTRO_WEB_SOURCE_URL_BASE", "/source/")
ASTRO_WEB_SOURCE_COLUMN = os.getenv("ASTRO_WEB_SOURCE_COLUMN", "source")


def get_source_url(results):
    """
    Given a pandas DataFrame or list of dictionaries, convert the ASTRO_WEB_SOURCE_COLUMN to a complete URL for the source detail page.

    Args:
        results: Either a pandas DataFrame or list of dictionaries to convert

    Returns:
        Same type as input: DataFrame or list of dictionaries with the ASTRO_WEB_SOURCE_COLUMN converted to a complete URL for the source detail page
    """
    if results is None:
        return None

    # Handle list of dictionaries (from database queries)
    if isinstance(results, list):
        new_results = []
        for record in results:
            new_record = record.copy()
            if ASTRO_WEB_SOURCE_COLUMN in new_record:
                new_record[ASTRO_WEB_SOURCE_COLUMN] = (
                    f"<a href='{ASTRO_WEB_SOURCE_URL_BASE}{quote(str(new_record[ASTRO_WEB_SOURCE_COLUMN]))}'>{new_record[ASTRO_WEB_SOURCE_COLUMN]}</a>"
                )
            new_results.append(new_record)
        return new_results

    # Handle pandas DataFrame
    elif isinstance(results, pd.DataFrame):
        new_results = results.copy()
        if ASTRO_WEB_SOURCE_COLUMN in new_results.columns:
            new_results[ASTRO_WEB_SOURCE_COLUMN] = new_results[ASTRO_WEB_SOURCE_COLUMN].apply(
                lambda x: f"<a href='{ASTRO_WEB_SOURCE_URL_BASE}{quote(str(x))}'>{x}</a>"
            )
        return new_results

    # Fallback for other types
    else:
        return results


def get_database_connection_string() -> str:
    """
    Get the database connection string.

    Returns:
        str: Database connection string
    """
    return DATABASE_CONNECTION_STRING
