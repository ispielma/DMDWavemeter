# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 19:57:31 2020

This is a tempory file with which I am working on the analysis methods for
typical data.

@author: ispielma
"""

import numpy as np
import h5py
import os
import lmfit

def gaussian(x, amp, cen, wid, off):
    return amp * np.exp(-(x-cen)**2 / wid) + off

gmodel = lmfit.Model(gaussian)


path = os.path.realpath(__file__)
path, _ = os.path.split(path)
import matplotlib.pyplot as pyplot
pyplot.style.use(path + '/matplotlibrc')

with h5py.File('demo.h5', "a") as file:
    image = file["image"][:]

# 100 mm focal lenght lens
f = 0.1
dx = 5.5e-6 # based on the CMV4000 NIR-enhanced
shape = image.shape
xmin = -shape[0]/2 * dx
ymin = -shape[1]/2 * dx

# Make angular scales
x_angle = np.linspace( xmin, xmin + shape[0] * dx, shape[0])
y_angle = np.linspace( ymin, ymin + shape[1] * dx, shape[1])

x_angle = np.arctan2(x_angle, f)
y_angle = np.arctan2(y_angle, f)

#
# Get X and y cuts of the central slice to define first fits (expecting one
# peak in y and maybe more than one in x)
#

width = 256
position = shape[1]//2
CentralSlice = image[:][position-width:position+width]
X_Slice_central = CentralSlice.mean(axis=0)
Y_Slice_central = CentralSlice.mean(axis=1)

y_angle_central = y_angle[position-width:position+width]

#
# Fit the y curve
#
params = gmodel.make_params(
    cen=-0.005, 
    amp=10, 
    wid=0.002)

params = lmfit.Parameters()
params.add('cen', value=-0.005, min=-0.015, max=0.015, vary=True)
params.add('amp', value=10, min=0, max=20, vary=True)
params.add('wid', value=0.002, min=0, max=0.015, vary=True)
params.add('off', value=1, min=-5, max=5, vary=True)

result = gmodel.fit(Y_Slice_central, params, x=y_angle_central)

fig = pyplot.figure(figsize=(12,6))
gs = fig.add_gridspec(1, 3)
gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

ax = fig.add_subplot(gs[0,0])
ax.imshow(image)

ax = fig.add_subplot(gs[0,1])
ax.plot(x_angle, X_Slice_central)

ax = fig.add_subplot(gs[0,2])
ax.plot(y_angle_central, Y_Slice_central)
ax.plot(y_angle_central, result.best_fit, 'r-', label='best fit')

fig.savefig('HighResolution.pdf')