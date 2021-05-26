import Pointing_Angle as pointer

# When called, asks the database where in the sky the celestial body is, and returns the actuation angle necessary
def basicTrack(bodyName, LAT, LON, current_time_dt, currentAngle):
    tALT, tAZ = currentAngle[0], currentAngle[1]
    dAngle = pointer.calcAngle(bodyName, LAT, LON, current_time_dt, tALT, tAZ)
    
    return dAngle