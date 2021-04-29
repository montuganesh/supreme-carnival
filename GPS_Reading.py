#That may all be unnecessary. https://github.com/MartijnBraam/gpsd-py3 may be a good source for everything
import gpsd #Make sure this is imported on the RPi
import time
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
    gpsd.connect(host=lHOST,port=PORT)
    seconds_count = 0
    while (gpsd.mode != 3):
        time.sleep(1)
        seconds_count=seconds_count+1
        if seconds_count >= timeout_seconds:
            return -1
    return 0

def getSingleLocation():
    return gpsd.posistion()
    # TODO We are not using the error data provided. Determine if useful, and if so implement.


def goFindLocation():
    #We know the gps unit won't be moving, thankfully. So I can take the median measurement.
    # I'm not entirely happy with this, it's too vulnerable to error. Put it on the re-engineer list. -CB
    LAT_list = []
    LON_list = []
    for _ciesnso in range(100):
        temphold = getSingleLocation()
        time.sleep(1)
        LAT_list.append(temphold[0])
        LON_list.append(temphold[1])
        del temphold
    return (statistics.median(LAT_list),statistics.median(LON_list))

def getGPStime():
    return gpsd.time_utc()