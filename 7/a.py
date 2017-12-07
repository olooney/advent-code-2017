import re
import sys

input_regex = re.compile(r'^(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<children>\w+(, \w+)*))?\n?$')

class Plate:
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
        self.parent = None
        self.children = list()

    def __repr__(self):
        return '{name} ({weight})'.format(**self.__dict__)

    def dump(self, indent=0):
        r = repr(self)
        if self.children:
            r += ' -> '
        print('\t'*indent + r)
        for child in self.children:
            child.dump(indent+1)
        
def parse_line(line):
    m = input_regex.match(line)
    if not m:
        raise ValueError("line {!r} could not be parsed".format(line))
    plate = Plate(m.group('name'), weight=m.group('weight'))

    if m.group('children'):
        child_names = m.group('children').split(', ')
    else:
        child_names = ''
    
    return plate, child_names

def parse_input(filename):
    plate_registry = {}
    child_map = {}

    # first pass, read each line and build a plate object
    for line in open(filename, 'r'):
        plate, child_names = parse_line(line)
        name = plate.name
        plate_registry[name] = plate
        child_map[name] = child_names

    # second pass, wire up parents to children and vice versa
    for parent_name, child_names in child_map.items():
        parent = plate_registry[parent_name]
        for child_name in child_names:
            child = plate_registry[child_name]

            # every child knows their parent
            if child.parent and child.parent != parent:
                raise ValueError("child already has different parent!")
            else:
                child.parent = parent

            # every parent knows all their children
            if child not in parent.children:
                parent.children.append(child)

    return list(plate_registry.values())

def find_root(plates):
    plate = plates[0]
    while plate.parent is not None:
        plate = plate.parent
    return plate
    

def main(filename=None):
    if not filename:
        print("USAGE: python a.py FILE")
    else:
        plates = parse_input(filename)
        root = find_root(plates)
        root.dump()
    return 0
            
if __name__ == '__main__':
    exit(main(*sys.argv[1:]))



