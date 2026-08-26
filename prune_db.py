#!/usr/bin/env python

# @file     prune_db.py
# @desc     Delete sensor_data / battery_data rows older than N days.
#
#           financials.db has no retention policy -- every DHT and VE.Direct
#           reading accumulates forever. Run this periodically (e.g. daily,
#           see prune-db.service / prune-db.timer for a systemd example) to
#           keep the table sizes -- and the SD card space they take up --
#           bounded.
#
#           Doesn't VACUUM: see db/helpers/sensors.py:prune_old_data() for why.
#
# Usage:
#           python prune_db.py --days 180


import argparse
import datetime

import db.helpers as dbh


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--days", type=int, default=180,
        help="Delete rows older than this many days (default: 180)"
    )
    args = parser.parse_args()

    cutoff = datetime.datetime.now() - datetime.timedelta(days=args.days)
    print(f"Pruning rows older than {cutoff} (retaining {args.days} days)...")

    sensor_deleted = dbh.sensors.prune_old_data(cutoff)
    battery_deleted = dbh.battery.prune_old_data(cutoff)

    print(f"Deleted {sensor_deleted} sensor_data row(s), {battery_deleted} battery_data row(s).")


if __name__ == "__main__":
    main()
