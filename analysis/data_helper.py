
# import needed modules
import time
from datetime import datetime
from bisect import bisect_left, bisect_right, bisect


# import user created modules
import db.helpers as dbh

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
def align_data(primary, data):
    print("\nAligning data ...")
    primary_timestamps = data[primary]["timestamp"]

    
    def nearest(pts, s_ts):
        s_ts = sorted(s_ts)
        
        # Use binary search to find the insertion point
        idx = bisect_left(s_ts, pts)
                
        # Handle edge cases where pts_dt is out of the range of s_timestamps_dt
        if idx == 0:
            closest = s_ts[0]
        elif idx == len(s_ts):
            closest = s_ts[-1]
        else:
            # Compare two neighbors to find the closest
            before = s_ts[idx - 1]
            after = s_ts[idx]
            closest = before if abs(before - pts) <= abs(after - pts) else after

        return closest
    
    # Initialize aligned data
    aligned_data = []

    # Align each primary timestamp to all sensor datasets
    n = len(primary_timestamps)
    i = 0
    for primary_ts in primary_timestamps:
        # DEBUG PRINTOUT
        if i == int(n/4):
            print("25% done ...")
        elif i == int(n/2):
            print("50% done ...")
        elif i == int(3*n/4):
            print("75% done ...")
        elif i == int(0.9*n):
            print("90% done ...")
        i += 1
        # END DEBUG

        row = {"timestamp": primary_ts, "temperatures": []}
        primary_ts_epoch = time.mktime(datetime.strptime(primary_ts, "%Y-%m-%d %H:%M:%S.%f").timetuple()) + datetime.strptime(primary_ts, "%Y-%m-%d %H:%M:%S.%f").microsecond / 1_000_000

        for sensor_data in data:
            secondary_temperatures = sensor_data["temperature"]

            # Preprocess secondary timestamps to epoch seconds
            def preprocess_timestamps(s_timestamps):
                """Pre-convert timestamps to epoch seconds for reuse."""
                return [
                    time.mktime(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f").timetuple()) + 
                    datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f").microsecond / 1_000_000
                    for ts in s_timestamps
                ]

            secondary_timestamps = sensor_data["timestamp"]
            secondary_timestamps_epoch = preprocess_timestamps(secondary_timestamps)

            # Call nearest function with preprocessed timestamps
            closest_ts_epoch = nearest(primary_ts_epoch, secondary_timestamps_epoch)
            closest_ts = datetime.fromtimestamp(closest_ts_epoch).strftime("%Y-%m-%d %H:%M:%S.%f")
            
            # now, match that timestamp with the specific index for the sample we want
            closest_index = secondary_timestamps.index(closest_ts)
            row["temperatures"].append(secondary_temperatures[closest_index])

        aligned_data.append(row)

    print("Finished aligning data")
    return aligned_data


def retrieve_aligned_data(max_limit):
    print(f"Retrieving aligned data with limit {max_limit}")

    primary_sensor = 1  # tag:HARDCODE

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
