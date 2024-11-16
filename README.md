# Van-Control
This repo is for creating a "smart" van environment control system, optimizing living in a van

## project goals
The goal of this project is to create some sort of control system for my van. A "smart van", if you will.
Mainly this will be executed on a Raspberry Pi system.

I think the aspects of control at a high-level will include

- sensor data capture and display
- various monitoring systems with alarms
- various control systems with input/output
  - example: rain sensor auto-closing roof vent


## directory structure
There are a couple key folders to keep in mind in this project

- `vc`
  - "van control"
  - This holds most of the modules for interfacing with things like sensors
  - Main goal for the sensors is to put data into the database
  - Other scripts will monitor for interface control (buttons, switches, etc)
- `vf`
  - "van flask"
  - This holds all the web interface code
- `db`
  - holds the database file itself `.db`
  - also holds `__init__.py` for creating your `.db` file
  - Helper functions for interfacing with the database