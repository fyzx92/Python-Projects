"""
Authored by Bryce Burgess

three body simulation

"""

def add_vecs(v1,v2):
    return [x+y for i,j in zip(v1, v2)]

class Body():
    def __init_(self, _pos, _mass = 1):
        self.mass = _mass
        self.pos = list(_pos)
        self.vel = 0
        self.acc = 0

    def apply_force(self, force, *fargs, **fkwargs):
        if fargs or fkwargs:
            f = force(fargs, fkwargs)
        else:
            f = force
        # need to divide force by mass
        self.acc = add_vecs(self.acc, f)

class Simulation():
    def __init__(self):
        self.b1 = Body()
        self.b2 = Body()
        self.b3 = Body()

        self.time = 10000

    def run(self):
        for t in range(self.time):

