import krpc
from toolbox import *
from time import sleep
from math import exp,sqrt,cos,pi,acos


conn = krpc.connect(name='Land Program')
vessel = conn.space_center.active_vessel
control = vessel.control
ap = vessel.auto_pilot
ap.reference_frame = vessel.surface_velocity_reference_frame
ap.set_pid_parameters(20,0,4)
ap.engage()


rm = runmode()

nengines = 4 # ONLY FOR IDENTICAL ENGINES

while rm:
    if rm(0):
        dv = vessel.flight(vessel.orbit.body.reference_frame).speed
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
        ap.target_direction=(0,-1,0)
        rm+1
    if rm(1):
        dir=vessel.direction(vessel.surface_velocity_reference_frame)
        angle = acos(abs(dir[1]/tnorm(dir)))*(360./(2.*pi))
        if angle < 1:
            rm+1
    if rm(2):
        dvvec=vessel.flight(vessel.orbit.body.reference_frame).velocity
        tcommand = 0.1*tnorm(dvvec)
        control.throttle = min(max(tcommand,0),1)
        if tnorm(dvvec)<5:
            control.throttle=0
            rm+2
            continue
        dir=vessel.direction(vessel.surface_velocity_reference_frame)
        angle = acos(abs(dir[1]/tnorm(dir)))*(360./(2.*pi))
        if angle > 5:
            control.throttle=0
            rm+1
    if rm(3):
        dir=vessel.direction(vessel.surface_velocity_reference_frame)
        angle = acos(abs(dir[1]/tnorm(dir)))*(360./(2.*pi))
        if angle <2:
            rm-1
    if rm(4):
        v=vessel.flight(vessel.orbit.body.reference_frame).speed
        T=0
        for eng in vessel.parts.engines:
            if eng.active:
                T=T+eng.available_thrust
#                break        
        g = vessel.orbit.body.surface_gravity
        m = vessel.mass
        hburn = v*v/(T/m-g)/2
        print "{:2.2f} {:2.2f}".format(hburn,vessel.flight(ap.reference_frame).surface_altitude)
        if vessel.flight(ap.reference_frame).surface_altitude < hburn + 50:
            rm+1
            control.throttle = 1
    if rm(5):
        if vessel.flight(vessel.orbit.body.reference_frame).speed < 7:
            rm+1
    if rm(6):
        print vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
        m = vessel.mass
        v=vessel.flight(vessel.orbit.body.reference_frame).speed
        tcommand = v-5
#        print min(max(0.05*tcommand + m*g/T,0),1)
        control.throttle = min(max(0.1*tcommand + m*g/T,0),1)
        if vessel.flight(vessel.orbit.body.reference_frame).surface_altitude < 10:
            rm+1
    if rm(7):
        print vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
        ap.reference_frame = vessel.surface_reference_frame
        ap.target_direction = (1,0,0)
        m = vessel.mass
        v=vessel.flight(vessel.orbit.body.reference_frame).speed
        tcommand = v-0.5
        control.throttle = min(max(0.1*tcommand + m*g/T,0),1)
        if vessel.flight(vessel.orbit.body.reference_frame).surface_altitude < 5:
            rm.finish()
            control.throttle=0


control.throttle = 0
sleep(10)
