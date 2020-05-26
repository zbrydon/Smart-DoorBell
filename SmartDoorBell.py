import os
from time import sleep
import RPi.GPIO as GPIO
import time
import serial
import webbrowser
import multiprocessing
import subprocess as sp
from tkinter import *
import tkinter.font

##HARDWARE##
GPIO.setmode(GPIO.BCM)
 

GPIO_TRIG = 14
GPIO_ECHO = 15
GPIO_COM = 18
GPIO_MO = 23
GPIO_COM2 = 24

GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_COM, GPIO.OUT)
GPIO.setup(GPIO_MO, GPIO.IN)
GPIO.setup(GPIO_COM2, GPIO.OUT)




##VAIRIABLES##
running = False
CameraOn = False
T1 = ()
T2 = ()
##Functions##
def distance():
    
    #print("Measuring distance...")
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIG, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    #print("Complete")
    return distance


##Widgets##



if __name__ == '__main__':
    print("Running...")
    try:
        while True:
            dist = int(distance())
            #print ("Measured Distance = %.1f cm" % dist)
            motion = int(GPIO.input(GPIO_MO))
            
            if(dist < 150 and motion == 1 ):
                
                GPIO.output(GPIO_COM, True)
                GPIO.output(GPIO_COM2, True)
                
                print("Start")
                print(dist)
                print(motion)
                if (CameraOn == False):
                    p1 = sp.Popen(['python3','Stream.py'])
                    CameraOn = True
                running = True
                time.sleep(10)
                webbrowser.open( "http://10.0.0.3:5000")
                time.sleep(300)
            elif(dist < 150 and motion == 0 and running == False):
                
                
                
                GPIO.output(GPIO_COM, True)
                GPIO.output(GPIO_COM2, False)
                
                print("Start")
                print(dist)
                print(motion)
                if (CameraOn == False):
                    p1 = sp.Popen(['python3','Stream.py'])
                    CameraOn = True
                
                    
                time.sleep(10)
                webbrowser.open( "http://10.0.0.3:5000")
                running = True
                time.sleep(300)
            elif(dist > 150 and motion == 1 ):
                
                GPIO.output(GPIO_COM, False)
                GPIO.output(GPIO_COM2, True)
                
                print("Start")
                print(dist)
                print(motion)
                if (CameraOn == False):
                    p1 = sp.Popen(['python3','Stream.py'])
                    CameraOn = True
                time.sleep(10)
                webbrowser.open( "http://10.0.0.3:5000")
                running = True
                time.sleep(300)
            elif(dist > 150 and motion == 0 ):
                GPIO.output(GPIO_COM, False)
                GPIO.output(GPIO_COM2, False)
                
                if(CameraOn == True):
                    sp.Popen.terminate(p1)
                    CameraOn = False
                print("Stop")
                print(dist)
                print(motion)
                running = False
                
            time.sleep(1)
            
                
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        if(CameraOn == True):
                sp.Popen.terminate(p1)
                CameraOn = False
        print("Stop")











































































