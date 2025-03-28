# License-Identifier: MIT

"""
DS1307 Real Time Clock driver
=============================

**Notes:**

#1.  the square-wave output facility is not supported by this driver.
#2.  milliseconds are not supported by this RTC.
#3.  alarms and timers are not supported by this RTC.
#4.  datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf

"""

__version__ = "v104"
__repo__ = "https://github.com/peter-l5"


from datetime import datetime
import smbus


# register definitions (see datasheet)
_DATETIME_REGISTER = 0x00
_CONTROL_REGISTER  = 0x07



class DS1307():
    """
    Interface to the DS1307 RTC.

    **Quickstart: Importing and using the device**

            ds1307rtc = ds1307.DS1307(1, 0x68)
            # set time (year, month, day, hours. minutes, seconds, weekday: integer: 0-6 )
            ds1307rtc.datetime = (2022, 12, 18, 18, 9, 17, 6)

            # You can access the current time with the :attr:`datetime` property.
            current_time = ds1307rtc.datetime

            # You can also access the current time with the :attr:`datetimeRTC` property.
            # This returns the time in a format suitable for directly setting the internal RTC clock
            # of the Raspberry Pi Pico (once the RTC module is imported).

        from machine import RTC
        machine.RTC().datetime(ds1307rtc.datetimeRTC)

        The disable oscillator property may be useful to stop the clock when not in use
        to reduce demand on the standby battery.
        
        See also the example code provided.
    """


class DS1307:
    def __init__(self, i2c_bus_number=1, addr=0x68) -> None:
        self.bus = smbus.SMBus(i2c_bus_number)
        self.addr = addr

    @property
    def datetime(self) -> tuple:
        """Returns the current date, time, and day of the week."""
        buf = self.bus.read_i2c_block_data(self.addr, _DATETIME_REGISTER, 7)
        
        hr24 = False if (buf[2] & 0x40) else True
        _datetime = datetime(
            self._bcd2dec(buf[6]) + 2000,  # Year
            self._bcd2dec(buf[5]),  # Month
            self._bcd2dec(buf[4]),  # Day
            self._bcd2dec(buf[2]) if hr24 else
            self._bcd2dec((buf[2] & 0x1F)) + 12 if (buf[2] & 0x20) else 0, # Hours?
            self._bcd2dec(buf[1]),  # Minutes
            self._bcd2dec(buf[0] & 0x7F),  # Seconds (mask oscillator disable flag)
#            buf[3] - 1,  # Day of the week (adjusted index)
#            None  # Unknown number of days since start of year
        )
        return _datetime

    @datetime.setter
    def datetime(self, datetime: tuple = None):
        """Set the current date, time, and day of the week, and start the clock."""
        buf = [
            self._dec2bcd(datetime[5]),  # Seconds
            self._dec2bcd(datetime[4]),  # Minutes
            self._dec2bcd(datetime[3]),  # Hours
            self._dec2bcd(datetime[6] + 1),  # Weekday (0-6)
            self._dec2bcd(datetime[2]),  # Days
            self._dec2bcd(datetime[1]),  # Months
            self._dec2bcd(datetime[0] % 100)  # Years (last two digits)
        ]
        self.bus.write_i2c_block_data(self.addr, _DATETIME_REGISTER, buf)

    @property
    def datetimeRTC(self) -> tuple:
        _dt = self.datetime
        return _dt[0:3] + (None,) + _dt[3:6] + (None,)

    
    def set_datetime_from_sys(self):
        # check if we are connected to the Internet
        import requests
        try:
            requests.get("https://www.google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            print("ERROR: can't set RTC time from sys clock. No internet.")
            return False

        # get system time
        current_time = datetime.now()
        print(f"... current system time is {current_time}")

        # Convert system time to the expected format (YYYY, MM, DD, HH, MM, SS, Weekday)
        rtc_time = (
            current_time.year,
            current_time.month,
            current_time.day,
            current_time.hour,
            current_time.minute,
            current_time.second,
            current_time.weekday()  # Weekday (0 = Monday, 6 = Sunday)
        )

        # Use the existing datetime setter
        self.datetime = rtc_time
        return True
    
        
    @property
    def disable_oscillator(self) -> bool:
        """True if the oscillator is disabled."""
        buf = self.bus.read_byte_data(self.addr, _DATETIME_REGISTER)
        return bool(buf & 0x80)

    @disable_oscillator.setter
    def disable_oscillator(self, value: bool):
        """Set or clear the DS1307 disable oscillator flag."""
        buf = self.bus.read_byte_data(self.addr, _DATETIME_REGISTER)
        buf &= 0x7F  # Preserve seconds
        buf |= (value << 7)
        self.bus.write_byte_data(self.addr, _DATETIME_REGISTER, buf)

    def _bcd2dec(self, bcd):
        """Convert binary-coded decimal to decimal. Works for values from 0 to 99."""
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def _dec2bcd(self, decimal):
        """Convert decimal to binary-coded decimal. Works for values from 0 to 99."""
        return ((decimal // 10) << 4) + (decimal % 10)

