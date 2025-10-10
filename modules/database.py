import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data/lofisensor_data.db"

def get_connection():
    """Öffnet eine Verbindung zur SQLite-Datenbank."""
    return sqlite3.connect(DB_PATH)

#def insert_sensor_data(sensor_data(timestamp, sensor_name, value)):
    