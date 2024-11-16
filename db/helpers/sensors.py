

# import needed modules
import sqlite3
import datetime

# import database path
from db import DATABASE_DIRECTORY

# import user created modules
from vc.classes.SensorEvent import SensorEvent


def insert_reading(sensor_event: SensorEvent) -> bool:
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sensor_data (sensor_id, temperature, humidity, timestamp) VALUES(?, ?, ?, ?)",
            (
                sensor_event.sensor_id,
                sensor_event.temperature,
                sensor_event.humidity,
                sensor_event.timestamp
            ),
        )
        conn.set_trace_callback(None)
    return True

# Function to query the database
def get_data(sensor_id, limit):
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()

        # Query to get the latest temperature and humidity data
        cur.execute("SELECT temperature, humidity, timestamp FROM sensor_data WHERE sensor_id=? ORDER BY timestamp DESC LIMIT ?",(sensor_id, limit))
        
        results = cur.fetchall()
        return results





