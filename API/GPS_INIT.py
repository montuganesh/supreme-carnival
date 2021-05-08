#!/usr/bin/env python3

from slowGPS import slowGPS
from set_system_time import set_clock_with_gps

# We need a place to set system time, ensure the gps system is working,
# and generate the average fix. GPS_API can give