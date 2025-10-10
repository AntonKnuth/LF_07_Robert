import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data/robert.db"

def connect_db():
    """Creates connection to SQLite-Database."""
    return sqlite3.connect(DB_PATH)

def create_table():
    """Creates sensor_data Table, falls sie noch nicht existiert."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                sensor TEXT NOT NULL,
                value REAL NOT NULL
            );
        """)
        conn.commit()

def insert_sensor_data(sensor_data: list[tuple[datetime, str, float]]):
    """Insert multiple sensor data."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO sensor_data (timestamp, sensor, value) VALUES (?, ?, ?);",
            sensor_data
        )
        conn.commit()

def get_current_sensor_value():
    """Select current sensor data"""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sensor, value
            FROM sensor_data
            WHERE timestamp = (SELECT MAX(timestamp) FROM sensor_data);
        """)
        return cursor.fetchall()
    
def get_average_sensor_value():
    """Select average value per sensor."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sensor, AVG(value) AS average_value
            FROM sensor_data
            GROUP BY sensor;
        """)
        return cursor.fetchall()