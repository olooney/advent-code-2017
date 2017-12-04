from __future__ import print_function
from collections import Counter
import sys


def is_valid(passphrase):
    words = passphrase.split(' ')
    word_counts = Counter(words)
    dupe, count = word_counts.most_common(1)[0]
    if count > 1:
        # print('dupe "{}" found with multiplicity {}'.format(dupe, count))
        return False
    else:
        return True

if __name__ == '__main__':
    total_invalid = 0
    total_valid = 0
    lines = sys.stdin.read().splitlines()
    for passphrase in lines:
        if is_valid(passphrase):
            print('passphrase {!r} is valid'.format(passphrase))
            total_valid += 1
        else:
            print('passphrase {!r} is invalid'.format(passphrase))
            total_invalid += 1
    print('total invalid: {}'.format(total_invalid))
    print('total valid: {}'.format(total_valid))
            

        
        
    
