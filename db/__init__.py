# @file db/__init__/.py
# @desc table initializer for my SQLite3 tables. Base code inherited from Financial-Analyzer project


# import needed modules
import sqlite3

# setup database master file
DATABASE_DIRECTORY = "db/financials.db"


class TableStatements:
    """
    A class for holding the SQL statements.
    """
    # Temperature and Humidity Table
    sensor_data = """CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sensor_id INTEGER NOT NULL,        -- ID of the sensor (could be unique for each sensor)
                        temperature REAL,         -- Temperature in Celsius
                        humidity REAL,            -- Humidity percentage
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );"""

    # Battery Data Table (BMV-712)
    battery_data = """CREATE TABLE IF NOT EXISTS battery_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        label VARCHAR(10),
                        value REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );"""


"""
Create all the tables. It uses a list instead
of importing the TableStatements class for
dependency injection reasons.
"""


def all_tables_init(statements: list, database_directory: str) -> bool:
    print("Initializing all tables in database .db file!!! Exciting!!!")
    try:
        with sqlite3.connect(database_directory) as conn:
            conn.set_trace_callback(print)
            cursor = conn.cursor()
            for statement in statements:
                try:
                    cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    print(e)
            conn.set_trace_callback(None)
    except sqlite3.OperationalError as e:
        print(f"\n{e}")
        print(f"Yikes, couldn't open your database file")
        print(f"\n\n##########################################################")
        print(f"\n\tYour path is currently \n\t{database_directory}. ")
        print(f"\n##########################################################")
        print(f"\nPlease review filepath and make any needed adjustments in src/db/__init__.py. Around line 6 ish\n\n")
        return False
    print("\n\n")
    return True


def populate_tables(database_directory: str):
    sensors_statement = """
        insert into `sensors` (`account_id`, `name`, `type`) values (2000000001, 'U.S. Bank', 1);
        insert into `sensors` (`account_id`, `name`, `type`) values (2000000002, 'WELLS CHECKING', 2);
    """

    # alter_statement = """
    #     ALTER TABLE account ADD COLUMN retirement BOOLEAN;
    # """

    statements = [sensors_statement]
    with sqlite3.connect(database_directory) as conn:
        conn.set_trace_callback(print)
        cursor = conn.cursor()
        for statement in statements:
            try:
                cursor.executescript(statement)
            except sqlite3.IntegrityError as e:
                print(e)
        conn.set_trace_callback(None)
