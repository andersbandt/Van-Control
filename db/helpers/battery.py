

# import needed modules
import sqlite3
import datetime

# import database path
from db import DATABASE_DIRECTORY



def insert_reading(label, value, timestamp) -> bool:
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
#        conn.set_trace_callback(print)
        cur.execute(
            "INSERT INTO battery_data (label, value, timestamp) VALUES(?, ?, ?)",
            (
                label, value, timestamp
            ),
        )
    return True


def insert_readings(readings: dict, timestamp) -> bool:
    """
    Insert every label/value pair from a single VE.Direct packet in one
    transaction (one connection open + one commit + one fsync), instead of
    one connection/commit per label (a BMV-712 frame has ~20-25 labels, and
    this runs on every main-loop iteration around the clock -- that was
    multiplying SD card writes ~20-25x versus this batched form).
    """
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        # WAL mode is already set persistently on the db file (see db/__init__.py),
        # but `synchronous` is a per-connection setting -- NORMAL is the
        # recommended, still-safe-from-corruption pairing with WAL, and fsyncs
        # less often than the library default of FULL.
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.executemany(
            "INSERT INTO battery_data (label, value, timestamp) VALUES(?, ?, ?)",
            [(label, value, timestamp) for label, value in readings.items()],
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
        data['connected'] = bool(rows)
        data['timestamp'] = rows[-1][2] if rows else None
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


##########################################################
### data retention
##########################################################
def prune_old_data(cutoff: datetime.datetime) -> int:
    """
    Delete battery_data rows older than `cutoff`. Returns the number of rows
    deleted. See sensors.py:prune_old_data() for why this doesn't VACUUM.
    """
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.execute("DELETE FROM battery_data WHERE timestamp < ?", (cutoff,))
        return cur.rowcount




