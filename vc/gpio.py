import RPi.GPIO as GPIO



# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)





# This is the GPIO pin number we have one of the door sensor
# wires attached to, the other should be attached to a ground 
pin.DOOR_SENSOR_PIN = 18

#Set up the door sensor pi
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)



while True: 
    oldIsOpen = isOpen 
    isOpen = GPIO.input(DOOR_SENSOR_PIN)  
    if (isOpen and (isOpen != oldIsOpen)):  
        print "Door has opened!"  
        sendemail(me, to, message, login, password, smptserver)
    elif (isOpen != oldIsOpen):  
        print "Door has closed"  
        GPIO.output(GREEN_LIGHT, False)  
        GPIO.output(RED_LIGHT, True)  
    time.sleep(0.1)




# sets a certain relay off by setting the output pin high
def relayOff(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 1)

# sets a certain relay on by setting the output low
def relayOn(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)

    
