import sys

def parse_firewall(lines):
    firewall = {}
    for line in lines:
        depth, range = [int(n) for n in line.split(': ')]
        firewall[depth] = range
    return firewall

class Scanner:
    def __init__(self, range):
        self.range = range
        self.index = 0
        self.step = 1
    
    def advance(self):
        future = self.index + self.step
        if not 0 <= future < self.range:
            self.step = -self.step
        self.index += self.step

    def __repr__(self):
        return 'S({}/{}, {})'.format(self.index, self.range-1, self.step)
        

def penetrate(firewall, packet_index=0, delay=0):
    scanners = { depth: Scanner(range) for depth, range in firewall.items() }
    position = -1
    severity = 0
    caught = False
    exit_depth = max(firewall.keys())


    # delay loop: only advance scanners
    while delay:
        for depth in scanners.keys():
            scanners[depth].advance()
        #print(scanners)
        delay -= 1

    # send packet
    while position <= exit_depth:
        # update packet position
        position += 1
        #print("packet position: {}".format(position))

        # detect collisions ("caught") when entering a new cell:
        if position in firewall.keys():
            if scanners[position].index == packet_index:
                cost = position * firewall[position]
                severity += cost
                caught = True
                print("Caught! +{}*{} sev = {}".format(position, firewall[position], severity))

        # advance scanners
        for depth in scanners.keys():
            scanners[depth].advance()
        #print(scanners)

    return caught, severity
        
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fin:
        firewall = parse_firewall(fin)
        results = []
        for delay in range(3905748, 3905748+1):
            caught, severity = penetrate(firewall, delay=delay)
            if not caught:
                results.append( (severity, delay) )
                severity, delay = results[0]
                print("best delay {} severity: {}".format(delay, severity))
                sys.exit(0)
            #print("{}caught at delay {} severity: {}".format('' if caught else 'not ', delay, severity))
        #results.sort()
        #print(results)

