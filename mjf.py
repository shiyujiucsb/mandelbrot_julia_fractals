
'''
Function:
Bezier curve calculation.
The number of points to define can be arbitrary.
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

c is the complex number of the point. max_iter is the maximum number of iterations.
colors are all the colors to use.
'''
def m_color(c, max_iter, colors):
    from cImage import Pixel
    
    # speed up using two facts:
    if abs(c+1)<0.25 or abs(2-4*c+2*pow(1-4*c,0.5))<1 or abs(2-4*c-2*pow(1-4*c,0.5))<1 :
        return Pixel(0,0,0)

    # calculate the number of iterations and the return the corresponding color
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return colors[i]
    return Pixel(0,0,0)

'''
Function:
To determine the color of each pixel for Julia set.

z0 is the initial z for iteration.
All the other parameters are similar to the function m_color().
'''
def j_color(c, z0, max_iter, colors):
    from cImage import Pixel
    
    # speed up using two facts:
    if abs(c+1)<0.25 or abs(2-4*c+2*pow(1-4*c,0.5))<1 or abs(2-4*c-2*pow(1-4*c,0.5))<1 :
        return Pixel(0,0,0)

    # calculate the number of iterations and the return the corresponding color
    z = z0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return colors[i]
    return Pixel(0,0,0)


"""
Prelim:
Mandelbrot set z <- z^2 + c includes all c, |c| < 2 such that lim|z| < 2, where z0 =(0,0) 

Function:
To plot a mandelbrot set. The parameter details are given below.
"""
def mandelbrot( ofile = '', \
                # file to save
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
                    {'index':0, 'color':{'R':0, 'G':0, 'B':90}},\
                    {'index':28, 'color':{'R':0, 'G':7, 'B':100}},\
                    {'index':92, 'color':{'R':32, 'G':107, 'B':203}}, \
                    {'index':196, 'color':{'R':237, 'G':255, 'B':255}}, \
                    {'index':285, 'color':{'R':255, 'G':170, 'B':0}}, \
                    {'index':371, 'color':{'R':49, 'G':2, 'B':48}},\
                    {'index':500, 'color':{'R':0, 'G':0, 'B':90}}\
                ], \
                # the points to define the gradient
                # index is the number of iteration to exit
                # the colors will be repeatedly used for each round
                ) : 
    # check the format of the gradient as input
    if gradient[0]['index'] != 0:
        print('The first index of gradient must be 0.')
        return
    for i in range(len(gradient)):
        if 'index' not in gradient[i].keys() or 'color' not in gradient[i].keys():
            print('Each entry must contain an index and a color.')
            return
            
    import cImage
    from cImage import Pixel
    
    myimagewindow = cImage.ImageWin('Mandelbrot',width,height)
    NewImage = cImage.EmptyImage(width,height)
    
    # prepare the colors
    colors = []
    period = gradient[-1]['index']
    for i in range(max_iter):
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
        colors.append(Pixel(int(R), int(G), int(B)))

    # imaginary part difference between top and bottom
    h = w/width*height
    # plot the set
    progress = 1
    for i in range(width):
        for j in range(height):
            c = cx+(i-width//2)/width*w - ((j-height//2)/height*h - cy)*1j
            NewImage.setPixel(i,j,m_color(c, max_iter, colors))
        # refresh the screen to reflect what've been drawn
        if (i+1)/width > progress/10:
            NewImage.setPosition(0,0)
            NewImage.draw(myimagewindow)
            progress += 1
    NewImage.setPosition(0,0)
    NewImage.draw(myimagewindow)
    if ofile != '' : 
        NewImage.save(ofile)
    myimagewindow.exitOnClick()


"""
Julia set z <- z^2 + c for a given complex c, includes all z0, |z0|<2 such that lim|z|<2
e.g., try c = (-0.123, 0.745), c = (-0.75,0), c = (-0.391, -0.587).

All the other parameters are similar to the Mandelbrot function.
"""
def julia(      c = -0.4+0.6j, \
                ofile = '', \
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
                    {'index':500, 'color':{'R':0, 'G':0, 'B':90}}\
                ], \
        ) :
    # check the format of the gradient as input
    if gradient[0]['index'] != 0:
        print('The first index of gradient must be 0.')
        return
    for i in range(len(gradient)):
        if 'index' not in gradient[i].keys() or 'color' not in gradient[i].keys():
            print('Each entry must contain an index and a color.')
            return
            
    import cImage
    from cImage import Pixel
    
    myimagewindow = cImage.ImageWin('Mandelbrot',width,height)
    NewImage = cImage.EmptyImage(width,height)
    
    # prepare the colors
    colors = []
    period = gradient[-1]['index']
    for i in range(max_iter):
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
        colors.append(Pixel(int(R), int(G), int(B)))

    # imaginary part difference between top and bottom
    h = w/width*height
    # plot the set
    progress = 1
    for i in range(width):
        for j in range(height):
            z0 = cx+(i-width//2)/width*w - ((j-height//2)/height*h - cy)*1j
            NewImage.setPixel(i,j,j_color(c, z0, max_iter, colors))
        # refresh the screen to reflect what've been drawn
        if (i+1)/width > progress/10:
            NewImage.setPosition(0,0)
            NewImage.draw(myimagewindow)
            progress += 1
    NewImage.setPosition(0,0)
    NewImage.draw(myimagewindow)
    if ofile != '' : 
        NewImage.save(ofile)
    myimagewindow.exitOnClick()


#
# if necessary, you can define more functions below 
#
