"""
Example Description:
        This example application demonstrates how to use the DAQ6510 to perform
        complex multi-channel, mixed function scanning in a production-test
        environment. The DAQ6510 can perform more than one function in a multichannel
        scan, providing a range of dataacquisition options in a single test.

        In this production environment the DAQ6510 is:
        - Integrated into a test stand.
        - Wired to a fixture that is connected to an active device under test (DUT).
        - Quickly capturing DC volts and current, temperature, and AC volts and current.

        Prior to the start of the scan, you can step through each of the configured
        channels on the DAQ6510, which allows you to troubleshoot the test
        configuration. This allows you to view the readings of individually closed
        channels to ensure that connections to the DUT are secure.

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

@file ex001_connect_and_measure_fwd_power_raw_sockets.py
 
"""
import pyvisa as visa
import pyvisa.constants as pyconst

MYSENSOR = "ASRL4::INSTR"

rm = visa.ResourceManager()  # Open the resource manager.

my4421A = rm.open_resource(MYSENSOR) # Open an instance of the sensor object.
my4421A.baud_rate = 9600
my4421A.data_bits = 8
my4421A.stop_bits = pyconst.StopBits.one
my4421A.parity = pyconst.Parity.none
my4421A.flow_control = 0
my4421A.write_termination = "\n"
my4421A.read_termination = "\n"
my4421A.send_end = True
my4421A.timeout = 5000

my4421A.write("*RST")

# Get the instrument identification information
print(my4421A.query("*IDN?\n").rstrip())

# Measure forward power on sensor 1
fwd = my4421A.query("MEAS:AVER? 1\n").rstrip()

# Measure reflected power on sensor 1
refl = my4421A.query("MEAS:REFL:AVER? 1\n").rstrip()

print(f"Instrument ID:\t{id}\nFWD Power:\t{fwd} W\nRFL Power:\t{refl} W")

my4421A.close()

rm.close()
