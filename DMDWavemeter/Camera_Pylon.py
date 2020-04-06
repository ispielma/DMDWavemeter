#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:01:11 2020

@author: ispielma
"""

import Camera_Generic
from pypylon import pylon, genicam
import numpy as np

class Camera(Camera_Generic.Camera):
    defaults = {
        'AcquisitionAttributes::CommandDuplicationEnable': {'value': False,
          'description': 'Enables sending all commands and receiving all acknowledges twice. This option should only be enabled in case of network problems.'},
         'AcquisitionAttributes::HeartbeatTimeout': {'value': 3000,
          'description': '',
          'min': 500,
          'max': 4294967295,
          'unit': ''},
         'AcquisitionAttributes::MaxRetryCountRead': {'value': 2,
          'description': '',
          'min': 0,
          'max': 20,
          'unit': ''},
         'AcquisitionAttributes::MaxRetryCountWrite': {'value': 2,
          'description': '',
          'min': 0,
          'max': 20,
          'unit': ''},
         'AcquisitionAttributes::ReadTimeout': {'value': 500,
          'description': '',
          'min': 5,
          'max': 3600000,
          'unit': ''},
         'AcquisitionAttributes::WriteTimeout': {'value': 500,
          'description': '',
          'min': 5,
          'max': 3600000,
          'unit': ''},
         'CameraAttributes::AOI::BinningHorizontal': {'value': 1,
          'description': 'Sets the number of binned adjacent horizontal pixels. Their charges will be summed and reported out of the camera as a single pixel.',
          'min': 1,
          'max': 4,
          'unit': ''},
         'CameraAttributes::AOI::BinningVertical': {'value': 1,
          'description': 'Sets the number of binned adjacent vertical pixels. Their charges will be summed and reported out of the camera as a single pixel.',
          'min': 1,
          'max': 4,
          'unit': ''},
         'CameraAttributes::AOI::CenterX': {'value': False,
          'description': 'This feature is used to center the image horizontally.'},
         'CameraAttributes::AOI::CenterY': {'value': False,
          'description': 'This feature is used to center the image vertically.'},
         'CameraAttributes::AOI::DecimationVertical': {'value': 1,
          'description': 'Vertical sub-sampling of the image. This has the net effect of reducing the vertical resolution (height) of the image by the specified vertical decimation factor. A value of 1 indicates that the camera performs no vertical decimation.',
          'min': 1,
          'max': 2047,
          'unit': ''},
         'CameraAttributes::AOI::Height': {'value': 2048,
          'description': 'This value sets the height of the area of interest in pixels.',
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AOI::OffsetX': {'value': 0,
          'description': 'This value sets the X offset (left offset) for the area of interest in pixels, i.e., the distance in pixels between the left side of the sensor and the left side of the image area.',
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AOI::OffsetY': {'value': 0,
          'description': 'This value sets the Y offset (top offset) for the area of interest, i.e., the distance in pixels between the top of the sensor and the top of the image area.',
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AOI::StackedZoneImaging::StackedZoneImagingEnable': {'value': False,
          'description': 'Enables the stacked zone imaging feature.'},
         'CameraAttributes::AOI::Width': {'value': 2048,
          'description': 'This value sets the width of the area of interest in pixels.',
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AcquisitionTrigger::AcquisitionFrameCount': {'value': 1,
          'description': 'This value sets the number of frames acquired in the multiframe acquisition mode',
          'min': 1,
          'max': 255,
          'unit': ''},
         'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateAbs': {'value': 1.0,
          'description': "Sets the 'absolute' value of the acquisition frame rate. The 'absolute' value is a float value that sets the acquisition frame rate in frames per second.",
          'min': 0.014901161415892265,
          'max': 1000000.0,
          'unit': 'Hz'},
         'CameraAttributes::AcquisitionTrigger::AcquisitionFrameRateEnable': {'value': False,
          'description': "This boolean value enables setting  the camera's acquisition frame rate to a specified value."},
         'CameraAttributes::AcquisitionTrigger::AcquisitionMode': {'value': 'Continuous',
          'description': 'This enumeration sets the image acquisition mode. ',
          'symbolics': ('SingleFrame', 'Continuous')},
         'CameraAttributes::AcquisitionTrigger::AcquisitionStatusSelector': {'value': 'FrameTriggerWait',
          'description': 'This enumeration is used to select which internal acquisition signal to read using AcquisitionStatus.',
          'symbolics': ('AcquisitionTriggerWait', 'FrameTriggerWait')},
         'CameraAttributes::AcquisitionTrigger::ExposureAuto': {'value': 'Off',
          'description': 'The exposure auto function automatically adjusts the Auto Exposure Time Abs parameter value within set limits, until a target average gray value for the pixel data of the related Auto Function AOI is reached.',
          'symbolics': ('Off', 'Once', 'Continuous')},
         'CameraAttributes::AcquisitionTrigger::ExposureMode': {'value': 'Timed',
          'description': 'This enumeration sets the exposure mode.',
          'symbolics': ('Timed', 'TriggerWidth')},
         'CameraAttributes::AcquisitionTrigger::ExposureTimeAbs': {'value': 100.0,
          'description': "This float value sets the camera's exposure time in microseconds.",
          'min': 24.0,
          'max': 10000000.0,
          'unit': 'us'},
         'CameraAttributes::AcquisitionTrigger::ExposureTimeRaw': {'value': 100,
          'description': 'This value sets an integer that will be used as a multiplier for the exposure timebase. The actual exposure time equals the current exposure time raw setting times the current exposure time base abs setting.',
          'min': 24,
          'max': 10000000,
          'unit': ''},
         'CameraAttributes::AcquisitionTrigger::TriggerActivation': {'value': 'RisingEdge',
          'description': 'This enumeration sets the signal transition needed to activate the selected trigger.',
          'symbolics': ('RisingEdge', 'FallingEdge')},
         'CameraAttributes::AcquisitionTrigger::TriggerDelayAbs': {'value': 0.0,
          'description': 'This float value sets the absolute trigger delay in microseconds to apply after the trigger reception before effectively activating it.',
          'min': 0.0,
          'max': 1000000.0,
          'unit': 'us'},
         'CameraAttributes::AcquisitionTrigger::TriggerMode': {'value': 'Off',
          'description': 'This enumeration sets the trigger mode for the selected trigger.',
          'symbolics': ('Off', 'On')},
         'CameraAttributes::AcquisitionTrigger::TriggerSelector': {'value': 'FrameStart',
          'description': 'This enumeration selects the trigger type to configure. Once a trigger type has been selected, all changes to the trigger settings will be applied to the selected trigger.',
          'symbolics': ('AcquisitionStart', 'FrameStart')},
         'CameraAttributes::AcquisitionTrigger::TriggerSource': {'value': 'Line1',
          'description': 'This enumeration sets the signal source for the selected trigger.',
          'symbolics': ('Software', 'Line1')},
         'CameraAttributes::AnalogControls::BlackLevelRaw': {'value': 0,
          'description': 'This value sets the selected black level control as an integer.',
          'min': 0,
          'max': 255,
          'unit': ''},
         'CameraAttributes::AnalogControls::BlackLevelSelector': {'value': 'All',
          'description': 'This enumeration selects the black level control to configure. Once a black level control has been selected, all changes to the black level settings will be applied to the selected control.',
          'symbolics': ('All',)},
         'CameraAttributes::AnalogControls::DigitalShift': {'value': 0,
          'description': 'This value sets the selected digital shift control',
          'min': 0,
          'max': 4,
          'unit': ''},
         'CameraAttributes::AnalogControls::GainAuto': {'value': 'Off',
          'description': 'The gain auto function automatically adjusts the Auto Gain Raw parameter value within set limits, until a target average gray value for the pixel data from Auto Function AOI1 is reached.',
          'symbolics': ('Off', 'Once', 'Continuous')},
         'CameraAttributes::AnalogControls::GainRaw': {'value': 36,
          'description': "Sets the 'raw' value of the selected gain control. The 'raw' value is an integer value that sets the selected gain control in units specific to the camera.",
          'min': 36,
          'max': 512,
          'unit': ''},
         'CameraAttributes::AnalogControls::GainSelector': {'value': 'All',
          'description': 'This enumeration selects the gain control to configure. Once a gain control has been selected, all changes to the gain settings will be applied to the selected control.',
          'symbolics': ('All',)},
         'CameraAttributes::AnalogControls::Gamma': {'value': 0.0,
          'description': 'This feature is used to perform gamma correction of pixel  intensity. This is typically used to compensate for non-linearity of the display system (such as CRT).',
          'min': 0.0,
          'max': 3.9999847412109375,
          'unit': ''},
         'CameraAttributes::AnalogControls::GammaEnable': {'value': False,
          'description': 'This boolean value enables the gamma correction.'},
         'CameraAttributes::AnalogControls::GammaSelector': {'value': 'User',
          'description': 'This enumeration selects the type of gamma to apply.',
          'symbolics': ('User', 'sRGB')},
         'CameraAttributes::AutoFunctions::AutoExposureTimeAbsLowerLimit': {'value': 100.0,
          'description': 'Lower limit of the Auto Exposure Time (Abs) parameter',
          'min': 24.0,
          'max': 500000.0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoExposureTimeAbsUpperLimit': {'value': 500000.0,
          'description': 'Upper limit of the Auto Exposure Time (Abs) parameter',
          'min': 100.0,
          'max': 10000000.0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIHeight': {'value': 2048,
          'description': 'This value sets the height of the auto function area of interest in pixels.',
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetX': {'value': 0,
          'description': 'This value sets the starting column of the auto function area of interest in pixels.',
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIOffsetY': {'value': 0,
          'description': 'This value sets the starting line of the auto function area of interest in pixels.',
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOISelector': {'value': 'AOI1',
          'description': 'Selects the Auto Function AOI.',
          'symbolics': ('AOI1', 'AOI2')},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageIntensity': {'value': True,
          'description': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIUsageWhiteBalance': {'value': False,
          'description': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionAOIs::AutoFunctionAOIWidth': {'value': 2048,
          'description': 'This value sets the width of the auto function area of interest in pixels.',
          'min': 1,
          'max': 2048,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoFunctionProfile': {'value': 'GainMinimum',
          'description': 'Selects the profile for controlling gain and shutter simultaneously.',
          'symbolics': ('GainMinimum', 'ExposureMinimum')},
         'CameraAttributes::AutoFunctions::AutoGainRawLowerLimit': {'value': 36,
          'description': 'Lower limit of the Auto Gain (Raw) parameter',
          'min': 36,
          'max': 512,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoGainRawUpperLimit': {'value': 512,
          'description': 'Upper limit of the Auto Gain (Raw) parameter',
          'min': 36,
          'max': 512,
          'unit': ''},
         'CameraAttributes::AutoFunctions::AutoTargetValue': {'value': 800,
          'description': 'The target average gray value may range from nearly black to nearly white. Note that this range of gray values applies to 8 bit and to 16 bit (12 bit effective) output modes. Accordingly, also for 16 bit output modes, black is represented by 0 and white by 255.',
          'min': 800,
          'max': 3280,
          'unit': ''},
         'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingAbs': {'value': 0.68359375,
          'description': 'The gray value adjustment damping parameter controls the rate by which pixel gray values are changed when Exposure Auto and/or Gain Auto are enabled.',
          'min': 0.0,
          'max': 0.78125,
          'unit': ''},
         'CameraAttributes::AutoFunctions::GrayValueAdjustmentDampingRaw': {'value': 700,
          'description': 'The gray value adjustment damping parameter controls the rate by which pixel gray values are changed when Exposure Auto and/or Gain Auto are enabled.',
          'min': 0,
          'max': 800,
          'unit': ''},
         'CameraAttributes::ChunkDataStreams::ChunkModeActive': {'value': False,
          'description': "This boolean value enables the camera's chunk mode."},
         'CameraAttributes::DeviceInformation::DeviceUserID': {'value': 'big_boy',
          'description': 'This is a read/write element. It is a user programmable string.'},
         'CameraAttributes::DigitalIO::LineDebouncerTimeAbs': {'value': 0.0,
          'description': 'Sets the absolute value of the selected line debouncer time in microseconds',
          'min': 0.0,
          'max': 20000.0,
          'unit': 'us'},
         'CameraAttributes::DigitalIO::LineFormat': {'value': 'OptoCoupled',
          'description': 'This feature controls the current electrical format of the selected physical input or output Line. Line Format can take any of the following values: No Connect: The Line is not connected. Tri-state: The Line is currently in Tri-state mode (Not driven). TTL: The Line is currently accepting or sending TTL level signals. LVDS: The Line is currently accepting or sending LVDS level signals. RS-422: The Line is currently accepting or sending RS-422 level signals. Opto-coupled: The Line is Opto-coupled. ',
          'symbolics': ('OptoCoupled',)},
         'CameraAttributes::DigitalIO::LineInverter': {'value': False,
          'description': 'This boolean value enables the signal inverter function for the selected input or output line.'},
         'CameraAttributes::DigitalIO::LineMode': {'value': 'Input',
          'description': 'This feature controls whether the physical Line is used to Input or Output a signal. When a Line supports input and output mode, the default state is Input to avoid possible electrical contention. Line Mode can take any of the following values: Input: The selected physical line is used to input an electrical signal. Output: The selected physical line is used to output an electrical signal.',
          'symbolics': ('Input',)},
         'CameraAttributes::DigitalIO::LineSelector': {'value': 'Line1',
          'description': 'This enumeration selects the I/O line to configure. Once a line has been selected, all changes to the line settings will be applied to the selected line.',
          'symbolics': ('Line1', 'Out1')},
         'CameraAttributes::DigitalIO::SyncUserOutputSelector': {'value': 'SyncUserOutput1',
          'description': '',
          'symbolics': ('SyncUserOutput1',)},
         'CameraAttributes::DigitalIO::SyncUserOutputValue': {'value': False,
          'description': 'This boolean value sets the state of the selected user settable synchronous output signal.'},
         'CameraAttributes::DigitalIO::SyncUserOutputValueAll': {'value': 0,
          'description': 'This integer value is a single bitfield that sets the state of all user settable synchronous output signals in one access.',
          'min': 0,
          'max': 268435455,
          'unit': ''},
         'CameraAttributes::DigitalIO::UserOutputSelector': {'value': 'UserOutput1',
          'description': 'This enumeration selects the user settable output signal to configure. Once a user settable output signal has been selected, all changes to the user settable output signal settings will be applied to the selected user settable output signal.',
          'symbolics': ('UserOutput1',)},
         'CameraAttributes::DigitalIO::UserOutputValue': {'value': False,
          'description': 'This boolean value sets the state of the selected user settable output signal.'},
         'CameraAttributes::DigitalIO::UserOutputValueAll': {'value': 0,
          'description': 'This integer value is a single bitfield that sets the state of all user settable output signals in one access.',
          'min': 0,
          'max': 268435455,
          'unit': ''},
         'CameraAttributes::EventsGeneration::EventNotification': {'value': 'Off',
          'description': 'This enumeration sets the notification type that will be sent to the host application for the selected event.',
          'symbolics': ('Off', 'GenICamEvent', 'On')},
         'CameraAttributes::EventsGeneration::EventSelector': {'value': 'ExposureEnd',
          'description': 'This enumeration selects the type of event for enabling.',
          'symbolics': ('ExposureEnd',
           'FrameStartOvertrigger',
           'AcquisitionStartOvertrigger',
           'FrameStart',
           'AcquisitionStart',
           'EventOverrun')},
         'CameraAttributes::ExpertFeatureAccess::ExpertFeatureAccessKey': {'value': 0,
          'description': 'Sets the key to access the selected feature',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::ExpertFeatureAccess::ExpertFeatureAccessSelector': {'value': 'ExpertFeature1',
          'description': 'Selects the feature to configure. Once a feature has been selected, all changes made using the feature enable feature will be applied to the selected feature',
          'symbolics': ('ExpertFeature1_Legacy',
           'ExpertFeature1',
           'ExpertFeature2',
           'ExpertFeature3',
           'ExpertFeature4',
           'ExpertFeature5')},
         'CameraAttributes::FileAccessControl::FileAccessLength': {'value': 0,
          'description': 'This feature controls the mapping between the device file storage and the FileAccessBuffer.',
          'min': 0,
          'max': 1056,
          'unit': ''},
         'CameraAttributes::FileAccessControl::FileAccessOffset': {'value': 0,
          'description': 'This feature controls the mapping between the device file storage and the FileAccessBuffer.',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::FileAccessControl::FileOpenMode': {'value': 'Read',
          'description': 'The File Open Mode feature selects the access mode in which a file is opened in the device.',
          'symbolics': ('Read', 'Write')},
         'CameraAttributes::FileAccessControl::FileOperationSelector': {'value': 'Open',
          'description': 'The File Operation Selector feature selects the target operation for the selected file in the device. This Operation is executed when the FileOperationExecute feature is called.',
          'symbolics': ('Open',)},
         'CameraAttributes::FileAccessControl::FileSelector': {'value': 'UserSet1',
          'description': 'The File Selector feature selects the target file in the device.',
          'symbolics': ('UserSet1', 'UserSet2', 'UserSet3')},
         'CameraAttributes::ImageFormat::PixelFormat': {'value': 'Mono12',
          'description': 'This enumeration sets the format of the pixel data transmitted for acquired images. ',
          'symbolics': ('Mono8',
           'Mono12',
           'Mono12Packed',
           'YUV422Packed',
           'YUV422_YUYV_Packed')},
         'CameraAttributes::ImageFormat::ReverseX': {'value': False,
          'description': 'This feature is used to flip horizontally the image sent by the device. The AOI is applied after the flipping.'},
         'CameraAttributes::ImageFormat::ReverseY': {'value': False,
          'description': 'This feature is used to flip vertically the image sent by the device. The AOI is applied after the flipping.'},
         'CameraAttributes::ImageFormat::TestImageSelector': {'value': 'Off',
          'description': 'This enumeration provides a list of the available test images. Selecting a test image from the list will enable the test image.',
          'symbolics': ('Off',
           'Testimage1',
           'Testimage2',
           'Testimage3',
           'Testimage4',
           'Testimage5')},
         'CameraAttributes::LUTControls::LUTEnable': {'value': False,
          'description': 'This boolean value enables the selected LUT.'},
         'CameraAttributes::LUTControls::LUTIndex': {'value': 0,
          'description': 'This value sets the LUT element to access. This value is used to index into a LUT array.',
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::LUTControls::LUTSelector': {'value': 'Luminance',
          'description': 'This enumeration the lookup table (LUT) to configure. Once a LUT has been selected, all changes to the LUT settings will be applied to the selected LUT.',
          'symbolics': ('Luminance',)},
         'CameraAttributes::LUTControls::LUTValue': {'value': 0,
          'description': 'This value sets the value of the LUT element at the LUT index.',
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::RemoveParamLimits::ParameterSelector': {'value': 'Gain',
          'description': 'This enumeration selects the parameter to configure. Selects the parameter to configure. Once a parameter has been selected, all changes made using the Remove Limits feature will be applied to the selected parameter',
          'symbolics': ('Gain',)},
         'CameraAttributes::RemoveParamLimits::RemoveLimits': {'value': False,
          'description': 'Removes the factory-set limits of the selected parameter. Having removed the factory-set limits you may set the parameter within extended limits. These are only defined by technical restrictions. Note:  Inferior image quality may result.'},
         'CameraAttributes::SequenceControl::SequenceControlConfiguration::SequenceAdvanceMode': {'value': 'Auto',
          'description': 'Selects the sequence set advance mode. Possible values: Auto - automatic sequence set advance as images are acquired. Controlled - sequence set advance controlled by settable source. Free selection - the sequence sets are selected according to the states of the input lines.',
          'symbolics': ('Auto', 'Controlled', 'FreeSelection')},
         'CameraAttributes::SequenceControl::SequenceEnable': {'value': False,
          'description': 'Enables the existing sequence sets for image acquisition.'},
         'CameraAttributes::SequenceControl::SequenceSetExecutions': {'value': 1,
          'description': 'Sets the number of consecutive executions per sequence cycle for the selected sequence set. Only available in Auto sequence advance mode.',
          'min': 1,
          'max': 256,
          'unit': ''},
         'CameraAttributes::SequenceControl::SequenceSetIndex': {'value': 0,
          'description': 'Selects the index number of a sequence set.',
          'min': 0,
          'max': 1,
          'unit': ''},
         'CameraAttributes::SequenceControl::SequenceSetTotalNumber': {'value': 2,
          'description': 'Sets the total number of sequence sets in the sequence.',
          'min': 1,
          'max': 64,
          'unit': ''},
         'CameraAttributes::TimerControls::CounterEventSource': {'value': 'FrameTrigger',
          'description': 'This enumeration selects the event that will be the source to increment the counter.',
          'symbolics': ('FrameTrigger',)},
         'CameraAttributes::TimerControls::CounterResetSource': {'value': 'Off',
          'description': 'This enumeration selects the source of the reset for the selected counter.',
          'symbolics': ('Off', 'Software', 'Line1')},
         'CameraAttributes::TimerControls::CounterSelector': {'value': 'Counter1',
          'description': 'This enumeration selects the counter to configure. Once a counter has been selected, all changes to the counter settings will be applied to the selected counter.',
          'symbolics': ('Counter1', 'Counter2')},
         'CameraAttributes::TimerControls::TimerDelayAbs': {'value': 0.0,
          'description': 'This float value sets the delay for the selected timer in microseconds.',
          'min': 0.0,
          'max': 4095.0,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDelayRaw': {'value': 0,
          'description': 'This value sets an integer that will be used as a multiplier for the timer delay timebase. The actual delay time equals the current timer delay raw setting times the current timer delay time base abs setting.',
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDelayTimebaseAbs': {'value': 1.0,
          'description': "This float value sets the time base (in microseconds) that is used when a timer delay is set with the 'raw' setting.",
          'min': 1.0,
          'max': 34.0,
          'unit': 'us'},
         'CameraAttributes::TimerControls::TimerDurationAbs': {'value': 4095.0,
          'description': 'This float value sets the duration for the selected timer in microseconds.',
          'min': 0.0,
          'max': 4095.0,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDurationRaw': {'value': 4095,
          'description': 'This value sets an integer that will be used as a multiplier for the timer duration timebase. The actual duration time equals the current timer duration raw setting times the current timer duration time base abs setting.',
          'min': 0,
          'max': 4095,
          'unit': ''},
         'CameraAttributes::TimerControls::TimerDurationTimebaseAbs': {'value': 1.0,
          'description': "This float value sets the time base (in microseconds) that is used when a timer duration is set with the 'raw' setting.",
          'min': 1.0,
          'max': 34.0,
          'unit': 'us'},
         'CameraAttributes::TimerControls::TimerSelector': {'value': 'Timer1',
          'description': 'This enumeration selects the timer to configure. . Once a timer has been selected, all changes to the timer settings will be applied to the selected timer.',
          'symbolics': ('Timer1',)},
         'CameraAttributes::TimerControls::TimerTriggerActivation': {'value': 'RisingEdge',
          'description': 'This enumeration sets the type of signal transistion that will start the timer.',
          'symbolics': ('RisingEdge',)},
         'CameraAttributes::TimerControls::TimerTriggerSource': {'value': 'ExposureStart',
          'description': 'This enumeration sets the internal camera signal used to trigger the selected timer.',
          'symbolics': ('ExposureStart',)},
         'CameraAttributes::TransportLayer::GevCurrentIPConfiguration': {'value': 5,
          'description': 'This value sets the IP configuration of the selected network interface, i.e., fixed IP, DHCP, auto IP. ',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevHeartbeatTimeout': {'value': 3000,
          'description': 'This value sets the heartbeat timeout in milliseconds.',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevInterfaceSelector': {'value': 'NetworkInterface0',
          'description': 'This selects the physical network interface to configure. Once a network interface has been selected, all changes to the network interface settings will be applied to the selected interface.',
          'symbolics': ('NetworkInterface0',)},
         'CameraAttributes::TransportLayer::GevPersistentDefaultGateway': {'value': 3232236033,
          'description': 'This value sets the fixed default gateway for the selected network interface (if fixed IP addressing is supported by the device and enabled).',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevPersistentIPAddress': {'value': 3232236132,
          'description': 'This value sets the fixed IP address for the selected network interface (if fixed IP addressing is supported by the device and enabled).',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevPersistentSubnetMask': {'value': 4294967040,
          'description': 'This value sets the fixed subnet mask for the selected network interface (if fixed IP addressing is supported by the device and enabled).',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCBWR': {'value': 20,
          'description': 'This value reserves a portion of Ethernet bandwidth assigned to the camera for packet resends and for the transmission of control data between the camera and the host PC. The setting is expressed as a percentage of the bandwidth assigned parameter. For example, if the Bandwidth Assigned parameter indicates that 30 MBytes/s have been assigned to the camera and the Bandwidth Reserve parameter is set to 5%, then the bandwidth reserve will be 1.5 MBytes/s.',
          'min': 0,
          'max': 71,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCBWRA': {'value': 1,
          'description': 'This value sets a multiplier for the Bandwidth Reserve parameter. The multiplier is used to establish an extra pool of reserved bandwidth that can be used if an unusually large burst of packet resends is needed.',
          'min': 1,
          'max': 1,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCDA': {'value': 0,
          'description': 'This value sets the stream channel destination IPv4 address for the selected stream channel. The destination can be a unicast or a multicast.',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCFTD': {'value': 0,
          'description': 'This value sets the frame transfer delay for the selected stream channel. This value sets a delay betweem when the camera would normally begin transmitted an acquired image (frame) and when it actually begins transmitting the acquired image.',
          'min': 0,
          'max': 50000000,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPD': {'value': 2000,
          'description': 'This value sets a delay between the transmission of each packet for the selected stream channel. The delay is measured in ticks.',
          'min': 0,
          'max': 42362,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPHostPort': {'value': 0,
          'description': 'This value sets the port to which the device must send data streams.',
          'min': 0,
          'max': 4294967295,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPInterfaceIndex': {'value': 0,
          'description': 'This value sets the index of the network interface to use.',
          'min': 0,
          'max': 0,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevSCPSBigEndian': {'value': False,
          'description': ''},
         'CameraAttributes::TransportLayer::GevSCPSDoNotFragment': {'value': True,
          'description': ''},
         'CameraAttributes::TransportLayer::GevSCPSPacketSize': {'value': 1500,
          'description': 'This value sets the packet size in bytes for the selected stream channel. Excludes data leader and data trailer. (The last packet may be smaller because the packet size is not necessarily a multiple of the block size for the stream channel.)',
          'min': 220,
          'max': 16404,
          'unit': ''},
         'CameraAttributes::TransportLayer::GevStreamChannelSelector': {'value': 'StreamChannel0',
          'description': 'This enumeration selects the stream channels to configure. Once a stream channel has been selected, all changes to the stream channel settings will be applied to the selected stream channel.',
          'symbolics': ('StreamChannel0',)},
         'CameraAttributes::UserDefinedValues::UserDefinedValue': {'value': 0,
          'description': '',
          'min': -2147483648,
          'max': 2147483647,
          'unit': ''},
         'CameraAttributes::UserDefinedValues::UserDefinedValueSelector': {'value': 'Value1',
          'description': '',
          'symbolics': ('Value1', 'Value2', 'Value3', 'Value4', 'Value5')},
         'CameraAttributes::UserSets::DefaultSetSelector': {'value': 'Standard',
          'description': 'Selects the which factory setting will be used as default set.',
          'symbolics': ('Standard', 'HighGain', 'AutoFunctions')},
         'CameraAttributes::UserSets::UserSetDefaultSelector': {'value': 'Default',
          'description': 'This enumeration sets the configuration set to be used as the default startup set. The configuration set that has been selected as the default startup set will be loaded as the active set whenever the camera is powered on or reset.',
          'symbolics': ('Default', 'UserSet1', 'UserSet2', 'UserSet3')},
         'CameraAttributes::UserSets::UserSetSelector': {'value': 'Default',
          'description': 'This enumeration selects the configuration set to load, save or configure. Possible values for the User Set Selector are: Default: Selects a configuration set that contains factory settings. User Set 1: Selects the first user set. When the Default configuration set is selected and loaded using User Set Load, the device must be in default factory settings state and must make sure the mandatory continuous acquisition use case works directly. Default User Set is read-only and cannot be modified.',
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
                d['description'] = inode.GetNode().GetDescription()
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
        
        data = np.array([])
        for attempt in range(attempts):
            try:
                with self.pylon_camera.RetrieveResult(5000) as result:
                    if result.GrabSucceeded():
                        # Access the image data.
        
                        data = result.Array
                    else:
                        print('Grab failed {}: {}'.format(result.GetErrorCode() , result.GetErrorDescription() ) )
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

