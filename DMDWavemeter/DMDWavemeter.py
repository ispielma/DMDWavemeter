# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:04:11 2020

Main code to write patterns to the DMD and to read back the Fourier space
results containing information about the optical wavelength.

@author: ispielma
"""

# COMMON IMPORTS
import time
import struct
import PIL.Image
import numpy as np
import io

import socket    
        
class LightCrafterWorker():

    #
    # Physical properties
    #

    
    WIDTH = 608
    HEIGHT = 684
    
    BLANK = np.zeros((HEIGHT, WIDTH))
    INDICES = np.meshgrid(np.arange(HEIGHT), np.arange(WIDTH), indexing='ij')
    XY_COORDS_ROT = (( 2*INDICES[1]+INDICES[0] + INDICES[0]%2)/2, 
                     (-2*INDICES[1]+INDICES[0] - INDICES[0]%2)/2 )
    XY_COORDS = ((XY_COORDS_ROT[0]+XY_COORDS_ROT[1])/np.sqrt(2), (XY_COORDS_ROT[1]-XY_COORDS_ROT[0])/np.sqrt(2))
    
    #
    # Command language
    #
    
    command = {'version' :             b'\x01\x00',
                'display_mode':         b'\x01\x01',
                'static_image':         b'\x01\x05',
                'sequence_setting':     b'\x04\x00',
                'pattern_definition':   b'\x04\x01',
                'start_pattern_sequence': b'\x04\x02',
                'display_pattern' :     b'\x04\x05',
                'advance_pattern_sequence' : b'\x04\x03',
                }
    send_packet_type = {   'read': b'\x04',
                            'write': b'\x02',
                }
    receive_packet_type = {    b'\x00' : 'System Busy',
                                b'\x01' : 'Error',
                                b'\x03' : 'Write response',
                                b'\x05' : 'Read response',
                            }
    flag = {'complete' : b'\x00',
            'beginning' : b'\x01',
            'intermediate' : b'\x02',
            'end': b'\x03'}
            
    error_messages = {  b'\x01' : "Command execution failed with unknown error",
                        b'\x02' : "Invalid command",
                        b'\x03' : "Invalid parameter",
                        b'\x04' : "Out of memory resource",
                        b'\x05' : "Hardware device failure",
                        b'\x06' : "Hardware busy",
                        b'\x07' : "Not Initialized (any of the preconditions for the command is not met",
                        b'\x08' : "Some object referred by the command is not found. For example, a solution name was not found",
                        b'\x09' : "Checksum error",
                        b'\x0A' : "Packet format error due to insufficient or larger than expected payload size",
                        b'\x0B' : "Command continuation error due to incorrect continuation flag"
                        }
    display_mode = {'static' : b'\x00',
                    'pattern': b'\x04',
                    }
    # Packets must be in the form [packet type (1 bit), command (2), flags (1), payload length (2), data (N), checksum (1)]

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.shutdown()

    def __init__(self, host='192.168.1.100', port=21845):

        self.host=host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        
        # Initialise it to a static image display
        self.send(self.send_packet_type['write'], self.command['display_mode'], self.display_mode['static'])
    
    def _arr_to_bmp(self, arr):
        """Convert array to 1 bit BMP, white wherever the array is nonzero, and return a
        bytestring of the BMP data"""
        binary_arr = 255 * (arr != 0).astype(np.uint8)
        im = PIL.Image.fromarray(binary_arr, mode='L').convert('1')
        f = io.BytesIO()
        im.save(f, "BMP")
        return f.getvalue()
    
    def send(self, type, command, data):
        packet = b''.join([type,command,self.flag['complete'],struct.pack('<H',len(data)),data])
        packet += struct.pack('<B',sum(bytearray(packet)) % 256) # add the checksum
        self.sock.send(packet)
        return self.receive()
        
    def _receive(self):
        # This function assumes that we are getting a fresh packet, i.e. there is nothing waiting in the buffer
        # First we get the header bits, to see how big the payload will be:
        header = self.sock.recv(6)
        pkt_type = self.receive_packet_type[header[0:1]]
        command = header[1:3]
        flag = header[3:4]
        length = struct.unpack('<H',header[4:6])[0]
        body = self.sock.recv(length + 1)
        checksum = body[-1:]
        body = body[:-1]
        return {'header' : header, 'type' : pkt_type, 'command' : command, 'flag' : flag, 'length' : length, 'body' : body, 'checksum' : checksum}
        
    def receive(self):
        recv = self._receive()
        # Check the type
        while recv['type'] == "System Busy":
            # the system is busy, guess we should try again in 5 seconds?
            time.sleep(5)
            recv = self._receive()
            
        if recv['type'] == "Error":
            # We have an error
            errors = ""
            for e in recv['body']:
                errors+= self.error_messages[e] + "\n"
            
            raise Exception("Error(s) in receive packet: %s"%errors)
        
        
        check = struct.pack('<B',sum(bytearray(recv['header'] + recv['body'])) % 256)
        
        if check != recv['checksum']:
            raise Exception('Incoming packet checksum does not match')
            
        if recv['flag'] != self.flag['complete']:
            raise Exception('Incoming packet is multipart, this is not implemented yet')
        
        if recv['type'] == 'Write response':
            return True
        else:
            return recv['body']
    
    
    
    def program_manual(self, data):
        """
        Parameters
        ----------
        data : np.array or bitmap
            DESCRIPTION.
        """
            
        ## Check to see if it's a BMP
        if data[0:2] != b"BM":
            
            if data.shape == (self.HEIGHT, self.WIDTH):
                data = np.round(np.clip(data, 0, 1))
                data = self._arr_to_bmp(data)
            else:
                raise Exception('Error loading image: Image in bmp format, and uable to convert to BMP of correct size')
        
        self.send(self.send_packet_type['write'], self.command['display_mode'], self.display_mode['static'])
        self.send(self.send_packet_type['write'], self.command['static_image'], data)
        return {}
        
    def shutdown(self):
        self.sock.close()
        
    #
    # Utility features
    # 

    def RandomPattern(self, scale=0.5):
        pattern = np.random.rand(self.HEIGHT, self.WIDTH)
        
        return self.ToBinary(pattern, scale=scale)
    
    def ToBinary(self, pattern, scale=0.5):
        ones = pattern > scale
        pattern.fill(0)
        pattern[ones] = 1
        pattern = pattern.round()
        
        return pattern        

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

class IMAQdx_Camera(object):
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
    
    def __init__(self, serial_number):


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
        self.img = nv.imaqCreateImage(nv.IMAQ_IMAGE_U16)
        self._abort_acquisition = False

    def set_attributes(self, attr_dict):
        for k, v in attr_dict.items():
            self.set_attribute(k, v)

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

    def get_attributes(self, visibility_level, writeable_only=True):
        """Return a dict of all attribute names of readable attributes, for the given
        visibility level. Optionally return only writeable attributes"""
        
        attributes = self.get_attribute_names(visibility_level, writeable_only=writeable_only)
        
        return {k: self.get_attribute(k) for k in attributes}
        
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
        nv.IMAQdxSnap(self.imaqdx, self.img)
        return self._decode_image_data(self.img)

    def configure_acquisition(self, continuous=True, bufferCount=5):
        nv.IMAQdxConfigureAcquisition(
            self.imaqdx, continuous=continuous, bufferCount=bufferCount
        )
        nv.IMAQdxStartAcquisition(self.imaqdx)

    def grab(self, waitForNextBuffer=True):
        nv.IMAQdxGrab(self.imaqdx, self.img, waitForNextBuffer=waitForNextBuffer)
        return self._decode_image_data(self.img)

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

    def abort_acquisition(self):
        self._abort_acquisition = True

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

class WaveMeter():
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.DMD.shutdown()
        self.Camera.close()
    
    def __init__(self, LightCrafterHost='192.168.1.100', IMAQdx_serial=0x30531DC20D):
        
        self.DMD = LightCrafterWorker(host=LightCrafterHost)
        self.Camera = IMAQdx_Camera(IMAQdx_serial)

# Demonstrate field propogation
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')

    with WaveMeter(LightCrafterHost='192.168.1.100', IMAQdx_serial=0x30531DC20D) as Wave:
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

    
    