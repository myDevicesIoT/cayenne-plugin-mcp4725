"""
This module provides classes for interfacing with a MCP4725 Analog I/O extension.
"""
from myDevices.devices.i2c import I2C
from myDevices.devices.analog import DAC
from myDevices.plugins.analog import AnalogOutput
from myDevices.utils.logger import info


class MCP4725(DAC, I2C):
    """Class for interacting with a MCP4725 extension."""

    def __init__(self, slave=0x60, vref=3.3):
        """Initializes PCF8591 device.

        Arguments:
        slave: The slave address
        vref: The reference voltage
        """           
        I2C.__init__(self, int(slave))
        DAC.__init__(self, 1, 12, float(vref))
        
    def __str__(self):
        return "MCP4725(slave=0x%02X)" % self.slave

    def __analogRead__(self, channel, diff=False):
        """Returns the value for the specified channel. Overrides ADC.__analogRead__."""
        d = self.readBytes(3)
        value = (d[1] << 8 | d[2]) >> 4
        return value       
    
    def __analogWrite__(self, channel, value):
        """Writes the value to the specified channel. Overrides DAC.__analogWrite__."""
        d = bytearray(2)
        d[0] = (value >> 8) & 0x0F
        d[1] = value & 0xFF
        self.writeBytes(d)


class MCP4725Test(MCP4725):
    """Class for simulating a MCP4725 device."""

    def __init__(self):
        """Initializes the test class."""
        self.bytes = bytearray(3)
        MCP4725.__init__(self)

    def readBytes(self, size=1):
        """Read specified number of bytes."""
        return self.bytes

    def writeBytes(self, data):
        """Write data bytes."""
        self.bytes[1] = (data[0] << 4) | (data[1] >> 4)
        self.bytes[2] = (data[1] << 4) & 0xF0
