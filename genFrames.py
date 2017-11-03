#!/usr/bin/python

from __future__ import print_function
from __future__ import division
from mjf import mandelbrot

def burning_ship_iter(z, c):
    return (abs(z.real) + abs(z.imag) * 1j)**2 + c

def pad(i, n):
    res = str(i)
    if len(res) < n:
        res = '0'*(n-len(res)) + res
    return res

import sys
wid = 10.0
assert len(sys.argv) == 2
c = int(sys.argv[1])
ratio = 0.999
mandelbrot(width=2560, height=1920, fz = burning_ship_iter, cx = -1.755, cy = -0.03, w = wid*(ratio**c), max_iter=50000, ofile='frames/burning_frame_'+pad(c+1,6)+'.png')


