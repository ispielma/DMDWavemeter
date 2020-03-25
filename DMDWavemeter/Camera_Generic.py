#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:01:11 2020

@author: ispielma
"""

import numpy as np

class Camera(object):
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
    
    def __init__(self, **kwargs):

        self._abort_acquisition = False

    def set_attributes(self, attr_dict, **kwargs):
        for k, v in attr_dict.items():
            self.set_attribute(k, v, **kwargs)

    def set_attribute(self, name, value):
        """Set the value of the attribute of the given name to the given value"""
        pass

    def get_attribute_names(self, visibility_level, writeable_only=True):
        """Return a list of all attribute names of readable attributes, for the given
        visibility level. Optionally return only writeable attributes"""
        attributes = []

        return sorted(attributes)

    def get_attributes(self, visibility_level, **kwargs):
        """Return a dict of all attribute names of readable attributes, for the given
        visibility level. Optionally return only writeable attributes"""
        
        attributes = self.get_attribute_names(visibility_level, **kwargs)
        
        return {k: self.get_attribute(k) for k in attributes}
        
    def get_attribute(self, name):
        """Return current value of attribute of the given name"""
        
        pass

    def snap(self):
        """Acquire a single image and return it"""
        return np.zeros( (0,0) )

    def configure_acquisition(self, continuous=True, bufferCount=5):
        pass

    def grab(self, waitForNextBuffer=True):
        return np.zeros( (0,0) )

    def grab_multiple(self, n_images, images, waitForNextBuffer=True):
        pass

    def stop_acquisition(self):
        pass

    def abort_acquisition(self):
        self._abort_acquisition = True

    def close(self):
        pass
