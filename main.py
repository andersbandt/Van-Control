
# @file     my_dht_11_lcd.py
# @desc     a first attempt at making a smart RASPI system 


import sys
import time


# import user created modules
from sensors import dht


# main loop of program
def main():
    while True:
        dht.update_all_dht()
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

    #populate_tables(DATABASE_DIRECTORY)
    return True



# thing that's gotta be here
if __name__ == "__main__":
    status = db_init()  # only used if database doesn't exist
    if not status:
        print("Something went wrong with database. EXITING!")
        sys.exit()

    main()

