import sys
from functools import reduce
from heapq import heappush, heappop, heapify
from math import pi, sin, cos, sqrt, hypot

def vector_add(a,b):
    return (float(a[0] + b[0]), float(a[1] + b[1]))

def hex_normalize(a):
    x, y = a

    # TODO: even/odd row logic
    xstep = sqrt(3)/2
    x = xstep * round(x/xstep)

    ystep = 0.5
    y = ystep * round(y/ystep)

    return (x,y)



def vector_subtract(a,b):
    return (float(a[0] - b[0]), float(a[1] - b[1]))

def distance(a,b):
    return hypot(a[0]-b[0], a[1]-b[1])


def polar(r, t):
    return (r*cos(t), r*sin(t))

def hex_unit(index):
    return polar(1, index*pi/3 + pi/6)

COMPASS = {
    'ne': hex_unit(0),
    'n': hex_unit(1),
    'nw': hex_unit(2),
    'sw': hex_unit(3),
    's': hex_unit(4),
    'se': hex_unit(5),
}
def compass(direction):
    return COMPASS[direction]

def hex_neighborhood(p):
    for i in range(0, 6):
        yield 1.0, hex_normalize(vector_add(p, hex_unit(i)))

def a_star(start, goal):
    def h(point):
        d = distance(point, goal)
        if d < 0.25: d = 0.0
        return d

    def unwind_path(p):
        while p:
            yield p
            p = prev.get(p, None)

    g = { start: 0.0 }
    closed_set = set()
    frontier = [ (g[start]+h(start), start)]
    prev = {}

    while frontier:
        old_f, point = heappop(frontier)
        closed_set.add(point)
        if h(point) == 0:
            return list(reversed(list(unwind_path(point))))
        for d, neighbor in hex_neighborhood(point):
            if neighbor in closed_set: continue
            new_g = g[point] + d
            if neighbor not in g:
                g[neighbor] = new_g
                heappush(frontier, (new_g+h(neighbor), neighbor))
                prev[neighbor] = point
            elif new_g < g[neighbor]:
                g[neighbor] = new_g
                prev[neighbor] = point
                if neighbor not in closed_set:
                    frontier = [ (f,p) for f,p in frontier if p != neighbor ]
                    heapify(frontier)
                    heappush(frontier, (new_g+h(neighbor), neighbor))

def movify(path):
    points = iter(path)
    try:
        prev_point = next(points)
        while True:
            next_point = next(points)
            move_vector = vector_subtract(next_point, prev_point)
            for direction, compass_vector in COMPASS.items():
                if distance(compass_vector, move_vector) < 1e-6:
                    yield direction
            prev_point = next_point
    except StopIteration:
        pass

def furthest(moves):
    largest_distance = 0
    furthest_point = (0,0)
    position = (0,0)
    for move in moves:
        move_vector = compass(move)
        position = hex_normalize(vector_add(position, move_vector))
        if distance( (0,0), position) > largest_distance:
            largest_distance = distance( (0,0), position)
            furthest_point = position
    return furthest_point


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        fin = open(sys.argv[1])
    else:
        fin = sys.stdin
    moves = [m.strip() for m in fin.read().split(',')]
    #goal = reduce(vector_add, (compass(m) for m in moves))
    goal = furthest(moves)
    print('goal point: {}'.format(goal))
    path = a_star((0,0), goal)
    #print(path)
    moves = list(movify(path))
    print(' '.join(moves))
    print(len(moves))



