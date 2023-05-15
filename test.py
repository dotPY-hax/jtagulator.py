from jtagulator import JtagulatorUART

j = JtagulatorUART(3.3)
#j._connection.debug = True
j.get_tx_only(0, 1)
