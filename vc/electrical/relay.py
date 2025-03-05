

import RPi.GPIO as GPIO
import time

# Define relay pins
RELAY_1 = 18
RELAY_2 = 19
RELAY_3 = 20
RELAY_4 = 21
RELAY_5 = 22
RELAY_6 = 23
RELAY_7 = 24
RELAY_8 = 25

# List of all relay pins
RELAY_PINS = [RELAY_1, RELAY_2, RELAY_3, RELAY_4, RELAY_5, RELAY_6, RELAY_7, RELAY_8]

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PINS, GPIO.OUT, initial=GPIO.LOW)  # Set all relays to OFF initially

def relay_on(num):
    """Turn on a specific relay."""
    if num in RELAY_PINS:
        GPIO.output(num, GPIO.HIGH)
    else:
        print(f"Invalid relay: {num}")

def relay_off(num):
    """Turn off a specific relay."""
    if num in RELAY_PINS:
        GPIO.output(num, GPIO.LOW)
    else:
        print(f"Invalid relay: {num}")

def all_relays_on():
    """Turn on all relays."""
    for pin in RELAY_PINS:
        GPIO.output(pin, GPIO.HIGH)

def all_relays_off():
    """Turn off all relays."""
    for pin in RELAY_PINS:
        GPIO.output(pin, GPIO.LOW)



# try:
#     # Example usage
#     relay_on(RELAY_1)
#     time.sleep(2)
#     relay_off(RELAY_1)
#     time.sleep(2)
#     all_relays_on()
#     time.sleep(2)
#     all_relays_off()
# except KeyboardInterrupt:
#     print("Exiting program.")
# finally:
#     GPIO.cleanup()  # Reset GPIO pins on exit
