import numpy as np
from astropy.time import Time
from datetime import datetime
from datetime import date
from datetime import time
#Make sure all of the inputs are in (decimal) degrees, not hours.
def AltAz(RA,DEC,LAT,LON,LST):
    #Use this to compute the Altitude and Azimuth of the celestial object
    #RA is Right Ascension 
    #DEC is Declination
    #LAT is Latitude
    #LON is Longitude
    #LST is Local Sideral Time
    HA = LST-RA
    #HA is Hour Angle
    if HA < 0:
        HA +=360
    A = np.sin(np.radians(DEC))*np.sin(np.radians(LAT))+np.cos(np.radians(DEC))*np.cos(np.radians(LAT))*np.cos(np.radians(HA))
    ALT = np.degrees(np.arcsin(A))
    #Final Altitude
    B = np.degrees(np.arccos((np.sin(np.radians(DEC))-np.sin(np.radians(ALT))*np.sin(np.radians(LAT)))/(np.cos(np.radians(ALT))*np.cos(np.radians(LAT)))))
    print(B)
    print(np.sin(np.radians(HA)))
    print(HA)
    AZ = 0
    if np.sin(np.radians(HA)) < 0:
        AZ = B
    else:
        AZ = 360-B
    return ALT,AZ

def getJ2000():
    #a is a placeholder variable
    a = str(datetime.utcnow())
    #d is the date and time in a format that the astropy package needs
    d = a.replace(" ","T",1)
    t = Time(d,format = 'isot', scale = 'utc')
    #t.jd returns the current date/time in terms of julian days (days since some date ~6000 years ago)
    j = t.jd - 2451545.0
    #to convert to J2000, subtract the number above
    return j

#The getNOW function should be obsolete because of the satellite time function.

def getNOW():
    #used for getting current UTC decimal time, for the getLST function
    a = str(datetime.now())
    time = a[11:]
    hour = float(time[0:2])
    minute = float(time[3:5])
    second = float(time[6:])
    decTime = hour + minute/60 + second/3600
    return decTime

def getLST(J, LON, NOW):
    #J is a placeholder variable, use the getJ2000 function for j
    #LON is Longitude
    #NOW is the current UTC time.  Make sure that NOW is in decimal hours, use getNOW
    lst = 100.46 + 0.985647*J + LON + 15*NOW
    if lst < 0:
        lst+= 360
    return lst

def getAngleDiff(ALT,AZ,tALT,tAZ):
    #ALT is Altitude of object
    #AZ is Azimuth of object
    #Get these from AltAz function
    #tALT is the Altitude that the Telescope is currently pointing at
    #tAZ is the Azimuth that the Telescope is currently pointing at
    altDiff = tALT - ALT
    azDiff = tAZ - AZ
    return altDiff,azDiff