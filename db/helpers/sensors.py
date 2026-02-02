

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


def get_data_by_date_range(sensor_id, start_datetime, end_datetime):
    """
    Fetch data from the sensor_data table within a date range.

    Args:
        sensor_id (int): The sensor ID
        start_datetime (str): Start datetime in 'YYYY-MM-DD HH:MM:SS' format
        end_datetime (str): End datetime in 'YYYY-MM-DD HH:MM:SS' format

    Returns:
        list: List of (timestamp, temperature, humidity) tuples
    """
    print(f"Executing get_data_by_date_range for sensor {sensor_id}...")

    query = """
        SELECT timestamp, temperature, humidity
        FROM sensor_data
        WHERE sensor_id = ?
          AND timestamp >= ?
          AND timestamp <= ?
        ORDER BY timestamp DESC
    """
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        cur.execute(query, (sensor_id, start_datetime, end_datetime))
        rows = cur.fetchall()
        print(f"Fetched {len(rows)} records successfully.")
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
        MAX(temperature) AS temp_high,
        MIN(temperature) AS temp_low,
        AVG(temperature) AS temp_mean,
        MAX(humidity) AS hum_high,
        MIN(humidity) AS hum_low,
        AVG(humidity) AS hum_mean,
        datetime(MAX(timestamp)) AS latest_time,
        datetime(MIN(timestamp)) AS earliest_time,
        COUNT(*) AS count
    FROM (
        SELECT *
        FROM sensor_data
        WHERE sensor_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    )
    """

    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, (sensor_id, limit))
        result = cur.fetchone()

        if not result:
            return None

        # Calculate standard deviation manually (SQLite doesn't have built-in STDDEV)
        stddev_query = """
        SELECT
            SQRT(AVG(temperature * temperature) - AVG(temperature) * AVG(temperature)) AS temp_stddev,
            SQRT(AVG(humidity * humidity) - AVG(humidity) * AVG(humidity)) AS hum_stddev
        FROM (
            SELECT temperature, humidity
            FROM sensor_data
            WHERE sensor_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        )
        """
        cur.execute(stddev_query, (sensor_id, limit))
        stddev_result = cur.fetchone()

        # Combine results
        stats = dict(result)
        if stddev_result:
            stats['temp_stddev'] = stddev_result['temp_stddev']
            stats['hum_stddev'] = stddev_result['hum_stddev']

        return stats  # Converts sqlite3.Row to a Python dict


def get_stats_by_date_range(sensor_id, start_datetime, end_datetime):
    """
    Get statistics for a sensor within a date range.

    Args:
        sensor_id (int): The sensor ID
        start_datetime (str): Start datetime in 'YYYY-MM-DD HH:MM:SS' format
        end_datetime (str): End datetime in 'YYYY-MM-DD HH:MM:SS' format

    Returns:
        dict: Statistics including high, low, mean, stddev for both temp and humidity
    """
    query = """
    SELECT
        MAX(temperature) AS temp_high,
        MIN(temperature) AS temp_low,
        AVG(temperature) AS temp_mean,
        MAX(humidity) AS hum_high,
        MIN(humidity) AS hum_low,
        AVG(humidity) AS hum_mean,
        datetime(MAX(timestamp)) AS latest_time,
        datetime(MIN(timestamp)) AS earliest_time,
        COUNT(*) AS count
    FROM sensor_data
    WHERE sensor_id = ?
      AND timestamp >= ?
      AND timestamp <= ?
    """

    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, (sensor_id, start_datetime, end_datetime))
        result = cur.fetchone()

        if not result:
            return None

        # Calculate standard deviation manually
        stddev_query = """
        SELECT
            SQRT(AVG(temperature * temperature) - AVG(temperature) * AVG(temperature)) AS temp_stddev,
            SQRT(AVG(humidity * humidity) - AVG(humidity) * AVG(humidity)) AS hum_stddev
        FROM sensor_data
        WHERE sensor_id = ?
          AND timestamp >= ?
          AND timestamp <= ?
        """
        cur.execute(stddev_query, (sensor_id, start_datetime, end_datetime))
        stddev_result = cur.fetchone()

        # Combine results
        stats = dict(result)
        if stddev_result:
            stats['temp_stddev'] = stddev_result['temp_stddev']
            stats['hum_stddev'] = stddev_result['hum_stddev']

        return stats


