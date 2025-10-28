"""Sources table database queries."""

from astrodbkit.astrodb import Database
from specutils import Spectrum

from src.config import CONNECTION_STRING, SPECTRA_URL_COLUMN


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


def get_source_spectra(source_name, convert_to_spectrum=False):
    """
    Retrieve all spectra for a specific source using db.query() with manual specutils conversion.

    Args:
        source_name (str): Source identifier

    Returns:
        pandas.DataFrame: DataFrame with spectrum records including wavelength and flux arrays,
                         plus metadata (source, access_url, observation_date, regime, telescope, 
                         instrument, etc.) or None on error
    """
    try:

        # Connect to database
        db = Database(CONNECTION_STRING)
        
        # Query spectra table for the source using astrodbkit's pandas method
        spectra_df = db.query(db.Spectra).filter(db.Spectra.c.source == source_name).pandas()
        
        if spectra_df.empty:
            return None

        spectra_df['processed_spectrum'] = None

        # Convert spectra URLs to spectra objects
        for index, row in spectra_df.iterrows():
            try:
                spectrum = Spectrum.read(row[SPECTRA_URL_COLUMN], cache=True)
                spectra_df.at[index, 'processed_spectrum'] = spectrum
            except Exception:
                continue

        return spectra_df
        
    except Exception:
        return None
