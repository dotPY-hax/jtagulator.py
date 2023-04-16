from jtagulator_serial import Connection


class Jtagulator:
    def __init__(self):
        self._connection = None
        self.voltage = None
        self.start()

    def start(self):
        print("Starting JTAGULATOR")
        self._connection = Connection(debug=False)
        self._connection.connect()
        result = self._connection.read()
        if self.voltage:
            self.set_voltage(self.voltage)
        return b"Welcome to JTAGulator. Press 'H' for available commands." in result

    def manual(self, to_write):
        return self._connection.write_read_print(to_write)

    def reset(self):
        print("resetting JTAGULATOR")
        self.start()

    def set_voltage(self, voltage):
        success = b"Enter new target I/O voltage (1.4 - 3.3, 0 for off)"
        result = self._connection.write_check("V", success)
        if not result:
            return False

        success = b"New target I/O voltage"
        result = self._connection.write_check(voltage, success)
        if result:
            self.voltage = voltage
            print(f"Set voltage to {voltage}")
        return result

class JtagulatorUART(Jtagulator):
    def __init__(self):
        self.rx = None
        self.tx = None
        self.baud = None
        self.possible_baud_rates = {}
        super().__init__()

    def uart(self):
        result = self._connection.write_read("U")
        if b"UART>" in result:
            return True

    def uart_pinout(self, start_pin, stop_pin):
        success = b"Enter starting channel"
        result = self._connection.write_check("U", success)
        if not result:
            return False

        success = b"Enter ending channel"
        result = self._connection.write_check(str(start_pin), success)
        if not result:
            return False

        success = b"Are any pins already known?"
        result = self._connection.write_check(str(stop_pin), success)
        if not result:
            return False

        success = b"Enter text string to output (prefix with \\x for hex)"
        result = self._connection.write_check("N", success)
        if not result:
            return False

        success = b"Enter delay before checking for target response"
        result = self._connection.write_check("", success)
        if not result:
            return False

        success = b"Ignore non-printable characters?"
        result = self._connection.write_check(str(10), success)
        if not result:
            return False

        success = b"Bring channels LOW before each permutation?"
        result = self._connection.write_check("N", success)
        if not result:
            return False

        success = b"Press spacebar to begin (any other key to abort)"
        result = self._connection.write_check("N", success)
        if not result:
            return False

        self._connection.serial_connection.write(b" ")
        result = self._connection.serial_connection.read_until(b"UART>")
        return result

    def parse_baudrates(self, console_output):
        console_output = console_output.decode()
        if "No target device(s) found!" in console_output:
            return
        start_baud_block = console_output.find("-\r\n")
        end_baud_block = console_output.find("-\r\n", start_baud_block+1)
        baud_block = console_output[start_baud_block+2:end_baud_block]
        baud_blocks = baud_block.split("\r\n\r\n")

        for block in baud_blocks:
            tx, rx, baud, data, *_ = block.split("\r\n")
            self.tx = tx.split()[-1]
            self.rx = rx.split()[-1]
            baud = baud.split()[-1]
            self.possible_baud_rates[int(baud)] = data

    def choose_baud_rate_manually(self):
        allowed = {}
        for i, key_value_pair in enumerate(self.possible_baud_rates.items()):
            allowed[str(i+1)] = key_value_pair
            baud, data = key_value_pair
            print(f"[{i+1}]", baud, data)
        prompt = "choose baud rate. choose 0 to cancel: "
        user_interaction = None

        while user_interaction not in list(allowed.keys()) + ["0"]:
            user_interaction = input(prompt)

        if user_interaction == "0":
            print("canceled - no baud rate was chosen")
        else:
            chosen = allowed[user_interaction]
            baud = chosen[0]
            print(f"baud rate {baud} chosen!")
            self.baud = baud

    def drop_to_passthru(self):
        result = self._drop_to_passthru()
        if not result:
            return False

        self._connection.drop_to_miniterm()
        return True

    def use_passthru(self):
        return self._drop_to_passthru()

    def _drop_to_passthru(self):
        self.uart()
        success = b"Enter TXD pin"
        result = self._connection.write_check("P", success)
        if not result:
            return False

        success = b"Enter RXD pin"
        result = self._connection.write_check(self.tx, success)
        if not result:
            return False

        success = b"Enter baud rate"
        result = self._connection.write_check(self.rx, success)
        if not result:
            return False

        success = b"Enable local echo?"
        result = self._connection.write_check(self.baud, success)
        if not result:
            return False

        success = b"Entering UART passthrough!"
        result = self._connection.write_check("N", success)
        if not result:
            return False
        return True

    def get_pinout(self, start_pin, stop_pin):
        print("JTAGULATING")
        self.uart()
        result = self.uart_pinout(start_pin, stop_pin)
        if result:
            self.parse_baudrates(result)
            self.choose_baud_rate_manually()
        self.reset()

    def __str__(self):
        rx = f"RX: {self.rx}"
        tx = f"TX: {self.tx}"
        baud = f"Baud rate: {self.baud}"
        voltage = f"Voltage: {self.voltage}V"
        return "\n".join((rx, tx, baud, voltage))
