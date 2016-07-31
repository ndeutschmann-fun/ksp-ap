import krpc
from toolbox import *
from time import sleep

import curses
from math import exp,sqrt

debug = True

if not debug:
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.border(0)
    curses.cbreak()
    stdscr.keypad(1)
    curses.noecho()
    stdscr.nodelay(1)
    lin,col = 18,40
    curses.resizeterm(lin, col)

conn = krpc.connect(name='Launch Program')
vessel = conn.space_center.active_vessel
control = vessel.control
ap = vessel.auto_pilot


rm = runmode()

# Target Orbit
alttarg = 100000
# G-force program:
gmin = 1.1
gmax = 1.35
transition_altitude = 25000

ap.target_pitch_and_heading(90,90)
ap.engage()
ap.set_pid_parameters(10,0,0.1)
control.throttle = 1

altitude = conn.add_stream(getattr,vessel.flight(),'mean_altitude')
airspeed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.reference_frame),'velocity')
orbspeed = conn.add_stream(getattr,vessel.flight(vessel.orbit.body.non_rotating_reference_frame),'velocity')
t = conn.add_stream(getattr,conn.space_center,'ut')

while rm:

#Target G-force
    gtgt = gmin+(gmax-gmin)*exp(- (altitude())**2/(2*transition_altitude**2))

#####PRINT####
    if not debug:
        stdscr.clear()
        stdscr.border(0)
        title = "------Launch Program------"
        curse_centered_addstr(title,2,stdscr)
        stdscr.addstr(4,2,str(rm))
        stdscr.addstr(9,1,"Air speed: {:2f}".format(tnorm(airspeed())))
        stdscr.addstr(11,1,"G-Force: {:2f}".format(vessel.flight().g_force))
        stdscr.addstr(12,1,"G-Force Target: {:2f}".format(gtgt))
        if rm(4):
            stdscr.addstr(14,1,"Distance to optimal Apoapsis ETA: {:2f}".format(deta))
            stdscr.addstr(15,1,"Throttle Increment: {:2f}".format(throttcommand))
        if rm(9):
            stdscr.addstr(11,1,"Time to burn: {}".format(ApoUT - t() < circT/2.))
            stdscr.addstr(12,1,"Delta V: {:2f}".format(circDV))
            stdscr.addstr(13,1,"Circularization time: {:2f}".format(circT))
            stdscr.addstr(16,1,"PITCH: {:2f}".format(vessel.flight().pitch))
        key = stdscr.getch()
        if key!=-1:
            try:
                stdscr.addstr(12,4,"Key Press Detected: "+chr(key))
            except ValueError:
                pass
        if key ==ord('t') :
            rm.finish()
            stdscr.addstr(13,15,"Terminating !")
            stdscr.refresh()
####PRINT####

    sleep(0.05)
    if control.current_stage < 3:
        ap.set_pid_parameters(5,0,0.01)
    if rm(0): #Ignite engines, then open clamps
        stage(vessel)
        if len(vessel.parts.launch_clamps) > 0:
            sleep(0.1)
            stage(vessel)
        rm+1
        continue
    if rm(1): # Go straight up until fast enough
         if tnorm(airspeed()) > 100:
            rm+1
    if rm(2): # Initiate gravity turn
        ap.target_pitch_and_heading(75,90)
        if tnorm(airspeed())>150:
            rm+1
            tmem = t()
    if rm(3): # Keep prograde until the target apoapsis is reached or the ship is horizontal enough
        ap.reference_frame = vessel.surface_velocity_reference_frame
        if altitude() > 35000: ## Transition from surface prograde to orbit prograde
            ap.reference_frame = vessel.orbital_reference_frame
        ap.target_direction = (0,1,0)
        acc = vessel.flight().g_force
        control.throttle += 0.1*(gtgt-acc)
        tmem = t()
        if vessel.orbit.apoapsis_altitude > alttarg:
            rm+3
        if vessel.flight().pitch < 25:
            detamem = 70-vessel.orbit.time_to_apoapsis
            throttcommand = 0
            rm+1
    if rm(4): # Keep the apoapsis 40s away until the ship is completely horizontal
        deta = (70 - vessel.orbit.time_to_apoapsis)
        dt = t()-tmem
        if dt > 0:
            throttcommand = 0.2*deta + 0.02*(detamem-deta)/dt
            control.throttle = max(min(throttcommand,1),0)
        tmem = t()
        detamem = deta
        if vessel.orbit.apoapsis_altitude > alttarg:
            rm+2
        if vessel.flight().pitch < 1:
            rm+1
    if rm(5):
        control.throttle=(alttarg-altitude())/alttarg
        if vessel.orbit.apoapsis_altitude > alttarg:
            rm+1
    if rm(6):
        control.throttle = 0
        if altitude() > 70000:
            if vessel.orbit.apoapsis_altitude<alttarg-100:
                control.throttle = 0.1
            if vessel.orbit.apoapsis_altitude>alttarg-100:
                rm+1
    if rm(7):
        if vessel.orbit.apoapsis_altitude > alttarg:
            control.throttle = 0
            rm+1
    if rm(8):
        ecc = vessel.orbit.eccentricity
        mu = vessel.orbit.body.gravitational_parameter
        a = vessel.orbit.semi_major_axis
        circDV = sqrt(mu/a)*(1-sqrt(1-ecc))/(1+ecc)
        ########################
        #Only for 1-engine vessels
        for eng in vessel.parts.engines:
            if eng.active:
                Isp=eng.specific_impulse
                break
        ########################
        mdot = vessel.max_thrust/9.82/Isp #mass flowrate
        mfoverm0 = exp(-circDV/Isp/9.82)
        circT = vessel.mass*(1-mfoverm0)/mdot
        ApoUT = t()+vessel.orbit.time_to_apoapsis
        rm+1

    if rm(9):
        if ApoUT - t() < circT/2.:
            control.throttle = 1
            vtarg=sqrt(mu/vessel.orbit.apoapsis)
            rm+1
    if rm(10):
        control.throttle = 0.1*(vtarg-tnorm(orbspeed()))
        if tnorm(orbspeed()) > vtarg:
            rm.finish()

    check_engines(vessel)

vessel.control.throttle = 0
sleep(5)
curses.endwin()
