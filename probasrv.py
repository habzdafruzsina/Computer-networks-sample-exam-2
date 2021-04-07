import sys
import socket
import select
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8081)
sock.bind(server_address)

container_addr = ('localhost', 8082)

packer = struct.Struct('f 1s f')
values = (1, bytes("+" ,"UTF8"), 2.7)
packed_data = packer.pack(*values)

sock.sendto(packed_data, container_addr)

sock.close()