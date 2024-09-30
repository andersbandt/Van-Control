






class SensorEvent:
    def __init__(self, sensor_id, temperature, humidity, timestamp):
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp


    def print(self):
        print(f"ID    : {self.sensor_id}")
        print(f"TEMP C: {self.temperature}")
        temperature_f = self.temperature * (9 / 5) + 32
        print(f"TEMP F: {temperature_f}")
        print(f"HUM   : {self.humidity}")
        print("\n")


