#!/usr/bin/env python3
#THIS CODE IS CURRENTLY UN-DEBUGGED, and cannot be until I can plug a gps module in to test it. This is a major problem
#Do not rely on this code until it can be checked.

import gpsd #Also make sure this downloads, because if it's not there we're going to have problems.
#That may all be unnecessary. https://github.com/MartijnBraam/gpsd-py3 may be a good source for everything
import time
import statistics #This is an easy way to find the mean of the array, without going to the expense of numpy
import socket

class GPS():
    def __init__(self,HOST="127.0.0.1",PORT=2947,timeout_seconds=360):
        gps_start_code = self.init_GPS(HOST,PORT,timeout_seconds)
        self.HOST=HOST
        self.PORT=PORT


    def init_GPS(self,HOST="127.0.0.1",PORT=2947,timeout_seconds=360):
        """Initializes the GPS Moudule with a python library for linux-gpsd.
           Tries until timeout or location is found.

        Args:
            timeout_seconds (int, optional): Seconds till gps times out as not able to get 3d fix. Defaults to 360.

        Returns:
            int: 0 for success, -1 for timeout
        """
        gpsd.connect(host=HOST,port=PORT)
        seconds_count = 0
        while (gpsd.mode != 3):
            time.sleep(1)
            seconds_count=seconds_count+1
            print("A")
            if seconds_count >= timeout_seconds:
                return -1
        return 0
    
    def get_single_gps_location(self):
        return gpsd.posistion()
    
    def find_most_probable_telescope_location(self):
        #We know the gps unit won't be moving, thankfully. So I can take the median measurement.
        # I'm not entirely happy with this, it's too vulnerable to error. Put it on the re-engineer list. -CB
        LAT_list = []
        LON_list = []
        for _11 in range(100):
            temphold = self.getSingleLocation()
            time.sleep(1)
            LAT_list.append(temphold[0])
            LON_list.append(temphold[1])
            del temphold
        return (statistics.median(LAT_list),statistics.median(LON_list))

    def get_satelite_time(self):
        return gpsd.time_utc()

import socket



if __name__ == "__main__":
    g = GPS(HOST='192.168.1.155')