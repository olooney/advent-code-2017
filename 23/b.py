from sys import argv
from functools import lru_cache

def is_prime(n):
    if n <= 3:
        return (n >= 2)

    if n % 2 == 0:
        return False

    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False
    print(n)
    return True

def count_composites(lower, upper, step):
    composites = 0
    for n in range(lower, upper, step):
        if not is_prime(n): composites += 1
    return composites

if __name__ == '__main__':
    if len(argv) == 3:
        print(count_composites(int(argv[1]), int(argv[2]), 1))
    elif len(argv) >= 4:
        print(count_composites(int(argv[1]), int(argv[2]), int(argv[3])))
    else:
        print(count_composites(109300, 126300+17, 17))
