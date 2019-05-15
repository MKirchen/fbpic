# Copyright 2016, FBPIC contributors
# Authors: Remi Lehe, Manuel Kirchen, Kevin Peters
# License: 3-Clause-BSD-LBNL
"""
This file is part of the Fourier-Bessel Particle-In-Cell code (FB-PIC)
It defines the linear and cubic particle shape factors for the deposition.
"""
import math

# -------------------------------
# Particle shape Factor functions
# -------------------------------

# Linear shapes
# longitudinal (z)
def Sz_linear(cell_position, index):
    iz = int(math.ceil(cell_position)) - 1
    s = iz+1.-cell_position
    if index == 1:
        s = 1.-s
    return s
# transversal (r)
# with Ruyten-correction (beta_n term) to account for the non-homogeneous
# radial cell volume (as defined in interpolation grid object)
def Sr_linear(cell_position, index, flip, beta_n):
    ir = int(math.ceil(cell_position)) - 1
    s = (ir+1.-cell_position)*(1.+beta_n*(cell_position-ir))
    if index == 0 and ir < 0:
        s *= flip
    elif index == 1:
        s = 1.-s
    return s

# Cubic shapes
# longitudinal (z)
def Sz_cubic(cell_position, index):
    iz = int(math.ceil(cell_position)) - 2
    s = 0.
    if index == 0:
        s = (-1./6.)*((cell_position-iz)-2)**3
    elif index == 1:
        s = (1./6.)*(3*((cell_position-(iz+1))**3)-6*((cell_position-(iz+1))**2)+4)
    elif index == 2:
        s = (1./6.)*(3*(((iz+2)-cell_position)**3)-6*(((iz+2)-cell_position)**2)+4)
    elif index == 3:
        s = (-1./6.)*(((iz+3)-cell_position)-2)**3
    return s
# transversal (r)
def Sr_cubic(cell_position, index, flip):
    flip_factor = 1.
    ir = int(math.ceil(cell_position)) - 2
    s = 0.
    if index == 0:
        if ir < 0:
            flip_factor = flip
        s = flip_factor*(-1./6.)*((cell_position-ir)-2)**3
    elif index == 1:
        if ir+1 < 0:
            flip_factor = flip
        s = flip_factor*(1./6.)*(3*((cell_position-(ir+1))**3)-6*((cell_position-(ir+1))**2)+4)
    elif index == 2:
        if ir+2 < 0:
            flip_factor = flip
        s = flip_factor*(1./6.)*(3*(((ir+2)-cell_position)**3)-6*(((ir+2)-cell_position)**2)+4)
    elif index == 3:
        if ir+3 < 0:
            flip_factor = flip
        s = flip_factor*(-1./6.)*(((ir+3)-cell_position)-2)**3
    return s
