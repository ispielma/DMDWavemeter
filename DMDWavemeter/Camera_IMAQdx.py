#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:01:11 2020

@author: ispielma
"""

import numpy as np
import Camera_Generic

def _monkeypatch_imaqdispose():
    """Monkeypatch a fix to a memory leak bug in pynivision. The pynivision project is
    no longer active, so we can't contribute this fix upstream. In the long run,
    hopefully someone (perhaps us) forks it so that bugs can be addressed in the
    normal way"""

    import nivision.core
    import ctypes

    _imaqDispose = nivision.core._imaqDispose

    def imaqDispose(obj):
        if getattr(obj, "_contents", None) is not None:
            _imaqDispose(ctypes.byref(obj._contents))
            obj._contents = None
        if getattr(obj, "value", None) is not None:
            _imaqDispose(obj)
            obj.value = None
        # This is the bugfix: pointers as raw ints were not being disposed:
        if isinstance(obj, int):
            _imaqDispose(obj)

    nivision.core.imaqDispose = nv.imaqDispose = imaqDispose

import nivision as nv
_monkeypatch_imaqdispose()

class Camera(Camera_Generic.Camera):
    defaults = {
        'AcquisitionAttributes::AdvancedEthernet::BandwidthControl::DesiredPeakBandwidth': 1000.0,
        'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode': 'Unicast',
        'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMulticastAddress': '239.192.0.1',
        'AcquisitionAttributes::AdvancedEthernet::EventParameters::MaxOutstandingEvents': 50,
        'AcquisitionAttributes::AdvancedEthernet::FirewallTraversal::Enabled': 1,
        'AcquisitionAttributes::AdvancedEthernet::FirewallTraversal::KeepAliveTime': 30,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::MaxResendsPerPacket': 25,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::MemoryWindowSize': 1024,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::MissingPacketTimeout': 2,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::NewPacketTimeout': 100,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendBatchingPercentage': 10,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendResponseTimeout': 2,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendThresholdPercentage': 5,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendTimerResolution': 1,
        'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendsEnabled': 1,
        'AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::MaxTestPacketRetries': 1,
        'AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::TestPacketEnabled': 1,
        'AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::TestPacketTimeout': 250,
        'AcquisitionAttributes::AdvancedGenicam::CommandTimeout': 100,
        'AcquisitionAttributes::AdvancedGenicam::EventsEnabled': 1,
        'AcquisitionAttributes::AdvancedGenicam::IgnoreCameraValidationErrors': 0,
        'AcquisitionAttributes::AdvancedGenicam::PersistenceAlgorithm': 'Auto',
        'AcquisitionAttributes::Bayer::Algorithm': 'Bilinear',
        'AcquisitionAttributes::Bayer::GainB': 1.0,
        'AcquisitionAttributes::Bayer::GainG': 1.0,
        'AcquisitionAttributes::Bayer::GainR': 1.0,
        'AcquisitionAttributes::Bayer::Pattern': 'Use hardware value',
        'AcquisitionAttributes::BitsPerPixel': 'Use hardware value',
        'AcquisitionAttributes::ChunkDataDecoding::ChunkDataDecodingEnabled': 0,
        'AcquisitionAttributes::ChunkDataDecoding::MaximumChunkCopySize': 64,
        'AcquisitionAttributes::HardwareMaximumQueuedBufferCount': 1000,
        'AcquisitionAttributes::HardwareRequeueBufferListThreshold': 50.0,
        'AcquisitionAttributes::ImageDecoderCopyMode': 'Auto',
        'AcquisitionAttributes::IncompleteBufferMode': 'Ignore',
        'AcquisitionAttributes::OutputImageType': 'Auto',
        'AcquisitionAttributes::OverwriteMode': 'Get Newest',
        'AcquisitionAttributes::PacketSize': 1500,
        'AcquisitionAttributes::ReceiveTimestampMode': 'None',
        'AcquisitionAttributes::ShiftPixelBits': 0,
        'AcquisitionAttributes::SwapPixelBytes': 0,
        'AcquisitionAttributes::Timeout': 5000,
        'CameraAttributes::AOI::BinningHorizontal': 1,
        'CameraAttributes::AOI::BinningVertical': 1,
        'CameraAttributes::AOI::CenterX': 0,
        'CameraAttributes::AOI::CenterY': 0,
        'CameraAttributes::AOI::DecimationVertical': 1,
        'CameraAttributes::AOI::Height': 2048,
        'CameraAttributes::AOI::OffsetX': 0,
        'CameraAttributes::AOI::OffsetY': 0,
        'CameraAttributes::AOI::StackedZoneImaging::StackedZoneImagingEnable': 0,
        'CameraAttributes::AOI::Width': 2048,
        'CameraAttributes::AcquisitionTrigger::AcquisitionFrameCount': 1,
        'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateAbs': 409.5004095004095,
        'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateEnable': 0,
        'CameraAttributes::AcquisitionTrigger::AcquisitionMode': 'Continuous',
        'CameraAttributes::AcquisitionTrigger::AcquisitionStatusSelector': 'Frame Trigger Wait',
        'CameraAttributes::AcquisitionTrigger::ExposureAuto': 'Off',
        'CameraAttributes::AcquisitionTrigger::ExposureMode': 'Timed',
        'CameraAttributes::AcquisitionTrigger::ExposureTimeAbs': 10000.0,
        'CameraAttributes::AcquisitionTrigger::ExposureTimeRaw': 10000,
        'CameraAttributes::AcquisitionTrigger::TriggerActivation': 'Rising Edge',
        'CameraAttributes::AcquisitionTrigger::TriggerDelayAbs': 0.0,
        'CameraAttributes::AcquisitionTrigger::TriggerMode': 'Off',
        'CameraAttributes::AcquisitionTrigger::TriggerSelector': 'Frame Start',
        'CameraAttributes::AcquisitionTrigger::TriggerSource': 'Line 1',
        'CameraAttributes::AnalogControls::BlackLevelRaw': 0,
        'CameraAttributes::AnalogControls::BlackLevelSelector': 'All',
        'CameraAttributes::AnalogControls::DigitalShift': 0,
        'CameraAttributes::AnalogControls::GainAuto': 'Off',
        'CameraAttributes::AnalogControls::GainRaw': 36,
        'CameraAttributes::AnalogControls::GainSelector': 'All',
        'CameraAttributes::AnalogControls::Gamma': 1.0,
        'CameraAttributes::AnalogControls::GammaEnable': 0,
        'CameraAttributes::AnalogControls::GammaSelector': 'User',
        # 'CameraAttributes::AutoFunctions::AutoExposureTimeAbsLowerLimit': 100.0,
        # 'CameraAttributes::AutoFunctions::AutoExposureTimeAbsUpperLimit': 500000.0,
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIHeight': 2048,
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetX': 0,
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetY': 0,
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOISelector': 'AOI 1',
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageIntensity': 1,
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageWhiteBalance': 0,
        # 'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIWidth': 2048,
        # 'CameraAttributes::AutoFunctions::AutoFunctionProfile': 'Gain at minimum',
        # 'CameraAttributes::AutoFunctions::AutoGainRawLowerLimit': 36,
        # 'CameraAttributes::AutoFunctions::AutoGainRawUpperLimit': 512,
        # 'CameraAttributes::AutoFunctions::AutoTargetValue': 128,
        # 'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingAbs': 0.68359375,
        # 'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingRaw': 700,
        'CameraAttributes::ChunkDataStreams::ChunkModeActive': 0,
        'CameraAttributes::DeviceInformation::DeviceUserID': 'big_boy',
        'CameraAttributes::DigitalIO::LineDebouncerTimeAbs': 0.0,
        'CameraAttributes::DigitalIO::LineFormat': 'Opto-coupled',
        'CameraAttributes::DigitalIO::LineInverter': 0,
        'CameraAttributes::DigitalIO::LineMode': 'Input',
        'CameraAttributes::DigitalIO::LineSelector': 'Line 1',
        'CameraAttributes::DigitalIO::SyncUserOutputSelector': 'Sync User Settable Output 1',
        'CameraAttributes::DigitalIO::SyncUserOutputValue': 0,
        'CameraAttributes::DigitalIO::SyncUserOutputValueAll': 0,
        'CameraAttributes::DigitalIO::UserOutputSelector': 'User Settable Output 1',
        'CameraAttributes::DigitalIO::UserOutputValue': 0,
        'CameraAttributes::DigitalIO::UserOutputValueAll': 0,
        'CameraAttributes::EventsGeneration::EventNotification': 'Notification Off',
        'CameraAttributes::EventsGeneration::EventSelector': 'Exposure End',
        'CameraAttributes::ExpertFeatureAccess::ExpertFeatureAccessKey': 0,
        'CameraAttributes::ExpertFeatureAccess::ExpertFeatureAccessSelector': 'Expert Feature 1',
        'CameraAttributes::FileAccessControl::FileAccessLength': 0,
        'CameraAttributes::FileAccessControl::FileAccessOffset': 0,
        'CameraAttributes::FileAccessControl::FileOpenMode': 'Read',
        'CameraAttributes::FileAccessControl::FileOperationSelector': 'Open',
        'CameraAttributes::FileAccessControl::FileSelector': 'User Set 1',
        'CameraAttributes::ImageFormat::PixelFormat': 'Mono 12 Packed',
        'CameraAttributes::ImageFormat::ReverseX': 0,
        'CameraAttributes::ImageFormat::ReverseY': 0,
        'CameraAttributes::ImageFormat::TestImageSelector': 'Test Image Off',
        'CameraAttributes::LUTControls::LUTEnable': 0,
        'CameraAttributes::LUTControls::LUTIndex': 0,
        'CameraAttributes::LUTControls::LUTSelector': 'Luminance LUT',
        'CameraAttributes::LUTControls::LUTValue': 0,
        'CameraAttributes::RemoveParamLimits::ParameterSelector': 'Gain',
        'CameraAttributes::RemoveParamLimits::RemoveLimits': 0,
        'CameraAttributes::SequenceControl::SequenceControlConfiguration::SequenceAdvanceMode': 'Auto',
        'CameraAttributes::SequenceControl::SequenceEnable': 0,
        'CameraAttributes::SequenceControl::SequenceSetExecutions': 1,
        'CameraAttributes::SequenceControl::SequenceSetIndex': 0,
        'CameraAttributes::SequenceControl::SequenceSetTotalNumber': 2,
        'CameraAttributes::TimerControls::CounterEventSource': 'Frame Trigger',
        'CameraAttributes::TimerControls::CounterResetSource': 'Off',
        'CameraAttributes::TimerControls::CounterSelector': 'Counter 1',
        'CameraAttributes::TimerControls::TimerDelayAbs': 0.0,
        'CameraAttributes::TimerControls::TimerDelayRaw': 0,
        'CameraAttributes::TimerControls::TimerDelayTimebaseAbs': 1.0,
        'CameraAttributes::TimerControls::TimerDurationAbs': 4095.0,
        'CameraAttributes::TimerControls::TimerDurationRaw': 4095,
        'CameraAttributes::TimerControls::TimerDurationTimebaseAbs': 1.0,
        'CameraAttributes::TimerControls::TimerSelector': 'Timer 1',
        'CameraAttributes::TimerControls::TimerTriggerActivation': 'Rising Edge',
        'CameraAttributes::TimerControls::TimerTriggerSource': 'Exposure Active',
        'CameraAttributes::TransportLayer::GevSCBWR': 10,
        'CameraAttributes::TransportLayer::GevSCBWRA': 6,
        'CameraAttributes::TransportLayer::GevSCFTD': 0,
        'CameraAttributes::UserDefinedValues::UserDefinedValue': 0,
        'CameraAttributes::UserDefinedValues::UserDefinedValueSelector': 'Value 1',
        'CameraAttributes::UserSets::DefaultSetSelector': 'Standard',
        'CameraAttributes::UserSets::UserSetDefaultSelector': 'Default User Set',
        'CameraAttributes::UserSets::UserSetSelector': 'Default Configuration Set'
        }
        
    def __init__(self, serial_number, **kwargs):
        super().__init__(**kwargs)
        
        # Find the camera:
        print("Finding camera...")
        for cam in nv.IMAQdxEnumerateCameras(True):
            if serial_number == (cam.SerialNumberHi << 32) + cam.SerialNumberLo:
                self.camera = cam
                break
        else:
            msg = f"No connected camera with serial number {serial_number:X} found"
            raise Exception(msg)
        # Connect to the camera:
        print("Connecting to camera...")
        self.imaqdx = nv.IMAQdxOpenCamera(
            self.camera.InterfaceName, nv.IMAQdxCameraControlModeController
        )
        
        # Keep an img attribute so we don't have to create it every time
        self._img = nv.imaqCreateImage(nv.IMAQ_IMAGE_U16)

    def set_attribute(self, name, value):
        """Set the value of the attribute of the given name to the given value"""
        _value = value  # Keep the original for the sake of the error message
        if isinstance(_value, str):
            _value = _value.encode('utf8')
        try:
            nv.IMAQdxSetAttribute(self.imaqdx, name.encode('utf8'), _value)
        except Exception as e:
            # Add some info to the exception:
            msg = f"failed to set attribute {name} to {value}"
            raise Exception(msg) from e

    def get_attribute_names(self, visibility_level, writeable_only=True):
        """Return a list of all attribute names of readable attributes, for the given
        visibility level. Optionally return only writeable attributes"""
        visibilities = {
            'simple': nv.IMAQdxAttributeVisibilitySimple,
            'intermediate': nv.IMAQdxAttributeVisibilityIntermediate,
            'advanced': nv.IMAQdxAttributeVisibilityAdvanced,
        }
        visibility_level = visibilities[visibility_level.lower()]
        attributes = []
        for a in nv.IMAQdxEnumerateAttributes2(self.imaqdx, b'', visibility_level):
            if writeable_only and not a.Writable:
                continue
            if not a.Readable:
                continue
            attributes.append(a.Name.decode('utf8'))
        return sorted(attributes)
        
    def get_attribute(self, name):
        """Return current value of attribute of the given name"""
        try:
            value = nv.IMAQdxGetAttribute(self.imaqdx, name.encode('utf8'))
            if isinstance(value, nv.core.IMAQdxEnumItem):
                value = value.Name
            if isinstance(value, bytes):
                value = value.decode('utf8')
            return value
        except Exception as e:
            # Add some info to the exception:
            raise Exception(f"Failed to get attribute {name}") from e

    def snap(self):
        """Acquire a single image and return it"""
        nv.IMAQdxSnap(self.imaqdx, self._img)
        return self._decode_image_data(self._img)

    def configure_acquisition(self, continuous=True, bufferCount=5):
        nv.IMAQdxConfigureAcquisition(
            self.imaqdx, continuous=continuous, bufferCount=bufferCount
        )
        nv.IMAQdxStartAcquisition(self.imaqdx)

    def grab(self, waitForNextBuffer=True):
        nv.IMAQdxGrab(self.imaqdx, self._img, waitForNextBuffer=waitForNextBuffer)
        return self._decode_image_data(self._img)

    def grab_multiple(self, n_images, images, waitForNextBuffer=True):
        print(f"Attempting to grab {n_images} images.")
        for i in range(n_images):
            while True:
                if self._abort_acquisition:
                    print("Abort during acquisition.")
                    self._abort_acquisition = False
                    return
                try:
                    images.append(self.grab(waitForNextBuffer))
                    print(f"Got image {i+1} of {n_images}.")
                    break
                except nv.ImaqDxError as e:
                    if e.code == nv.IMAQdxErrorTimeout.value:
                        print('.', end='')
                        continue
                    raise
        print(f"Got {len(images)} of {n_images} images.")

    def stop_acquisition(self):
        nv.IMAQdxStopAcquisition(self.imaqdx)
        nv.IMAQdxUnconfigureAcquisition(self.imaqdx)


    def _decode_image_data(self, img):
        img_array = nv.imaqImageToArray(img)
        img_array_shape = (img_array[2], img_array[1])
        # bitdepth in bytes
        bitdepth = len(img_array[0]) // (img_array[1] * img_array[2])
        dtype = {1: np.uint8, 2: np.uint16, 4: np.uint32}[bitdepth]
        data = np.frombuffer(img_array[0], dtype=dtype).reshape(img_array_shape)
        return data.copy()

    def close(self):
        nv.IMAQdxCloseCamera(self.imaqdx)

# Demonstrate
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')

    with Camera(0x30531DC20D) as cam:
        
        cam.set_attributes(cam.defaults)
        attrs = cam.get_attributes('advanced')
        
        image = cam.snap()
        
    fig = pyplot.figure(figsize=(6,6))
    gs = fig.add_gridspec(1, 1)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

    ax = fig.add_subplot(gs[0,0])
    ax.imshow(image)
