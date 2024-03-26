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

@file ex006_fast_sample_and_log_power_lan_interface.py
 
"""
import pyvisa as visa
import matplotlib.pyplot as plt

import time

MYSENSOR = "TCPIP0::172.100.0.79::5025::SOCKET"

rm = visa.ResourceManager()  # Open the resource manager.

my4421A = rm.open_resource(MYSENSOR) # Open an instance of the sensor object.
my4421A.write_termination = "\n"
my4421A.read_termination = "\n"
my4421A.send_end = True
my4421A.timeout = 5000

resp = my4421A.query("*RST\n")
resp = my4421A.query("*CLS\n")

# Get the instrument identification information
print(my4421A.query("*IDN?\n").rstrip())

state = my4421A.query("SYST:ERR?")
while "No error" not in state:
    state = my4421A.query("SYST:ERR?")

# Get first data
t1 = time.time()
x = [0]
y = [float(my4421A.query("MEAS:AVER? 1\n").rstrip())]

# Create the first plot and frame
graph = plt.plot(x,y,color = 'g')[0]
plt.ylim(50, 110)
plt.title("4421A Forward Power Sampling")
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.pause(1)

TIME_LIMIT_S = 36
is_at_time_Limit = False
while(not is_at_time_Limit): 
    # updating the data
    t2 = time.time()
    dt = t2 - t1
    x.append(dt)
    y.append(float(my4421A.query("MEAS:AVER? 1\n").rstrip()))
    
    # remove older graph
    graph.remove()

    # create a new graph or updating the graph
    # plotting newer graph
    graph = plt.plot(x,y,color = 'g')[0]
    plt.xlim(x[0], x[-1])
     
    # calling pause function for 0.25 seconds
    plt.pause(0.25)
    if dt >= TIME_LIMIT_S:
        is_at_time_Limit = True

my4421A.close()
rm.close()
