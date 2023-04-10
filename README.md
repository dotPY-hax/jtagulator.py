# jtagulator.py
run JTAGULATOR or JHACKULATOR  from python

This lets you control your JTAGULATOR or JHACKULATOR from Python!

![image](https://user-images.githubusercontent.com/67259802/230999195-a4a8e13c-cd2f-42ff-a9ac-2695e79fad08.png)


![image](https://user-images.githubusercontent.com/67259802/230999092-b42a452d-6c92-484d-b191-d12882f44702.png)

## Whats this?

The module communicates with the JTAGULATOR or JHACKULATOR and exposes it as a class abstracting the serial interaction.

At the moment it only does UART unfortunately because I dont have a jtag device at hand. Jtag support will come soon(tm)!
 ## Usage example
 
 Plug in your JTAGULATOR or JHACKULATOR and prepare it like you would normally.
 ```python
 from jtagulator import JtagulatorUART

j = JtagulatorUART()
j.set_voltage(3.3)
j.get_pinout(0, 1)
print("="*10)
print(j)`
