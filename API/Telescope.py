import numpy as np
import time 
import sys
from Motor import Motor  
from Encoder import Encoder
# from UNITS_API import UNITS_API as GPS
from Hardware_Config import azMotorCfg, altMotorCfg
import pigpio

# import set_system_time

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
    currentAngle = np.array([alt, az])
    
    LAT, LON = None, None
    gps = None
    
    def __init__(self, server_IP, server_port):
        #Telescope.gps = GPS(server_IP, server_port) #Hangs until done - this is deliberate
        
        #Telescope.LAT, Telescope.LON = Telescope.gps.getLocation()

        initialAzAngle = self.getAzAngle()
        initialAltAngle = self.getAltAngle()
        initialAngle = np.array([initialAltAngle, initialAzAngle])
        Telescope.currentAngle = initialAngle


    # Absolute target angle is passed in
    def target(self, angle):
        dAngle = np.asarray(angle) - Telescope.currentAngle
        self.actuate(dAngle)
        
        
    # Relative angle is passed in
    def actuate(self, dAngle):
        
        constraints_passed = self.checkConstraints(dAngle)
        
        if constraints_passed: 
            try:
                alt_actuation_angle = dAngle[Telescope.alt]*Telescope.gearRatio
                az_actuation_angle = dAngle[Telescope.az]*Telescope.gearRatio
                print(f"Alt: {alt_actuation_angle}")
                print(f"Az: {az_actuation_angle}")
                Telescope.altMotor.actuate(alt_actuation_angle)
                Telescope.azMotor.actuate(az_actuation_angle)
                
            except KeyboardInterrupt:
                Telescope.altMotor.cancel()
                Telescope.azMotor.cancel()
        else:
            print("Target angle outside of physical constraints... \nCommand was aborted")
            
    
    def activeTrack(self, angleFunc, timeDelta=1, trackTime=None, **kwargs):
        # Begins a loop over either a certain trackTime (float) or until user override (None)
        # kwargs takes in a  dictionary of arguments for angleFunc. 
        # If angleFunc requires information from the telescope at runtime (runtime variables),
        # the value in the dictionary should be the name of 'getter' Telescope function that returns the desired value.
        # For example, if angleFunc(telescope_az_angle) takes in the az angle of the telescope, kwargs should contain
        # kwargs = {'telescope_az_angle': Telescope.getAzAngle}
        # Otherwise, variables not contained in the Telescope class are accepted too.
        
        # I don't know how I'm supposed to interface with the GPS time from here, just using python time as placeholder
        startTime = time.time()
        
        try:
            endTime = startTime + trackTime
        except TypeError:
            endTime = None
            
        
        keepRunning = True        
        
        try:
            # Main Loop
            while keepRunning:
                now = time.time()
                
                # Sleeps until sufficient time has passed
                while time.time() - now < timeDelta:
                    # We really don't need a high sleep resolution, might increase this value significantly
                    time.sleep(0.1)
                        
                # Handles runtime variables in kwargs
                for key in kwargs:
                    if callable(kwargs[key]):
                        kwargs[key] = self.kwargs[key]()
                
                # Call angleFunc which returns angle difference as [alt, az], then actuate.
                dAngle = angleFunc(**kwargs)
                self.actuate(dAngle)
                
                
                if not trackTime:
                    keepRunning = True 
                else:
                    keepRunning = now < endTime
        
        except KeyboardInterrupt:
            Telescope.altMotor.cancel()
            Telescope.azMotor.cancel()
            print("Keyboard interrupt...")
        
        print("Active tracking terminated")

            
    def checkConstraints(self, dAngle):        
        # Limitations on single instance actuation
        d_az_min, d_az_max = -180, 180      # We don't want to actuate more than hald a full rotation in one go -- thats just inefficient
        d_alt_min, d_alt_max = -90, 90
        
        # Limitations on absolute actuation
        az_min, az_max = 0, 360             # Really up to Collin based on the design. I say we keep within one revolution to simplify the encoder's job
        alt_min, alt_max = 0, 90            # Spherical polar coordinates constraints (0 to 90 or 90 to 0?)
        
        d_alt = dAngle[Telescope.alt]
        d_az = dAngle[Telescope.az]
        
        next_alt = d_alt + Telescope.currentAngle[Telescope.alt]
        next_az = d_az + Telescope.currentAngle[Telescope.az]
        
        d_az_good, d_alt_good, az_good, alt_good = False, False, False, False
        
        if d_az >= d_az_min and d_az <= d_az_max:
            d_az_good = True
        else:
            print(f"Input change in azimuthal angle is not within constraints, must be within [{d_az_min}, {d_az_max}]")
        if d_alt >= d_alt_min and d_alt <= d_alt_max:
            d_alt_good = True
        else:
            print(f"Input change in altitudinal angle is not within constraints, must be within [{d_alt_min}, {d_alt_max}]")
        if  next_az >= az_min and next_az <= az_max:
            az_good = True
        else:
            print(f"Azimuthal angle after execution will not be within constraints, must be within [{az_min}, {az_max}]")
        if next_alt >= alt_min and next_alt <= alt_max:
            alt_good = True
        else:
            print(f"Altitudinal angle after execution will not be within constraints, must be within [{alt_min}, {alt_max}]")

        return d_az_good and d_alt_good and az_good and alt_good

        
        
    def getAngles(self):
        azAngle = self.getAzAngle()
        altAngle = self.getAltAngle()
        angle = np.array([azAngle, altAngle])
        return angle
    
    def getAzAngle(self):
        azAngle = Telescope.azEncoder.getAngle()
        #return azAngle
        return 170
        
    def getAltAngle(self):
        altAngle = Telescope.altEncoder.getAngle()
        #return altAngle
        return 50
    
    def getLAT(self):
        return Telescope.LAT
    
    def getLON(self):
        return Telescope.LON
    
    def getGearRatio(self):
        return Telescope.gearRatio
    
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
