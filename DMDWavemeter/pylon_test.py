#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:16:43 2020

@author: ispielma
"""


from pypylon import pylon, genicam



def RecurseNodeTree(Roots, visibility_string, ParentName='',  writeable_only=True):
    """
    Recurse  the Node tree and return a list of redreadable nodes
    writeable_only further limits to rw

    """
    visibilities = {
        'simple': 0,
        'intermediate': 1,
        'advanced': 2,
    }
    visibility_level = visibilities[visibility_string.lower()]

    
    Names = []
    for inode in Roots:
        node = inode.GetNode()
        if node.IsFeature():

            visibility = node.GetVisibility()
            accessmode = genicam.EAccessModeClass_ToString(node.GetAccessMode())
            if len(ParentName) == 0:
                FullName = node.GetName()
            else:
                FullName = ParentName + '::' + node.GetName()

            children = node.GetChildren()
            
            # If we have some children, see if they are to be added
            if len(children) > 0:
                NewNames = RecurseNodeTree(children, visibility_string, ParentName=FullName)
            else:
                NewNames = []
            
            if len(NewNames) > 0:
                Names += NewNames
            
            # Make sure we can set and get values
            
            
            if visibility <= visibility_level:
                if writeable_only:
                    if accessmode.lower() in ['rw'] and hasattr(inode, 'GetValue') and hasattr(inode, 'SetValue') :
                        Names.append(FullName)
                elif accessmode.lower() in ['rw', 'ro'] and hasattr(inode, 'GetValue'):
                    Names.append(FullName)

    return Names
        
def GetRoots(camera):
    nodemap = camera.GetNodeMap()
    inodes = nodemap.GetNodes()
    
    Roots = []
    for inode in inodes:
        node = inode.GetNode()
        children = node.GetChildren()
        parents = node.GetParents()
        feature = node.IsFeature()
    
        
        # Find Root features
        if feature and len(parents) == 0 and len(children) > 0:
            Roots.append(inode)
            
    return Roots
    
def GetValue(camera, key, nodemap=None):
    if nodemap is None:
        nodemap = camera.GetNodeMap()
    inode = nodemap.GetNode(key)
    
    value = inode.GetValue()

    return value

cam = pylon.TlFactory.GetInstance().CreateFirstDevice()
camera = pylon.InstantCamera(cam)
camera.Open()

Roots = GetRoots(camera)
Keys = RecurseNodeTree(Roots, 'intermediate')
AllKeys = {k: GetValue(camera, k.split("::")[-1]) for k in Keys}

camera.Close()