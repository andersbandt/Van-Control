

# import needed modules
import sqlite3
import datetime

# import database path
from db import DATABASE_DIRECTORY

# import user created modules
from vc.classes.SensorEvent import SensorEvent


##########################################################
### data insertion
##########################################################
def insert_reading(sensor_event: SensorEvent) -> bool:
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        conn.set_trace_callback(print)
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


##########################################################
### data retrieval
##########################################################
# Function to query the database
def get_data(sensor_id, limit):
    query = """
        SELECT timestamp, temperature, humidity 
        FROM sensor_data 
        WHERE sensor_id=? 
        ORDER BY timestamp 
        DESC LIMIT ?
    """
    
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()

        # Query to get the latest temperature and humidity data
        cur.execute(query,(sensor_id, limit))
        
        results = cur.fetchall()
        return results


def get_data_from_time(sensor_id, timestamp_limit):
    """
    Fetch data from the sensor_data table based on a timestamp limit.
    """
    print("Executing get_data_from_time...")

    query = """
        SELECT timestamp, temperature, humidity 
        FROM sensor_data 
        WHERE sensor_id = ? 
          AND timestamp >= ?
        ORDER BY timestamp DESC
    """
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        cur.execute(query, (sensor_id, timestamp_limit))
        rows = cur.fetchall()
        print("Fetched data successfully.")
        return rows


def get_timestamp_from_limit(sensor_id, limit):
    """
    Get the timestamp of the Nth most recent sample for a specific sensor.
    """
    print("Executing get_timestamp_from_limit...")

    query = """
        SELECT timestamp
        FROM sensor_data
        WHERE sensor_id = ?
        ORDER BY timestamp DESC
        LIMIT 1 OFFSET ?
    """
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        cur.execute(query, (sensor_id, limit - 1))  # OFFSET is zero-indexed
        row = cur.fetchone()

    if row:
        print("Fetched timestamp successfully.")
        return row[0]  # Return the timestamp
    else:
        print("No data found for the given parameters.")
        return None
    

def get_stats(sensor_id, limit):
    query = """
    SELECT
        MAX(temperature) AS high, 
        MIN(temperature) AS low, 
        AVG(temperature) AS mean,
        datetime(MAX(timestamp)) AS latest_time,
        datetime(MIN(timestamp)) AS earliest_time
    FROM (
    SELECT * 
        FROM sensor_data 
        WHERE sensor_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    )

    """

    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        conn.row_factory = sqlite3.Row  # Ensures rows are returned as dictionaries
        cur = conn.cursor()
        cur.execute(query, (sensor_id, limit))
        result = cur.fetchone()
        
        return dict(result) if result else None  # Converts sqlite3.Row to a Python dict


