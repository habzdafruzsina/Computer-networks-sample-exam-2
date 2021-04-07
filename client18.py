import sys
import socket
import struct

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
server_sock.connect(server_address)


packer = struct.Struct('f 1s f')
values = (1, bytes("+" ,"UTF8"), 2.7)
packed_data = packer.pack(*values)


server_sock.sendall(packed_data)


unpacker = struct.Struct('f')
result = unpacker.unpack(server_sock.recv(unpacker.size))

print(result)



server_sock.close()