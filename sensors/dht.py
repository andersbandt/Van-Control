
# import needed modules
import adafruit_dht
import board
import datetime

# import user created modules
from classes.SensorEvent import SensorEvent
import db.helpers as dbh


dht_device1 = adafruit_dht.DHT22(board.D13, use_pulseio=False)
dht_device2 = adafruit_dht.DHT11(board.D19, use_pulseio=False)
dht_device3 = adafruit_dht.DHT22(board.D26, use_pulseio=False)

dht_device_list = [dht_device1, dht_device2, dht_device3]


def check_dht(sensor_index):
    dht_device = dht_device_list[sensor_index]

    try:
        temperature_c = dht_device.temperature
        timestamp = datetime.datetime.now()
        humidity = dht_device.humidity
    except RuntimeError:
        return None

    # set up SensorEvent
    event = SensorEvent(sensor_index, temperature_c, humidity, timestamp)
    return event



def update_all_dht():
    for i in range(0, len(dht_device_list)):
        # set up SensorEvent
        sensor_event = check_dht(i)
        if sensor_event is not None:
            sensor_event.print()
            # handle logging to database
            dbh.sensors.insert_reading(sensor_event)
