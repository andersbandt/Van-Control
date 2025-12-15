

# import driver modules
from vc.display import I2C_LCD_driver


### NOTES:
#    I'm using the LCM1602 I2C LCD module
#    this thing has room for 16x2 characters (16 characters per row, 2 characters)
#    VCC voltage is 5V
#    I2C address: 0x27 (default, can vary)

# TODO: add generic function to display a dict with keys?


class Display:
    def __init__(self):
        self.display = I2C_LCD_driver.lcd()
        if self.display.status:
            print("LCD is good, clearing and turning on backlight")
            mylcd.lcd_clear()
            mylcd.backlight(1)
        else:
            print("Some issue with initializing LCD")

    def get_status(self):
        return self.display.status

    def display_out(self, string, line):
        if self.display.status:
            self.display.lcd_display_string(string, line=line, pos=0)
        else:
            print(f"LCD not active --> {string}")

    def display_bat_out(self, soc, voltage, current):
        self.display_out(
            f"{current} A  {voltage} V",
            1
        )
        self.display_out(
            f"SOC: {soc} %",
            2
        )

    def display_temp_out(self, string, temp, humidity, timestamp):
        self.display_out(
            f"Area: {string}= {temp} F / {humidity} RH",
            1
        )
        self.display_out(
            f"{timestamp}",
            2
        )







