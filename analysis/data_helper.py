
# import needed modules
from datetime import datetime


# import user created modules
import db.helpers as dbh




def align_data(primary, data):
    """
    Aligns the data from multiple sensors to the primary sensor's timestamps.
    
    Args:
        primary (int): Index of the primary sensor in the data list.
        data (list): List of sensor data dictionaries where each dictionary contains:
                     - 'timestamp': List of timestamps
                     - 'temperature': List of temperatures
    
    Returns:
        list: A list of aligned data where each row contains the primary timestamp and 
              temperatures from all sensors, aligned to the primary timestamps.
    """
    primary_timestamps = data[primary]["timestamp"]

    def nearest(primary_ts, secondary_timestamps):
        """
        Finds the sample in secondary_timestamps that is closest to the given primary_ts.
        """
        # Convert secondary timestamps to datetime and calculate the minimum time difference
        primary_ts = datetime.strptime(primary_ts, "%Y-%m-%d %H:%M:%S.%f")
        secondary_timestamps_dt = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f") for ts in secondary_timestamps]
        closest_ts = min(secondary_timestamps_dt, key=lambda ts: abs(ts - primary_ts))
        closest_ts = datetime.strftime(closest_ts, "%Y-%m-%d %H:%M:%S.%f")
        return closest_ts
    
    # Initialize aligned data
    aligned_data = []

    # Align each primary timestamp to all sensor datasets
    for primary_ts in primary_timestamps:
        row = {"timestamp": primary_ts, "temperatures": []}

        for sensor_data in data:
            secondary_timestamps = sensor_data["timestamp"]
            secondary_temperatures = sensor_data["temperature"]

            # Find the nearest timestamp in the secondary dataset
            closest_ts = nearest(primary_ts, secondary_timestamps)
            closest_index = secondary_timestamps.index(closest_ts)
            row["temperatures"].append(secondary_temperatures[closest_index])

        aligned_data.append(row)

    return aligned_data


def retrieve_aligned_data(max_limit):
    """
    Retrieves raw data from the database and aligns it based on the primary sensor's timestamps.

    Args:
        max_limit (int): The maximum number of samples to retrieve.
    
    Returns:
        list: Aligned dataset based on the primary sensor's timestamps.
    """
    primary_sensor = 1  # Tag:HARDCODE

    # Retrieve the timestamp limit for the primary sensor
    timestamp_limit = dbh.sensors.get_timestamp_from_limit(primary_sensor, max_limit)

    # Get the raw data for each sensor
    raw_data0 = dbh.sensors.get_data_from_time(0, timestamp_limit)
    raw_data1 = dbh.sensors.get_data_from_time(1, timestamp_limit)
    raw_data2 = dbh.sensors.get_data_from_time(2, timestamp_limit)

    # Convert raw data to dictionary format
    def process_raw_data(raw_data):
        return {
            "timestamp": [row[0] for row in raw_data],
            "temperature": [float(row[1]) for row in raw_data]
        }

    data = [
        process_raw_data(raw_data0),
        process_raw_data(raw_data1),
        process_raw_data(raw_data2),
    ]

    # Align the data
    aligned_data = align_data(primary_sensor, data)

    return aligned_data
