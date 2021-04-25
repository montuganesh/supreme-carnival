import numpy as np
import time
from Motor import Motor  
from Encoder import Encoder

class Telescope():
    
    # Class variables, these are static variables just in case multiple instances of Telescope are created
    # Otherwise, we may have two instances of azMotor pointing to the same hardware, which would be very bad    
    
    azMotor = Motor()
    altMotor = Motor()
    azEncoder = Encoder()
    altEncoder = Encoder()
    targetAngle = np.array([])
    
    def __init__(self):
        initialAzAngle = self.getAzAngle()
        initialAltAngle = self.getAltAngle()
        initialAngle = np.array([initialAzAngle, initialAltAngle])
        Telescope.targetAngle = initialAngle
        
    
    def main(self):
        # Calls on the motors to rotate the telescope to point at the current Telescope.targetAngle
        # Will also include safety features like a constraint test to make sure the target angle is within hardware capabilities
        return
    
    
    def activeTrack(self, angleFunc, timeDelta=1, trackTime=None, *args):
        # Begins a loop over either a certain trackTime (float) or until user override (None)
        # Takes in a function angleFunc which must return the desired tracking angle as an ndArray in [az, alt] form and runs this angleFunc every timeDelta
        # This function then sets Telescope.targetAngle accordingly and runs self.main() to actuate the motors in the desired manner
        # The *args allow for runtime parameters to be passed into angleFunc (may need to change to *kwargs)
        return
    
        
    def setTarget(self, angle):
        # Sets a target angle
        return
    
    def getAngles(self):
        azAngle = self.getAzAngle()
        altAngle = self.getAltAngle()
        angle = np.array([azAngle, altAngle])
        return angle
    
    def getAzAngle():
        azAngle = Telescope.azEncoder.getAngle()
        return azAngle
        
    def getAltAngle():
        altAngle = Telescope.altEncoder.getAngle()
        return altAngle
        