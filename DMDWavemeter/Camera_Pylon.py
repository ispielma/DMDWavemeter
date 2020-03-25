#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:01:11 2020

@author: ispielma
"""

import Camera_Generic
from pypylon import pylon, genicam

class Camera(Camera_Generic.Camera):
    defaults = {
         'Root::ImageFormat::PixelFormat': 'Mono12',
         'Root::ImageFormat::ReverseX': False,
         'Root::ImageFormat::ReverseY': False,
         'Root::ImageFormat::TestImageSelector': 'Off',
         'Root::AOI::BinningHorizontal': 1,
         'Root::AOI::BinningVertical': 1,
         'Root::AOI::CenterX': False,
         'Root::AOI::CenterY': False,
         'Root::AOI::DecimationVertical': 1,
         'Root::AOI::Height': 2048,
         'Root::AOI::OffsetX': 0,
         'Root::AOI::OffsetY': 0,
         'Root::AOI::StackedZoneImaging::StackedZoneImagingEnable': False,
         'Root::AOI::Width': 2045,
         'Root::AcquisitionTrigger::AcquisitionFrameCount': 1,
         'Root::AcquisitionTrigger::AcquisitionFrameRateAbs': 1.0,
         'Root::AcquisitionTrigger::AcquisitionFrameRateEnable': False,
         'Root::AcquisitionTrigger::AcquisitionMode': 'Continuous',
         'Root::AcquisitionTrigger::AcquisitionStatusSelector': 'FrameTriggerWait',
         'Root::AcquisitionTrigger::ExposureAuto': 'Off',
         'Root::AcquisitionTrigger::ExposureMode': 'Timed',
         'Root::AcquisitionTrigger::ExposureTimeAbs': 100.0,
         'Root::AcquisitionTrigger::ExposureTimeRaw': 100,
         'Root::AcquisitionTrigger::TriggerActivation': 'RisingEdge',
         'Root::AcquisitionTrigger::TriggerDelayAbs': 0.0,
         'Root::AcquisitionTrigger::TriggerMode': 'Off',
         'Root::AcquisitionTrigger::TriggerSelector': 'FrameStart',
         'Root::AcquisitionTrigger::TriggerSource': 'Line1',
         'Root::AnalogControls::BlackLevelRaw': 0,
         'Root::AnalogControls::BlackLevelSelector': 'All',
         'Root::AnalogControls::DigitalShift': 0,
         'Root::AnalogControls::GainAuto': 'Off',
         'Root::AnalogControls::GainRaw': 36,
         'Root::AnalogControls::GainSelector': 'All',
         'Root::AnalogControls::Gamma': 1.0,
         'Root::AnalogControls::GammaEnable': False,
         'Root::AnalogControls::GammaSelector': 'User',
         'Root::AutoFunctions::AutoExposureTimeAbsLowerLimit': 100.0,
         'Root::AutoFunctions::AutoExposureTimeAbsUpperLimit': 500000.0,
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIHeight': 2048,
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetX': 0,
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetY': 0,
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOISelector': 'AOI1',
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageIntensity': True,
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageWhiteBalance': False,
         'Root::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIWidth': 2048,
         'Root::AutoFunctions::AutoFunctionProfile': 'GainMinimum',
         'Root::AutoFunctions::AutoGainRawLowerLimit': 36,
         'Root::AutoFunctions::AutoGainRawUpperLimit': 512,
         'Root::AutoFunctions::AutoTargetValue': 2048,
         'Root::AutoFunctions::GrayValueAdjustmentDampingAbs': 0.68359375,
         'Root::AutoFunctions::GrayValueAdjustmentDampingRaw': 700,
         'Root::ChunkDataStreams::ChunkModeActive': False,
         'Root::DeviceInformation::DeviceUserID': 'big_boy',
         'Root::DigitalIO::LineDebouncerTimeAbs': 0.0,
         'Root::DigitalIO::LineFormat': 'OptoCoupled',
         'Root::DigitalIO::LineInverter': False,
         'Root::DigitalIO::LineMode': 'Input',
         'Root::DigitalIO::LineSelector': 'Line1',
         'Root::DigitalIO::SyncUserOutputSelector': 'SyncUserOutput1',
         'Root::DigitalIO::SyncUserOutputValue': False,
         'Root::DigitalIO::SyncUserOutputValueAll': 0,
         'Root::DigitalIO::UserOutputSelector': 'UserOutput1',
         'Root::DigitalIO::UserOutputValue': False,
         'Root::DigitalIO::UserOutputValueAll': 0,
         'Root::EventsGeneration::EventNotification': 'Off',
         'Root::EventsGeneration::EventSelector': 'ExposureEnd',
         'Root::LUTControls::LUTEnable': False,
         'Root::LUTControls::LUTIndex': 0,
         'Root::LUTControls::LUTSelector': 'Luminance',
         'Root::LUTControls::LUTValue': 0,
         'Root::SequenceControl::SequenceEnable': False,
         'Root::SequenceControl::SequenceSetIndex': 0,
         'Root::SequenceControl::SequenceSetTotalNumber': 2,
         'Root::TimerControls::CounterEventSource': 'FrameTrigger',
         'Root::TimerControls::CounterResetSource': 'Off',
         'Root::TimerControls::CounterSelector': 'Counter1',
         'Root::TimerControls::TimerDelayAbs': 0.0,
         'Root::TimerControls::TimerDelayRaw': 0,
         'Root::TimerControls::TimerDelayTimebaseAbs': 1.0,
         'Root::TimerControls::TimerDurationAbs': 4095.0,
         'Root::TimerControls::TimerDurationRaw': 4095,
         'Root::TimerControls::TimerDurationTimebaseAbs': 1.0,
         'Root::TimerControls::TimerSelector': 'Timer1',
         'Root::TimerControls::TimerTriggerActivation': 'RisingEdge',
         'Root::TimerControls::TimerTriggerSource': 'ExposureStart',
         'Root::TransportLayer::GevSCBWR': 10,
         'Root::TransportLayer::GevSCBWRA': 2,
         'Root::TransportLayer::GevSCFTD': 0,
         'Root::TransportLayer::GevSCPD': 0,
         'Root::TransportLayer::GevSCPSPacketSize': 1500,
         'Root::UserSets::DefaultSetSelector': 'Standard',
         'Root::UserSets::UserSetDefaultSelector': 'Default',
         'Root::UserSets::UserSetSelector': 'Default'
         }        
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
        print("Connected to to camera!")
        
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

    def get_attribute(self, FullName, return_dict=False):
        """Return current value of attribute of the given name
        if return_dict, we will return a populated dictionary for the value
        {'value': value, 'min':min, ...}
        """
        name = FullName.split("::")[-1]
        try:
            
            inode = self._nodemap.GetNode(name)    
            value = inode.GetValue()
            return value
        except Exception as e:
            # Add some info to the exception:
            raise Exception(f"Failed to get attribute {name}") from e

    def set_attribute(self, FullName, value):
        """Set the value of the attribute of the given name to the given value"""
        name = FullName.split("::")[-1]

        try:
            inode = self._nodemap.GetNode(name) 
            inode.SetValue(value)

        except Exception as e:
            # Add some info to the exception:
            msg = f"failed to set attribute {name} to {value}"
            raise Exception(msg) from e

    def snap(self):
        """Acquire a single image and return it"""
        attempts = 128
        
        print("Snapping... Setup")
        self.pylon_camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
        print("Snapping... Acquring")
        
        for attempt in range(attempts):
            try:
                with self.pylon_camera.RetrieveResult(5000) as result:
                    if result.GrabSucceeded():
                        # Access the image data.
        
                        data = result.Array
            except:
                print("Fail grab attempt {}".format(attempt))
        
        print("Snapping... Stopping")
        self.pylon_camera.StopGrabbing()        
            
        return data

# Demonstrate field propogation
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')

    with Camera(0x14eef0d) as cam:
        cam.set_attributes(cam.defaults)
        
        image = cam.snap()
        
    fig = pyplot.figure(figsize=(6,6))
    gs = fig.add_gridspec(1, 1)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

    ax = fig.add_subplot(gs[0,0])
    ax.imshow(image)

