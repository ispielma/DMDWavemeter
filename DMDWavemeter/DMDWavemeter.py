# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:04:11 2020

Main code to write patterns to the DMD and to read back the Fourier space
results containing information about the optical wavelength.

@author: ispielma
"""

# COMMON IMPORTS
import time
import h5py  
from Camera_Pylon import Camera

from DMD_Lightcrafter import LightCrafterWorker
        

class WaveMeter():
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        
        try:
            self.DMD.shutdown()
        except:
            print("DMD Shutdown Falied")
            
        self.Camera.close()
    
    def __init__(self, LightCrafterHost='192.168.1.100', Camera_serial=0x30531DC20D):
        
        self.DMD = LightCrafterWorker(host=LightCrafterHost)
        self.Camera = Camera(Camera_serial)
        
    def AcquireStandardFrame(self, option=None):
        """
        Configure the DMD for a standard acquisition and grab a frame.

        Returns
        -------
        None.

        """

        
        self.DMD.SetStandardFrame(option=option)
        time.sleep(0.1)
        self.StandardFrame = Wave.Camera.snap()
        
        return self.StandardFrame

    def SaveAll(self, filename, name='StandardFrame'):
        """
        Sdaves the current full frame into an h5 file

        Parameters
        ----------
        filename : string
            where to save the file.

        Returns
        -------
        None.

        """
        
        with h5py.File(filename, "a") as file:
             file.create_dataset(name, 
                                 data=self.StandardFrame,
                                 compression="gzip")

# Sample execution of wavemeter
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')
    Camera_serial = 0x30531DC20D # for imaqdx bigboy
    Camera_serial = 0x14eef0d # for pylon bigboy
    FileName='data/2020_03_27_data_780_0008.h5'
    
    with WaveMeter(LightCrafterHost='192.168.1.100', Camera_serial=Camera_serial) as Wave:        
    
        # image = Wave.AcquireStandardFrame(option='ones')
        # Wave.SaveAll(FileName, name='ones')

        # image = Wave.AcquireStandardFrame(option='ones')
        # Wave.SaveAll(FileName, name='zeros')   
        
        # image = Wave.AcquireStandardFrame(option='random')
        # Wave.SaveAll(FileName, name='random')   
        
        image = Wave.AcquireStandardFrame()
        # Wave.SaveAll(FileName)

    # subimage = image[1024-64:1024+64, 150-64:150+64]
    # print(subimage.max() )

    fig = pyplot.figure(figsize=(12,6))
    gs = fig.add_gridspec(1, 2)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

    

    ax = fig.add_subplot(gs[0,0])
    ax.imshow(image, aspect='auto')
    # ax.set_ylim([1024-128, 1024+128])
    # ax.set_xlim([200-128, 200+128])
    ax.axhline(1028)
    
    ax = fig.add_subplot(gs[0,1])
    ax.plot(image.max(axis=0))

    
    