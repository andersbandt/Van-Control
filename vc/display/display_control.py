

from display.drivers import I2C_LCD_driver



mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()
mylcd.backlight(1)


def return_lcd():
    return mylcd





def display_out(string):
    mylcd.lcd_display_string(string)


# TODO: add generic function to display a dict with keys?


