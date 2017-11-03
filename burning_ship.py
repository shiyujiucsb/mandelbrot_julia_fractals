#!/usr/bin/python3

from mjf import mandelbrot

def burning_ship_iter(z, c):
    return (abs(z.real) + abs(z.imag) * 1j)**2 + c

mandelbrot(width=256, height=192, fz = burning_ship_iter, cx = -0.45, cy = -0.5, w = 3.4, max_iter=500, ofile='burning_ship_fractal_1.png')

