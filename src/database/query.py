"""
Database query helper functions.

This module contains helper functions for executing database queries
with timing and error handling.
"""

import time
from astrodbkit.astrodb import Database
from astropy.coordinates import SkyCoord

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


def parse_coordinate_to_decimal(coord_str, is_ra=False):
    """
    Parse coordinate string (sexagesimal or decimal) to decimal degrees.
    
    Args:
        coord_str (str): Coordinate string in sexagesimal or decimal format
        is_ra (bool): Whether this is a Right Ascension coordinate
        
    Returns:
        float: Coordinate in decimal degrees
        
    Raises:
        ValueError: If coordinate cannot be parsed or is out of range
    """
    coord_str = coord_str.strip()
    
    try:
        # Try to parse as sexagesimal first (spec requirement)
        if is_ra:
            # RA format: "13h57m12.37s" or "13h 57m 12s" or "13 57 12.37"
            # Check if coord_str contains sexagesimal separators
            if any(char in coord_str.lower() for char in ['h', 'm', 's', 'd']):
                # Parse as sexagesimal RA
                skycoord = SkyCoord(coord_str, frame='icrs')
                coord_value = skycoord.ra.deg
            else:
                # Try decimal degrees
                coord_value = float(coord_str)
        else:
            # Dec format: "+14d28m39.8" or "-45d30m" or "+14° 28' 39""
            # Check if coord_str contains sexagesimal separators
            if any(char in coord_str for char in ['d', '°', 'm', "'", 's', '"']):
                # Parse as sexagesimal Dec
                skycoord = SkyCoord(coord_str, frame='icrs')
                coord_value = skycoord.dec.deg
            else:
                # Try decimal degrees
                coord_value = float(coord_str)
        
        # Validate coordinate ranges
        if is_ra:
            if not (0 <= coord_value <= 360):
                raise ValueError(f"RA must be between 0 and 360 degrees, got {coord_value}")
        else:
            if not (-90 <= coord_value <= 90):
                raise ValueError(f"Dec must be between -90 and +90 degrees, got {coord_value}")
        
        return coord_value
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid coordinate format: {coord_str}") from e


def convert_radius_to_degrees(radius_value, radius_unit):
    """
    Convert radius from user-selected unit to degrees.
    
    Args:
        radius_value (str or float): Radius value as number
        radius_unit (str): Unit of radius ("degrees", "arcminutes", "arcseconds")
        
    Returns:
        float: Radius in degrees
        
    Raises:
        ValueError: If radius_unit is invalid or radius exceeds 10 degrees
    """
    # Convert to float
    radius_val = float(radius_value)
    
    # Validate radius is positive
    if radius_val <= 0:
        raise ValueError("Radius must be a positive number")
    
    # Convert based on unit
    if radius_unit == "degrees":
        radius_deg = radius_val
    elif radius_unit == "arcminutes":
        radius_deg = radius_val / 60.0
    elif radius_unit == "arcseconds":
        radius_deg = radius_val / 3600.0
    else:
        raise ValueError(f"Invalid radius unit: {radius_unit}. Must be degrees, arcminutes, or arcseconds")
    
    # Validate radius does not exceed 10 degrees
    if radius_deg > 10.0:
        raise ValueError("Radius must not exceed 10 degrees after unit conversion")
    
    return radius_deg


def cone_search(ra, dec, radius_deg):
    """
    Perform a cone search for objects within a specified region of the sky.
    
    Args:
        ra (float): Right Ascension in decimal degrees (0-360)
        dec (float): Declination in decimal degrees (-90 to +90)
        radius_deg (float): Search radius in degrees
        
    Returns:
        tuple: (results, execution_time) where results is a DataFrame
               and execution_time is the time taken in seconds
    """
    start_time = time.time()
    db = Database(CONNECTION_STRING)
    results = db.query_region(ra, dec, radius_deg, coord_frame='icrs')
    execution_time = time.time() - start_time
    
    # Apply 10,000 result cap if needed
    if len(results) > 10000:
        results = results.head(10000)
    
    return results, execution_time
