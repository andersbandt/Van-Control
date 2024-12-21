

import glob
import pprint
import time

from vc.electrical.vedirect import Vedirect


# get available serial ports (for Linux only)
ports = glob.glob('/dev/tty[A-Za-z]*')
print("Hey your available ports are below!")
print(ports)


# ve = Vedirect(port=ports[1], timeout=10)
ve = Vedirect(port=None, timeout=10)

def print_data_callback(packet):
    pprint.pprint(packet)


while True:
    ve.save_data_single()
    time.sleep(5)
