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

def chunk_image(img, n):
    size = len(img)
    if size % n:
        raise ValueError("chunk size {} does not evenly divide image size {}".format(n, size))
    chunks = []
    chunk_size = int(size/n)
    for i in range(chunk_size):
        chunk_row = []
        for j in range(chunk_size):
            chunk = ''
            for x in range(n):
                for y in range(n):
                    chunk += img[i*n + x][j*n + y]
            chunk_row.append(chunk)
        chunks.append(chunk_row)
    return chunks
        

def unchunk(chunks):
    n = int(sqrt(len(chunks[0][0])))
    m = len(chunks)
    size = n*m
    img = []
    for i in range(size):
        row = []
        for j in range(size):
            chunk = chunks[i//n][j//n]
            y = i % n
            x = j % n
            bit = chunk[x + y*n]
            row.append(bit)
        img.append(row)
    return img

def flip(s):
    n = int(sqrt(len(s)))
    s2 = [ ' ' for c in s ]
    for x in range(n):
        for y in range(n):
            c = s[x + y*n]
            x2, y2 = n - x - 1, y
            s2[x2 + y2*n] = c
    return ''.join(s2)

def rotate(s):
    n = int(sqrt(len(s)))
    s2 = [ ' ' for c in s ]
    for x in range(n):
        for y in range(n):
            c = s[x + y*n]
            x2, y2 = n-y-1, x
            s2[x2 + y2*n] = c
    return ''.join(s2)

def read_rules(filename):
    rules = {}
    with open(filename) as fin:
        lines = fin.read().splitlines()
        for line in lines:
            match, produce = [s.strip().replace('/', '') for s in line.split(' => ')]
            for f in range(2):
                for r in range(4):
                    rules[match] = produce
                    match = rotate(match)
                match = flip(match)
    return rules

def apply_rules(img, rules):
    n = 2 if len(img) % 2 == 0 else 3
    chunks = chunk_image(img, n)
    new_chunks = [ [ rules[chunk] for chunk in row] for row in chunks ]
    return unchunk(new_chunks)

if __name__ == '__main__':
    img = load_image('seed')
    rules = read_rules('input')
    print("Initially: ")
    write_image(img)
    print()
    for iterations in range(1, 5+1):
        img = apply_rules(img, rules)
        print("After {} iterations: ".format(iterations))
        write_image(img)
        print("Pixels: {}".format(count_pixels(img)))
        print()



