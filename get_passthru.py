from jtagulator import JtagulatorUART


def force_passthru(rx, tx, baud, voltage):
    uart = JtagulatorUART(voltage)
    uart.rx = rx
    uart.tx = tx
    uart.baud = baud
    uart.reset()
    uart.drop_to_passthru()
