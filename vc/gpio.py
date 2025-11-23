


# import needed modules
import RPi.GPIO as GPIO
import board


# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)


# Dictionary to store all pin assignments
PINS = {
    # Sensors
    "rain_sensor": 4,  # Example GPIO pin for a rain sensor

    # 3 x 2 PIN CONNECTORS
    "reed_1": 17,
    "reed_2": 27,
    "reed_3": 22,
    
    # ??? currently extra 
    "ex1": 10,
    "ex2": 9,
    "ex3": 11,
    "ex4": 0,
    "ex5": 5,
    "ex6": 6,

    # 3 x 3 PIN CONNECTOR = dht temp/humidity sensors
    "dht_device1": board.D13,
    "dht_device2": board.D19,
    "dht_device3": board.D26,

    # buzzer
    "buzzer": 8,
    
    # ??? PIN CONNECTOR = button input
    # pins controlling mux module
    "button_in": 21,

    # I2C Pins (Raspberry Pi default)
    "i2c_sda": board.SDA,  # GPIO 2 (BCM)
    "i2c_scl": board.SCL,  # GPIO 3 (BCM)

    
    # 8 PIN CONNECTOR = relays
    "relay": {
        "relay_1": 14, # aux lighting for electrical module
        "relay_2": 15,    
        "relay_3": 15, # aux lighting for urinal
        "relay_4": 18, # lift motor power
        "relay_5": 23,
        "relay_6": 24,
        "relay_7": 24,
        "relay_8": 8,
    },

    
    # 4 PIN CONNECTOR
    # Lift motor relay, 3 decoder pins for maxaiir roof fan control
    "fan_lift_dpdt": 1,  # Changed from 26 to avoid conflict with DHT sensor
    "fan_c1": 12,
    "fan_c2": 16,
    "fan_c3": 20,
}


### DEFINE SUB PIN LISTS
# relay pins
# PINS["relay_pins"] = list(PINS["relays"].values())
RELAY_PINS = list(PINS["relay"].values())


# button pins
# BUTTONS = {
#     1: PINS["button_1"],
#     2: PINS["button_2"],
#     3: 9,  4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15,
#     10: 16, 11: 17, 12: 18, 13: 19, 14: 20, 15: 21, 16: 22, 17: 23, 18: 24
# }


### SET UP INITIAL PIN STATES
# inputs
GPIO.setup(PINS["button_in"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS["reed_1"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS["reed_2"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS["reed_3"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# outputs
GPIO.setup(PINS["buzzer"], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PINS["fan_lift_dpdt"], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PINS["fan_c1"], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PINS["fan_c2"], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PINS["fan_c3"], GPIO.OUT, initial=GPIO.LOW)

for pin in RELAY_PINS:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)


#### METHODS
def gpio_out(pin, state):
	GPIO.output(pin, state)    


def gpio_read(pin):
    state = GPIO.input(pin)
    return state
    


# decoder_out: takes in a number of output and toggles the needed GPIO pins to the correct binary state
def decoder_out(num):
    if not (0 <= num <= 7):
        raise ValueError("3x8 decoder currently set (input should be between 0 and 7)")

    binary_values = [(num >> i) & 1 for i in range(3)] # LSB first

    for pin, state in zip([PINS["fan_c1"], PINS["fan_c2"], PINS["fan_c3"]], binary_values):
        gpio_out(pin, state)


def gpio_clean():    
    GPIO.cleanup()  # Reset GPIO settings on exit
        
