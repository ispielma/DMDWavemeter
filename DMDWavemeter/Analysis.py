# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 19:57:31 2020

This is a tempory file with which I am working on the analysis methods for
typical data.

@author: ispielma
"""

import numpy as np
import scipy.signal
import h5py
import lmfit

def gaussian(x, amp, cen, wid, off):
    return amp * np.exp(-(x-cen)**2 / wid**2) + off

gmodel = lmfit.Model(gaussian)




def QuickProcess(FileName):

    with h5py.File(FileName, "a") as file:
        image = file["image"][:]
    
    # 100 mm focal lenght lens
    f = 0.1
    dx = 5.5e-6 # based on the CMV4000 NIR-enhanced
    dx_DMD = 7.637e-6 # based on DLP3000
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
    
    Y_Slice = image.mean(axis=1)
    
    #
    # Estimate peak properties
    #
    
    Y_peaks, stats = scipy.signal.find_peaks(Y_Slice, 
                                           height=Y_Slice.max()/5,
                                           width=10)
    
    #
    # The peak closest to zero should be from the overall pixel structure
    #

    # keep three central peaks
    indices = np.argsort(np.abs(y_angle[Y_peaks]))

    y_0_index = Y_peaks[indices[0]]
    
    y_angle -= y_angle[y_0_index]
    
    #
    # First estimate of wavelength
    # 
    
    
    
    AngleCoarse = np.mean(np.abs(y_angle[Y_peaks[indices[1:3]]]))
    print(4*np.sin(AngleCoarse)*dx_DMD/np.sqrt(2) )
    
    #
    # Do an X slice along the center discovered from the peak
    #
    
    width = 256
    position = y_0_index
    CentralSlice = image[:][position-width:position+width]
    y_angle_central = y_angle[position-width:position+width]
    
    X_Slice_central = CentralSlice.mean(axis=0)
    Y_Slice_central = CentralSlice.mean(axis=1)

    #
    # Fit the y curve
    #
    
    params = lmfit.Parameters()
    
    wid = (y_angle_central.max() - y_angle_central.min()) / 20
    params.add('wid', value=wid, min=0, max=wid*10, vary=True)
    
    cen = y_angle_central[np.argmax(Y_Slice_central)]
    params.add('cen', value=cen, min=cen-5*wid, max=cen+5*wid, vary=True)
    
    amp = Y_Slice_central.max()
    params.add('amp', value=0.9*amp, min=0.1*amp, max=2*amp, vary=True)
    
    off = (Y_Slice_central[0:width//8].mean() + Y_Slice_central[-width//8:-1].mean()) / 2
    params.add('off', value=off, vary=True)
    
    result = gmodel.fit(Y_Slice_central, params, x=y_angle_central)
    
    results = {
        'result': result,
        'image': image,
        'x_angle': x_angle,
        'X_Slice_central': X_Slice_central,
        'y_angle': y_angle,
        'Y_Slice': Y_Slice,
        'Y_peaks': Y_peaks,
        'y_angle_central': y_angle_central
    }
    
    return results
    
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    pyplot.style.use(path + '/matplotlibrc')
    
    results = QuickProcess('demo.h5')
    
    fig = pyplot.figure(figsize=(12,6))
    gs = fig.add_gridspec(1, 3)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  
    
    ax = fig.add_subplot(gs[0,0])
    ax.imshow(results['image'])
    
    ax = fig.add_subplot(gs[0,1])
    ax.plot(results['x_angle'], results['X_Slice_central'])
    
    ax = fig.add_subplot(gs[0,2])
    ax.plot(results['y_angle'], results['Y_Slice'])
    ax.plot(results['y_angle'][results['Y_peaks']], results['Y_Slice'][results['Y_peaks']], ".")
    
    ax.plot(results['y_angle_central'], results['result'].best_fit, 'r-', label='best fit')
    