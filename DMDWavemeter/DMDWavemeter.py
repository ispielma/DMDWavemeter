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
import h5py
import io
import socket    
from Camera_Pylon import Camera

        
class LightCrafterWorker():

    #
    # Physical properties
    #
    
    WIDTH = 608
    HEIGHT = 684
    
    ZEROS = np.zeros((HEIGHT, WIDTH))
    ONES = np.ones((HEIGHT, WIDTH))
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
            
        if data.shape == (self.HEIGHT, self.WIDTH):
            data = np.round(np.clip(data, 0, 1))
            data = self._arr_to_bmp(data)
        else:
            raise Exception('Error loading image: unable to convert to BMP of correct size')
        
        self.send(self.send_packet_type['write'], self.command['display_mode'], self.display_mode['static'])
        self.send(self.send_packet_type['write'], self.command['static_image'], data)
        return {}
        
    def shutdown(self):
        self.sock.close()
        
    #
    # Utility features
    # 
    
    def ToBinary(self, pattern, scale=0.5):
        ones = pattern > scale
        pattern.fill(0)
        pattern[ones] = 1
        pattern = pattern.round()
        
        return pattern        

    #
    # Utility features
    # 

    def RandomPattern(self, scale=0.5):
        pattern = np.random.rand(self.HEIGHT, self.WIDTH)
        
        return self.ToBinary(pattern, scale=scale)

    def GridPattern(self, scale=0.5):
        coords = self.XY_COORDS_ROT
        pattern = (1+np.cos(np.pi*coords[0])) / 2
        pattern += (1+np.cos(np.pi*coords[1])) / 2
        pattern /=2      
        return self.ToBinary(pattern)




class WaveMeter():
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        
        try:
            self.DMD.shutdown()
        except:
            print("DMD Shutdown Falied")
            
        self.Camera.close()
    
    def __init__(self, LightCrafterHost='192.168.1.100', Camera_serial=0x30531DC20D):
        
        self.DMD = LightCrafterWorker(host=LightCrafterHost)
        self.Camera = Camera(Camera_serial)

    def AcquireStandardFrame(self, option=None):
        """
        Configure the DMD for a standard acquisition and grab a frame.

        Returns
        -------
        None.

        """

    
        if option=='ones':
            pattern = self.DMD.ONES
        elif option=='zeros':
            pattern = self.DMD.ZEROS            
        else:
            pattern = self.DMD.GridPattern()
            
        self.DMD.program_manual(pattern)
        time.sleep(0.1)
        self.StandardFrame = Wave.Camera.snap()
        
        return self.StandardFrame

    def SaveAll(self, filename, name='StandardFrame'):
        """
        Sdaves the current full frame into an h5 file

        Parameters
        ----------
        filename : string
            where to save the file.

        Returns
        -------
        None.

        """
        
        with h5py.File('demo.h5', "a") as file:
             file.create_dataset(name, data=self.StandardFrame)

# Sample execution of wavemeter
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')
    Camera_serial = 0x30531DC20D # for imaqdx bigboy
    Camera_serial = 0x14eef0d # for pylon bigboy
    
    with WaveMeter(LightCrafterHost='192.168.1.100', Camera_serial=Camera_serial) as Wave:        
        
        image = Wave.AcquireStandardFrame()
        Wave.SaveAll('demo.h5')

        image = Wave.AcquireStandardFrame(option='ones')
        Wave.SaveAll('demo.h5', name='ones')

        image = Wave.AcquireStandardFrame(option='zeros')
        Wave.SaveAll('demo.h5', name='zeros')   
        

    fig = pyplot.figure(figsize=(12,6))
    gs = fig.add_gridspec(1, 2)
    gs.update(left=0.13, right=0.95, top=0.92, bottom = 0.15, hspace=0.5, wspace = 0.35)  

    ax = fig.add_subplot(gs[0,0])
    ax.imshow(image)
    
    ax = fig.add_subplot(gs[0,1])
    ax.imshow(Wave.DMD.GridPattern())

    
    