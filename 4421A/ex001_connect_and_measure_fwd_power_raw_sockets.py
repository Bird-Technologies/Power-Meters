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
import socket
import time

IPADDR = "192.168.1.44"
MYPORT = 5025
TIMEOUT = 5000
RECVSIZE = 256

# Establish a TCP/IP socket object
s = socket.socket()

# Open the socket connection
s.connect((IPADDR, MYPORT)) # input to connect must be a tuple
s.settimeout(TIMEOUT)

# Query the instrument ID...
s.send(f"*IDN?\n".encode())
time.sleep(0.05)
id = s.recv(RECVSIZE).decode().rstrip()
time.sleep(0.05)

# Measure forward power
s.send(f"MEAS:AVER? 1\n".encode())
time.sleep(0.05)
fwd = s.recv(RECVSIZE).decode().rstrip()
time.sleep(0.05)

# Measure reflected power
s.send(f"MEAS:REFL:AVER? 1\n".encode())
time.sleep(0.05)
refl = s.recv(RECVSIZE).decode().rstrip()
time.sleep(0.05)

print(f"Instrument ID:\t{id}\nFWD Power:\t{fwd} W\nRFL Power:\t{refl} W")
s.close()
