import Pointing_Angle as pointer

# When called, asks the database where in the sky the celestial body is, and returns the actuation angle necessary
def basicTrack(bodyName, LAT, LON, current_time_dt, currentAngle):
    
    dAngle = pointer.calcAngle(bodyName, LAT, LON, current_time_dt, *currentAngle)
    
    return dAngle