# Mandelbrot Julia Fractals (MJF) Project

This project plots Mandelbrot and Julia sets using Python 3 + cImage.
The goal is to let everyone freely verify the correctness of fractal images on the Internet.
Wikipedia gives great articles and references about the related concepts here. 
This program considers the iteration: z = z^2 + c.


## Requirements

This program needs **Python** 3.4+ with Pillow and **cImage**. To install Pillow and cImage, please follow the link:
http://wp.stolaf.edu/it/installing-pil-pillow-cimage-on-windows-and-mac/

A few words about the fractals: 
* Each point within the Mandelbrot/Julia set is supposed to be __black__.
* The color of each point outside the set is decided by the number of rounds this point takes to exit the iterations.
* The function mapping the number of rounds to the color is given by the parameter gradient (see below), which contains a few colors that we should use in plot for certain indices. Each index corresponds to some number of rounds to exit the iterations. 
	* Optionally one may also define Bezier curves between the color points. That is, suppose the RGB color space as a 3-dim cube with edge length of 256. To choose different patterns of color choice, one can define Bezier curves between two adjacent colors. In other words, the program chooses the colors along the Bezier curves, arriving at color points correspondingly to the indices. See below for a little example.
	* The number of the points to define Bezier curves can be arbitrary and different for each curve. 


## Quick start

Just type mandelbrot(), and you can get a copy of the entire Mandelbrot set. Similarly by typing julia() you can see the Julia set with c = -0.4+0.6j.
For more details please read the parameter specification in the code. More detailed docs are to follow.


## Options

In this program, to plot Mandelbrot set, one uses the function mandelbrot(). Similarly use julia() to plot Julia set given the input complex c.
We discuss the parameters for these two main functions. 
The definition of the function mandelbrot() is as follows:

```python
def mandelbrot (...): # below are the param spec for this function
```

* __ofile__: the filename to save

* __fz__: the iteration function, by default z := z^2 + c

* __width__: width of the plot image (in number of pixels)
				
* __height__: height of the plot image (in number of pixels)
				
* __cx__: real part of the complex number at the center of the plot
				
* __cy__: imaginary part of the complex number at the center of the plot
				
* __w__: real part difference between leftmost and rightmost of the plot
				
* __max_iter__: number of maximum iterations, the more the better quality, but will take more time
				
* __gradient__: the most complicated argument
	* The points to define the gradient.
	* The 'index' is the number of iteration to exit.
	* The colors will be repeatedly used round by round.
	* One can use 'anchors' to define Bezier curves between the points.
	* The current default settings are heuristic and need to be improved.
	
* __density__: given the index __i__ of the rount to exit the iteration, 
	the index of the gradient the pixel will use is determined by:
	gradient index = ( __density__ * __i__ + __rotation__) mod max gradient index.
	That is, density reflects the changing speed of the colors used.
	The parameter __ratation__ is given below.
	
* __rotation__: the inital gradient index that is used by the pixel with exiting index i = 0.

* __mapping__: the function that maps index (round to exit) to the offset of color.
	
### An example of gradient profile

```python
	gradient = [\
					{'index':0, 'color':{'R':0, 'G':0, 'B':0}},\
					{'index':30, 'color':{'R':10, 'G':10, 'B':10}},\
					{'index':60, 'color':{'R':50, 'G':50, 'B':50}}, \
					{'index':90, 'color':{'R':100, 'G':100, 'B':100}}, \
					{'index':120, 'color':{'R':255, 'G':255, 'B':255}} \
				]
```
In this example, we define the gradient of the colors by specifying 5 color points, all of which are greyscale, i.e., R = G = B. 
For each large round, the color will choose from black to white. All the Bezier curves are straight lines. 
For instance, 
* for round 30, the color will be R = G = B = 10.
* for round 100, since the curve is straight, the color will R = G = B = 100 + (255 - 100)/3, which is about 152.
* for round 210, the color is the same as round 210 - 120 = 90.

The parameters for julia() function are similarly defined, except that the default c is -0.4 + 0.6j.
				
Note that all the default settings are from Wikipedia article: Mandelbrot set.		

## Output samples

See the __img__ directory for the output images. Their ideas come from Wikipedia images of Mandelbrot set and Julia sets. More details will follow.

## Licensing

This program is under CC0 license.
Everyone is free to participate and share with comments and suggestions!
But please keep the licensing.
