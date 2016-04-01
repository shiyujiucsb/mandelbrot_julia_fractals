# Mandelbrot Julia Fractals (MJF) Project

This project plots Mandelbrot and Julia sets using Python 3 + cImage.
The goal is to let everyone freely verify the correctness of fractal images on the Internet.


## Requirements

This program needs python 3.4+ and cImage. To install cImage, please follow the link:
http://wp.stolaf.edu/it/installing-pil-pillow-cimage-on-windows-and-mac/

A few words about the fractals: 
Each point within the Mandelbrot/Julia set is supposed to be black.
The color of each point outside the set is decided by the number of rounds this point takes to exit the iterations.
The function mapping the number of rounds to the color is given by the parameter gradient (see below), which contains a few colors that we should use in plot, and the Bezier curves between the points (optional).


## Quick start

Just type mandelbrot(), and you can get a copy of the entire Mandelbrot set. Similarly by typing julia() you can see the Julia set with c = -0.4+0.6j.
For more details please read the parameter specification in the code. More detailed docs are to follow.


## Options

The definition of the function mandelbrot() is as follows:
def mandelbrot

ofile: the filename to save

width: width of the plot image (in number of pixels)
				
height: height of the plot image (in number of pixels)
				
cx: real part of the complex number at the center of the plot
				
cy: imaginary part of the complex number at the center of the plot
				
w: real part difference between leftmost and rightmost of the plot
				
max_iter: number of maximum iterations, the more the better quality, but will take more time
				
gradient: 
The points to define the gradient.
The 'index' is the number of iteration to exit.
The colors will be repeatedly used round by round.
One can use 'anchors' to define Bezier curves between the points.
The current default settings are heuristic and need to be improved.

The parameters for julia() function are similarly defined.
				
Note that all the default settings are from Wikipedia article: Mandelbrot set.		

## Licensing

This program is under CC0 license.
