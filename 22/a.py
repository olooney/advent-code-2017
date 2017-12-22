import sys
from math import sqrt
from pprint import pprint

def load_image(filename):
    img = []
    with open(filename) as fin:
        lines = fin.read().splitlines()
        for line in lines:
            row = [ c for c in line ]
            img.append(row)
    return img

def write_image(img):
    for row in img:
        for bit in row:
            print(bit, end='')
        print()

def count_pixels(img):
    pixels = 0
    for row in img:
        for bit in row:
            if bit == '#': pixels += 1
    return pixels

def empty_image(size):
    return [ ['.' for _ in range(size)] for _ in range(size) ]


def blit(target, source, position):
    px, py = position
    for y, row in enumerate(source):
        for x, bit in enumerate(row):
            target[y+py][x+px] = bit

class Virus:
    def __init__(self, position, grid):
        self.x, self.y = position
        self.direction = (0,-1)
        self.grid = grid
        self.infections_caused = 0

    def turn_left(self):
        vx, vy = self.direction
        self.direction = (vy, -vx)

    def turn_right(self):
        vx, vy = self.direction
        self.direction = (-vy, vx)
    
    def on_infected_cell(self):
        return self.grid[self.y][self.x] == '#'

    def conditional_turn(self):
        if self.on_infected_cell():
            self.turn_right()
        else:
            self.turn_left()

    def toggle_infection(self):
        if self.on_infected_cell():
            self.grid[self.y][self.x] = '.' 
        else:
            self.grid[self.y][self.x] = '#' 
            self.infections_caused += 1

    def move(self):
        vx, vy = self.direction
        self.x += vx
        self.y += vy

    def work(self):
        self.conditional_turn()
        self.toggle_infection()
        self.move()


def main(filename, N):
    N = int(N)
    img = load_image(filename)
    grid = empty_image(1001)
    corner = (len(grid)-1)//2 - (len(img)-1)//2
    blit(grid, img, (corner, corner))
    #write_image(grid)
    center = ((len(grid)-1)//2, (len(grid)-1)//2)
    virus = Virus(center, grid)
    for iteration in range(1,N+1):
        virus.work()
        if iteration % 100 == 0 or iteration == N:
            #print("\nafter {} iterations:".format(iteration))
            #write_image(grid)
            print("virus infected {} cells after {} iterations".format(virus.infections_caused, iteration))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

