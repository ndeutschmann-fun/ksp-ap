# My KSP KRPC codes

## Toolbox

A toolbox of small functions used in most my other codes. In particular, the Runmode class provides a nice small framework for programs with a sequence of commands that each need to be repeated. Its use is the following:

* The constructor has an optional argument that sets up the value of the runmode to something else than 0.
* A runmode is callable: rm(k) returns *True* if the run mode is k and *False* otherwise.
* "+" and "-" are overloaded so that rm+k changes the run mode by the corresponding amount.
* The *reset* method sets back the run mode to 0.
* The *finish* method sets the mode to -1, which can be used as a terminating condition for the program.
* A runmode has a truth value, which checks wether the mode is -1.

## KSP

## Launch

## Suicide Burn

## Execute Manoeuver

## Hover
