

from db import DATABASE_DIRECTORY
import sqlite3

# Function to query the database
def get_data():
            conn = sqlite3.connect(DATABASE_DIRECTORY)
            cursor = conn.cursor()

            # Query to get the latest temperature and humidity data
            cursor.execute("SELECT sensor_id, temperature, humidity, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
            
            data = cursor.fetchall()
            conn.close()
            return data
