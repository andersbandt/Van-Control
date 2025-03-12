

# import needed modules
from vc import gpio
from vc.gpio import RELAY_PINS
import time





def relay_on(num):
    """Turn on a specific relay."""
    if num in RELAY_PINS:
        gpio.gpio_out(num, 1)
    else:
        print(f"Invalid relay: {num}")

        
def relay_off(num):
    """Turn off a specific relay."""
    if num in RELAY_PINS:
        gpio.gpio_out(num, 0)
    else:
        print(f"Invalid relay: {num}")

        
def all_relays_on():
    """Turn on all relays."""
    for pin in RELAY_PINS:
        gpio.gpio_out(pin, 1)

def all_relays_off():
    """Turn off all relays."""
    for pin in RELAY_PINS:
        gpio.out(pin, 0)



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
