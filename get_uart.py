from jtagulator import JtagulatorUART


def get_shell(voltage, start_pin, stop_pin):
    jtagulator_object = get_uart(voltage, start_pin, stop_pin)
    if jtagulator_object.rx and jtagulator_object.tx and jtagulator_object.baud:
        print(jtagulator_object)
        jtagulator_object.drop_to_passthru()


def get_uart(voltage, start_pin, stop_pin):
    jtagulator_object = JtagulatorUART(voltage)
    jtagulator_object.get_pinout(start_pin, stop_pin)
    return jtagulator_object
