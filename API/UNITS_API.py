#!/usr/bin/env python3
import socket
import pynmea2
import datetime
import threading
import time
import gpsd

from slowGPS import slowGPS
from set_system_time import set_system_time

#IP_ADDRESS = '192.168.1.155'
#PORT = 2497

# What does UNITS API need to do? It needs to give the current time to anybody
# that asks. It needs to give the best estimation for the location to anybody
# who asks. It doesn't need to do more than that. So the init function should
# set system time and get a location estimate. It should then disconnect so
# those things cannot be screwed up in the future.

class UNITS_API:
    def __init__(self,IP_ADDRESS,PORT):
        self.IP_ADDRESS = IP_ADDRESS
        self.PORT = PORT

        #Creates sgps, checks that gps is connected
        print("Please activate GPS now.")
        SGPS = slowGPS(self.IP_ADDRESS,self.PORT)
        SGPS.SG_check_GPS_connection()

        set_system_time(method_used = "phone",
                        server_IP=self.IP_ADDRESS,
                        server_port = self.PORT)

        self.lat, self.lon = *SGPS.SG_generateAverageGPSlocation()
    
    def getLocation(self):
        return (self.lat,self.lon)


