import krpc
from toolbox import *
from time import sleep
from math import exp,sqrt

conn = krpc.connect(name='Interactive krpc')
vessel = conn.space_center.active_vessel
control = vessel.control
ap = vessel.auto_pilot
