

# import needed modules
import time


# import user created modules
import vc.fan
from vc import gpio
from vc.gpio import PINS



def parse_button(btn_num):
    # TODO: need to finish code here to take my btn_num and get the proper mux output going

    
    # now that mux is setup properly, can sample button input
    state = gpio.gpio_read(PINS["button_in"]) # HIGH = not pressed, LOW = press

    # return state
    return not state


                    
def action(btn_num):
    """Perform an action based on button press."""
    if btn_num == 1:
        vc.fan.forward(10)
    elif btn_num == 2:
        vc.fan.backward(10)
    elif btn_num == 3:
        print("Button 3 action triggered")  # Placeholder
    elif btn_num == 4:
        print("Button 4 action triggered")  # Placeholder
    # Add more cases up to button 18
    else:
        print(f"Unknown button: {btn_num}")

                     
# # Interrupt-based event handling (optional)
# def button_callback(channel):
#     """Interrupt handler for button presses."""
#     for btn_num, pin in BUTTONS.items():
#         if pin == channel and parse_button(btn_num) == 0:  # If button is pressed
#             action(btn_num)
#             break

# # Attach event detection to buttons
# for pin in BUTTONS.values():
#     GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)





