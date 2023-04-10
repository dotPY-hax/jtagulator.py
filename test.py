from jtagulator import JtagulatorUART

j = JtagulatorUART()
j.set_voltage(3.3)
j.get_pinout(0, 1)
print("="*10)
print(j)
