import krpc, curses, time, sys
import os
import numpy as np
import numpy.linalg as la

conn = krpc.connect(name='Docking Guidance')
vessel = conn.space_center.active_vessel
control = vessel.control

altitude_target = 10

def tdef(vessel):
    g = vessel.orbit.body.surface_gravity
    return g*vessel.mass/vessel.available_thrust


kp = 0.1
kd = 0.1

tmem = conn.space_center.ut
altmem = vessel.flight().surface_altitude
tmemprint = conn.space_center.ut - 0.1
while not control.get_action_group(1):
    
    alt=vessel.flight().surface_altitude
    dt = conn.space_center.ut-tmem
    if dt>0:
        vessel.control.throttle = tdef(vessel)+kp*(altitude_target-alt)+kp*(altmem-alt)/dt
        if (conn.space_center.ut-tmemprint>0.2):
            os.system('clear')
            print "Delta: "+str(altitude_target-alt)
            print "Thrott: "+str(kp*(altitude_target-alt)+kp*(altmem-alt)/dt)
            tmemprint = conn.space_center.ut
        tmem = conn.space_center.ut
        tmem = alt
