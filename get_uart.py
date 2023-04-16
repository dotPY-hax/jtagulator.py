from jtagulator import JtagulatorUART


def pwn_uart(voltage):
    _pwn_uart(voltage, 0, 1)


def pwn_uart_unknown_pins(voltage, start_pin, stop_pin):
    _pwn_uart(voltage, start_pin, stop_pin)


def _pwn_uart(voltage, start_pin, stop_pin):
    jtagulator_object = get_uart(voltage, start_pin, stop_pin)
    if jtagulator_object.rx and jtagulator_object.tx and jtagulator_object.baud:
        print(jtagulator_object)
        jtagulator_object.drop_to_passthru()


def get_uart(voltage, start_pin, stop_pin):
    jtagulator_object = JtagulatorUART()
    jtagulator_object.set_voltage(voltage)
    jtagulator_object.get_pinout(start_pin, stop_pin)
    return jtagulator_object