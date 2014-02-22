from socket import socket, AF_INET, SOCK_RAW, inet_ntoa
from struct import unpack

class sniffer:
    def __init__(self):
        self._listen_socket = socket(AF_INET, SOCK_RAW, 6)
    
    def listen_loop(self):
        self._listening = True 
        while self._listening:
            packet, address = self._listen_socket.recvfrom(65565)
            ip_header = packet[0:20]

            unpacked_header = unpack("!BBHHHBBH4s4s", ip_header)

            version = unpacked_header[0] >> 4
            header_length = unpacked_header[0] & 0xF
            dscp = unpacked_header[1] >> 2
            ecn = unpacked_header[1] & 0x3
            total_length = unpacked_header[2]
            flags = unpacked_header[4] >> 5
            protocol = unpacked_header[6] 
            checksum = unpacked_header[7]
            source_ip = inet_ntoa(unpacked_header[8])
            dest_ip = inet_ntoa(unpacked_header[9])

            print("Version:" + str(version) + "\nHeader Length: " + str(header_length) + "\nTotal length: " + str(total_length) + "\nFlags: " + str(flags) + "\nProtocol: " + str(protocol) + "\nChecksum: " + str(checksum) + "\nSourceIP: " + str(source_ip) + "\nDestIP: " + str(dest_ip) + "\n")
    
    def stop(self):
        self._listening = False
