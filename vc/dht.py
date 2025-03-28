# import needed modules
import adafruit_dht
import board
import datetime

# import user created modules
from vc.classes.SensorEvent import SensorEvent
from vc.gpio import PINS
from vc import ds1307
import db.helpers as dbh

dht_device1 = adafruit_dht.DHT22(PINS["dht_device1"], use_pulseio=False)
dht_device2 = adafruit_dht.DHT22(PINS["dht_device2"], use_pulseio=False)
dht_device3 = adafruit_dht.DHT22(PINS["dht_device3"], use_pulseio=False)

dht_device_list = [dht_device1, dht_device2, dht_device3]





def check_dht(sensor_index):
    dht_device = dht_device_list[sensor_index]

    try:
        temperature_c = dht_device.temperature
        #timestamp = datetime.datetime.now()
        ds1307rtc = ds1307.DS1307(i2c_bus_number=1, addr=0x68) # TODO; is turning this into an object really the best way to do this? Should I just make one instance and make that callable in a module?
        timestamp = ds1307rtc.datetime
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
        else:
            print(f"ERROR: can't read from sensor #{i}")
            
