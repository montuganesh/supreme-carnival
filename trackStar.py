from Telescope import Telescope
from basicTrack import basicTrack as angleFunc
from Pointing_Angle import getRA
from astropy.coordinates.name_resolve import NameResolveError
from datetime import datetime

print('Initializing...')

# Server IP and port placeholders
telescope = Telescope(1,1) 

name = input('Input name of celestial body to be tracked: ')
while True:
    try:
        getRA(name)
        print("Located! Beginning tracking...")
        break
    except NameResolveError:
        print("Input name could not be resolved")
        name = input("Please try again: ")

# Using datetime.now as a placeholder
trackParams = {
    'bodyName': name,
    'LAT': Telescope.getLAT,
    'LON': Telescope.getLON,
    'currentTimeDt': datetime.now(), #Telescope.getCurrentTime,
    'currentAngle': Telescope.getAngles
    }

terminateType = telescope.activeTrack(angleFunc, 5, 20, **trackParams)

if terminateType:
    print("Tracking terminated (timeout)")
else:
    print("Tracking terminated (user interrupt)")
    
telescope.shutdown()
