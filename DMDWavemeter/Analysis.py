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

DO_GAUSS = False

# 100 mm focal lenght lens
f = 0.10
dx = 5.5e-6 # based on the CMV4000 NIR-enhanced
dx_DMD = 7.637e-6 # based on DLP3000
theta = (77.6) * np.pi / 180 # DMD beam angle,


def gaussian(x, amp, cen, wid, off):
    return amp * np.exp(-(x-cen)**2 / wid**2) + off


def gaussian2D(xy_mesh, amp, x0, y0, xwidth, ywidth, offset):
    (x, y) = xy_mesh
    
    return amp*np.exp(-(((x0-x)/xwidth)**2 + ((y0-y)/ywidth)**2)/2.0) + offset

gmodel = lmfit.Model(gaussian2D)

def PixelToAngle(pixel, size, dx, f):
    angle = dx * (pixel - size/2)
    return angle / f

def QuickProcess(FileName, ImageMax=4095, DoPlot=False):
    """
    ImageMax defines what consititutes saturation
    """

    data = {}
    with h5py.File(FileName, "a") as file:
        data['StandardFrame'] = file["StandardFrame"][:]
        data['ones'] = file["ones"][:]
        data['zeros'] = file["zeros"][:]

    shape = data['ones'].shape

    xvals = PixelToAngle(np.arange(shape[1]),shape[1], dx, f)
    yvals = PixelToAngle(np.arange(shape[0]),shape[0], dx, f)

    xyvals = np.meshgrid(xvals, yvals)

    
    #
    # subtract ones (which is dark) from other frames
    # 
    
    kernel = astropy.convolution.Gaussian2DKernel(x_stddev=3)

    image_conv = astropy.convolution.convolve(data['ones'], kernel)

    kernel = astropy.convolution.Gaussian2DKernel(x_stddev=2)

    # data['StandardFrame'] = data['StandardFrame'] -image_conv
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
                                   threshold_abs=image.max() / 10,
                                   exclude_border=50,
                                   min_distance=300)
    num_peaks = peaks.shape[0]
    angular_coords = PixelToAngle(peaks, np.array(shape), dx, f)    
    
    for j in range(num_peaks):
        angular_coord = angular_coords[j]
        
        peak = peaks[j]
        
        #
        # Chop a box around each peak
        # 

        ROI = image[peak[0]-50:peak[0]+50, peak[1]-50:peak[1]+50]
        ROI_yvals = xyvals[0][peak[0]-50:peak[0]+50, peak[1]-50:peak[1]+50]
        ROI_xvals = xyvals[1][peak[0]-50:peak[0]+50, peak[1]-50:peak[1]+50]

        #
        # Fit to 2D gaussian
        #
        
        params = lmfit.Parameters()
        
        params.add('x0', value=angular_coord[0], vary=True)
        params.add('y0', value=angular_coord[1], vary=True)
        
        params.add('xwidth', value=0.0002, min=0, max=2, vary=True)
        params.add('ywidth', value=0.0002, min=0, max=2, vary=True)
        
        amp = image[peak[0], peak[1]]

        params.add('amp', value=amp, min=0, max=4096, vary=True)
        params.add('offset', value=0, min=-1000, max=1000, vary=True)
        
        xy_mesh = ( ROI_xvals.ravel(), ROI_yvals.ravel() )
        
        fit_results = gmodel.fit(ROI.ravel(), params, xy_mesh=xy_mesh)
        
        angular_coord[0] = fit_results.best_values['x0']
        angular_coord[1] = fit_results.best_values['y0']
        print(fit_results.best_values)


    
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
    

    # The factor of 2 here is from the fact that we are diffracting from a
    # checkerboard pattern that doubles the DMD's period.
    wavelength = d*dx_DMD*2
    print("lambda = {:.3e} +- {:.2e}".format ( wavelength, 2*delta_d * (dx_DMD) ) )
    
    # Now try to work out n+m for the peaks
    
    kicks = []
    for j in range(num_peaks):
        angular_coord = angular_coords[j]
        peak = peaks[j]
               
        d_angle = np.array([0.0,0.0])
        # Compute the number of momentum kicks it should have received.
        d_angle[1] = (np.sin(theta) - angular_coord[1]) 
        d_angle[0] = angular_coord[0]
        d_angle /= (d / np.sqrt(2))
        
        kicks.append (np.round(d_angle) ) 
        
        print("Looking at: ", peak, d_angle, np.round(d_angle), 
              2*np.sqrt(2)*dx_DMD*(np.sin(theta) - angular_coord[1]) / kicks[-1][1]
              )
        
    kicks = np.array(kicks)   
    
    xvals = 2*np.sqrt(2)*dx_DMD*(np.sin(theta) - xvals) / 12
    
    #
    # Make a new x axis in units of wavelength
    # 

    # Find best angle so peaks are an integer number of events from zero
    # TODO:
        
    
    x_lambda = PixelToAngle(np.arange(shape[1]),shape[1], dx, f)
    y_lambda = PixelToAngle(np.arange(shape[0]),shape[0], dx, f)

            
    #
    #Slices
    # 
    
    xslice = image[shape[0]//2 - 32:shape[0]//2 + 32,:].max(axis=0)

    results = {
        'data': data,
        'xslice': xslice,
        'peaks': peaks,
        'angular_coords': angular_coords,
        'xyvals': xyvals,
        'xvals': xvals,
        'yvals': yvals,
        'x_lambda': x_lambda,
        'y_lambda': y_lambda,
        'ROI': ROI,
        'kicks': kicks
        }


    if DoPlot:
        fig = pyplot.figure(figsize=(6,8))
        gs = fig.add_gridspec(2, 2, height_ratios=[1,0.3])
        gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.2, wspace = 0.35)  
        
        ax = fig.add_subplot(gs[0,0:2])
        ax.pcolormesh(
            results['xyvals'][0],
            results['xyvals'][1],
            results['data']['StandardFrame'],
            vmax=256
            )
        ax.plot(results['angular_coords'][:, 1], 
                results['angular_coords'][:, 0], 'ro', markersize=12, fillstyle='none')
        
        ax = fig.add_subplot(gs[1,0])
        ax.plot(results['xvals'], results['xslice'])
        
        ax = fig.add_subplot(gs[1, 1])
        ax.imshow( results['ROI'], 
            vmin=0, 
            )
        
    return results

