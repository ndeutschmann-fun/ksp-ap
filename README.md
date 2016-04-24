# My KSP KRPC codes

## Toolbox

A toolbox of small functions used in most my other codes.

* The **runnmode** class provides a nice small framework for programs with a sequence of commands that each need to be repeated. Its use is the following:
  * The constructor has an optional argument that sets up the value of the runmode to something else than 0.
  * A runmode is callable: rm(k) returns **True** if the run mode is k and **False** otherwise.
  * "+" and "-" are overloaded so that rm+k changes the run mode by the corresponding amount.
  * The **reset** method sets back the run mode to 0.
  * The **finish** method sets the mode to -1, which can be used as a terminating condition for the program.
  * A runmode has a truth value, which checks wether the mode is -1.

* The **stage** function takes a vessel as argument and activates its staging

* The **check_engines** function deals with getting rid of fueled out engines under the assumptions that the staging is setup properly (check that you don't only get a subset of your stage that gets fueld out).

* The **tnorm** function returns the norm of a list considered as a vector

* The **curse_centered_addstr(l,pos,scr)** function adds a string **l** at line **pos** in **curse** screen **scr** such that it is centered horizontally.



## KSP

This is a mini-library that allows you yo have an interactive **KRPC** session in your python iterface. Just do **import ksp** and you'll get a connected terminal with a minimal setup: the active ship (**vessel**), its controls (**control**) and its autopilot (**ap**).

## Launch

A fairly generic launch code. It only uses kinematic information (acceleration and speed) as input for its controls so that it should not depend on your rocket too much as long as your engines are well aligned and you have enough torque control. In practice, there is a significant difference between the ideal situation and real-life - due to the finite time needed to rotate to desired directions and aerodynamic forces - so that some parameter adjustment is needed.

The altitude target for the orbit is called **alttarg**

The launch sequence is the following:

* Start Engines. If there is a Launch Clamp, release it *after ignition*. (Run Mode 0)

* Point straight up and wait for speed to build up (75m/s). (Run Mode 1)

* Tilt the direction by 5° East and wait for more speed to build up (200m/s). (Run mode 2)

* Point prograde and keep a target acceleration, which transitions smoothly between **gmax** and **gmin**, with a steep drop-off at **transition_altitude** (gaussian transition). (Run mode 3)

* If the ship is has a pitch below 25°, transition to keeping the apoapsis 40s away. (Run mode 4)

* When the pitch is below 1°, throttle up proportionally to your distance to the target altitude until the target apoapsis is reached. (Run mode 5)

* Coast until outside of the atmosphere. (Run mode 6)

* If needed, throttle up to compensate for drag and reach the target apoapsis again. (Run mode 6)

* Compute the burn time accurately using the rocket equation and the *vis viva* equation. (Run mode 8)

* When the apoapsis is half the burn time away, fire the engines. (Run mode 9)

* Keep a P-loop on the throttle until the right speed is achieved. (Run mode 10)

## Suicide Burn

## Execute Manoeuver

## Hover
