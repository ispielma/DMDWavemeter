#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:01:11 2020

@author: ispielma
"""

import numpy as np
import Camera_Generic
from pypylon import pylon

class Camera(Camera_Generic.Camera):
        
    def __init__(self, serial_number, **kwargs):
        super().__init__(**kwargs)
        
        # Find the camera:
        print("Finding camera...")
        for cam in pylon.TlFactory.GetInstance().EnumerateDevices():
            sn = cam.GetSerialNumber()
            print("{0:} {1:x} {2:x}".format(sn, int(sn), serial_number))
            if serial_number == sn:
                self.camera = cam
                break
        else:
            msg = f"No connected camera with serial number {serial_number:X} found"
            raise Exception(msg)
        # Connect to the camera:
        print("Connecting to camera...")
        # self.imaqdx = nv.IMAQdxOpenCamera(
        #    self.camera.InterfaceName, nv.IMAQdxCameraControlModeController
        #)
        
        # Keep an img attribute so we don't have to create it every time
        # self._img = nv.imaqCreateImage(nv.IMAQ_IMAGE_U16)

# Demonstrate field propogation
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')

    with Camera(0x30531DC20D) as cam:
        pass
        

