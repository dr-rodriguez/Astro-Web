"""Database module for Astrodbkit database interactions."""

from src.config import get_database_connection_string

__all__ = ['sources']

CONNECTION_STRING = get_database_connection_string()