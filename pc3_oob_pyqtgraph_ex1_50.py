 # -*- coding: utf-8 -*-
"""
****************************************
version: v1.0 2020/02/27 release
OOB API
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 601 OOB mmWave Sensor SDK
 Jetson nano or pi 4
 
**************
Install Jetson nano: Please reference

https://makerpro.cc/2019/05/the-installation-and-test-of-nvida-jetson-nano/
it will teach you how to install
 
(1)install Jetson nano GPIO
    $sudo pip3 install Jetson.GPIO
    $sudo groupadd -f -r gpio
    
    #please change pi to your account
    $cd practice sudo usermod -a -G gpio pi
    
    $sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/
    
    reboot system and run
    
    $sudo udevadm control --reload-rules && sudo udevadm trigger
(2)install mmWave lib
$sudo pip3 install mmWave
(3) upgarde mmWave lib
$sudo pip3 install mmWave -U

************************************************
raspberry pi 4 UART setting issues reference:
https://www.raspberrypi.org/documentation/configuration/uart.md

************************************************

"""
#https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
#https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/scrollingPlots.py
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

import serial
import pc3_oob

import time
import struct
import sys

from threading import Thread
'''
import datetime
from scipy.fftpack import fft
import numpy as np
from scipy import signal
'''


cfg = 0
PORT_CFG = "/dev/tty.usbmodemGY0050511"
PORT_DATA = "/dev/tty.usbmodemGY0050514"

BANDWIDTH = 0.6144 * 1e9 # GHz/us
RES = 3 * 1e8 / (2 * BANDWIDTH)  #range resolution = c / (2 * bandwidth) = 0.2441 m 
MAX_RANGE = RES * 256   # 62.4896(m)
scaleX = 256/MAX_RANGE


#pg win
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

win.resize(1200,1200)
#pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'y')
 
win.setWindowTitle('OOB Radar')

maxlen = 200
v4 =[]

# 1) for detected object scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[-15,15],yRange= [0,50])
w0.setLabel('bottom', 'V1 Object Location (curveS0)', 'm')
w0.setLabel('left', 'Range', 'm')
curveS0 = pg.ScatterPlotItem(size =10, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)

# 2) for detected object Doppler scatterPlot
w1 = win.addPlot()
w1.setRange(xRange=[0,40],yRange= [-40,40]) 
w1.setLabel('bottom', 'V1 Doppler/Range (curveS1)', 'm')
w1.setLabel('left', 'V1 Doppler', 'm/s')

curveS1 = pg.ScatterPlotItem(size=5, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 

# 3)plot Range Profile window setting 
win.nextRow()
rp = np.zeros(256)
p2 = win.addPlot(colspan=2)
p2xtick = np.linspace(0,MAX_RANGE,256)
p2.setRange(xRange=[0,MAX_RANGE],yRange= [0,15]) 
p2.setLabel('bottom', 'V2 Range Profile (curve5,curve6)', 'm')

curve5 = p2.plot()
curve6 = pg.ScatterPlotItem(size =10, pen=pg.mkPen('g'), pxMode=True)
p2.addItem(curve6)


sensor0A = []
rangeAY = []
rangeA  = []
 
# 
# plot data update 
#
def updatePlot():
	global rp,sensor0A,curveS0,p2xtick,curve6,rangeA,rangeAY,curveS1
	curveS0.setData(x=sensor0A[:,0],y=sensor0A[:,1], pen = 'g', symbol='o') 
	curve5.setData(p2xtick,rp)
	curve6.setData(x=rangeA,y=rangeAY, pen = 'g', symbol='o')
	curveS1.setData(x=rangeA,y=sensor0A[:,3], pen = 'g', symbol='o') 
	
	
# update all plots
def update():
	updatePlot()
	 
#
#----------timer Update-------------------- 

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(150) #150  80: got(20 Times)   *50ms from uart: 

#------------------------------------------

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

#Mac OS


if cfg == 1:
	portCFG = serial.Serial(PORT_CFG,baudrate = 115200 , timeout = 0.5)
	#file1 = open('xwr68xx_profile_2022_02_21T08_22_32_992_forZach.cfg', 'r')
	#file1 = open('xwr68xx_profile_2022_02_24T06_32_54_632_33ms.cfg', 'r')
	file1 = open('xwr18xx_profile_2022_03_01T08_09_36_974_33ms.cfg','r')
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

v2 = []
prev_fn = 0 

def radarExec():
	global rp,sensor0A,rangeA,rangeAY,p2xtick,scaleX,prev_fn
	 
	(dck,v1,v6,v9)  = radar.tlvRead(False,df = 'DataFrame')
	#radar.headerShow()
	
	fn = radar.hdr.frameNumber
	if prev_fn == fn: 
		prev_fn = fn
		return
		
	if len(radar.v2) != 0:
		rp = np.array(radar.v2)
		 
	if len(v1)!= 0:
		v1A  = v1.loc[:,['X','Y','Z','doppler']]
		sensor0A = v1A.to_numpy()
		rA = np.absolute(sensor0A[:,0] + sensor0A[:,1]* 1j) # r= a+bj
		rangeAY = []
		rangeA = []
		for i in rA:
			rangeIdx = int(np.round(i * scaleX )) 
			rangeA.append(p2xtick[rangeIdx])
			rangeAY.append(rp[rangeIdx])
		
		print("======sensor0A: {:} ============len:{:}".format(radar.frameNumber,radar.hdr.totalPackLen))
		print(sensor0A)
		print("=============rangeA==============")
		print(rangeA)
		print("===========rangeAY==================")
		print(rangeAY)
	
	if not v6.empty:
		print(v6)
	if not v9.empty:
		print(v9) 
	
	
	
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		radarExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
