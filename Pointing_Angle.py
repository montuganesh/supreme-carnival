import numpy as np
from astropy.time import Time
from astropy import coordinates as coord
#Make sure all of the inputs are in (decimal) degrees, not hours.
def getAltAz(RA,DEC,LAT,LON,LST):
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
    AZ = 0
    if np.sin(np.radians(HA)) < 0:
        AZ = B
    else:
        AZ = 360-B
    return ALT,AZ

def getJ2000(dt):
    #dt is the datetime object we want the J2000 date of
    #a is a placeholder variable
    a = str(dt)
    #d is the date and time in a format that the astropy package needs
    d = a.replace(" ","T",1)
    t = Time(d,format = 'isot', scale = 'utc')
    #t.jd returns the current date/time in terms of julian days (days since some date ~6000 years ago)
    j = t.jd - 2451545.0
    #to convert to J2000, subtract the number above
    return j

def getTime(dt):
    #dt is the datetime object we want the decimal time from
    a = str(dt)
    time = a[11:]
    hour = float(time[0:2])
    minute = float(time[3:5])
    second = float(time[6:])
    decTime = hour + minute/60 + second/3600
    return decTime

def getLST(J, LON, NOW):
    #J is a placeholder variable, use the getJ2000 function for j
    #LON is Longitude
    #NOW is the current UTC time.  Make sure that NOW is in decimal hours, use getTime
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

def getRA(name):
    c = coord.SkyCoord.from_name(name, frame='icrs')
    #The above line returns some high-level object containing the information we want
    d = c.to_string('decimal')
    #The .to_string() method for this object returns the right ascension and declination, separated by a space
    e = d.split()
    #The .split() separates the string into a list, using spaces as the points of separation
    RA = float(e[0])
    #Since right ascension is the first value listed from the .to_string() method, it is the first item in the list
    return RA

def getDEC(name):
    c = coord.SkyCoord.from_name(name, frame='icrs')
    d = c.to_string('decimal')
    e = d.split()
    DEC = float(e[1])
    #Since declination is the second value listed from the .to_string() method, it is the second item in the list
    return DEC

def calcAngle(name,LAT,LON,dt,tALT,tAZ):
    RA = getRA(name)
    DEC = getDEC(name)
    J2000 = getJ2000(dt)
    NOW = getTime(dt)
    LST = getLST(J2000,LON,NOW)
    ALT,AZ = getAltAz(RA,DEC,LAT,LON,LST)
    # print(f"Alt: {ALT}, Az: {AZ}")
    diff = getAngleDiff(ALT,AZ,tALT,tAZ)
    return diff