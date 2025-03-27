

# import driver modules
from vc.display import I2C_LCD_driver



### NOTES:
#    I'm using the LCM1602 I2C LCD module
#    this thing has room for 16x2 characters (16 characters per row, 2 characters)
#    VCC voltage is 5V
#    I2C address: 0x27 (default, can vary)



# TODO: is this the best way to manage this class?
# initialize LCD object we will be using
mylcd = I2C_LCD_driver.lcd()


if mylcd.status:
    mylcd.lcd_clear()
    mylcd.backlight(1)


def return_lcd():
    return mylcd


def display_out(string, line):
    if mylcd.status:
        mylcd.lcd_display_string(string, line=line, pos=0)
    else:
        print(f"LCD not active --> {string}")


##########################################################
### custom display functions
##########################################################
def display_bat_out(soc, voltage, current):
    mylcd.lcd_display_string(f"{current} A  {voltage} V")
    mylcd.lcd_display_string(f"SOC: {soc} %", line=2)



def display_temp_out(string, temp, humidity, timestamp):
    mylcd.lcd_display_string(f"Area: {string}= {temp} F / {humidity} RH")
    mylcd.lcd_display_string(f"{timestamp}", line=2)

        
# TODO: add generic function to display a dict with keys?


