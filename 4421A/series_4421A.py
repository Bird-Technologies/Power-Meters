"""
Example Description:
        This example is an instrument class library used for automation
        of the Bird 4421A Multifuntion Power Meter. 

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

@file series_4421A.py
 
"""
import pyvisa

class Series4421A():
    """_summary_
    """
    def __init__(self, instrument_resource_string=None):
        self.__instrument_resource_string = instrument_resource_string
        self.__resource_manager = None
        self.__instr_obj = None
        self.__timeout = 5000
        self.__echo_cmds = False
        self.__mfg_id = ""
        self.__model = ""
        self.__sn = ""
        self.__fw = ""
        self.__general = ""

        self.measure = None
        self.system = None

        try:
            if self.__resource_manager is None:
                self.__resource_manager = pyvisa.ResourceManager()
        except pyvisa.VisaIOError as visaerror:
            print(f"{visaerror}")
        except pyvisa.VisaIOWarning as visawarning:
            print(f"{visawarning}")

    def connect(self, instrument_resource_string:str=None, timeout:int=None, **kwargs):
        """Creates the VISA session connection to the instrument represented by the
        instrument resource string. 

        Args:
            instrument_resource_string (str, optional): VISA instrument resource string. Defaults to None.
            timeout (int, optional): The instrument timeout response value. Defaults to None.
            stop_bits (pyvisa.constant.StopBits, optional): The number of stop bits used for RS232 comms.
            data_bits (int, optional): The number of data bits used for RS232 comms. 
            baud_rate (int, optional): The baud rate used for RS232 comms.
            parity (pyvisa.constant.Parity, optional): The parity type used for RS232 comms. 
        """
        try:
            if instrument_resource_string != None:
                self.__instrument_resource_string = instrument_resource_string
                
            self.__instr_obj = self.__resource_manager.open_resource(
                self.__instrument_resource_string
            )

            if timeout is None:
                self.__instr_obj.timeout = self.__timeout
            else:
                self.__instr_obj.timeout = timeout
                self.__timeout = timeout

            self.__instr_obj.send_end = True
            self.__instr_obj.write_termination = "\n"
            self.__instr_obj.read_termination = "\n"   

            for key, value in kwargs.items():
                print(f"key = {key} and value = {value}")
                if key == 'stop_bits':
                    self.__instr_obj.stop_bits = value
                if key == 'data_bits':
                    self.__instr_obj.data_bits = value
                if key == 'baud_rate':
                    self.__instr_obj.baud_rate = value
                if key == 'parity':
                    self.__instr_obj.parity = value

            self.measure = self.Measure(self.__instr_obj)
            self.system = self.System(self.__instr_obj)

        except pyvisa.VisaIOError as visaerr:
            print(f"{visaerr}")
        return
    
    def write(self, cmd):
        self.__instr_obj.write(f"{cmd}")

    def query(self, cmd):
        return self.__instr_obj.query(f"{cmd}")

    def disconnect(self):
        """
        Close an instance of an instrument object.

        Args:
            None

        Returns:
            None
        """
        try:
            self.__instr_obj.close()
        except pyvisa.VisaIOError as visaerr:
            print(f"{visaerr}")
        return
    
    @property
    def idn(self):
        """Returns the full instrument ID string.

        Returns:
            str: Returns the full instrument ID string. 
        """
        str = self.__instr_obj.query("*IDN?").rstrip()
        self.__mfg_id, self.__model, self.__sn, self.__fw = str.split(',')
        return str
    
    @property
    def manufacturer(self):
        """Reports the instrument manufacturer name. 

        Returns:
            str: The instrument manufacaturer name. 
        """
        return self.__mfg_id
    
    @property
    def model(self):
        """Reports the instrument model number. 

        Returns:
            str: The instrument model number. 
        """
        return self.__model
    
    @property
    def fw_version(self):
        """Reports the instrument firmware version. 

        Returns:
            str: The instrument firmware version. 
        """
        return self.__fw
    
    @property
    def serial_number(self):
        """Reports the instrument serial number. 

        Returns:
            str: The instrument serial number. 
        """
        return self.__sn
    
    class Measure():
        def __init__(self, instrobj):
            self.__instr_obj = instrobj

        def forward_power(self, sensor_number:int=1):
            """
            Initiate, and retrieve a forward average power measurment.
            If the sensor channel to read (1 or 2) is omitted, channel 1 is returned.

            Args:
                sensor_number (int): The number of the sensor connected to the meter input.

            Returns:
                float: Power in Watts
            """
            if sensor_number is None:
                sensor_number = 1
            return float(self.__instr_obj.query(f"MEAS:AVER? {sensor_number}").rstrip())
        
        def reflected_power(self, sensor_number:int=1):
            """
            Initiate, and retrieve a reflected average power measurement. If the sensor
            channel to read (1 or 2) is omitted, channel 1 is returned.

            Args:
                sensor_number (int): The number of the sensor connected to the meter input.

            Returns:
                float: Power in Watts
            """
            if sensor_number is None:
                sensor_number = 1
            return float(self.__instr_obj.query(f"MEAS:REFL:AVER? {sensor_number}").rstrip())
    
    class System():
        def __init__(self, instrobj):
            self.__instr_obj = instrobj

        def firmware_version(self):
            """
            Reads the MCU firmware revision.

            Returns:
                str: MCU firmware revision
            """
            return self.__instr_obj.query("SYST:IDEN:FWR?").rstrip()
        
        def model_number(self):
            """
            Returns the model number as given in the *IDN? response

            Returns:
                str: Instrument model number
            """
            return self.__instr_obj.query("SYSTem:IDENtity:MODel?").rstrip()
        
        def serial_number(self):
            """
            Returns the serial number as given in the *IDN? response

            Returns:
                str: Instrument serial number
            """
            return self.__instr_obj.query("SYSTem:IDENtity:SN?").rstrip()
        
        def preset(self):
            """
            Restores factory settings without changing the RS232 or LAN
            settings.
            """
            return self.__instr_obj.query("SYSTem:PRESet").rstrip()
        
        def scpi_version(self):
            """
            Returns the SCPI version.

            Returns:
                str: SCPI version.
            """
            return self.__instr_obj.query("SYSTem:VERSion?").rstrip()
