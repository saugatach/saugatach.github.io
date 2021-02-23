---
layout: page
title: Tutorials
description: Lectures and tutorials on statistics, machine learning, physics, computational physics
background: '/img/bg-tutorial-black-blur.jpg'
---
# Statistics

List of lectures on main topics in Statistics. These are at 100 level and do not use the 
concepts of $$\sigma$$-spaces.  

1. [Binomial Distribution](/tutorials/tutorials-lectures-binomial-distribution.html)
2. [Normal Distribution](/tutorials/tutorials-lectures-normal-distribution.html)

## R Labs

1. [Quick Introduction to R](/tutorials/tutorials-intro-r.html)

# Physics
## Sagemath

Sagemath simplifies general relativistic calculation and can replace Maple completely. Sagemath is 
built on a solid mathematical framework and all functions follow a robust geometrical hierarchy.
It is easy to define metric spaces and calculate the Riemann tensor and other geometric quantities 
in curved space. The main strength of this package is in visualizing embedding 
spaces.
For example, a graphical representation of the Bondi coordinates shows that it is only a tiny patch
on the deSitter hyperboloid in a higher dimensional embedding space. It does not cover the entire 
spacetime. We explore this in #4 below. 

The following are Sagemath tutorials which are rendered live by GitHub nbviewer. 

1. [Substitution in Sagemath is tricky](https://nbviewer.jupyter.org/github/saugatach/sagemanifold/blob/master/Sagemath%20tutorial%20-%20substitution.ipynb)
2. [Embedding of torus and $$dS^2$$ in $$R^3$$](https://nbviewer.jupyter.org/github/saugatach/sagemanifold/blob/master/Embedding.ipynb)
3. [FRW metric](https://nbviewer.jupyter.org/github/saugatach/sagemanifold/blob/master/FRWmetrictest.ipynb)
4. [Bondi coordinates cover only a part of deSitter – embedding diagram](https://nbviewer.jupyter.org/github/saugatach/sagemanifold/blob/master/BirrelDavies-chap5.ipynb)

The files can be directly accessed from my [GitHub page](http://github.com/saugatach/sagemanifold). 

If we want to download and run these files locally then we will need to install Sagemath.
Each notebook is written in the language of SageManifold and requires Sage to run.
You can install Sagemath from [here](https://doc.sagemath.org/html/en/installation/). 
On Ubuntu use
```bash
apt install sagemath
```

