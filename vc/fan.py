

# import needed modules
import time


# import user created modules
from vc import relay
from vc import gpio
from vc.gpio import PINS


# define pins for motor control
power_pin = "relay_3" # tag:HARDCODE
dir_pin = "fan_lift_dpdt" # tag:HARDCODE



### BUTTON EMULATION - DECODER TO SSR RELAY BOARD FUNCTIONS
def fan_power():
    gpio.decoder_out(1)
    time.sleep(0.1)
    gpio.decoder_out(0)

def fan_in_out():
    gpio.decoder_out(2)
    time.sleep(0.1)
    gpio.decoder_out(0)

    
def fan_auto():
    gpio.decoder_out(3)
    time.sleep(0.1)
    gpio.decoder_out(0)


def fan_up():
    gpio.decoder_out(4)
    time.sleep(0.1)
    gpio.decoder_out(0)


def fan_down():
    gpio.decoder_out(5)
    time.sleep(0.1)
    gpio.decoder_out(0)



#########################################################
### LIFT MOTOR CONTROL FUNCTIONS
#########################################################
def lift_power(state):
    if state:
        relay.relay_on(PINS["relay"][power_pin])
    else:
        relay.relay_off(PINS["relay"][power_pin])


        
def forward(delay):
    # adjust settings to forward
    gpio.gpio_out(PINS[dir_pin], 0)
    time.sleep(0.1)
    

    # apply power for time period
    lift_power(1)
    time.sleep(delay)
    lift_power(0)

    # disable settings
    gpio.gpio_out(PINS[dir_pin], 1)
    time.sleep(0.1)


def backward(delay):
    # adjust backward settings
    gpio.gpio_out(PINS[dir_pin], 0)
    time.sleep(0.1)

    # apply power for time period
    lift_power(1)
    time.sleep(delay)
    lift_power(0)

    # disable settings
    gpio.gpio_out(PINS[dir_pin], 1)
    time.sleep(0.1)


# TODO: what is this actually doing
def cleanup():
    GPIO.cleanup()
    
