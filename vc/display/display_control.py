

# import driver modules
from vc.display import I2C_LCD_driver


### NOTES:
#    I'm using the LCM1602 I2C LCD module
#    this thing has room for 16x2 characters (16 characters per row, 2 characters)
#    VCC voltage is 5V
#    I2C address: 0x27 (default, can vary)

# TODO: add generic function to display a dict with keys?


LCD_WIDTH = 16


class Display:
    def __init__(self):
        self.status = False
        try:
            # SMBus() raises if I2C isn't enabled / bus doesn't exist, before the driver's own try
            self.display = I2C_LCD_driver.lcd()
            self.status = self.display.status
        except OSError as e:
            print(f"Could not open I2C bus for LCD: {e}")

        if self.status:
            print("LCD is good, clearing and turning on backlight")
            self.display.lcd_clear()
            self.display.backlight(1)
        else:
            print("Some issue with initializing LCD")

    def get_status(self):
        return self.status

    def display_out(self, string, line):
        # pad/truncate so a shorter string fully overwrites the previous one
        string = f"{string:<{LCD_WIDTH}}"[:LCD_WIDTH]
        if self.status:
            try:
                self.display.lcd_display_string(string, line=line, pos=0)
            except OSError as e:
                print(f"LCD write failed ({e}) --> {string}")
        else:
            print(f"LCD not active --> {string}")

    def display_bat_out(self, voltage, current, power, consumed_ah):
        self.display_out(f"{voltage}V {current}A", 1)
        self.display_out(f"{power}W {consumed_ah}Ah", 2)

    def display_bat_offline(self):
        self.display_out("Battery", 1)
        self.display_out("  no data yet", 2)

    def display_temp_out(self, name, temp_c, humidity, timestamp):
        temp_f = temp_c * (9 / 5) + 32
        self.display_out(f"{name[:10]:<10}{temp_f:5.1f}F", 1)
        # timestamp is 'YYYY-MM-DD HH:MM:SS...' -> show HH:MM
        self.display_out(f"{humidity:4.1f}%RH    {str(timestamp)[11:16]}", 2)







