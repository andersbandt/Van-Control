
# @file     my_dht_11_lcd.py
# @desc     a first attempt at making a smart RASPI system 

import time
import adafruit_dht
import board


dht_device1 = adafruit_dht.DHT11(board.D21, use_pulseio=False)
dht_device2 = adafruit_dht.DHT22(board.D20, use_pulseio=False)


dht_device_list = [dht_device1, dht_device2]


import I2C_LCD_driver
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()
mylcd.backlight(1)



    # update temperature and humidity
while True:
    num = 0
    for dht_device in dht_device_list:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32            
            humidity = dht_device.humidity
        except RuntimeError as err:
            temperature_c = 0
            temperature_f = 0
            humidity = 0
            
        # perform data conversion
        #temperature_f = round(temperature_f, 2)
            
        print(f"TEMP C: {temperature_c}")
        print(f"TEMP F: {temperature_f}")
        print(f"HUM   : {humidity}")
        print("\n")
        
        # print out on LCD
        mylcd.lcd_clear()
        mylcd.lcd_display_string(f"TMP {temperature_f:.1f}F {temperature_c:.1f}C", 1)
        mylcd.lcd_display_string(f"HUM: {humidity:.1f}%  #{num}", 2)
        
        # add some delay
        time.sleep(4)
        num += 1
            
    
            
            
