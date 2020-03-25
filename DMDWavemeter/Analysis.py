# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 19:57:31 2020

This is a tempory file with which I am working on the analysis methods for
typical data.

@author: ispielma
"""

import numpy as np
import astropy.convolution
import skimage.feature
import h5py
import lmfit

def gaussian(x, amp, cen, wid, off):
    return amp * np.exp(-(x-cen)**2 / wid**2) + off


gmodel = lmfit.Model(gaussian)


def PixelToAngle(pixel, size, dx, f):
    angle = dx * (pixel - size/2)
    return angle / f

def QuickProcess(FileName, ImageMax=4095):
    """
    ImageMax defines what consititutes saturation
    """

    # 100 mm focal lenght lens
    f = 0.1
    dx = 5.5e-6 # based on the CMV4000 NIR-enhanced
    dx_DMD = 7.637e-6 # based on DLP3000
    theta = 26 * np.pi / 180 # DMD beam angle

    data = {}
    with h5py.File(FileName, "a") as file:
        data['StandardFrame'] = file["StandardFrame"][:]
        data['ones'] = file["ones"][:]
        data['zeros'] = file["zeros"][:]

    shape = data['ones'].shape


    
    #
    # subtract ones (which is dark) from other frames
    # 
    
    kernel = astropy.convolution.Gaussian2DKernel(x_stddev=3)

    image_conv = astropy.convolution.convolve(data['ones'], kernel)

    kernel = astropy.convolution.Gaussian2DKernel(x_stddev=2)

    data['StandardFrame'] = data['StandardFrame'] -image_conv
    data['StandardFrame'] = astropy.convolution.convolve(data['StandardFrame'], kernel)
    data['zeros'] = data['zeros'] -image_conv
    data['zeros'] = astropy.convolution.convolve(data['zeros'], kernel)

    
    #
    # Begin with the 2a data with the goal of locating the grid of
    # peaks
    # 

    image = data['StandardFrame'] 


    #
    # Try scikit image
    #

    peaks = skimage.feature.peak_local_max(image, 
                                   threshold_abs=image.max() / 50,
                                   exclude_border=50,
                                   min_distance=400)

    #
    # Fit the y curve
    #
    
    # params = lmfit.Parameters()
    
    # wid = (y_angle_central.max() - y_angle_central.min()) / 20
    # params.add('wid', value=wid, min=0, max=wid*10, vary=True)
    
    # cen = y_angle_central[np.argmax(Y_Slice_central)]
    # params.add('cen', value=cen, min=cen-5*wid, max=cen+5*wid, vary=True)
    
    # amp = Y_Slice_central.max()
    # params.add('amp', value=0.9*amp, min=0.1*amp, max=2*amp, vary=True)
    
    # off = (Y_Slice_central[0:width//8].mean() + Y_Slice_central[-width//8:-1].mean()) / 2
    # params.add('off', value=off, vary=True)
    
    # result = gmodel.fit(Y_Slice_central, params, x=y_angle_central)
    
    
    angular_coords = PixelToAngle(peaks, np.array(shape), dx, f)
    num_peaks = angular_coords.shape[0]
    d = []
    for i in range(num_peaks -1):
        for j in range(i+1, num_peaks):
            
            delta = angular_coords[i,:]  - angular_coords[j,:] 
            d.append (  np.sqrt(delta @ delta) )
         

    d = np.array(d)
    keep = d < 1.2*d.min()
    d = d[keep]
    delta_d = d.std()
    d = d.mean()
    
    
    
    #
    # Estimate of wavelength from smallest spacing
    # 
    
    # I divide d by sqrt(2) because my equations look at x and y 
    # directions seperatly, not the diagional as computed above
    # 
    # There is a fudge factor of before the dx_DMD here.  And also in the 
    # ewquation for d_angle
    wavelength = (d / np.sqrt(2) )* (2*2*dx_DMD / np.sqrt(2))
    print("Wavelength from small kick", wavelength, delta_d * (2*dx_DMD) )
    
    print("incident angle / Angle between two on-axes orders ", 
          theta / (d*np.sqrt(2)) )
    
    # Now try to work out n+m for the peaks
    
    for angular_coord in angular_coords:
        print("Looking at: ", angular_coord)
        
        # Compute the number of momentum
        # kicks it should have received.
        d_angle = (np.sin(theta) - angular_coord[1])
        d_angle *= (2*2*dx_DMD/np.sqrt(2)) / wavelength
        
        print(d_angle)
            
            
    
    
    # x_tan = 
    
    
    results = {
        'data': data,
        'peaks': peaks
    }
    
    return results
    
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    pyplot.style.use(path + '/matplotlibrc')
    
    results = QuickProcess('demo.h5')
    
    fig = pyplot.figure(figsize=(6,8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1,0.3])
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  
    
    ax = fig.add_subplot(gs[0,0:2])
    ax.imshow(results['data']['StandardFrame'])
    ax.plot(results['peaks'][:, 1], 
            results['peaks'][:, 0], 'ro', markersize=12, fillstyle='none')
    
    