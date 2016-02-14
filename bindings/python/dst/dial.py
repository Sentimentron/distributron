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
		print(response)
		s.close()
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

	cmd = "{:<8}".format("REGISTER")
	payload = "%s:%s:%d" % (service, hostname, port)
	payload = "{:<1024}".format(service)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 118118))
	s.send(cmd + payload)
	response = s.recv(32).decode('utf8')
	s.close()

	if response == "OK":
		return True
	else:
		raise Exception(response)

def withdraw(service, port, hostname=socket.gethostname()):
	
	cmd = "{:<8}".format("WITHDRAW")
	payload = "%s:%s:%d" % (service, hostname, port)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 118118))
	s.send(cmd + payload)
	response = s.recv(32).decode('utf8')
	s.close()

	if response == "OK":
		return True
	else:
		raise Exception(response)
	