def BigGauss(FileName, maskpixels, ImageMax=4095, DoPlot=False):
    """
    ImageMax defines what consititutes saturation
    
    Here we are expecting a large gaussian.  This is to assure the alignment of the system
    """

    data = {}
    with h5py.File(FileName, "a") as file:
        data['random'] = file["random"][:]
        data['StandardFrame'] = file["StandardFrame"][:]
        data['ones'] = file["ones"][:]
        data['zeros'] = file["zeros"][:]

    shape = data['ones'].shape

    xvals = PixelToAngle(np.arange(shape[1]),shape[1], dx, f)
    yvals = PixelToAngle(np.arange(shape[0]),shape[0], dx, f)

    xyvals = np.meshgrid(xvals, yvals)

    
    #
    # subtract ones (which is dark) from other frames
    # 
    
    kernel = astropy.convolution.Gaussian2DKernel(x_stddev=3)

    image_conv = astropy.convolution.convolve(data['ones'], kernel)

    data['random'] = data['random'] -image_conv
    image = data['random']
    
    #
    # mask peaks
    # 

    for p in maskpixels:
       image[p[0][0]:p[0][1], p[1][0]:p[1][1]].fill(0)    


    #
    # Fit to 2D gaussian
    #
    
    params = lmfit.Parameters()
    
    params.add('x0', value=0.00, min=-0.05, max=0.05, vary=True)
    params.add('y0', value=0.00, min=-0.05, max=0.05, vary=True)
    
    params.add('xwidth', value=0.04, min=0, max=2, vary=True)
    params.add('ywidth', value=0.04, min=0, max=2, vary=True)
    
    params.add('amp', value=128, min=0, max=4096, vary=True)
    params.add('offset', value=0, min=-1000, max=1000, vary=True)
    
    xy_mesh = ( xyvals[0].ravel(), xyvals[1].ravel() )
    
    fit_results = gmodel.fit(image.ravel(), params, xy_mesh=xy_mesh)


    
    results = {
        'data': data,
        'xyvals': xyvals,
        'xvals': xvals,
        'yvals': yvals,
        'fit_results': fit_results
    }
    
    if DoPlot:
        fig = pyplot.figure(DoPlot, figsize=(12,4))
        gs = fig.add_gridspec(1, 3)
        gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.2, wspace = 0.35)  
        
        ax = fig.add_subplot(gs[0,0])
        ax.pcolormesh(
            results['xyvals'][0],
            results['xyvals'][1],
            results['data']['zeros'],
            vmin=0, vmax=256
            )
    
        ax = fig.add_subplot(gs[0,1])
        ax.pcolormesh(
            results['xyvals'][0],
            results['xyvals'][1],
            results['data']['random'],
            vmin=0, vmax=256
            )
     
        ax = fig.add_subplot(gs[0,2])
        ax.pcolormesh(
            results['xyvals'][0],
            results['xyvals'][1],
            results['data']['random'],
            vmin=0, vmax=256
            )
        ax.contour(
            results['xyvals'][0],
            results['xyvals'][1],
            results['fit_results'].best_fit.reshape( results['xyvals'][0].shape ),
            )       
    return results
    

    
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    pyplot.style.use(path + '/matplotlibrc')
    
    
    #
    # Analysis for typical noise case.  Super-bright beams.
    #
    
    if DO_GAUSS:
    
        mask_pixels = [ 
            [[1024-20,1024+20], [1200, 1800]],
            [[1024-100,1024+100], [1490-20, 1490+20]],        
            [[1024-20,1024+20], [100, 200]],
            [[765-20,765+20], [120, 250]]
    
            ]
        GaussResults = BigGauss('data/2020_03_27_data_780_0001.h5', 
                                mask_pixels, DoPlot=1)
    
 

    #
    # Analysis for typical grid.  First 87 line
    #
    
    First87Results_4 = QuickProcess('data/2020_08_03_data_780_0000.h5', 
                            DoPlot=True)


    fig = pyplot.figure(0, figsize=(8,5))
    gs = fig.add_gridspec(1, 1)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.2, hspace=0.4, wspace = 0.35)  
    
    ax = fig.add_subplot(gs[0,0])
    ax.plot(First87Results_4['xvals']*1e9, First87Results_4['xslice'], "-", color='r')
    # ax.plot(First87Results_5['xvals'], First87Results_5['xslice'], color='k')
    # ax.plot(First87Results_6['xvals'], First87Results_6['xslice'], color='b')
    # ax.plot(First87Results_7['xvals'], First87Results_7['xslice'], color='g')
    # ax.plot(First87Results_8['xvals'], First87Results_8['xslice'], color='g')
    
    # ax.set_xlim([776, 782])
    ax.set_ylim([0, 1e3])
    ax.set_xlabel('Wavelength (nm)')

    