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
         'AcquisitionAttributes::CommandDuplicationEnable': {'value': False},
         'AcquisitionAttributes::HeartbeatTimeout': {'value': 3000,
          'min': 500,
          'max': 4294967295,
          'unit': ''},
         'AcquisitionAttributes::MaxRetryCountRead': {'value': 2,
          'min': 0,
          'max': 20,
          'unit': ''},
         'AcquisitionAttributes::MaxRetryCountWrite': {'value': 2,
          'min': 0,
          'max': 20,
          'unit': ''},
         'AcquisitionAttributes::ReadTimeout': {'value': 500,
          'min': 5,
          'max': 3600000,
          'unit': ''},
         'AcquisitionAttributes::WriteTimeout': {'value': 500,
          'min': 5,
          'max': 3600000,
          'unit': ''},
         'CameraAttributes::AOI::BinningHorizontal': {'value': 1,
          'min': 1,
          'max': 4,
          'unit': ''},
         'CameraAttributes::AOI::BinningVertical': {'value': 1,
          'min': 1,
          'max': 4,
          'unit': ''},
         'CameraAttributes::AOI::CenterX': {'value': False},
         'CameraAttributes::AOI::CenterY': {'value': False},
         'CameraAttributes::AOI::DecimationVertical': {'value': 1,
          'min': 1,
          'max': 2047,
          'unit': ''},
         'CameraAttributes::AOI::Height': {'value': 2048,
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AOI::OffsetX': {'value': 0,
          'min': 0,
          'max': 3,
          'unit': ''},
         'CameraAttributes::AOI::OffsetY': {'value': 0,
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AOI::StackedZoneImaging::StackedZoneImagingEnable': {'value': False},
         'CameraAttributes::AOI::Width': {'value': 2048,
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AcquisitionTrigger::AcquisitionFrameCount': {'value': 1,
          'min': 1,
          'max': 255,
          'unit': ''},
         'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateAbs': {'value': 1.0,
          'min': 0.014901161415892265,
          'max': 1000000.0,
          'unit': 'Hz'},
         'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateEnable': {'value': False},
         'CameraAttributes::AcquisitionTrigger::AcquisitionMode': {'value': 'Continuous',
          'symbolics': ('SingleFrame', 'Continuous')},
         'CameraAttributes::AcquisitionTrigger::AcquisitionStatusSelector': {'value': 'FrameTriggerWait',
          'symbolics': ('AcquisitionTriggerWait', 'FrameTriggerWait')},
         'CameraAttributes::AcquisitionTrigger::ExposureAuto': {'value': 'Off',
          'symbolics': ('Off', 'Once', 'Continuous')},
         'CameraAttributes::AcquisitionTrigger::ExposureMode': {'value': 'Timed',
          'symbolics': ('Timed', 'TriggerWidth')},
         'CameraAttributes::AcquisitionTrigger::ExposureTimeAbs': {'value': 100.0,
          'min': 24.0,
          'max': 10000000.0,
          'unit': 'us'},
         'CameraAttributes::AcquisitionTrigger::ExposureTimeRaw': {'value': 100,
          'min': 24,
          'max': 10000000,
          'unit': ''},
         'CameraAttributes::AcquisitionTrigger::TriggerActivation': {'value': 'RisingEdge',
          'symbolics': ('RisingEdge', 'FallingEdge')},
         'CameraAttributes::AcquisitionTrigger::TriggerDelayAbs': {'value': 0.0,
          'min': 0.0,
          'max': 1000000.0,
          'unit': 'us'},
         'CameraAttributes::AcquisitionTrigger::TriggerMode': {'value': 'Off',
          'symbolics': ('Off', 'On')},
         'CameraAttributes::AcquisitionTrigger::TriggerSelector': {'value': 'FrameStart',
          'symbolics': ('AcquisitionStart', 'FrameStart')},
         'CameraAttributes::AcquisitionTrigger::TriggerSource': {'value': 'Line1',
          'symbolics': ('Software', 'Line1')},
         'CameraAttributes::AnalogControls::BlackLevelRaw': {'value': 0,
          'min': 0,
          'max': 255,
          'unit': ''},
         'CameraAttributes::AnalogControls::BlackLevelSelector': {'value': 'All',
          'symbolics': ('All',)},
         'CameraAttributes::AnalogControls::DigitalShift': {'value': 0,
          'min': 0,
          'max': 4,
          'unit': ''},
         'CameraAttributes::AnalogControls::GainAuto': {'value': 'Off',
          'symbolics': ('Off', 'Once', 'Continuous')},
         'CameraAttributes::AnalogControls::GainRaw': {'value': 36,
          'min': 36,
          'max': 512,
          'unit': ''},
         'CameraAttributes::AnalogControls::GainSelector': {'value': 'All',
          'symbolics': ('All',)},
         'CameraAttributes::AnalogControls::Gamma': {'value': 0.0,
          'min': 0.0,
          'max': 3.9999847412109375,
          'unit': ''},
         'CameraAttributes::AnalogControls::GammaEnable': {'value': False},
         'CameraAttributes::AnalogControls::GammaSelector': {'value': 'User',
          'symbolics': ('User', 'sRGB')},
         'CameraAttributes::AutoFunctions::AutoExposureTimeAbsLowerLimit': {'value': 100.0,
          'min': 24.0,
          'max': 500000.0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoExposureTimeAbsUpperLimit': {'value': 500000.0,
          'min': 100.0,
          'max': 10000000.0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIHeight': {'value': 2048,
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetX': {'value': 0,
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetY': {'value': 0,
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOISelector': {'value': 'AOI1',
          'symbolics': ('AOI1', 'AOI2')},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageIntensity': {'value': True},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageWhiteBalance': {'value': False},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIWidth': {'value': 2048,
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionProfile': {'value': 'GainMinimum',
          'symbolics': ('GainMinimum', 'ExposureMinimum')},
         'CameraAttributes::AutoFunctions::AutoGainRawLowerLimit': {'value': 36,
          'min': 36,
          'max': 512,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoGainRawUpperLimit': {'value': 512,
          'min': 36,
          'max': 512,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoTargetValue': {'value': 2048,
          'min': 800,
          'max': 3280,
          'unit': ''},
         'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingAbs': {'value': 0.68359375,
          'min': 0.0,
          'max': 0.78125,
          'unit': ''},
         'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingRaw': {'value': 700,
          'min': 0,
          'max': 800,
          'unit': ''},
         'CameraAttributes::ChunkDataStreams::ChunkModeActive': {'value': False},
         'CameraAttributes::DeviceInformation::DeviceUserID': {'value': 'big_boy'},
         'CameraAttributes::DigitalIO::LineDebouncerTimeAbs': {'value': 0.0,
          'min': 0.0,
          'max': 20000.0,
          'unit': 'us'},
         'CameraAttributes::DigitalIO::LineFormat': {'value': 'OptoCoupled',
          'symbolics': ('OptoCoupled',)},
         'CameraAttributes::DigitalIO::LineInverter': {'value': False},
         'CameraAttributes::DigitalIO::LineMode': {'value': 'Input',
          'symbolics': ('Input',)},
         'CameraAttributes::DigitalIO::LineSelector': {'value': 'Line1',
          'symbolics': ('Line1', 'Out1')},
         'CameraAttributes::DigitalIO::SyncUserOutputSelector': {'value': 'SyncUserOutput1',
          'symbolics': ('SyncUserOutput1',)},
         'CameraAttributes::DigitalIO::SyncUserOutputValue': {'value': False},
         'CameraAttributes::DigitalIO::SyncUserOutputValueAll': {'value': 0,
          'min': 0,
          'max': 268435455,
          'unit': ''},
         'CameraAttributes::DigitalIO::UserOutputSelector': {'value': 'UserOutput1',
          'symbolics': ('UserOutput1',)},
         'CameraAttributes::DigitalIO::UserOutputValue': {'value': False},
         'CameraAttributes::DigitalIO::UserOutputValueAll': {'value': 0,
          'min': 0,
          'max': 268435455,
          'unit': ''},
         'CameraAttributes::EventsGeneration::EventNotification': {'value': 'Off',
          'symbolics': ('Off', 'GenICamEvent', 'On')},
         'CameraAttributes::EventsGeneration::EventSelector': {'value': 'ExposureEnd',
          'symbolics': ('ExposureEnd',
           'FrameStartOvertrigger',
           'AcquisitionStartOvertrigger',
           'FrameStart',
           'AcquisitionStart',
           'EventOverrun')},
         'CameraAttributes::ExpertFeatureAccess::ExpertFeatureAccessKey': {'value': 0,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::ExpertFeatureAccess::ExpertFeatureAccessSelector': {'value': 'ExpertFeature1',
          'symbolics': ('ExpertFeature1_Legacy',
           'ExpertFeature1',
           'ExpertFeature2',
           'ExpertFeature3',
           'ExpertFeature4',
           'ExpertFeature5')},
         'CameraAttributes::FileAccessControl::FileAccessLength': {'value': 0,
          'min': 0,
          'max': 1056,
          'unit': ''},
         'CameraAttributes::FileAccessControl::FileAccessOffset': {'value': 0,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::FileAccessControl::FileOpenMode': {'value': 'Read',
          'symbolics': ('Read', 'Write')},
         'CameraAttributes::FileAccessControl::FileOperationSelector': {'value': 'Open',
          'symbolics': ('Open',)},
         'CameraAttributes::FileAccessControl::FileSelector': {'value': 'UserSet1',
          'symbolics': ('UserSet1', 'UserSet2', 'UserSet3')},
         'CameraAttributes::ImageFormat::PixelFormat': {'value': 'Mono12',
          'symbolics': ('Mono8',
           'Mono12',
           'Mono12Packed',
           'YUV422Packed',
           'YUV422_YUYV_Packed')},
         'CameraAttributes::ImageFormat::ReverseX': {'value': False},
         'CameraAttributes::ImageFormat::ReverseY': {'value': False},
         'CameraAttributes::ImageFormat::TestImageSelector': {'value': 'Off',
          'symbolics': ('Off',
           'Testimage1',
           'Testimage2',
           'Testimage3',
           'Testimage4',
           'Testimage5')},
         'CameraAttributes::LUTControls::LUTEnable': {'value': False},
         'CameraAttributes::LUTControls::LUTIndex': {'value': 0,
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::LUTControls::LUTSelector': {'value': 'Luminance',
          'symbolics': ('Luminance',)},
         'CameraAttributes::LUTControls::LUTValue': {'value': 0,
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::RemoveParamLimits::ParameterSelector': {'value': 'Gain',
          'symbolics': ('Gain',)},
         'CameraAttributes::RemoveParamLimits::RemoveLimits': {'value': False},
         'CameraAttributes::SequenceControl::SequenceControlConfiguration::SequenceAdvanceMode': {'value': 'Auto',
          'symbolics': ('Auto', 'Controlled', 'FreeSelection')},
         'CameraAttributes::SequenceControl::SequenceEnable': {'value': False},
         'CameraAttributes::SequenceControl::SequenceSetExecutions': {'value': 1,
          'min': 1,
          'max': 256,
          'unit': ''},
         'CameraAttributes::SequenceControl::SequenceSetIndex': {'value': 0,
          'min': 0,
          'max': 1,
          'unit': ''},
         'CameraAttributes::SequenceControl::SequenceSetTotalNumber': {'value': 2,
          'min': 1,
          'max': 64,
          'unit': ''},
         'CameraAttributes::TimerControls::CounterEventSource': {'value': 'FrameTrigger',
          'symbolics': ('FrameTrigger',)},
         'CameraAttributes::TimerControls::CounterResetSource': {'value': 'Off',
          'symbolics': ('Off', 'Software', 'Line1')},
         'CameraAttributes::TimerControls::CounterSelector': {'value': 'Counter1',
          'symbolics': ('Counter1', 'Counter2')},
         'CameraAttributes::TimerControls::TimerDelayAbs': {'value': 0.0,
          'min': 0.0,
          'max': 4095.0,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDelayRaw': {'value': 0,
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDelayTimebaseAbs': {'value': 1.0,
          'min': 1.0,
          'max': 34.0,
          'unit': 'us'},
         'CameraAttributes::TimerControls::TimerDurationAbs': {'value': 4095.0,
          'min': 0.0,
          'max': 4095.0,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDurationRaw': {'value': 4095,
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDurationTimebaseAbs': {'value': 1.0,
          'min': 1.0,
          'max': 34.0,
          'unit': 'us'},
         'CameraAttributes::TimerControls::TimerSelector': {'value': 'Timer1',
          'symbolics': ('Timer1',)},
         'CameraAttributes::TimerControls::TimerTriggerActivation': {'value': 'RisingEdge',
          'symbolics': ('RisingEdge',)},
         'CameraAttributes::TimerControls::TimerTriggerSource': {'value': 'ExposureStart',
          'symbolics': ('ExposureStart',)},
         'CameraAttributes::TransportLayer::GevCurrentIPConfiguration': {'value': 5,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevHeartbeatTimeout': {'value': 3000,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevInterfaceSelector': {'value': 'NetworkInterface0',
          'symbolics': ('NetworkInterface0',)},
         'CameraAttributes::TransportLayer::GevPersistentDefaultGateway': {'value': 3232236033,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevPersistentIPAddress': {'value': 3232236132,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevPersistentSubnetMask': {'value': 4294967040,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCBWR': {'value': 10,
          'min': 0,
          'max': 74,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCBWRA': {'value': 2,
          'min': 1,
          'max': 2,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCDA': {'value': 0,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCFTD': {'value': 0,
          'min': 0,
          'max': 50000000,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPD': {'value': 0,
          'min': 0,
          'max': 38037,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPHostPort': {'value': 0,
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPInterfaceIndex': {'value': 0,
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPSBigEndian': {'value': False},
         'CameraAttributes::TransportLayer::GevSCPSDoNotFragment': {'value': True},
         'CameraAttributes::TransportLayer::GevSCPSPacketSize': {'value': 1500,
          'min': 220,
          'max': 16404,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevStreamChannelSelector': {'value': 'StreamChannel0',
          'symbolics': ('StreamChannel0',)},
         'CameraAttributes::UserDefinedValues::UserDefinedValue': {'value': 0,
          'min': -2147483648,
          'max': 2147483647,
          'unit': ''},
         'CameraAttributes::UserDefinedValues::UserDefinedValueSelector': {'value': 'Value1',
          'symbolics': ('Value1', 'Value2', 'Value3', 'Value4', 'Value5')},
         'CameraAttributes::UserSets::DefaultSetSelector': {'value': 'Standard',
          'symbolics': ('Standard', 'HighGain', 'AutoFunctions')},
         'CameraAttributes::UserSets::UserSetDefaultSelector': {'value': 'Default',
          'symbolics': ('Default', 'UserSet1', 'UserSet2', 'UserSet3')},
         'CameraAttributes::UserSets::UserSetSelector': {'value': 'Default',
          'symbolics': ('Default', 'UserSet1', 'UserSet2', 'UserSet3')}
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
        self._tlnodemap = self.pylon_camera.GetTLNodeMap()
        
        print("Connected to to camera!")
        
        # Keep an img attribute so we don't have to create it every time
        # self._img = nv.imaqCreateImage(nv.IMAQ_IMAGE_U16)

    def close(self):
        self.pylon_camera.Close()

    def _attribute_names(self, inodes, visibility_level, root=None, writeable_only=True, **kwargs):
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
            
            Names.append(self._GetFullNodeName(node, root=root))
    
        return sorted(Names)        

    def get_attribute_names(self, visibility_string, **kwargs):
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
        CameraNames = self._attribute_names(inodes, visibility_level, 
                                            root='CameraAttributes', **kwargs)
        
        inodes = self._tlnodemap.GetNodes()
        TransportNames = self._attribute_names(inodes, visibility_level, 
                                               root='AcquisitionAttributes', **kwargs)
        
    
        return sorted(CameraNames + TransportNames)
        
    def _GetFullNodeName(self, node, root=None):
            
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
        
        if root is not None:
            Names[0] = root
        
        FullName = Names.pop()
        Names.reverse()
        for Name in Names:
            FullName = Name + "::" + FullName
            
        return FullName

    def _inode_from_name(self, FullName):
        name = FullName.split("::")[-1]
        group = FullName.split("::")[0]
        if group == 'CameraAttributes':
            inode = self._nodemap.GetNode(name)  
        elif group == 'AcquisitionAttributes':
            inode = self._tlnodemap.GetNode(name)  
        else:
            raise ValueError('Invalid root path for attribute {}'.format(FullName))
        return inode

    def get_attribute(self, FullName, return_dict=False):
        """Return current value of attribute of the given name
        if return_dict, we will return a populated dictionary for the value
        {'value': value, 'min':min, ...}
        """
        inode = self._inode_from_name(FullName)
        try:                
            value = inode.GetValue()
            
            if return_dict:
                d = {}
                d['value'] = inode.GetValue()
                try:
                    d['min'] = inode.GetMin()
                    d['max'] = inode.GetMax()
                    d['unit'] = inode.GetUnit()
                except:
                    pass

                try:
                    d['symbolics'] = inode.GetSymbolics()
                except:
                    pass
                
                
                return d
            else:
                return value
        except Exception as e:
            # Add some info to the exception:
            raise Exception(f"Failed to get attribute {FullName}") from e

    def set_attribute(self, FullName, value):
        """Set the value of the attribute of the given name to the given value"""
        inode = self._inode_from_name(FullName)

        try:
            # value might be a dict with extra info, so test for this
            try:
                value = value['value']
            except:
                pass
            inode.SetValue(value)

        except Exception as e:
            # Add some info to the exception:
            msg = f"failed to set attribute {FullName} to {value}"
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
                    else:
                        print('Grab failed')
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
        attrs = cam.get_attributes('advanced', return_dict=True)
        
        image = cam.snap()
        
    fig = pyplot.figure(figsize=(6,6))
    gs = fig.add_gridspec(1, 1)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

    ax = fig.add_subplot(gs[0,0])
    ax.imshow(image)

