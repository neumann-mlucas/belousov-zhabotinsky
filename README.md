# Belousov-Zhabotinsky

![](demo.gif)

## About

**The python package you never knew you needed!**
Now you can appreciate all the glory of the Belousov-Zhabotinsky reaction from the comfort of your console window in a state of the art *ASCII art* rendering. *Your life will never be the same!*

This a little python script I made for a class sometime ago. You can play around with the equations coefficients and rendering parameters with command line arguments (see usage). Besides the **BZ** equation there's also the **FitzHugh-Nagumo** (for Turing patterns), **Gray-Scoot** and **Cahn-Hilard** (simulates phase separation) equations.

## Theory

The Belousov-Zhabotinsky reaction is the classical examples of non-linear/oscillatory dynamics in chemical systems. The equations that describe the process are reaction-diffusion equations:

**BZ Equations:**


<img src="https://latex.codecogs.com/svg.latex?\large&space;a_{t+1}=a_t+a_t({\alpha}b_t-{\gamma}c_t)" title="A" class="center" />


<img src="https://latex.codecogs.com/svg.latex?\large&space;b_{t+1}=b_t+b_t({\beta}c_t-{\alpha}a_t)" title="B" class="center" />


<img src="https://latex.codecogs.com/svg.latex?\large&space;c_{t+1}=c_t+c_t({\gamma}a_t-{\beta}b_t)" title="C" class="center" />


Numerally you iterate the equations in a 2D grid. The Laplace operator in a discrete grid is simply a convolution.

You can learn more about the Belousov-Zhabotinsky reaction here:

- Dynamics and Chaos - Steven H. Strogatz

- Chaotic Dynamics, an introduction - G. L. Baker and J. P. Gollub

Inspired by the following blog posts:

![scipy blog](https://scipython.com/blog/simulating-the-belousov-zhabotinsky-reaction/)

![degenerate state](http://www.degeneratestate.org/posts/2017/May/05/turing-patterns/)

## Installation

> *Should work in any python3 version*

> *Needs numpy and scipy*

> See piplock file

You can pip install the python module with the following command

`pip install --user belousov-zhabotinsky`


## Usage

`$ belousov-zhabotinsky`

or

`$ python -m belousov-zhabotinsky`

Check cli options with:

`$ belousov-zhabotinsky --help`

You can exit the program by pressing any key

- Gray-Scott mode requires a terminal size bigger than 100x100 to work properly
- There's a **plot.py** script thay can be use to plot the system in matplotlib.

`$ python -m belousov-zhabotinsky.plot`

## Future

- [x] Fix Gray-Scott
- [x] Make it faster


*My First GitHub project; HOORAY!*
