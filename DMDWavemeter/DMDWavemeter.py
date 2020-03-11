# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:04:11 2020

Main code to write patterns to the DMD and to read back the Fourier space
results containing information about the optical wavelength.

@author: ispielma
"""

# COMMON IMPORTS
import base64
import time
import struct
import PIL.Image
import numpy as np
import io

import socket

def arr_to_bmp(arr):
    """Convert array to 1 bit BMP, white wherever the array is nonzero, and return a
    bytestring of the BMP data"""
    binary_arr = 255 * (arr != 0).astype(np.uint8)
    im = PIL.Image.fromarray(binary_arr, mode='L').convert('1')
    f = io.BytesIO()
    im.save(f, "BMP")
    return f.getvalue()


WIDTH = 608
HEIGHT = 684
BLANK_BMP = arr_to_bmp(np.zeros((HEIGHT, WIDTH)))
       
        
class LightCrafterWorker():
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
    
    def init(self, host='192.168.1.100', port=21845):

        self.host=host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        
        # Initialise it to a static image display
        self.send(self.send_packet_type['write'], self.command['display_mode'], self.display_mode['static'])
        
        # self.program_manual({"None" : base64.b64encode(blank_bmp)})
        
        
        
    
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
    
    
    
    def program_manual(self, values):
        for region, value in values.items():
            data = value
            data = base64.b64decode(data)
        # Replace empty data with the black picture
        if not data:
            data = BLANK_BMP
        ## Check to see if it's a BMP
        
        
        if data[0:2] != b"BM":
                raise Exception('Error loading image: Image does not appear to be in bmp format (Initial bits are %s)'%data[0:2])
        
        self.send(self.send_packet_type['write'], self.command['display_mode'], self.display_mode['static'])
        self.send(self.send_packet_type['write'], self.command['static_image'], data)
        return {}
        
    def shutdown(self):
        self.sock.close()

# Demonstrate field propogation
if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path, _ = os.path.split(path)
    import matplotlib.pyplot as pyplot
    
    pyplot.style.use(path + '/matplotlibrc')
    
    # LightCrafterWorker()
