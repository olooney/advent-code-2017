import sys
from pprint import pprint

def parse(lines):
    pipes = {}
    for line in lines:
        left, right = line.split('<->')
        left_node = int(left.strip())
        right = [ int(r.strip()) for r in right.split(',') ]
        for right_node in right:
            if left_node not in pipes: pipes[left_node] = []
            if right_node not in pipes: pipes[right_node] = []

            if right_node not in pipes[left_node]:
                pipes[left_node].append(right_node)

            if left_node not in pipes[right_node]:
                pipes[right_node].append(left_node)
    return pipes

def island(pipes, start):
    closed_set = set()

    # sanity check
    if start not in pipes:
        return set()

    # explore the island
    open_set = set([start])
    while open_set:
        node = open_set.pop()
        closed_set.add(node)
        for neighbor in pipes[node]:
            if neighbor not in closed_set:
                open_set.add(neighbor)
    
    return closed_set

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        fin = open(sys.argv[1])
    else:
        fin = sys.stdin

    pipes = parse(fin)
    # pprint(pipes, width=40)

    discovered = set()
    number_of_islands = 0
    while len(discovered) < len(pipes.keys()):
        start = min(node for node in pipes.keys() if node not in discovered)
        isle = island(pipes, start)
        number_of_islands += 1
        print("island starting at {}: n={}/{}".format(start, len(isle), len(pipes.keys())))
        discovered = discovered.union(isle)
    print("found {} islands".format(number_of_islands))
