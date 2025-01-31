"""
Example Description:
        This example shows how to connect to the 4421A using the pyserial
        interface, query its measured forward and reflected power values     

@verbatim

The MIT License (MIT)

Copyright (c) 2025 Bird

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

@file ex008_connect_and_measure_fwd_power_pyserial.py
 
"""
import serial
from time import sleep
from enum import Enum


def writer(sp: serial, cmd:str):
    sp.write(f'{cmd}\n'.encode())

def reader(sp:serial)->str:
    return sp.read_until(b'\n').decode("utf-8").rstrip()

def query(sp:serial, cmd:str)->str:
    sp.write(f'{cmd}\n'.encode())
    return sp.read_until(b'\n').decode("utf-8").rstrip()

### MAIN PROGRAM STARTS HERE ###
my4421a = serial.Serial(port='COM11', baudrate=9600, parity="N", stopbits=1,bytesize=8)

my4421a.flush()

# get the ID string
writer(my4421a, "*IDN?")
print(reader(my4421a))
print(query(my4421a, "*IDN?"))

for j in range(0, 100):
    y1 = float(query(my4421a, "MEAS:AVER? 1").rstrip())
    y2 = float(query(my4421a, "MEAS:REFL:AVER? 1").rstrip())

    print(f"Forward = {y1:0.2f} W, Reflected = {y2:0.2f} W")
    sleep(0.5)

my4421a.close()
