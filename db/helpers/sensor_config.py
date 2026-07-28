

# import needed modules
import sqlite3

# import database path
from db import DATABASE_DIRECTORY
from config import NUM_SENSORS

DEFAULT_NAMES = {0: 'Internal', 1: 'Living Room', 2: 'Bedroom'}


def get_sensor_names():
    """Return {sensor_id: name} for every sensor, falling back to defaults."""
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        cur.execute("SELECT sensor_id, name FROM sensor_config")
        overrides = dict(cur.fetchall())

    names = {i: DEFAULT_NAMES.get(i, f"Sensor {i}") for i in range(NUM_SENSORS)}
    names.update(overrides)
    return names


def set_sensor_name(sensor_id, name) -> bool:
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        conn.execute(
            """
            INSERT INTO sensor_config (sensor_id, name) VALUES (?, ?)
            ON CONFLICT(sensor_id) DO UPDATE SET name = excluded.name
            """,
            (sensor_id, name),
        )
    return True
