"""
Example Description:
        This example shows how to connect to the 4421A, query its
        measured forward and reflected power values, then use 
        matplotlib to display the results in a plot with a primary
        and secondary axis for forward and reflected power, respectively.

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

@file ex007_fast_sample_and_log_fwd_and_rev_power_lan_interface.py
 
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
y1 = [float(my4421A.query("MEAS:AVER? 1\n").rstrip())]
y2 = [float(my4421A.query("MEAS:REFL:AVER? 1\n").rstrip())]

# Create the first plot and frame and add a secondary axis
COLOR_FWD_W = "#69b3a2"
COLOR_REV_W = "#3399e6"

fig, ax1 = plt.subplots(figsize=(8, 8))
ax2 = ax1.twinx()

ax1.plot(x, y1, color=COLOR_FWD_W, lw=1) # lw = 3
ax2.plot(x, y2, color=COLOR_REV_W, lw=1)

ax1.set_ylim(0, 120e-3)
ax2.set_ylim(0, 10e-3)

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("FWD Power (W)", color=COLOR_FWD_W, fontsize=14)
ax1.tick_params(axis="y", labelcolor=COLOR_FWD_W)

ax2.set_ylabel("REV Power (W)", color=COLOR_REV_W, fontsize=14)
ax2.tick_params(axis="y", labelcolor=COLOR_REV_W)

fig.suptitle("4421A Forward Power Sampling", fontsize=20)
fig.autofmt_xdate()

TIME_LIMIT_S = 36
is_at_time_Limit = False
while(not is_at_time_Limit):
    # update the data
    t2 = time.time()
    dt = t2 - t1
    x.append(dt)
    y1.append(float(my4421A.query("MEAS:AVER? 1\n").rstrip()))
    y2.append(float(my4421A.query("MEAS:REFL:AVER? 1\n").rstrip()))
    
    # update the lists passed to the axes
    ax1.plot(x, y1, color=COLOR_FWD_W, lw=3)
    ax2.plot(x, y2, color=COLOR_REV_W, lw=4)
    plt.xlim(x[0], x[-1])
     
    # calling pause function for 0.25 seconds; this forces an update
    plt.pause(0.25)

    # Test to see if the target test time has been met
    if dt >= TIME_LIMIT_S:
        is_at_time_Limit = True

# Save the data plot to file
output_data_path = time.strftime("power_capture_%Y-%m-%d_%H-%M-%S.png")
plt.savefig("C:\\Temp\\" + output_data_path)
my4421A.close()
rm.close()
