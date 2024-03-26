"""
Example Description:
        This example shows how to connect to the 4421A then query its
        measured forward and reflected power values.

@verbatim

The MIT License (MIT)

Copyright (c) 2024 Bird

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@endverbatim

@file ex005_connect_and_measure_fwd_power_pyvisa_lan.py
 
"""
import pyvisa as visa
import pyvisa.constants as pyconst

MYSENSOR = "TCPIP0::192.168.1.151::5025::SOCKET"

rm = visa.ResourceManager()  # Open the resource manager.

my4421A = rm.open_resource(MYSENSOR) # Open an instance of the sensor object.
my4421A.write_termination = "\n"
my4421A.read_termination = "\n"
my4421A.send_end = True
my4421A.timeout = 5000

my4421A.write("*RST\n")

# Get the instrument identification information
print(my4421A.query("*IDN?\n").rstrip())

# Measure forward power on sensor 1
fwd = my4421A.query("MEAS:AVER? 1\n").rstrip()

# Measure reflected power on sensor 1
refl = my4421A.query("MEAS:REFL:AVER? 1\n").rstrip()

print(f"Instrument ID:\t{id}\nFWD Power:\t{fwd} W\nRFL Power:\t{refl} W")

my4421A.close()
rm.close()
