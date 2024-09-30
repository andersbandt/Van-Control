

from display.drivers import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()
mylcd.backlight(1)

