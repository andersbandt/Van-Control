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

# Store last valid readings for outlier detection
# Format: {sensor_index: {'temperature': float, 'humidity': float}}
last_valid_readings = {}

# Outlier detection thresholds - tag:HARDCODE
MAX_TEMP_CHANGE = 10.0  # Maximum degrees C change per reading cycle
MAX_HUMIDITY_CHANGE = 20.0  # Maximum % humidity change per reading cycle


def is_valid_reading(sensor_index, temperature, humidity):
    """
    Check if a sensor reading is valid by comparing rate of change
    against the last valid reading for this sensor.

    Returns: (is_valid: bool, reason: str)
    """
    # First reading for this sensor is always considered valid
    if sensor_index not in last_valid_readings:
        return True, "First reading"

    last_temp = last_valid_readings[sensor_index]['temperature']
    last_humidity = last_valid_readings[sensor_index]['humidity']

    temp_change = abs(temperature - last_temp)
    humidity_change = abs(humidity - last_humidity)

    # Check temperature change
    if temp_change > MAX_TEMP_CHANGE:
        return False, f"Temperature spike: {temp_change:.1f}°C change (limit: {MAX_TEMP_CHANGE}°C)"

    # Check humidity change
    if humidity_change > MAX_HUMIDITY_CHANGE:
        return False, f"Humidity spike: {humidity_change:.1f}% change (limit: {MAX_HUMIDITY_CHANGE}%)"

    return True, "Valid"


def check_dht(sensor_index):
    dht_device = dht_device_list[sensor_index]

    try:
        temperature_c = dht_device.temperature        
        humidity = dht_device.humidity

        # add some calibration constant -- tag:HARDCODE
        if sensor_index == 0:
            temperature_c = temperature_c + 1.34
            humidity = humidity - 11.4490
        elif sensor_index == 1:
            temperature_c = temperature_c - 0.5163
            humidity = humidity - 3.0096

        # TODO: make this dynamic based on wifi connection
        # METHOD1: using systime which MAY BE INACCURATE if we lose wifi connection
        timestamp = datetime.datetime.now()

        # METHOD2: using external RTC (DS1307)
        #ds1307rtc = ds1307.DS1307(i2c_bus_number=1, addr=0x68) # TODO; is turning this into an object really the best way to do this? Should I just make one instance and make that callable in a module?
        #timestamp = ds1307rtc.datetime
        
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

            # add some hard coded bounds to handle erroneous readings
            if -45 < sensor_event.temperature < 85:
                # Check for outliers using rate-of-change validation
                is_valid, reason = is_valid_reading(i, sensor_event.temperature, sensor_event.humidity)

                if is_valid:
                    # Update last valid reading
                    last_valid_readings[i] = {
                        'temperature': sensor_event.temperature,
                        'humidity': sensor_event.humidity
                    }
                    # handle logging to database
                    dbh.sensors.insert_reading(sensor_event)
                else:
                    # Outlier detected - skip and log warning
                    print(f"WARNING: Outlier detected for sensor #{i}: {reason}")
                    print(f"  Rejected: T={sensor_event.temperature:.1f}°C, H={sensor_event.humidity:.1f}%")
                    if i in last_valid_readings:
                        print(f"  Previous: T={last_valid_readings[i]['temperature']:.1f}°C, H={last_valid_readings[i]['humidity']:.1f}%")
        else:
            print(f"ERROR: can't read from sensor #{i}")
            
