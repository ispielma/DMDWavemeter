#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:16:43 2020

@author: ispielma
"""


from pypylon import pylon, genicam



def RecurseNodeTree(camera, visibility_string, writeable_only=True):
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

    nodemap = camera.GetNodeMap()
    inodes = nodemap.GetNodes()
    
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
        
        Names.append(GetFullName(node))

    return Names
        
def GetFullName(node):
    
    parents = node.GetParents()
    
    Names = [node.GetName()]
    while len(parents) > 0:
        node = parents[0].GetNode()
        parents = node.GetParents()
        Name = node.GetName()
        
        # Avoid infinite recursion
        if Name in Names:
            break
        
        Names.append( Name )
    Names.reverse()
    
    FullName = Names.pop()
    for Name in Names:
        FullName = Name + "::" + FullName
    
    return FullName
    
def GetValue(camera, key, nodemap=None):
    if nodemap is None:
        nodemap = camera.GetNodeMap()
    inode = nodemap.GetNode(key)
    
    value = inode.GetValue()

    return value

cam = pylon.TlFactory.GetInstance().CreateFirstDevice()
camera = pylon.InstantCamera(cam)
camera.Open()

Keys = RecurseNodeTree(camera, "advanced", writeable_only=True)

camera.Close()