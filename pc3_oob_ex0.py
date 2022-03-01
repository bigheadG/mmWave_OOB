''' 
PC3 + Vital Signs : 2022/2/16 15:47
ex0:
  pc3 + heart rate & breathing rate data

(1)Download lib:

install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
import time
#from mmWave import pc3_oob
import pc3_oob
cfg = 0
PORT_CFG = "/dev/tty.usbmodemGY0050511"
PORT_DATA = "/dev/tty.usbmodemGY0050514"


if cfg == 1:
	portCFG = serial.Serial(PORT_CFG,baudrate = 115200 , timeout = 0.5)
	#file1 = open('xwr68xx_profile_2022_02_21T08_22_32_992_forZach.cfg', 'r')
	file1 = open('xwr68xx_profile_2022_02_24T06_32_54_632_33ms.cfg', 'r')
	
	Lines = file1.readlines()
	# Strips the newline character
	for line in Lines:
		if "%" not in line:
			#tail : bytes = b'\x0d\x0a'
			tail : bytes = b'\x0d\x0a'
			d = str.encode(line+'\n')
			portCFG.write(d)
			print("Send Command:{:}".format(line.strip()))
			time.sleep(0.05)
			da0 = portCFG.readlines()
			time.sleep(0.05)
			print(da0) 
		else:
			print(line.strip())
		

port  = serial.Serial(PORT_DATA,baudrate = 921600 , timeout = 0.5)
radar = pc3_oob.Pc3_OOB(port)
#radar.sm = True

def radarExec(name):
	print("mmWave: {:} example:".format(name))
	while True:
		(dck,v1,v6,v9)  = radar.tlvRead(False,df = 'DataFrame')
		#if len(radar.v2) != 0:
		# print(radar.v2) 
		if not v1.empty:
			print(v1)
		if not v6.empty:
			print(v6)
		if not v9.empty:
			print(v9)
 

radarExec("OOB mmWave")






