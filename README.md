![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# mmWave-PC3_OOB (People Counting 3D + OOB)

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-PC3 People Counting & Detection mmWave Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-PC3-OOB Python Program will work with Batman BM501-PC3/BM601-PC3_OOB mmWave Kit solution. This Python Program works with a Raspberry Pi 4 , NVIDIA Jetson Nano, windows/linux computer or MAC with Batman BM201-PC3 Kit attached via Kit’s HAT Board; and that the BM601/BM501 Kit is an easy-to-use mmWave sensor evaluation kit for Object Sensing, People Counting. Range area without privacy invasion; and where the Python Program would have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.


# Hardware:
    Batman kit-601 (ISK)
    Measure Range: ~150m meters
    
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:
    
    pc3_oob_ex0.py #  show data on text mode
    pc3_oob_pyqtgraph_ex1_50.py # plot range profile 
    
If Run demo program can not find any Raw data output:
      Please set UART to R/W mode: 
      
      pi 3
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyS0
      
      pi 2 
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyAMA0
      
      jetson
      $ls -l /dev/ttyTHS1
      $sudo chmod +777 /dev/ttyTHS1



 # import lib

    from mmWave import pc3_oob

## UART Seting in different host:
	  raspberry pi 4 use ttyS0
	    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

	  Jetson Nano use ttyTHS1
	      port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	    and please modify: 

	  use USB-UART
	    port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)

	  Mac OS use tty.usbmodemxxxx
	    port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)

	  ubuntu NUC
	    port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)


## define

    radar = pc3_oob.Pc3_OOB(port)

## Header:

    class header:
        version = 0
        totalPackLen = 0
        platform = 0
        frameNumber = 0
        timeInCPUcycle = 0
        numDetectedObj = 0
        numTLVs = 0
        subframeNumber = 0
        
        ex.
        radar = pc3_oob.Pc3_OOB(port)
        frameNum = radar.hdr.frameNumber #get frameNumber  
        radar.headerShow()  #show header information
        (dck,v1,v6,v9)  = radar.tlvRead(True,df = 'DataFrame') #Set True on first argument
 
 # Data Structure(Raw Data):
        
    class statistics: # V6 data (data type:dataframe & list)
        interFrameProcessTime = 0.0   #unit: usec
        transmitOutTime = 0.0         #unit: usec
        interFrameProcessMargin = 0.0 #unit: usec
        interChirpProcessMargin = 0.0 #unit: usec
        activeFrameCPULoad = 0.0      #unit: %
        interFrameCPULoad = 0.0       #unit: %
        
        ex:
        if not v6.empty:
            print(v6)
            
        result:
            fN type  iFPT  xOutputT   iFPM  iCPM  aFCpu  iFCpu
        0  387   v6     1      7984  16723     0      0      1
        
    class temperatureStatistics: # V9 data  (data type:dataframe & list)
        tempReportValid  = 0    #(used to know if values are valid)
        timeRadarSS       = 0   #radarSS local time from device powerup (ms)
        tmpRx0Sens         = 0  #unit: °C
        tmpRx1Sens         = 0  #unit: °C
        tmpRx2Sens         = 0  #unit: °C
        tmpRx3Sens         = 0  #unit: °C
        tmpTx0Sens         = 0  #unit: °C
        tmpTx1Sens         = 0  #unit: °C
        tmpTx2Sens         = 0  #unit: °C
        tmpPmSens          = 0  #unit: °C
        tmpDig0Sens      = 0  #unit: °C
        tmpDig1Sens      = 0  #unit: °C(Not valid for devices without DSP)
        
        ex: 
        if not v9.empty: 
            print(v9) 
        
        result:   
            fN type  tRValid   time  tmpRX0  tmpRX1  tmpRX2  tmpRX3  tmpTX0  tmpTX1  tmpTX2  tmpPm  tmpDig0  tmpDig1
        0  387   v9        0  64807      48      49      49      49      50      50      50     51       49       49


## V1: Detected Points: (data type:dataframe & list)
    Will output Array of detected points, Each point is represented by a giving postion(X,Y,Z) and Doppler velocity.
    
        point Struct:
        X : float  unit:m
        Y : float  unit:m
        Z : float  unit:m
        Doppler : float unit: m/s
        
        ex:
        if not v1.empty:
            print(v1)
        
        result:
            fN type         X          Y    Z  doppler
        0  613   v1 -0.366405   1.419079  0.0      0.0
        1  613   v1  8.244106  10.296886  0.0      0.0
    
 ## V2: Range Profile: (data type: list)
    An array of 256 float complex data:(real,image), The points represent the sum of magnitudes of received antennas.
    usuage please refer to example:
    
    
![rangeProfile](https://user-images.githubusercontent.com/2010446/156333660-f31976ff-c343-457e-906a-c10b450d0246.jpg)
  
    
    
    
## pc3_oob_pyqtgraph_ex1_50.py 

![IMG_8447](https://user-images.githubusercontent.com/2010446/156317589-6bacf303-bf2e-4d5d-864d-61b30aa14410.jpg)

https://user-images.githubusercontent.com/2010446/156316819-086a1902-4a1e-49d1-be57-2870749d0a7d.mov
    
  
## Main function:
 
        (dck,v1,v6,v9)  = radar.tlvRead(False,df = 'DataFrame')
        dck : True  : data avaliable
              False : data invalid
        v1: Detected Points
        v6: Statistics information
        v9: Temperature Statistics

        return dck, v1,v6,v9 
      
   
        getHeader()
        headerShow()
        
    Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
    
 ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/objGeoSmall.png)
			


## Reference

 
1. LabGuide: 



