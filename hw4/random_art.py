# -*- coding: utf-8 -*-
"""
Random_art.py

@author: Toni Saylor
10/6/2014
A program to generate random art.
"""

# import choice, math, Image, and time
from random import choice
import math
import Image
import time


def buildrandfunc(min_depth, max_depth, rlevel):
    """ 
    buildrandfunc takes pieces from a list to build a random function.
    It takes the minimum recursion depth, maximum recursion depth, and the 
    current recursion level as inputs.
    """
    
    # piecelist contains my possible functions, and backup list contains x 
    # and y so that I can make sure I have an x and y somewhere in the function
    piecelist= ['prod','cos_pi', 'sin_pi', 'square', 'cube']
    backuplist = ['x', 'y']
    
    # if the recursion level is less than the minimum depth
    if rlevel < min_depth:
        # pick a random list from piecelist
        function = choice(piecelist)
        # if that random string is prod, I need to take an extra function so 
        # that I can take the product of the first thing it takes after prod 
        # and the second.
        if function == 'prod':
            return ['prod',[buildrandfunc(min_depth,max_depth,rlevel+1),buildrandfunc(min_depth,max_depth,rlevel+1)]]
        return [function,buildrandfunc(min_depth,max_depth,rlevel+1)]# + function2
    # if the recursion level is greater than or equal to minimum depth but less
    # than maximum depth, pick a random thing, and still account for the differences
    # between prod and other functions.
    elif rlevel >= min_depth and rlevel < max_depth:
        function = choice(piecelist)
        if function == 'prod':
            return ['prod', [buildrandfunc(min_depth, max_depth, rlevel+1), buildrandfunc(min_depth, max_depth, rlevel+1)]]
        return [function, buildrandfunc(min_depth, max_depth, rlevel+1)]
    # otherwise when recursion level is greater than max depth pick x or y.
    else:
        function = choice(backuplist)
        return function



def evalrandfunc(f, x, y):
    """ 
    takes input from build_random function and user input to evaluate random function
    f is the random function, x is the value of x, and y is the value of y    
    """
    
    # if the random function first part is cosine, evaluate the cosine of pi
    # times the next thing. it then goes to the next thing and this whole process
    # virtually starts over. The same goes for everything except for prod.
    if f[0] == 'cos_pi':
        return math.cos(math.pi*evalrandfunc(f[1],x,y))
    elif f[0] == 'sin_pi':
        return math.sin(math.pi*evalrandfunc(f[1],x,y))
    elif f[0] == 'cube':
        return (evalrandfunc(f[1],x,y))**3.0
    elif f[0] == 'square':
        return (evalrandfunc(f[1],x,y))**2.0
    # if it's a product, take the first thing inside product and evaluate it
    # then take the second thing in product and evaluate it before moving on.
    elif f[0] == 'prod':
        return (evalrandfunc(f[1][0],x,y))*(evalrandfunc(f[1][1],x,y))
    elif f == 'x':
        return x
    elif f == 'y':
        return y
        
    
    
def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ 
    Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
    The formula takes whether or not the value being remapped is x or y, the original interval start,
    the original inverval end, the new interval start, and the new interval end.
        
    """
    # for example, (x-0)*(1/499-0)*(1--1)--1
    return float((val - input_interval_start)*(1.0/(input_interval_end-input_interval_start))*(output_interval_end - output_interval_start)-output_interval_start)

def image_fun():
    # set up my 500 by 500 image
    im = Image.new("RGB",(500,500))
    # the function for creating green, red, and blue uses buildrandfunc to come
    # up with the random values of g,r, and b.
    green = buildrandfunc(1,3,0)
    red = buildrandfunc(1,3,0)
    blue = buildrandfunc(1,3,0)
    # evaluate all combinations of x, and y in range 500 for both of them
    for x in range(500):
        for y in range(500):
            # your new g evaluates the function you just built, and it inputs 
            # x and y values from -1 to 1 because that's what evalrandfunc
            # takes.
            g = evalrandfunc(green,remap_interval(x,0,499,-1,1),remap_interval(y,0,499,-1,1))
            b = evalrandfunc(blue,remap_interval(x,0,499,-1,1),remap_interval(y,0,499,-1,1))
            r = evalrandfunc(red,remap_interval(x,0,499,-1,1),remap_interval(y,0,499,-1,1))
            # remaps again to get it to fit with pixels            
            gf = remap_interval(g,-1,1,0,255)
            bf = remap_interval(b,-1,1,0,255)
            rf = remap_interval(r,-1,1,0,255)
            # puts the pixels in
            im.putpixel((x,y), (min(255,max(0,int(rf))),min(255,max(0,int(gf))),min(255,max(0,int(bf)))))
    # saves the picture with a different timestamp
    im.save('pic1' +str(time.time())+ '.jpg')

image_fun()
#your additional code and functions go here

