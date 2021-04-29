#That may all be unnecessary. https://github.com/MartijnBraam/gpsd-py3 may be a good source for everything
import gpsd #Make sure this is imported on the RPi
import time.sleep

gpsd.connect(host=lHost,port=PORT)

#Gets local gps packet every time it's called, should return values as angles
#Initalize GPS until 3d mode found
def init_GPS(timeout_seconds=360):
    """[summary]

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

def build