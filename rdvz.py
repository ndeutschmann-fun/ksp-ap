import krpc
from toolbox import *
from time import sleep
from math import exp,sqrt, acos,pi, pow
conn = krpc.connect(name='Launch Program')
vessel = conn.space_center.active_vessel
tgt = conn.space_center.target_vessel
control = vessel.control
ap = vessel.auto_pilot
now = conn.add_stream(getattr,conn.space_center,'ut')
orbspeed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.non_rotating_reference_frame),'velocity')

# Input Parameters
r = vessel.orbit.apoapsis
R = tgt.orbit.apoapsis
Dr = R-r
mu = vessel.orbit.body.gravitational_parameter

xch = vessel.position(vessel.orbit.body.non_rotating_reference_frame)
xtgt = tgt.position(tgt.orbit.body.non_rotating_reference_frame)
xch = xch
xtgt = xtgt
alpha = acos((xch[0]*xtgt[0]+xch[1]*xtgt[1]+xch[2]*xtgt[2])/tnorm(xch)/tnorm(xtgt))
t= now()

# Hohman transfer parameters
a = (r+R)/2.
TransferTime = pi*sqrt(a**3/mu)
delta = 2.*pi*(1/2. - pow(1.+r/R,3./2.)/4./sqrt(2) )
vp = sqrt(mu*(2./r - 1./a))
Dv = vp-sqrt(mu/r)

## Only for 1-engine vessels
for eng in vessel.parts.engines:
    if eng.active:
        Isp=eng.specific_impulse
        break

mdot = vessel.max_thrust/9.82/Isp #mass flowrate
mfoverm0 = exp(-Dv/Isp/9.82)
Bt = vessel.mass*(1-mfoverm0)/mdot

# Transfer Timing

Dw = sqrt(mu)/pow(r,1.5)*(pow(1+Dr/r,1.5)-1)/pow(1+Dr/r,1.5)
beta = alpha-delta
Dt = beta/Dw
Tt = t+Dt

BurnDate = Tt-Bt/2.

#Arrival Timing # This could maybe be put after the transfer burn!
ArrivalDate = Tt + TransferTime
vpa = sqrt(mu/R)
Dv = vpa-sqrt(mu*(2./R-1./a))
mfoverm0 = exp(-Dv/Isp/9.82)
Bt = vessel.mass*(1-mfoverm0)/mdot
ArrivalBurnDate = ArrivalDate-Bt/2.

rm = runmode()

ap.reference_frame = vessel.orbital_reference_frame
ap.target_direction = (0,1,0)
ap.engage()

while rm:
    if rm(0):
        print "Burn in "+str(BurnDate-now())+"s"
        if now()>=BurnDate:
            rm+1
    if rm(1):
        print "Delta v: "+str(vp-tnorm(orbspeed()))
        control.throttle = 0.1*(vp-tnorm(orbspeed()))
        if abs(tnorm(orbspeed())-vp)<0.1:
            control.throttle=0
            rm+1
    if rm(2):
        print "Burn in "+str(ArrivalBurnDate-now())+"s"
        if now()>=ArrivalBurnDate:
            rm+1
    if rm(3):
        print "Delta v: "+str(vpa-tnorm(orbspeed()))
        control.throttle = 0.1*(vpa-tnorm(orbspeed()))
        if abs(tnorm(orbspeed())-vpa)<0.1:
            control.throttle=0
            rm.finish()
