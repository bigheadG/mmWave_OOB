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

This repository contains the Batman mmWave-PC3 People Counting & Detection mmWave Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-PC3 Python Program will work with People Counting & Detection based Batman BM201-PC3 mmWave Kit solution. This Python Program works with a Raspberry Pi 4 , NVIDIA Jetson Nano, windows/linux computer or MAC with Batman BM201-PC3 Kit attached via Kit’s HAT Board; and that the BM201 Kit is an easy-to-use mmWave sensor evaluation kit for People Sensing, People Counting, or People Occupancy Density Estimation in approx. 6m x 6m area without privacy invasion; and where the Python Program would have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.


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
    
    pyqtgraph_3d_pc3_xyz.py # show detected point cloud in 3D
    pyqtgraph_3d_pc3_occupancy.py # show occupancy detection
    
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

## pyqtgraph_3d_pc3_xyz.py screenshot

![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/pc3_xyz.png)

## pyqtgraph_3d_pc3_occupancy.py screenshot

 
https://user-images.githubusercontent.com/2010446/118247174-7510c880-b4d5-11eb-91a2-173c0d3ddb3b.mov



 # import lib

    from mmWave import pc3_oob

  ### raspberry pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

  ### Jetson Nano use ttyTHS1
      port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    and please modify: 
    
  ### use USB-UART
    port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
 
  ### Mac OS use tty.usbmodemxxxx
    port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
  
  ### ubuntu NUC
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


    V1: Detected Points: (data type:dataframe & list)
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
    
    V2: Range Profile: (data type: list)
    An array of 256 float complex data:(real,image), The points represent the sum of magnitudes of received antennas.
    
    
    
## pc3_oob_pyqtgraph_ex1_50.py 

![IMG_8447](https://user-images.githubusercontent.com/2010446/156317589-6bacf303-bf2e-4d5d-864d-61b30aa14410.jpg)

https://user-images.githubusercontent.com/2010446/156316819-086a1902-4a1e-49d1-be57-2870749d0a7d.mov
    
    

# Data Structure(Raw Data):
V6: Point Cloud<br/>
Each Point Cloud list consists of an array of points,Each point data structure is defined as following
   
    point Struct:
        elevation: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians 
        doppler:  float   #Doppler in m/s
        range:    float   #Range in meters
        snr:      float   #SNR, ratio
        
V7: Target Object<br/>
Each Target List consists of an array of targets. Each target data structure defind as following:
    
    target Struct:
        tid: Int        #Track ID
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        posZ: float     #Target position in Z, m
        velZ: float     #Target velocity in Z, m/s
        accZ: float     #Target velocity in Z, m/s2
        
V8: Target Index<br/> 
Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
    TargetIndex Struct(V8):
        tragetID: Int #Track ID
        {targetID0,targetID1,.....targetIDn}
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
   
    Function call: 
        
        (dck,v6,v7,v8) = radar.tlvRead(False)
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array

        return dck,v6,v7,v8 
      
      
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

 
1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/3d_pplcount_user_guide.pdf



