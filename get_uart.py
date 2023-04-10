from jtagulator import JtagulatorUART

def pwn_uart(voltage):
    jtagulator_object = JtagulatorUART()
    jtagulator_object.set_voltage(voltage)
    jtagulator_object.get_pinout(0, 1)
    if jtagulator_object.rx and jtagulator_object.tx and jtagulator_object.baud:
        print(jtagulator_object)
        jtagulator_object.drop_to_passthru()
