

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


    # Preprocess secondary timestamps to epoch seconds
    def preprocess_timestamps(s_timestamps):
        """Pre-convert timestamps to epoch seconds for reuse."""
        return [
            time.mktime(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f").timetuple()) +
            datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f").microsecond / 1_000_000
            for ts in s_timestamps
        ]

    # Initialize aligned data
    aligned_data = [
        {"timestamp": ts, "temperature": [], "humidity": []}
        for ts in primary_timestamps
    ]
    primary_timestamps_epoch = preprocess_timestamps(primary_timestamps)

    for sensor_data in data:
        secondary_temperatures = sensor_data["temperature"]
        secondary_humidity = sensor_data["humidity"]
        secondary_timestamps = sensor_data["timestamp"]
        secondary_timestamps_epoch = preprocess_timestamps(secondary_timestamps)

        # Loop through each primary timestamp (inner loop)
        for i, (primary_ts, primary_ts_epoch) in enumerate(zip(primary_timestamps, primary_timestamps_epoch)):
            # Find the closest timestamp in the secondary dataset
            closest_ts_epoch = nearest(primary_ts_epoch, secondary_timestamps_epoch)
            closest_ts = datetime.fromtimestamp(closest_ts_epoch).strftime("%Y-%m-%d %H:%M:%S.%f")

            # Match that timestamp with the specific index for the sample we want
            closest_index = secondary_timestamps.index(closest_ts)

            # Append the temperature corresponding to the closest timestamp
            aligned_data[i]["temperature"].append(secondary_temperatures[closest_index])
            aligned_data[i]["humidity"].append(secondary_humidity[closest_index])


    print("Finished aligning data")
    return aligned_data


def retrieve_aligned_data(max_limit, scale='c'):
    print(f"Retrieving aligned data with limit {max_limit}")

    primary_sensor = 2  # tag:HARDCODE

    # Get the raw data for each sensor
    raw_data0 = dbh.sensors.get_data(0, max_limit)
    raw_data1 = dbh.sensors.get_data(1, max_limit)
    raw_data2 = dbh.sensors.get_data(2, max_limit)

    # Convert raw data to dictionary format
    def process_raw_data(raw_data):
        return {
            "timestamp": [row[0] for row in raw_data],
            "temperature": [float(row[1]) for row in raw_data],
            "humidity": [float(row[2]) for row in raw_data]
        }

    data = [
        process_raw_data(raw_data0),
        process_raw_data(raw_data1),
        process_raw_data(raw_data2),
    ]

    # Align the data
    aligned_data = align_data(primary_sensor, data)

    # ---- temperature scaling ----
    scale = scale.lower()
    if scale not in ("c", "f"):
        raise ValueError("scale must be 'c' or 'f'")

    if scale == "f":
        for sensor in aligned_data:
            sensor["temperature"] = [
                (t * 9.0 / 5.0) + 32.0 for t in sensor["temperature"]
            ]

    return aligned_data
