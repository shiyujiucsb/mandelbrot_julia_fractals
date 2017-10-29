from mjf import julia

def burning_ship_iter(z, c):
    return (abs(z.real) + abs(z.imag) * 1j)**2 + c

julia(width=2560, height=1920, fz = burning_ship_iter, cx = 0.45, cy = 0.5, w = 1.7, max_iter=50000, ofile='burning_ship_fractal_1.png')

