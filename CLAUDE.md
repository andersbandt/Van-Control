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
  - `/` - Home page (current temp per sensor, via `/current_temps`)
  - `/data.html` - Temperature/humidity charts (supports AJAX updates), statistics table, and the daily-trends chart
  - `/battery.html` - Battery status display; shows an offline banner instead of erroring when no VE.Direct data has been received yet (`connected: false` from `db/helpers/battery.py:get_battery_data()`)
  - `/settings.html` - Sensor rename UI
  - `/control.html` / `/automate.html` - **Leftover from a previous "Hidden Hydroponics" project.** Titles, button labels, and JS all reference that domain (pH/EC/TDS, air/water/light relays) and call endpoints (`/airOn`, `/readpH`, etc.) that don't exist in `routes.py`. Still linked from the navbar. Not wired to any of this project's hardware — treat as dead code, not a spec for van control features.
  - `/stats` - API endpoint for sensor statistics (high/low/mean/stddev/range) over either a sample-count window or an explicit date range
  - `/daily_trends` - Binned temperature trends (high/low/mean) over an arbitrary `start_date`/`end_date`, grouped into `bin_days`-sized buckets (see `db/helpers/sensors.py:get_binned_stats`)
  - `/current_temps` - Latest reading per sensor, with display name from `sensor_config`
  - `/sensor_names` - GET returns `{sensor_id: name}`; POST `{sensor_id, name}` renames a sensor (persisted in the `sensor_config` table, UI on `/settings.html`)

**Frontend:**
- Templates in `vf/templates/`
- Static assets in `vf/static/` including `chart.js` for data visualization
- Charts use aligned data from multiple sensors via `analysis/data_helper.py`

### Database Layer - `db/`
SQLite database (`db/financials.db`) with helper modules:

**Schema:**
- `sensor_data` - DHT22 readings (sensor_id, temperature, humidity, timestamp)
- `battery_data` - VE.Direct readings (label, value, timestamp)
- `sensor_config` - User-editable display name per `sensor_id` (defaults to Internal/Living Room/Bedroom if no row exists)

**Helper modules:**
- `db/__init__.py` - Table creation via `TableStatements` class
- `db/helpers/sensors.py` - Sensor data insertion/retrieval with statistics, including `get_binned_stats()` for the arbitrary-range/bin-size trends chart
- `db/helpers/battery.py` - Battery data operations
- `db/helpers/sensor_config.py` - Get/set sensor display names (`get_sensor_names()`, `set_sensor_name()`)

**`config.py`** (repo root) holds shared constants: `NUM_SENSORS` (currently 3) and `PRIMARY_SENSOR` (the alignment reference used in `analysis/data_helper.py`). Import from here rather than hardcoding the sensor count elsewhere.

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
Note: `requirements.txt` currently only lists `adafruit-blinka`, `adafruit-circuitpython-dht`, and `rpi.gpio`. It's missing `flask` (all of `vf/`), `pyserial` (`vc/vedirect.py`), `smbus` (LCD + `vc/ds1307.py`), and `gpiozero` (`vc/rain.py`) — a fresh install from this file alone won't actually run either service yet.

## Important Notes

### Hardcoded values (tagged with `tag:HARDCODE`)
- Sensor calibration offsets in `vc/dht.py` (lines 28-33)
- Temperature bounds checking (-45°C to 85°C) in `vc/dht.py`
- Number of sensors and the primary/alignment sensor index are centralized in `config.py` (`NUM_SENSORS`, `PRIMARY_SENSOR`) — use these instead of hardcoding `3`/`2` in new code

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

### New tables require a `vc.service` restart
`sensor_config` (and any future table added to `TableStatements`) is only created via `db_init()` in `main_vc.py`, which runs on process start. `main_vf.py` never calls it. After adding a table, restart `vc.service` before the corresponding `vf` route/feature will work — `main_vf.py` alone won't create it.

### Known issues (not yet fixed)
- `main_vf.py` runs Flask with `debug=True` bound to `0.0.0.0:80`, as root. The Werkzeug interactive debugger is a remote-code-execution risk if this is ever reachable beyond localhost — worth turning off `debug` (or at least binding to a non-public interface) before exposing this past a trusted home network.
- `vc/gpio.py`: `PINS["relay"]` assigns the same GPIO pin to `relay_2`/`relay_3` (both 15) and `relay_6`/`relay_7` (both 24) — looks like a copy-paste typo, not an intentional shared pin.
- `vc/gpio.py`: `fan_lift_dpdt` is assigned GPIO 1, which is normally reserved for the HAT ID EEPROM (ID_SD) on a Pi.
- `vc/relay.py:all_relays_off()` calls `gpio.out(...)`, which doesn't exist (should be `gpio.gpio_out`) — will raise `AttributeError` if ever called.
