

# import needed modules
import sqlite3
import datetime

# import database path
# from db import DATABASE_DIRECTORY

# import user created modules
from classes.SensorEvent import SensorEvent


def insert_reading(sensor_event: SensorEvent) -> bool:
    with sqlite3.connect(DATABASE_DIRECTORY) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (date, account_id, category_id, amount, description, note, date_added) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (
                sensor_event.
                transaction.account_id,
                transaction.category_id,
                transaction.amount,
                transaction.description,
                transaction.note,
                datetime.datetime.now(),
            ),
        )
        conn.set_trace_callback(None)
    return True






