#! /usr/bin/env python

import unittest
import sys

def f(digits):
    if not digits:
        return 0

    next_digit = digits[-1] + digits[:-1]
    #print digits
    #print next_digit
    #print '\n'.join(' '.join([str(d), str(nd), repr(d==nd)]) for d, nd in zip(digits, next_digit))
    c = sum( int(d) for d, nd in zip(digits, next_digit) if d == nd )
    return c

class Test(unittest.TestCase):
    def test_0(self):
        self.assertEqual(f(''), 0)
        self.assertEqual(f('0'), 0)
        self.assertEqual(f('00'), 0)
        self.assertEqual(f('1'), 1)
        self.assertEqual(f('12'), 0)

    def test_1(self):
        self.assertEqual(f('1122'), 3)

    def test_2(self):
        self.assertEqual(f('1111'), 4)

    def test_3(self):
        self.assertEqual(f('1234'), 0)

    def test_4(self):
        self.assertEqual(f('91212129'), 9)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        print f(sys.argv[1])
