encoding = 'utf-8'
import os
import pyvisa as visa
from datetime import date

today = date.today()
d1 = today.strftime("%Y%m%d")
path = os.getcwd()

try:                                    # Tested on Linux with pyvisa-py and linux-gpib
    rm = visa.ResourceManager('@py')    # and with NI-VISA under windows 7
except:
    rm = visa.ResourceManager()

adr=input('Enter HP 437B GPIB adress: ')                # dialog for 437B GPIB address
HP437B = rm.open_resource('GPIB0::%s::INSTR' % (adr))

sensor=input('Enter sensor table number: ')             # dialog to input what table to read from

try:
    HP437B.write('SE%sEN' % (sensor))                       # try reading from 437B
    data = HP437B.query('OD')
except:
    print("Error communicating with: %s\n" % HP437B)        # exit with error if no communication with 437B
    exit()

if 'NO TBL DATA' in data:                                   # Check it there is cal data in selected table
    print('Error! No table data in selected sensor number\n')
else:
    try:
        HP437B.write('SE' + sensor)                         # Read selected sensor ID
        data = HP437B.query('OD').strip("\n")
        HP437B.write('EN')
        print(data[2:].strip())
        allData = data[2:]
        name = data.strip() + '_' + d1 + '.txt'             # make filename from ID#, ID name and date
        HP437B.write('RF' + sensor)                         # Read sensor ref cal factor
        data = HP437B.query('OD')
        HP437B.write('EN')
        print(data.strip())
        allData = allData + data.strip("\n")
        HP437B.write('ET' + sensor)                         # start reading table data
    except:
        print('Error reading table')                        # exit if error reading
        HP437B.write('EX')
        exit()

    while not '00.00GZ 100.0%' in data:                     # read all table data, end indicated by 00.00GZ 100.0%
        try:
            data = HP437B.query('OD').strip("\n")
            print(data.strip())
            allData = allData + data.strip("\n")
            HP437B.write('EN')
        except:
            print('Error reading table')
            HP437B.write('EX')
            exit()

    HP437B.write('EX')
    
    name = name.replace(" ", "_")
    outFeFile=os.path.join(path,name)
    try:
        fout = open(outFeFile, 'w')                         # write file to disk
        fout.write(allData)
        fout.close()
    except:
        print('Error saving file: %s.txt\n' % (name))
        exit()

    print('\nData saved to: %s.txt'  % (name))

HP437B.write('EX')
HP437B.close()