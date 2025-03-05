

# Import needed modules
import RPi.GPIO as GPIO
import time

import vc.motor.motor  # Import motor module
from vc import *  # Import other control modules if needed

# Define button GPIO pins
BUTTONS = {
    1: 7,  2: 8,  3: 9,  4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15,
    10: 16, 11: 17, 12: 18, 13: 19, 14: 20, 15: 21, 16: 22, 17: 23, 18: 24
}

# GPIO setup
GPIO.setmode(GPIO.BCM)
for pin in BUTTONS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistors

def parse_button(btn_num):
    """Check if a button is pressed and return its state."""
    return GPIO.input(BUTTONS[btn_num])  # HIGH = not pressed, LOW = pressed

def action(btn_num):
    """Perform an action based on button press."""
    if btn_num == 1:
        vc.motor.motor.forward(10)
    elif btn_num == 2:
        vc.motor.motor.backward(10)
    elif btn_num == 3:
        print("Button 3 action triggered")  # Placeholder
    elif btn_num == 4:
        print("Button 4 action triggered")  # Placeholder
    # Add more cases up to button 18
    else:
        print(f"Unknown button: {btn_num}")

# Interrupt-based event handling (optional)
def button_callback(channel):
    """Interrupt handler for button presses."""
    for btn_num, pin in BUTTONS.items():
        if pin == channel and parse_button(btn_num) == GPIO.LOW:  # If button is pressed
            action(btn_num)
            break

# Attach event detection to buttons
for pin in BUTTONS.values():
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("Waiting for button presses...")
    while True:
        time.sleep(0.1)  # Keep the program running

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    GPIO.cleanup()  # Reset GPIO settings on exit


