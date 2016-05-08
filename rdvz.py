import krpc
from toolbox import *
from time import sleep
from math import exp,sqrt, acos
conn = krpc.connect(name='Launch Program')
vessel = conn.space_center.active_vessel
tgt = conn.space_center.target_vessel
control = vessel.control
ap = vessel.auto_pilot

r = vessel.orbit.apoapsis
R = tgt.orbit.apoapsis
Dr = R-r
mu = vessel.orbit.body.gravitational_parameter

xch = vessel.position(vessel.orbit.body.non_rotating_reference_frame)
xtgt = vessel.position(vessel.orbit.body.non_rotating_reference_frame)
xch = xch/tnorm(xch)
xtgt = xtgt/tnorm(xtgt)
alpha = acos(xch[0]*xtgt[0]+xch[1]*xtgt[1]+xch[2]*xtgt[2])

t = conn.space_center.ut
#Checks
if Dr <= 0:
    raise NameError("LowerTarget")

print "Separation angle "+str(alpha)
