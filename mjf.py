#!/usr/bin/python3

try:
    from PIL import Image as Image
except:
    print("Need install PIL: pip install PIL")
    exit()
from math import log


'''
Function: the iteration function, by default z := z^2 + c
'''
def iter_func(z, c):
    return z*z + c

'''
Function: maps index to color offset (by linear)
'''
def rount_to_index_linear(index, n_color):
    return (int(index)%n_color)

'''
Function: maps index to color offset (by log)
'''
def rount_to_index_log(index, n_color):
    return (int(log(1+index)/log(1+n_color)*n_color))%n_color



'''
Prelim:
Mandelbrot set z <- z^2 + c includes all c, |c| < 2 such that lim|z| < 2, where z0 =(0,0) 

Function:
To plot a mandelbrot set. The parameter details are given below.
'''
def mandelbrot( ofile = '', \
                # file to save
                fz = iter_func, \
                # the iteration function, by default z := z^2 + c
                width = 960, \
                # width of the plot image
                height = 720, \
                # height of the plot image
                cx = -0.7, \
                # real part of the complex number at the center of the plot
                cy = 0, \
                # imaginary part of the complex number at the center of the plot
                w = 3.0769, \
                # real part difference between leftmost and rightmost of the plot
                max_iter = 50000, \
                # number of maximum iterations
                gradient = [\
                    {'index':0, 'color':{'R':25, 'G':5, 'B':74}},\
                    {'index':28, 'color':{'R':0, 'G':7, 'B':100}},\
                    {'index':92, 'color':{'R':32, 'G':107, 'B':203}}, \
                    {'index':196, 'color':{'R':237, 'G':255, 'B':255}}, \
                    {'index':285, 'color':{'R':255, 'G':170, 'B':0}}, \
                    {'index':371, 'color':{'R':49, 'G':2, 'B':48}},\
                    {'index':399, 'color':{'R':25, 'G':5, 'B':74}},\
                ], \
                # the points to define the gradient
                # index is the number of iteration to exit
                # the colors will be repeatedly used for each round
                density = 0.42, \
                # color density (on the number of rounds to exit)
                rotation = 29, \
                # initial (gradient) index to start when coloring
                mapping = rount_to_index_log \
                # index mapping function (by default log)
				) : 
                
    # check the format of the gradient as input
    if check_gradient_profile(gradient) == False:
        return # means failed the check
    
    NewImage = Image.new('RGB', (width, height), (255, 255, 255))
    colors = define_colors(gradient)

    # imaginary part difference between top and bottom
    h = w/width*height
    # plot the set
    for i in range(width):
        for j in range(height):
            c = cx+(i-width//2)/width*w - ((j-height//2)/height*h - cy)*1j
            NewImage.putpixel((i, height-1-j), m_color(c, fz, max_iter, colors, density, rotation, mapping))
    if ofile != '' : 
        NewImage.save(ofile)


"""
Prelim:
Julia set z <- z^2 + c for a given complex c, includes all z0, |z0|<2 such that lim|z|<2
e.g., try c = (-0.123, 0.745), c = (-0.75,0), c = (-0.391, -0.587).

All the other parameters are the same as the Mandelbrot function.
"""
def julia(      c = -0.4+0.6j, \
                ofile = '', \
                fz = iter_func, \
                width = 800, \
                height = 800, \
                cx = 0, \
                cy = 0, \
                w = 4, \
                max_iter = 50000, \
                gradient = [\
                    {'index':0, 'color':{'R':0, 'G':0, 'B':90}},\
                    {'index':28, 'color':{'R':0, 'G':7, 'B':100}},\
                    {'index':92, 'color':{'R':32, 'G':107, 'B':203}}, \
                    {'index':196, 'color':{'R':237, 'G':255, 'B':255}}, \
                    {'index':285, 'color':{'R':255, 'G':170, 'B':0}}, \
                    {'index':371, 'color':{'R':49, 'G':2, 'B':48}},\
                    {'index':400, 'color':{'R':0, 'G':0, 'B':90}}\
                ], \
                density = 3, \
                rotation = 0,\
                mapping = rount_to_index_linear \
        ) :
        
    # check the format of the gradient as input
    if check_gradient_profile(gradient) == False:
        return # means failed the check
    
    NewImage = Image.new('RGB', (width, height), (255, 255, 255))
    colors = define_colors(gradient)

    # imaginary part difference between top and bottom
    h = w/width*height
    # plot the set
    for i in range(width):
        for j in range(height):
            z0 = cx+(i-width//2)/width*w - ((j-height//2)/height*h - cy)*1j
            NewImage.putpixel((i, height-1-j), j_color(c, z0, fz, max_iter, colors, density, rotation, mapping))
    if ofile != '' : 
        NewImage.save(ofile)



# Below are other functions.

'''
Function:
Bezier curve calculation.
The number of points to define can be arbitrary. The points are in the parameter anchors.
The function takes a recursion to calculate the curve.
'''
def bezier(t, start, end, anchors):  
    if len(anchors)==0:
        return (1-t)*start['R'] + t*end['R'], \
               (1-t)*start['G'] + t*end['G'], \
               (1-t)*start['B'] + t*end['B']
    return (1-t)*bezier(t, start, anchors[-1], anchors[:-1])[0] + t*bezier(t, anchors[0], end, anchors[1:])[0], \
           (1-t)*bezier(t, start, anchors[-1], anchors[:-1])[1] + t*bezier(t, anchors[0], end, anchors[1:])[1], \
           (1-t)*bezier(t, start, anchors[-1], anchors[:-1])[2] + t*bezier(t, anchors[0], end, anchors[1:])[2]

'''
Function:
To determine the color of each pixel for Mandelbrot set.

c is the complex number of the point.
fz is the iteration function, by default z := z^2 + c.
max_iter is the maximum number of iterations.
colors are all the colors to use. For example, colors[i] is the color of the point taking i rounds to exit.
'''
def m_color(c, fz, max_iter, colors, density, rotation, mapping):
    
    # speed up using two facts:
    if fz == iter_func and (abs(c+1)<0.25 or abs(2-4*c+2*pow(1-4*c,0.5))<1 or abs(2-4*c-2*pow(1-4*c,0.5))<1) :
        return (0,0,0)

    n_color = len(colors)
    # calculate the number of iterations and the return the corresponding color
    z = 0
    for i in range(max_iter):
        z = fz(z, c)
        if abs(z) > 2:
            index = int(i*density)
            return colors[(mapping(index, n_color)+rotation)%n_color]
    return (0,0,0)

'''
Function:
To determine the color of each pixel for Julia set.

z0 is the initial z for iteration.
All the other parameters are similar to the function m_color().
'''
def j_color(c, z0, fz, max_iter, colors, density, rotation, mapping):

    n_color = len(colors)
    # calculate the number of iterations and then return the corresponding color
    z = z0
    for i in range(max_iter):
        z = fz(z, c)
        if abs(z) > 2:
            index = int(i*density)
            return colors[(mapping(index, n_color)+rotation)%n_color]
    return (0,0,0)

'''
Function:
Define the color for each round to exit the iteration.

Parameters: max_iter is the maximum no. of iterations to observe.
    gradient is the color profile.
'''
def define_colors(gradient):
    # prepare the colors
    colors = []
    period = gradient[-1]['index']+1
    for i in range(gradient[-1]['index']):
        for j in range(len(gradient)):
            if gradient[j]['index'] > i%period:
                start_ind = gradient[j-1]['index']
                end_ind = gradient[j]['index']
                start_color = gradient[j-1]['color']
                end_color = gradient[j]['color']
                t = (i%period-start_ind)/(end_ind-start_ind)
                anchors = {}
                if 'anchors' in gradient[j].keys():
                    anchors = gradient[j]['anchors']
                break
        R, G, B = bezier(t, start_color, end_color, anchors)
        R = 0 if R<0 else 255 if R>255 else R
        G = 0 if G<0 else 255 if G>255 else G
        B = 0 if B<0 else 255 if B>255 else B
        colors.append((int(R), int(G), int(B)))
    return colors

'''
Function:
Check whether the format of the profile 'gradient' is correct.
The details are given as inline comments as below.
'''
def check_gradient_profile(gradient):
    # check the format of the gradient as input
    if gradient[0]['index'] != 0:
        print('The first index of gradient must be 0.')
        return False
    for i in range(len(gradient)):
        if 'index' not in gradient[i].keys() or 'color' not in gradient[i].keys():
            print('Each entry must contain an index and a color.')
            return False
        if 'R' not in gradient[i]['color'] or 'G' not in gradient[i]['color'] or 'B' not in gradient[i]['color']:
            print('Need give RGB for index ', gradient[i]['index'])
            return False
        if i>0:
            if gradient[i]['index'] < gradient[i-1]['index']:
                print('The index must be in ascending order.')
                return False
    return True

