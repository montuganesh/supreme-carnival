import numpy as np
import time 
import sys
from Motor import Motor  
from Encoder import Encoder
from UNITS_API import UNITS_API
from Hardware_Config import azMotorCfg, altMotorCfg
import pigpio

import set_system_time

class Telescope():

    # Class variables, these are static variables just in case multiple instances of Telescope are created
    # Otherwise, we may have two instances of azMotor pointing to the same hardware, which would be very bad    

    pi = pigpio.pi()
    azMotor = Motor(azMotorCfg)
    altMotor = Motor(altMotorCfg)
    azEncoder = Encoder()
    altEncoder = Encoder()
    
    alt = 0
    az = 1
    gearRatio = 729 #?
    targetAngle = np.array([alt, az])
    currentAngle = np.array([alt, az])

    units_seek = UNITS_API(IP_ADDRESS, PORT)
    
    def __init__(self, server_IP, server_port):
        units_seek = UNITS_API(server_IP, server_port) #Hangs until done - this is deliberate

        initialAzAngle = self.getAzAngle()
        initialAltAngle = self.getAltAngle()
        initialAngle = np.array([initialAzAngle, initialAltAngle])
        Telescope.targetAngle = initialAngle
        Telescope.currentAngle = initialAngle


    # Absolute target angle is passed in
    def target(self, angle):
        dAngle = np.asarray(angle) - Telescope.currentAngle
        self.actuate(dAngle)
        
    # Relative angle is passed in
    def actuate(self, dAngle):
        # Calls on the motors to rotate the telescope to point at the current Telescope.targetAngle
        # Will also include safety features like a constraint test to make sure the target angle is within hardware capabilities
        
        constraints_passed = self.checkConstraints(dAngle)
        
        if constraints_passed: 
            try:
                Telescope.altMotor.actuate(dAngle[Telescope.alt]*Telescope.gearRatio)
                Telescope.azMotor.actuate(dAngle[Telescope.az]*Telescope.gearRatio)
                
            except KeyboardInterrupt:
                Telescope.altMotor.cancel()
                Telescope.azMotor.cancel()
        else:
            print("Target angle outside of physical constraints... \nCommand was aborted")
            
    
    def activeTrack(self, angleFunc, timeDelta=1, trackTime=None, *args):
        # Begins a loop over either a certain trackTime (float) or until user override (None)
        # Takes in a function angleFunc which must return the desired tracking angle as an ndArray in [az, alt] form and runs this angleFunc every timeDelta
        # This function then sets Telescope.targetAngle accordingly and runs self.main() to actuate the motors in the desired manner
        # The *args allow for runtime parameters to be passed into angleFunc (may need to change to *kwargs)
        return
            
    # Not complete
    def checkConstraints(self, dAngle):        
        # Limitations on single instance actuation
        d_az_min, d_az_max = -180, 180      # We don't want to actuate more than hald a full rotation in one go -- thats just inefficient
        d_alt_min, d_alt_max = -90, 90
        
        # Limitations on absolute actuation
        az_min, az_max = -180, 180          # Really up to Collin based on the design. I say we keep within one revolution to simplify the encoder's job
        alt_min, alt_max = 0, 90            # Spherical polar coordinates constraints
        
        # Debug
        return True
        
        
    def getAngles(self):
        azAngle = self.getAzAngle()
        altAngle = self.getAltAngle()
        angle = np.array([azAngle, altAngle])
        return angle
    
    def getAzAngle(self):
        azAngle = Telescope.azEncoder.getAngle()
        return azAngle
        
    def getAltAngle(self):
        altAngle = Telescope.altEncoder.getAngle()
        return altAngle
    
    def shutdown(self):
        Telescope.pi.stop()
        sys.exit(0)
    
    
    # Can this be moved somewhere where it can interact with the GPS? I don't want this in the Telescope class itself
    def calculateDeclination(latitude,altAngle,azAngle):
        declination = np.arcsin(np.sin(latitude)*np.sin(altAngle)+np.cos(latitude)*np.cos(altAngle)*np.cos(azAngle))
        return declination

    def calculateHourAngle(altAngle,latitude,declination,):
        hourAngle = np.arccos((np.sin(altAngle)-np.sin(latitude)*np.sin(declination)) / (np.cos(latitude)*np.cos(declination)))
        return hourAngle

    def calculateLocalSiderialTime():
        LST = hourAngle + rightAscension
        return LST
