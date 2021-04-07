import sys
import socket
import select
import struct

def char_to_command(values):
	switcher = {
		'+': values[0] + values[2],
		'-': values[0] + values[2],
		'/': values[0] + values[2],
		'*': values[0] + values[2],
	}
	return switcher.get(values[1].decode('utf-8'))

def countOut(data):
	values = unpacker.unpack(data)
	return char_to_command(values)
	#switch(values[1]) {
	#	case '+':	result = values[0] + values[2]; break;
	#	case '-':	result = values[0] - values[2]; break;
	#	case '/':	result = values[0] / values[2]; break;
	#	case '*':	result = values[0] * values[2]; break;
	#}
	#return result

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
sock.bind(server_address)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_server_address = ('localhost', 8082)
udp_sock.bind(udp_server_address)

container_addr = ('localhost', 8083)

sock.listen()

unpacker = struct.Struct('f 1s f')
packer = struct.Struct('f')


inputs = [sock]
outputs = []

while inputs:
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	
	for s in readable:
		if s is sock:
			connection, client_address = s.accept()
			connection.setblocking(0)
			inputs.append(connection)
		else:
			data = s.recv(unpacker.size)
			if data:
				udp_sock.sendto(data, container_addr)
				result = countOut(data)
				s.sendall(packer.pack(result))
				if s not in outputs:
					outputs.append(s)
			else:
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()

	for s in exceptional:
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()