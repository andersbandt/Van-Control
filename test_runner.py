

import glob
import pprint
import time

from vc import fan
# from vc import gpio
from vc.vedirect import Vedirect
from vc.display import display_control as dispc


# get available serial ports (for Linux only)
ports = glob.glob('/dev/tty[A-Za-z]*')
print("Hey your available ports are below!")
print(ports)


ve = Vedirect(port=None, timeout=10)


def print_data_callback(packet):
    pprint.pprint(packet)


while True:
    # test ve.direct from BMV-712
    print("\n\nTESTING: ve.direct for BMV-712")
    time.sleep(1)
    ve.save_data_single()
    time.sleep(5)


    # test LCD
    print("\n\nTESTING: LCD")
    time.sleep(1)
    dispc.display_out("testing123")
    time.sleep(5)


    # TEST MAXXAIR ROOF FAN
    print("\n\nTESTING: MAXAIIR ROOF VAN CONTROL")
    time.sleep(1)

    print("\n... testing button control ...")
    fan.fan_power()
    time.sleep(1)
    fan.fan_in_out()
    time.sleep(1)
    fan.fan_auto()
    time.sleep(1)
    fan.fan_up()
    time.sleep(1)
    fan.fan_down()

    print("\n... testing lift motor control")
    print("... fan UP ...")
    fan.forward(1)
    print("... fan DOWN")
    fan.backward(1)


    
