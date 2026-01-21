# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Van-Control is a Raspberry Pi-based "smart van" environmental control system. The system collects sensor data (temperature, humidity, battery metrics), stores it in SQLite, and provides a web interface for monitoring and control.

## Architecture

The codebase is split into two main subsystems that run as separate systemd services:

### Van Control (VC) - `main_vc.py` / `vc.service`
The data collection and control subsystem. Runs as user `anders`.

**Main loop responsibilities:**
1. Poll DHT22 sensors (temperature/humidity) via `dht.update_all_dht()`
2. Read battery data from Victron BMV-712 via VE.Direct serial protocol (`vedirect.py`)
3. Monitor control panel buttons (currently commented out)
4. Update LCD display with current readings

**Key modules in `vc/`:**
- `dht.py` - DHT22 sensor interface with hardcoded calibration offsets for sensors 0 and 1
- `vedirect.py` - VE.Direct protocol parser for Victron battery monitor (auto-connects to USB VID:PID 0x10C4:0xEA60)
- `display/display_control.py` - I2C LCD driver interface
- `vc_driver.py` - Button/control panel handling (work in progress)
- `classes/SensorEvent.py` - Data structure for sensor readings
- `gpio.py` - GPIO pin mappings stored in `PINS` dictionary

### Van Flask (VF) - `main_vf.py` / `vf.service`
Web interface for data visualization and control. Runs as `root` on port 80.

**Flask app structure:**
- `vf/app.py` - Flask app factory with logging to `app.log`
- `vf/routes.py` - All routes defined in a Blueprint
  - `/` - Home page
  - `/data.html` - Temperature/humidity charts (supports AJAX updates)
  - `/battery.html` - Battery status display
  - `/control.html` - Control interface (placeholder)
  - `/stats` - API endpoint for sensor statistics

**Frontend:**
- Templates in `vf/templates/`
- Static assets in `vf/static/` including `chart.js` for data visualization
- Charts use aligned data from multiple sensors via `analysis/data_helper.py`

### Database Layer - `db/`
SQLite database (`db/financials.db`) with helper modules:

**Schema:**
- `sensor_data` - DHT22 readings (sensor_id, temperature, humidity, timestamp)
- `battery_data` - VE.Direct readings (label, value, timestamp)

**Helper modules:**
- `db/__init__.py` - Table creation via `TableStatements` class
- `db/helpers/sensors.py` - Sensor data insertion/retrieval with statistics
- `db/helpers/battery.py` - Battery data operations

### Data Processing - `analysis/`
- `data_helper.py` - `align_data()` function synchronizes timestamps across multiple sensors using binary search for nearest-neighbor matching. The `retrieve_aligned_data()` function fetches data for 3 hardcoded sensors and optionally converts to Fahrenheit.

## Hardware Dependencies

This codebase is designed for Raspberry Pi with:
- 3x DHT22 sensors (temperature/humidity) on GPIO pins defined in `vc/gpio.py`
- I2C LCD display
- Victron BMV-712 battery monitor via USB serial (VE.Direct protocol)
- DS1307 RTC module (optional, currently not in use - see commented code in `dht.py`)

## Common Commands

### Running the services manually
```bash
# Data collection service
python main_vc.py

# Web interface (requires root for port 80)
sudo python main_vf.py
```

### Managing systemd services
```bash
# Start/stop/restart services
sudo systemctl start vc.service
sudo systemctl start vf.service
sudo systemctl restart vc.service
sudo systemctl restart vf.service

# View service status and logs
sudo systemctl status vc.service
sudo systemctl status vf.service
sudo journalctl -u vc.service -f
sudo journalctl -u vf.service -f
```

### Database initialization
Database is auto-created on first run of `main_vc.py`. Manual initialization:
```python
from db import DATABASE_DIRECTORY, TableStatements, all_tables_init
statements = [TableStatements.sensor_data, TableStatements.battery_data]
all_tables_init(statements, DATABASE_DIRECTORY)
```

### Installing dependencies
```bash
pip install -r requirements.txt
```

## Important Notes

### Hardcoded values (tagged with `tag:HARDCODE`)
- Sensor calibration offsets in `vc/dht.py` (lines 28-33)
- Number of sensors (3) in multiple locations
- Primary sensor index (2) in `analysis/data_helper.py`
- Temperature bounds checking (-45°C to 85°C) in `vc/dht.py`

### Timestamp handling
- Currently uses system time via `datetime.datetime.now()`
- DS1307 RTC module code exists but is commented out
- Comment in `dht.py` notes concern about wifi-dependent system time accuracy

### Database path
The database file is located at `db/financials.db` (note: name inherited from previous project). This is defined in `db/__init__.py` as `DATABASE_DIRECTORY`.

### Sensor data flow
1. `vc/dht.py` reads sensors → creates `SensorEvent` objects
2. `db/helpers/sensors.py` inserts readings into database
3. `analysis/data_helper.py` retrieves and aligns data from multiple sensors
4. `vf/routes.py` serves data to web interface via AJAX or template rendering

### VE.Direct battery monitoring
The `Vedirect` class implements a state machine parser for the VE.Direct text protocol. It auto-discovers the USB serial device and parses key-value pairs from the battery monitor, saving all labels to the database.

### Control panel (incomplete)
Button handling in `vc_driver.py` is partially implemented. The main loop in `main_vc.py` has button polling commented out (lines 34-37).
