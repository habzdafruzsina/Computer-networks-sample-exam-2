import sys
import socket
import select
import struct

unpacker = struct.Struct('f 1s f')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('localhost', 8083)
sock.bind(address)


udp_server_address = ('localhost', 8082)


container = []

while(True):
	result, udp_server_address = sock.recvfrom(unpacker.size)
	unpacked_data = unpacker.unpack(result)
	if(unpacked_data):
		container.append(unpacked_data)
		print(str(unpacked_data[0]) + unpacked_data[1].decode('utf-8') + str(unpacked_data[2]))



socket.close()
