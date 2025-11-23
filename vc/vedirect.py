# -*- coding: utf-8 -*-

# import user defined modules
import serial
from serial.tools import list_ports
import datetime

# import user created modules
import db.helpers as dbh


def autoconnect_serial(target_vid, target_pid):
    ports = list_ports.comports()

    for port in ports:
        if port.vid == target_vid and port.pid == target_pid:
            return port.device

    print("Target device not found.")
    return None


class Vedirect:
    # VID and PID for the Silicon Labs CP210x USB to UART Bridge
    vid = 0x10C4
    pid = 0xEA60

    
    def __init__(self, port=None, timeout=3):
        # establish port
        if port is None:
            self.serialport = autoconnect_serial(self.vid, self.pid)
        else:
            self.serialport = port

        # connect to serial port
        if self.serialport is not None:
            self.ser = serial.Serial(self.serialport, 19200, timeout=timeout)
            print(f"VE.Direct connected at port {self.serialport} with a timeout of {timeout}\n")
        else:
            print("Connect sequence for VE.Direct FAILED")
            self.ser = None

        # setup various other things
        self.header1 = ord('\r')
        self.header2 = ord('\n')
        self.hexmarker = ord(':')
        self.delimiter = ord('\t')
        self.key = ''
        self.value = ''
        self.bytes_sum = 0
        self.state = self.WAIT_HEADER
        self.dict = {}

    (HEX, WAIT_HEADER, IN_KEY, IN_VALUE, IN_CHECKSUM) = range(5)

    def input(self, byte):
        if byte == self.hexmarker and self.state != self.IN_CHECKSUM:
            self.state = self.HEX

        if self.state == self.WAIT_HEADER:
            self.bytes_sum += byte
            if byte == self.header1:
                self.state = self.WAIT_HEADER
            elif byte == self.header2:
                self.state = self.IN_KEY

            return None
        elif self.state == self.IN_KEY:
            self.bytes_sum += byte
            if byte == self.delimiter:
                if self.key == 'Checksum':
                    self.state = self.IN_CHECKSUM
                else:
                    self.state = self.IN_VALUE
            else:
                self.key += chr(byte)
            return None
        elif self.state == self.IN_VALUE:
            self.bytes_sum += byte
            if byte == self.header1:
                self.state = self.WAIT_HEADER
                self.dict[self.key] = self.value;
                self.key = '';
                self.value = '';
            else:
                self.value += chr(byte)
            return None
        elif self.state == self.IN_CHECKSUM:
            self.bytes_sum += byte
            self.key = ''
            self.value = ''
            self.state = self.WAIT_HEADER
            if self.bytes_sum % 256 == 0:
                self.bytes_sum = 0
                return self.dict
            else:
                self.bytes_sum = 0
        elif self.state == self.HEX:
            self.bytes_sum = 0
            if byte == self.header2:
                self.state = self.WAIT_HEADER
        else:
            raise AssertionError()

    # read_data_single: returns a single dict with a reading sample
    def read_data_single(self):
        if self.ser is not None:
            self.ser.flush()
        # perform read
            data = self.ser.read_until('\n')
            for single_byte in data:
                packet = self.input(single_byte)
                if packet is not None:
                    return packet
        else:
            print("Can't read data ve.direct data. No serial connection.")
            return None
                    

    ## read_data_callback: performs `callback` on the read sample
    # def read_data_callback(self, callback):
    #     data = self.ser.read()
    #     for byte in data:
    #         packet = self.input(byte)
    #         if packet is not None:
    #             callback(packet)

    def save_data_single(self):
        packet = self.read_data_single()

        if packet is not None:
            timestamp = datetime.datetime.now()
            for label in packet:
                dbh.battery.insert_reading(
                    label,
                    packet[label],
                    timestamp
                )
            print("... BMV-712 packet saved")
        else:
            print("ERROR: issue with ve.direct saving")


    def flush_port(self):
        self.ser.flush()
