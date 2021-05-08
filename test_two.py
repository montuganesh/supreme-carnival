#!/usr/bin/env python3
import time
import datetime
import calendar
import socket
from slowGPS import slowGPS

def set_clock_with_gps(method_used = "phone",
                       server_IP="127.0.0.1",
                       server_port=2947):
    if method_used == "phone":
        check_phone_connection(server_IP, server_port)
    elif method_used == "gpsd":
        print("Not currently implemented. Please use phone.")
        return 0
    else:
        print("Please chose method.")
        return 0
    
    #finds current gps time
    sGPS = slowGPS(server_IP,server_port)
    gps_timestamp = sGPS.SG_getGPStimestamp()
    # Converts UTC from GPS to unix epoch to set clock
    a = gps_timestamp.timetuple()
    b = calendar.timegm(a)
    #sets time to computer
    #time.clock_settime(CLOCK_REALTIME,b)
    # WARNING! DO NOT UNCOMMENT PREVIOUS LINE OUTSIDE PRODUCTION
    # IT WILL SET YOUR CLOCK. THIS CAUSES MASSIVE INTERNET PROBLEMS.
    # ONLY TEST ON TESTING HARDWARE! 


def check_phone_connection(server_IP,server_port):
    while True == True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_IP,server_port))
        except:
            print("""Server not found. Waiting 5 seconds and trying again.""")
            time.sleep(5)
            continue
        break
    return 0

if __name__ == "__main__":
    set_clock_with_gps(method_used="phone",server_IP="192.168.1.155")

