from numpy.linalg import *
from numpy import array


def curse_centered_addstr(l,pos,scr):
    my,mx=scr.getmaxyx()
    try:
        scr.addstr(pos,mx/2-len(l)/2,l)
    except ERR:
        scr.addstr(my-1,0,"ERROR IN PRINTING")
        pass


def stage(vess):
    vess.control.activate_next_stage()

class runmode:
    def __init__(self,mode=0):
        self.mode = mode
    def __add__(self,n):
        self.mode = self.mode+n
    def __sub__(self,n):
        self.mode = self.mode-n
    def reset(self):
        self.mode = 0
    def finish(self):
        self.mode = -1
    def __nonzero__(self):
        return not self.mode == -1
    def __call__(self,n):
        return self.mode == n
    def __str__(self):
        return "Run Mode: "+str(self.mode)

def check_engines(vessel):
    for eng in vessel.parts.engines:
        if not eng.has_fuel:
            stage(vessel)
            break

def tnorm(tu):
    return float(linalg.norm(array(tu)))
