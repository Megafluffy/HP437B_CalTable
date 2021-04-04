# HP437B_CalTable

This is two small Python scripts that uses pyvisa to read/write HP437B probe calibration table.
PyVISA_CalTable_437B-to-file_06.py:  Reads probe calibration table from 437B and save to file (filename is probe ID# and name, and current date)
PyVISA_CalTable_File-to-437B_06.py:  Give a file dialog to select a file to load calibration table to the 437B

This is tested on Linux(Mint) using pyvisa -> pyvisa-py -> Linux-GPIB, and on Windows 7 using pyvisa and NI-VISA.
It should function on other operating systems and with other VISA versions, but this has not been tested.
You might have to do a small chang in the beginning of the script.

I'm new to Python and VISA!!!

This is updated vesion with small changes.
 - Fixed extra linefeeds on output file on windows
 - Changed 'import visa' to 'import pyvisa as visa'
 - Fixed the 'close' function in the end of the file


Requirements:
	python (think most 2.x and 3.x versions should work)
	pyvisa
	VISA, pyvisa-py if using linux-gpib
	functional GPIB adapter  


I have included 3 files with sensor cal data, so these can be used as reference when making a file from the cal table on a sensor.
Its much easier to make the file, then using the scrip to load it to the 437B, than inputing it manually using the fron panel buttons.


Warning!! You use this on your own risk. I take no responsibility for any loss or damages. 


Askild Eide
