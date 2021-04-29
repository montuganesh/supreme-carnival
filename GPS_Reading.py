#That may all be unnecessary. https://github.com/MartijnBraam/gpsd-py3 may be a good source for everything
import gpsd #Make sure this is imported on the RPi
import time.sleep
import statistics #This is an easy way to find the mean of the array, without going to the expense of numpy

#Gets local gps packet every time it's called, should return values as angles
#Initalize GPS until 3d mode found
def init_GPS(lHOST="127.0.0.1",PORT=None,timeout_seconds=360):
    """Initializes the GPS Moudule with a python library for linux-gpsd.

    Args:
        timeout_seconds (int, optional): Seconds till gps times out as not able to get 3d fix. Defaults to 360.

    Returns:
        int: 0 for success, -1 for timeout
    """
    gpsd.connect(host=lHost,port=PORT)
    seconds_count = 0
    while (gpsd.mode != 3):
        time.sleep(1)
        seconds_count=seconds_count+1
        if seconds_count >= timeout_seconds:
            return -1
    return 0

def getSingleLocation():
    latitude = gpsd.lat()
    longitude = gpsd.lon()
    error_dict = gpsd.error()
    return {"LAT":latitude,"LON":longitude,"LAT_ERROR":error_dict['y'],"LON_ERROR":error_dict["x"]} 
    #I think error_dict["x"] and y may be bugged. Check the documentation file in the gpsd library 
    # for what it should be, and get ready to fix.


def goFindLocation():
    #We know the gps unit won't be moving, thankfully. So I can take the median measurement.
    # I'm not entirely happy with this, it's too vulnerable to error. Put it on the re-engineer list. 
    lat_list = []
    lon_list = []
    for x in range(100):
        temphold = getSingleLocation()
        lat_list.append(temphold["LAT"])
        lon_list.append(temphold["LON"])
        del temphold
    return (statistics.median(lat_list),statistics.median(lon_list))