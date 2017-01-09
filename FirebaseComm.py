
# This python code performs communication between arduino hardware and Firebase cloud.
# Sharvari Malunjkar Jan 5, 2017.
#------------------------------------------------------------------------------------------------------------------------------------
#Note: pyserial and reuests dependant libraries are needed to be installed.
# For windows users get requests libary tar fine from python libraries online, extract and save it to Python27/Lib/site-packages.
# Linux/unix users can install using install command.
#-------------------------------------------------------------------------------------------------------------------------------------

import serial
import time
import requests
import json

#----------------------------------------------------------------------------------------
# After creating account on firbase console please note the realtime data base url below.
#----------------------------------------------------------------------------------------
firebase_url = 'Your Firebase URL here'

#----------------------------------------------------------------------------------------
#Connect to Serial Port for communication : Find out the serial port connected to Arduino
# Please change 'COMX' according to your serail port of connection.
#----------------------------------------------------------------------------------------

ser = serial.Serial('COMX', 9600, timeout=0)

ser.flushInput()
ser.flushOutput()

#----------------------------------------------------------------------------------
# you can change the interval for sending data by changing fixed_interval variable.
#---------------------------------------------------------------------------------
fixed_interval = 10

while 1:
  try:
    #temperature value obtained from Temperature Sensor         
    temperature_c = ser.readline()
    
    #current time and date
    time_hhmmss = time.strftime('%H:%M:%S')
    date_mmddyyyy = time.strftime('%d/%m/%Y')
    
    #User info
    temperature_checker = 'User1';
    print temperature_c+ ',' + time_hhmmss + ',' + date_mmddyyyy + ',' + temperature_checker
    
    #insert record
    data = {'date':date_mmddyyyy,'time':time_hhmmss,'value':temperature_c[0:5]}
    result = requests.post(firebase_url + '/' + temperature_checker + '/temperature.json', data=json.dumps(data))
    
    print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text
    time.sleep(fixed_interval)
  except IOError:
    print('Error! Something went wrong.')
  time.sleep(fixed_interval)
  