# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:51:34 2020

Demonstration of wavemeter

@author: rubidium
"""
import numpy as np
import time

from DMDWavemeter import WaveMeter
import os
path = os.path.realpath(__file__)
path, _ = os.path.split(path)
import matplotlib.pyplot as pyplot
pyplot.style.use(path + '/matplotlibrc')

attributes = {
    'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode': 'Unicast',
    'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMulticastAddress': '239.192.0.1',
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::MaxResendsPerPacket': 25,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::MemoryWindowSize': 1024,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::MissingPacketTimeout': 2,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::NewPacketTimeout': 100,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendBatchingPercentage': 10,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendResponseTimeout': 2,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendThresholdPercentage': 5,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendTimerResolution': 1,
    'AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendsEnabled': 1,
    'AcquisitionAttributes::AdvancedGenicam::EventsEnabled': 1,
    'AcquisitionAttributes::Bayer::Algorithm': 'Bilinear',
    'AcquisitionAttributes::Bayer::GainB': 1.0,
    'AcquisitionAttributes::Bayer::GainG': 1.0,
    'AcquisitionAttributes::Bayer::GainR': 1.0,
    'AcquisitionAttributes::Bayer::Pattern': 'Use hardware value',
    'AcquisitionAttributes::BitsPerPixel': 'Use hardware value',
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
    'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateAbs': 1.0,
    'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateEnable': 1,
    'CameraAttributes::AcquisitionTrigger::AcquisitionMode': 'Continuous',
    'CameraAttributes::AcquisitionTrigger::AcquisitionStatusSelector': 'Frame Trigger Wait',
    'CameraAttributes::AcquisitionTrigger::ExposureAuto': 'Off',
    'CameraAttributes::AcquisitionTrigger::ExposureMode': 'Timed',
    'CameraAttributes::AcquisitionTrigger::ExposureTimeAbs': 40.0,
    'CameraAttributes::AcquisitionTrigger::ExposureTimeRaw': 40,
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
    'CameraAttributes::AutoFunctions::AutoExposureTimeAbsLowerLimit': 100.0,
    'CameraAttributes::AutoFunctions::AutoExposureTimeAbsUpperLimit': 500000.0,
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIHeight': 2048,
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetX': 0,
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetY': 0,
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOISelector': 'AOI 1',
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageIntensity': 1,
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageWhiteBalance': 0,
    'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIWidth': 2048,
    'CameraAttributes::AutoFunctions::AutoFunctionProfile': 'Gain at minimum',
    'CameraAttributes::AutoFunctions::AutoGainRawLowerLimit': 36,
    'CameraAttributes::AutoFunctions::AutoGainRawUpperLimit': 512,
    'CameraAttributes::AutoFunctions::AutoTargetValue': 128,
    'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingAbs': 0.68359375,
    'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingRaw': 700,
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
    'CameraAttributes::ImageFormat::PixelFormat': 'Mono 8',
    'CameraAttributes::ImageFormat::ReverseX': 0,
    'CameraAttributes::ImageFormat::ReverseY': 0,
    'CameraAttributes::ImageFormat::TestImageSelector': 'Test Image Off',
    'CameraAttributes::LUTControls::LUTEnable': 0,
    'CameraAttributes::LUTControls::LUTIndex': 0,
    'CameraAttributes::LUTControls::LUTSelector': 'Luminance LUT',
    'CameraAttributes::LUTControls::LUTValue': 0,
    'CameraAttributes::SequenceControl::SequenceEnable': 0,
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
    'CameraAttributes::TransportLayer::GevSCBWRA': 10,
    'CameraAttributes::TransportLayer::GevSCFTD': 0,
    'CameraAttributes::UserSets::DefaultSetSelector': 'Standard',
    'CameraAttributes::UserSets::UserSetSelector': 'Default Configuration Set'
}


with WaveMeter(LightCrafterHost='192.168.1.100', IMAQdx_serial=0x30531DC20D) as Wave:
    Wave.Camera.set_attributes(attributes)
    
    coords = Wave.DMD.XY_COORDS_ROT

    pattern = (1+np.cos(np.pi*coords[0])) / 2
    pattern += (1+np.cos(np.pi*coords[1])) / 2
    pattern /=2
    Wave.DMD.program_manual(pattern)

    time.sleep(1)

    image = Wave.Camera.snap()
    attributes = Wave.Camera.get_attributes('advanced', writeable_only=True)
  

fig = pyplot.figure(figsize=(12,6))
gs = fig.add_gridspec(1, 2)
gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

ax = fig.add_subplot(gs[0,0])
ax.imshow(image)

ax = fig.add_subplot(gs[0,1])
ax.imshow(pattern)
