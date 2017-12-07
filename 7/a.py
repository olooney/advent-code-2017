import re
import sys
from statistics import median

input_regex = re.compile(r'^(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<children>\w+(, \w+)*))?\n?$')

def first_truthy_value(S):
    for x in S:
        if x:
            return x
    return None

class Plate:
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
        self._total_weight = None
        self.parent = None
        self.children = list()

    def __repr__(self):
        return '{name} ({weight})'.format(**self.__dict__)

    def dump(self, indent=0, show_total_weight=False, depth=999):
        if depth <= 0:
            return

        r = repr(self)
        if show_total_weight:
            r += ' (total: {})'.format(self.total_weight)
        if self.children:
            if depth == 1:
                r += ' -> ...'
            else:
                r += ' -> '
        print('\t'*indent + r)
        for child in self.children:
            child.dump(indent+1, show_total_weight, depth-1)

    @property
    def total_weight(self):
        if self._total_weight is None:
            self._total_weight = self.weight + sum(child.total_weight for child in self.children)
        return self._total_weight
        
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

def find_unbalanced(plate):
    # every leaf is balanced by definition
    if not plate.children:
        return None

    # search for unbalanced children first, so we find the deepest cause
    # of the problem
    unbalanced_child = first_truthy_value(find_unbalanced(child) for child in plate.children)
    if unbalanced_child: 
        return unbalanced_child

    # if this node as zero or 1 children, and all those children are balanced,
    # we must be balanced too.
    if len(plate.children) < 2:
        return None

    # maybe it's us...
    correct_total_weight = int(median(child.total_weight for child in plate.children))
    # TODO: this is kind of ambiguous in the case of exactly two children.
    # which one do we "fix"?
    for child in plate.children:
        if child.total_weight != correct_total_weight:
            return child, correct_total_weight
        

def main(filename=None):
    if not filename:
        print("USAGE: python a.py FILE")
    else:
        plates = parse_input(filename)
        root = find_root(plates)
        root.dump(show_total_weight=True)
        solution = find_unbalanced(root)
        if solution:
            unbalanced_child, correct_total_weight = solution
            correction = correct_total_weight - unbalanced_child.total_weight
            corrected_weight = unbalanced_child.weight + correction
            print('\nunbalanced part of the tree:')
            unbalanced_child.parent.dump(show_total_weight=True, indent=1, depth=2)
            print('\nunbalanced node: {!r}'.format(unbalanced_child))
            print('weight should be correct by {} to a weight of {} so that total weight is {}'.format(correction, corrected_weight, correct_total_weight))
        else:
            print('no unbalanced nodes found')
    return 0
            
if __name__ == '__main__':
    exit(main(*sys.argv[1:]))



