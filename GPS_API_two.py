#!/usr/bin/env python3
import socket
import pynmea2
import datetime
import threading
import time
import gpsd

import slowGPS

IP_ADDRESS = '192.168.1.155'
PORT = 2497

class GPS_API:
    # What needs to happen here? There needs to be an initilization cycle,
    # which checks connection to the external gps and sets time, but from
    # that point forward, it's not necessary for the gps to be connected.
    # Disconnection is likely, so at that point, the computer should store
    # info for later. So there should be no direct access from the API.
    # That suggests making the gps test, get data, and then stop looking
    # for connections.

    #Plugging in a gps should also be an option, so make sure to check for that.

    def __init__(self,IP_ADDRESS,PORT):
        self.using_GPSD_flag = True
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT
        try:
            gpsd.connect() #looks for GPSD instance in default location. If not found, it sets a flag and moves on.
        except json.decoder.JSONDecodeError:
            self.using_GPSD_flag = False
            self.SGU = slowGPS.slowGPS(self.IP_ADDRESS, self.PORT)

        self.SGU.SG_checkGPSconnection() 
        # This should be a check that looks for the GPS receiver, and refuses
        # to go on until it finds it. It'll need some work later. If anyone wants
        # to implement it, I would appreciate not having to. -CB

    def initializeGPSunit(self):
        if self.using_GPSD_flag == True:
            pass
        
    def getGPStimestamp(self):
        ts_thread = threading.Thread(target=self.SGU.SG_getGPStimestamp)
        ts_thread.start()

    def getSingleGPSlocation(self):
        ls_thread = threading.Thread(target=self.SGU.SG_getSingleGPSlocation)
        ls_thread.start()
