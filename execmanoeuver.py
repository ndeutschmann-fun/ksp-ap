import krpc
from toolbox import *
from time import sleep
from math import exp,sqrt,cos,pi

conn = krpc.connect(name='Launch Program')
vessel = conn.space_center.active_vessel
control = vessel.control
ap = vessel.auto_pilot
ap.reference_frame = vessel.orbit.body.reference_frame
ap.set_pid_parameters(30,0,6)
ap.engage()

if len(control.nodes)<1:
    raise NameError('NoNode')
    

rm = runmode()

mynode = control.nodes[0]


while rm:
    if rm(0):
        dv =  mynode.delta_v
        ########################
        #Only for 1-engine vessels
        for eng in vessel.parts.engines:
            if eng.active:
                Isp=eng.specific_impulse
                break
        ########################
        mdot = vessel.max_thrust/9.82/Isp #mass flowrate
        mfoverm0 = exp(-dv/Isp/9.82)
        dt = vessel.mass*(1-mfoverm0)/mdot
        rm+1
    if rm(1):
        ap.target_direction=mynode.burn_vector(vessel.orbit.body.reference_frame)
        print "ETA: {0:0.2f}".format(mynode.time_to-dt/2)
        if mynode.time_to<dt/2:
            rm+1
    if rm(2):
        dvvec=mynode.remaining_burn_vector(vessel.orbit.body.reference_frame)
        ap.target_direction=dvvec
        tcommand = 0.07*mynode.remaining_delta_v
        control.throttle = min(max(tcommand,0),1)
        if tnorm(dvvec)<0.2:
            rm.finish()


control.throttle = 0

