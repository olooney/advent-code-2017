import sys

def find_bridges(parts, partial_bridge=[]):
    port = partial_bridge[-1][1] if partial_bridge else 0 
    for index, part in enumerate(parts):
        if part[0] == port or part[1] == port:
            if part[1] == port and part[0] != port:
                part = (part[1], part[0])
            bridge = partial_bridge + [part]
            remaining_parts = parts.copy()
            del remaining_parts[index]
            yield from find_bridges(remaining_parts, bridge)
    if partial_bridge:
        yield partial_bridge

def strength_of(bridge):
    return sum( sum(part) for part in bridge )

def inline(bridge):
    return "--".join(["{}/{}".format(*part) for part in bridge])

def read_parts(lines):
    parts = []
    for line in lines:
        part = tuple([int(n) for n in line.split('/')])
        parts.append(part)
    return parts

if __name__ == '__main__':
    with open(sys.argv[1]) as fin:
        parts = read_parts(fin)
        possible_bridges = find_bridges(parts)
        bridge_ranks = sorted([ (len(bridge), strength_of(bridge), bridge) for bridge in possible_bridges ])
        for length, strength, bridge in bridge_ranks[-10:]:
            print(inline(bridge), ":", length, ':', strength)
