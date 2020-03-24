#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:01:11 2020

@author: ispielma
"""

import numpy as np
import Camera_Generic
from pypylon import pylon, genicam

class Camera(Camera_Generic.Camera):
        
    def __init__(self, serial_number, **kwargs):
        super().__init__(**kwargs)
        
        # Find the camera:
        print("Finding camera...")
        Tl_instance = pylon.TlFactory.GetInstance()
        for cam in Tl_instance.EnumerateDevices():
            sn = cam.GetSerialNumber()
            print("{0:} {1:x} {2:x}".format(sn, int(sn), serial_number))
            if serial_number == int(sn):
                self.camera = Tl_instance.CreateDevice(cam)
                
                break
        else:
            msg = f"No connected camera with serial number {serial_number:X} found"
            raise Exception(msg)
        # Connect to the camera:
        print("Connecting to camera...")
        self.pylon_camera = pylon.InstantCamera(self.camera)
        self.pylon_camera.Open()
        self._nodemap = self.pylon_camera.GetNodeMap()
        
        # Keep an img attribute so we don't have to create it every time
        # self._img = nv.imaqCreateImage(nv.IMAQ_IMAGE_U16)

    def close(self):
        self.pylon_camera.Close()

    def get_attribute_names(self, visibility_string, writeable_only=True):
        """Return a list of all attribute names of readable attributes, for the given
        visibility level. Optionally return only writeable attributes
        
        This will be accomplished by recursivly traveling the nodemap
        """
        visibilities = {
            'simple': 0,
            'intermediate': 1,
            'advanced': 2,
        }
        visibility_level = visibilities[visibility_string.lower()]
    
        inodes = self._nodemap.GetNodes()
        
        Names = []
        for inode in inodes:
            node = inode.GetNode()
            
            # now filter this guy
            if not node.IsFeature():
                continue
    
            if node.GetVisibility() > visibility_level:
                continue
            
            if not hasattr(inode, 'GetValue'):
                continue
            
            accessmode = genicam.EAccessModeClass_ToString(node.GetAccessMode())
                
            if writeable_only:
                if accessmode.lower() not in ['rw'] or not hasattr(inode, 'SetValue') :
                    continue
            elif accessmode.lower() not in ['rw', 'ro']:
                continue
            
            Names.append(self._GetFullNodeName(node))
    
        return sorted(Names)
        
    def _GetFullNodeName(self, node):
            
        parents = node.GetParents()
            
        Names = [node.GetName()]
        while len(parents) > 0:
            node = parents[0].GetNode()
            parents = node.GetParents()
            Name = node.GetName()
                
            # Avoid infinite recursion
            if Name in Names:
                break
                
            Names = [Name] + Names
            
        FullName = Names.pop()
        Names.reverse()
        for Name in Names:
            FullName = Name + "::" + FullName
            
        return FullName
    
def GetValue(camera, key, nodemap=None):
    if nodemap is None:
        nodemap = camera.GetNodeMap()
    inode = nodemap.GetNode(key)
    
    value = inode.GetValue()

    return value

# Demonstrate field propogation
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')

    with Camera(0x14eef0d) as cam:
        attrs = cam.get_attribute_names("intermediate", writeable_only=True)
        print(attrs)
        

