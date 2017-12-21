
def load_image(filename):
    img = []
    with open(filename) as fin:
        lines = fin.read().splitlines()
        for line in lines:
            row = [ (c == '#') for c in line ]
            img.append(row)
    return img

def write_image(img):
    for row in img:
        for bit in row:
            print('#' if bit else '.', end='')
        print()

if __name__ == '__main__':
    img = load_image('seed')
    write_image(img)
