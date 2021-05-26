# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:59:12 2021

@author: Sam Crossley
"""

import Motor
from Hardware_Config import azMotorCfg as az_cfg
from Harware_Config import altMotorCfg as alt_cfg

az_motor = Motor.Motor(az_cfg)
alt_motor = Motor.Motor(alt_cfg)

az_motor.actuate(360)
alt_motor.actuate(-360)