import sys
import time

import serial
from serial.tools.list_ports import comports
from serial.tools.miniterm import Miniterm


class Connection:
    def __init__(self, debug=True):
        self.serial_connection = None
        self.debug = debug


    def get_device(self):
        ports = comports()
        for port in ports:
            try:
                # this is a weak check make sure to only have one USB Serial connected
                # might or might not work with an actual jtagulator which uses ftdi
                if "USB Serial" in port.description:
                    return port.device

            except AttributeError:
                pass

    def connect(self):
        device = self.get_device()
        baud = 115200
        try:
            self.serial_connection = serial.Serial(device, baud)
        except serial.serialutil.SerialException:
            sys.stderr.write(f"permission denied {device}\n")
            sys.exit()

        if not self.serial_connection.is_open:
            sys.stderr.write("NO DEVICE\n")
            sys.exit()

        time.sleep(3)
        self.serial_connection.write(b"\r\n")
        time.sleep(0.1)

    def read(self):
        if self.debug:
            return self.print()
        return self._read()

    def _read(self):
        time.sleep(0.1)
        buffer = b""
        while self.serial_connection.in_waiting:
            time.sleep(0.1)
            n_bytes = self.serial_connection.in_waiting
            part = self.serial_connection.read(n_bytes)
            buffer += part
        return buffer

    def print(self):
        content = self._read()
        print(content.decode())
        return content

    def write(self, to_write):
        if not isinstance(to_write, bytes):
            to_write = str(to_write)
        try:
            to_write = to_write.encode()
        except AttributeError:
            pass

        self.serial_connection.write(to_write)
        self.serial_connection.write(b"\r")

    def write_read_print(self, to_write):
        self.write(to_write)
        self.print()

    def write_read(self, to_write):
        self.write(to_write)
        return self.read()

    def write_check(self, to_write, success_indicator):
        result = self.write_read(to_write)
        return success_indicator in result

    def drop_to_miniterm(self):
        miniterm = Miniterm(self.serial_connection)
        miniterm.exit_character = chr(3)
        miniterm.set_rx_encoding('utf-8')
        miniterm.set_tx_encoding('utf-8')

        print("Dropping to miniterm - press CTRL-C to exit")
        miniterm.start()

        try:
            miniterm.join(True)
        except KeyboardInterrupt:
            print("got ctrl-c")
