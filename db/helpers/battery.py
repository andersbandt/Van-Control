

# import needed modules
import sqlite3

# import database path
from db import DATABASE_DIRECTORY



def insert_reading(label, value, timestamp) -> bool:
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        conn.set_trace_callback(print)
        cur.execute(
            "INSERT INTO battery_data (label, value, timestamp) VALUES(?, ?, ?)",
            (
                label, value, timestamp
            ),
        )
    return True


def get_battery_data():
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        # TODO: is the below LIMIT=4 needed? Seems like a hardcode? More elegant way to handle it?
        query = """
            SELECT label, value, timestamp
            FROM battery_data
            WHERE label IN ('V', 'I', 'P', 'CE')
            ORDER BY timestamp DESC
            LIMIT 4
        """
        cur.execute(query)
        rows = cur.fetchall()

        # Map the data to a dictionary
        data = {}
        # Ensure all keys are present, even if no data is found
        data.setdefault('voltage', 'N/A')
        data.setdefault('current', 'N/A')
        data.setdefault('power', 'N/A')
        data.setdefault('state_of_charge', 'N/A')
        data['timestamp'] = rows[-1][2]
        for row in rows:
            label, value, timestamp = row
            if label == 'V':
                data['voltage'] = f"{value / 1000:.2f}"  # Convert from mV to V
            elif label == 'I':
                data['current'] = f"{value / 1000:.2f}"  # Convert from mA to A
            elif label == 'P':
                data['power'] = f"{value:.2f}"          # Power is in W
            elif label == 'CE':
                data['state_of_charge'] = f"{value:.2f}"  # State of charge in Ah

        return data




