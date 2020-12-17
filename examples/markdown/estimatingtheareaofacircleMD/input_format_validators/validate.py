#!/usr/bin/python

import sys
import re

realnum_regex = r'(0|[1-9]\d*)(\.\d{1,5})?'
int_regex = r'(0|[1-9][0-9]*)'
line_regex = re.compile('^{0} {1} {1}\n$'.format(realnum_regex, int_regex))

numCases = 0
line = sys.stdin.readline()
while line != '0 0 0\n':
    numCases += 1
    print line,
    assert line_regex.match(line)
    r, sample_size, in_circle = line.split()
    r = float(r)
    in_circle = int(in_circle)
    sample_size = int(sample_size)

    assert 0 < r <= 1000.0
    assert 1 <= sample_size <= 100000

    assert 0 <= in_circle <= sample_size

    line = sys.stdin.readline()

assert sys.stdin.readline() == ''
assert numCases <= 1000

sys.exit(42)

