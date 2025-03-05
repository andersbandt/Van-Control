

# import needed modules
import RPi.GPIO as GPIO
import time
from vc.electrical import relay

on_relay_num = 8


# set up pins needed
F_RELAY = 20
B_RELAY = 20

# set up everything as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(F_RELAY, GPIO.OUT)
GPIO.setup(B_RELAY, GPIO.OUT)


def power(state):
    if state:
        relay.relay_on(on_relay_num)
    else:
        relay.relay_off(on_relay_num)


def forward(delay):
    # adjust settings to forward
    GPIO.output(F_RELAY, GPIO.HIGH)

    # apply power for time period
    power(1)
    time.sleep(delay)
    power(0)

    # disable settings
    GPIO.output(F_RELAY, GPIO.LOW)


def backward(delay):
    # adjust backward settings
    GPIO.output(B_RELAY, GPIO.HIGH)

    # apply power for time period
    power(1)
    time.sleep(delay)
    power(0)

    # disable settings
    GPIO.output(B_RELAY, GPIO.LOW)


# TODO: what is this actually doing
def cleanup():
    GPIO.cleanup()
    