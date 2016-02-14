#!/bin/env python3

import socket
from time import sleep

def rawsend(payload):	
	response = "ERR_BAD_CMD_READ"
	while response == "ERR_BAD_CMD_READ":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", 11818))
		s.sendall(payload.encode('utf8'))
		response = s.recv(1024).decode('utf8')
		s.close()
		if response == "ERR_BAD_CMD_READ":
			sleep(0.05)
	return response.split(u'\0',1)[0]

def broker(service):	
	cmd = "{:<8}".format("BROKER")
	payload = "{:<1024}".format(service)

	response = rawsend(cmd + payload)
	
	# If the response is valid, the first few characters
	# should be 'OK' followed by a space.
	if response[0:3] == "OK ":
		response = response[3:]
		# Each response consists of a port and a FQDN
		# followed by a comma
		responses = response.split(',')
		for response in responses:
			fqdn,_,port = response.partition(':')
			yield fqdn, int(port)

	# Otherwise, the entire response is the error message
	else:
		raise Exception(response)

def register(service, port):
	hostname = socket.gethostname()

	if type(port) != type(0):
		raise TypeError("port: must be integer")
	if port <= 0 or port >= 65536:
		raise ValueError("port: must be 1-65535")

	cmd = "{:<8}".format("REGISTER")
	payload = "%s:%d:%s," % (hostname, port, service)
	l = len(payload)
	l = "{:<4}".format(l)
	payload = "{:<1024}".format(payload)

	response = rawsend(cmd + l + payload)
	return response

def clearall():
	cmd = "{:<8}".format("CLEARALL")
	response = rawsend(cmd)
	return response

def withdraw(service, port, hostname=socket.gethostname()):
	
	cmd = "{:<8}".format("WITHDRAW")
	payload = "%s:%d:%s," % (hostname, port, service)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 118118))
	s.send(cmd + payload)
	response = s.recv(32).decode('utf8')
	s.close()

	if response == "OK":
		return True
	else:
		raise Exception(response)
	
