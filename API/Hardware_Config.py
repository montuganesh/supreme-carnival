# Config
# pin numbers in GPIO.BCM (Broadcom) configuration

azMotorCfg = {
    'PUL': 17,
    'DIR': 27,
    'PWMCLOCKS': [10,20,40,50,80,100,160,200,250,320,400,500,800,1000,1600,2000,4000,8000],     #Hz
    'MCSTP': 400,       # pulses per revolution (400 minimum)
    'MXSPD': 1800,       # max motor rotation speed in degrees/sec, must be an element of PWMCLOCKS / MCSTP * 360 (Currently capped at 1000 Hz, will look into this but probably wont need to go faster)
    'MXACC': 300,        # max motor acceleration in degrees/sec^2.
    }

altMotorCfg = {
    'PUL': 15,
    'DIR': 17,
    # etc.
    }