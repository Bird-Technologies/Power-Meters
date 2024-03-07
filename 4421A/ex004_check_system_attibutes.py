"""
Example Description:
        This example shows how a user can get the 4421A intrument information
        from either the driver properties or the methods from the system functions.

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

@file ex004_check_system_attributes.py
 
"""
from series_4421A import Series4421A
import pyvisa.constants as pycon

mysensor = Series4421A()

mysensor.connect("TCPIP0::192.168.3.44::5025::SOCKET", 20000)

print(mysensor.idn)
print(mysensor.manufacturer)

# Get system information from properties or the system functions.
print(mysensor.model)
print(mysensor.system.model_number())

print(mysensor.fw_version)
print(mysensor.system.firmware_version())

print(mysensor.serial_number)
print(mysensor.system.serial_number())

print(mysensor.system.scpi_version())

mysensor.disconnect()
