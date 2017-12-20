import sys
import pyparsing
from pprint import pprint
from functools import reduce
from pyparsing import Literal, Word, Forward, Group, nums, Regex, oneOf, StringEnd, OneOrMore

L = Literal
Ls = lambda expr: L(expr).suppress()

# atoms
integer = Word(nums + '-')
integer.setParseAction(lambda t: int(t[0]))
comma = Ls(',')
vector = Group( Ls('<') + integer + comma + integer + comma + integer + Ls('>') )
vector.addParseAction(lambda t: tuple(t[0]))
p, v, a = L('p'), L('v'), L('a')
eq = Ls('=') 
row = Group(Group(p + eq + vector) + comma + Group(v + eq + vector) + comma + Group(a + eq + vector))
document = OneOrMore(row) + StringEnd()

def vadd(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2])

def vmul(c, x):
    return (c*x[0], c*x[1], c*x[2])

def l1(x):
    return abs(x[0]) + abs(x[1]) + abs(x[2])

class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a
        self.id = None
        self.dead = False

    def __repr__(self):
        return "Particle(id={}, p={!r}, v={!r}, a={!r})".format(self.id, self.p, self.v, self.a)

    def at_time(self, t):
        return reduce(vadd, [
            self.p,
            vmul(t, self.v),
            vmul((t+1)*t/2, self.a)
        ])


def parse(src):
    rows = document.parseString(src).asList()
    particles = [ Particle(**dict(row)) for row in rows ]
    for i, part in enumerate(particles):
        part.id = i
    return particles


if __name__ == "__main__":
    src = open(sys.argv[1]).read()
    particles = parse(src)
    # part 1 solution
    #big_t = 10000
    #particles = sorted([ (l1(part.at_time(big_t)), part.at_time(big_t), part) for part in particles ])[:5]

    # part 2 solution
    for t in range(1000):
        positions = [ (particle.at_time(t), particle) for particle in particles ]
        for px, partx in positions:
            for py, party in positions:
                if partx.id < party.id and px == py:
                    print("{!r} collided with {!r} at t={}, p={}".format(partx, party, t, px))
                    partx.dead = True
                    party.dead = True

        particles = [ p for p in particles if not p.dead ]
        if t % 100 == 0:
            print("{} particles remaining at t={}".format(len(particles), t))
    pprint(particles, width=80)


