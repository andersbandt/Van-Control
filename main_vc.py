

# @file     my_dht_11_lcd.py
# @desc     a first attempt at making a smart RASPI system 


import sys
import time

# import database
import db.helpers as dbh

# import user created modules
from vc import vc_driver
from vc import dht
from vc.vedirect import Vedirect
from vc.display import display_control as dispc


# main loop of program
def main():
    ve = Vedirect(port=None, timeout=2)
    lcd = dispc.Display()


    while True:
        print("\n")

        # read and log sensor data
        dht.update_all_dht()
        ve.save_data_single()         # TODO: check for disconnect cases to possibly reconnect with things like `ve`

        # check control panel
#        for i in range(1, 19):
#            state = vc_driver.parse_button(i)
#            if state:
#                vc_driver.action(i)

                
        # get battery statistics and update display
        battery_data = dbh.battery.get_battery_data()


        #        dispc.display_bat_out(
#            battery_data['state_of_charge'],
#            battery_data['voltage'],
#            battery_data['current'],
        # )
        # timestamp=battery_data['timestamp']


        # get temperature data and update display
        for i in range(0, 3): # TODO: eliminate this tag:HARDCODE
            data = dbh.sensors.get_data(i, 1)
            lcd.display_temp_out(f"{i}", data[0][1], data[0][2], data[0][0])
            time.sleep(3)
                

        # main loop delay
        # TODO: need a way to bring this delay DOWN but still only log things like DHT sensor samples every 5 seconds ....
        #   the problem also gets complicated when I consider the delays I'm adding for
        time.sleep(5)


def db_init():
    """Create the database using the values of TableStatements."""
    from db import DATABASE_DIRECTORY, TableStatements, all_tables_init, populate_tables

    print("NOTICE: you are currently using ...")
    print(f"\t\t {DATABASE_DIRECTORY}")
    print("... as your database directory!!!\n")

    # append every single variable string in class
    statements = []
    for value in TableStatements.__dict__.values():
        if str(value).startswith(
                "CREATE"
        ):  # Only append the values of the variables. Without this we would get the built-ins and the docstring.
            statements.append(value)

    # execute init sequence
    db_status = all_tables_init(statements, DATABASE_DIRECTORY)
    if not db_status:
        print("I don't think database file was able to be located!!!")
        return False

    # return True if we made it this far
    return True


# thing that's gotta be here
if __name__ == "__main__":
    status = db_init()  # only used if database doesn't exist
    if not status:
        print("Something went wrong with database. EXITING!")
        sys.exit()

    main()
