from socket import socket, AF_INET, SOCK_RAW, inet_ntoa
from struct import unpack
from collections import namedtuple
import time

class Sniffer:
    def __init__(self):
        self._listen_socket = socket(AF_INET, SOCK_RAW, 6)
        self._callbacks = list()

    def add_callback(self, callbackObject):
        self._callbacks.append(callbackObject)

    def listen_loop(self):
        self._listening = True 
        while self._listening:
            packet, address = self._listen_socket.recvfrom(65565)

            packet_dict = {}

            ip_header = packet[0:20]

            unpacked_header = unpack("!BBHHHBBH4s4s", ip_header)

            packet_dict['source_ip'] = inet_ntoa(unpacked_header[8])
            packet_dict['dest_ip'] = inet_ntoa(unpacked_header[9])
            if packet_dict['source_ip'] == packet_dict['dest_ip']:
                continue
            packet_dict['version'] = unpacked_header[0] >> 4
            packet_dict['header_length'] = unpacked_header[0] & 0xF
            packet_dict['dscp'] = unpacked_header[1] >> 2
            packet_dict['ecn'] = unpacked_header[1] & 0x3
            packet_dict['total_length'] = unpacked_header[2]
            packet_dict['flags'] = unpacked_header[4] >> 5
            packet_dict['protocol'] = unpacked_header[6] 
            packet_dict['checksum'] = unpacked_header[7]
            packet_dict['time'] = time.time()

            for obj in self._callbacks:
                obj.packet_received(packet_dict)

            print("Packet Received: Source IP: " + packet_dict['source_ip'] + " Dest IP: " + packet_dict['dest_ip'])
    
    def __call__(self):
        self.listen_loop()
    
    def stop(self):
        self._listening = False
