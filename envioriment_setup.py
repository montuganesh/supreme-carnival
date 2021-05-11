import pip3

#This function from https://stackoverflow.com/questions/4527554/check-if-module-exists-if-not-install-it
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip3.main(['install', package])

packages_to_import = [
    'numpy'
    'time'
    'statistics'
    'gpsd-py3' #This needs citation
    'pynmea2' #This needs citation
    'pigpio'
    ]

#Should I create a virtual envioriment for all of this? GPSD feels like a binding that should go
#in it's own special place. But on the other hand, this will probably use a
#dedicated controller, so it's fine. 