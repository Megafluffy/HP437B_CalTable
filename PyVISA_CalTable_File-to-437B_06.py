encoding = 'utf-8'
import os
import pyvisa as visa
# import tkinter
from tkinter import *
from tkinter import filedialog

root = Tk()                         # uses Tk for file dialog
path = os.getcwd()

try:                                    # Tested on Linux with pyvisa-py and linux-gpib
    rm = visa.ResourceManager('@py')    # nd with NI-VISA under windows 7
except:
    rm = visa.ResourceManager()

i = 0

adr = input('Enter HP 437B GPIB address: ')                 # dialog for 437B GPIB address
HP437B = rm.open_resource('GPIB0::%s::INSTR' % adr)

sensor = input('Enter sensor table number to update: ')     # dialog to input what table to write to

try:
    HP437B.write('SE%sEN' % sensor)                         # Read selected sensor ID
    data = HP437B.query('OD')
except:
    print("Error communicating with: %s\n" % HP437B)        # exit with error if no communication with 437B
    exit()

if 'NO TBL DATA' not in data:                               # Check it there is already cal data in selected table
    HP437B.write('SE' + sensor)
    data = HP437B.query('OD')
    HP437B.write('EN')
    yn = input('Warning!!!\nTable: %s is not empty!\n'
               'Are you really sure you want to overwrite (y/n): ' % (data.strip()))
    if 'y' not in yn:
        HP437B.write('EX')
        exit()

try:
    file_path = filedialog.askopenfilename()                # open file dialog to select file
    source_file = os.path.split(file_path)[1]
except:
    print('User abort')
    exit()

try:
    f=open(file_path, 'r')                                  # load table from file
    lines = f.readlines()
    f.close()
    l = len(lines)
except:
    print("could not open file: %s\n" % (source_file))
    root.destroy()
    exit()

print(lines[i].strip()[:10])                                 # Send sensor ID name, max 7 characters
HP437B.write('SN' + sensor + lines[i].strip('ID ').strip()[:7])
HP437B.write('CT' + sensor)
i += 1

if not '%' in lines[i] or not 'REF CF' in lines[i]:
    print('Error in line %d in file: %s' % (i+1, source_file))

else:
    print(lines[i].strip())                                 # send sensor ref cal factor
    HP437B.write('RF' + sensor + lines[i].strip('REF CF'+' '+'\n'+'\r'))
    i += 1
    HP437B.write('ET' + sensor)
    while i < l:                                            # send rest of cal table
        print(lines[i].strip())
        if not 'Z' in lines[i] or not '%' in lines[i]:
            print('Error in line %d in file: %s' % (i+1, source_file))
            break
        else:
            try:
                le=lines[i].strip().split(" ")
                HP437B.write(le[0])
                HP437B.write(le[1])
                HP437B.write('EN')
            except:
                print('Error in line %d in file: %s' % (i + 1, source_file))
                break
        i += 1

HP437B.write('EX')
root.destroy()
HP437B.close()
