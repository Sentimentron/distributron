#!/bin/env python3

import socket
from time import sleep

def _val_service(s):
	if ":" in s:
		raise ValueError("service names cannot include ':'")
	if "," in s:
		raise ValueError("service names cannot include ','")
	if " " in s:
		raise ValueError("service names cannot include ' '")

def rawsend(payload, return_all=False):	
	status = "ERR_BAD_CMD_READ"
	while status == "ERR_BAD_CMD_READ":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", 11818))
		s.sendall(payload.encode('utf8'))
		response = s.recv(1024)
		response = response.split(b'\x00')
		response = [r.decode('utf8') for r in response]
		response = [r for r in response if len(r) > 0]
		s.close()
		status = response[0]
		if status == "ERR_BAD_CMD_READ":
			sleep(0.05)
	if return_all:
		return response
	return response[0]

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
	return response.split(u'\0', 1)[0]

def broker(service):	
	cmd = "{:<8}".format("BROKER")
	l = len(service)
	payload = "{:<1024}".format(service)
	l = "{:<4}".format(l)

	response = rawsend(cmd + l + payload)

	if response == "<null>":
		return None

	# If the response is valid, the first few characters
	# should be 'OK' followed by a space.
	if response[0:3] == "OK ":
		response = response[3:]
		# Each response consists of a port and a FQDN
		# followed by a comma
		responses = response.split(',')
		for response in responses:
			if len(response) == 0:
				break
			fqdn, port, service = response.split(':')
			yield fqdn, int(port), service

	# Otherwise, the entire response is the error message
	else:
		raise Exception(response)

def clearall():
	return rawsend("{:<8}".format("CLEARALL"))

def register(service, port):

	_val_service(service)

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

def search(prefix):
	
	_val_service(prefix)

	# Format arguments
	cmd = "{:<8}".format("SEARCH")
	l = "{:<4}".format(len(prefix))
	payload = cmd + l + prefix
	
	# Open the socket, manually decode the response
	status = "ERR_BAD_CMD_READ"
	while status == "ERR_BAD_CMD_READ":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", 11818))
		s.sendall(payload.encode('utf8'))
		response = s.recv(1024).decode('utf8')
		response = response.split(' ')
		response = [r for r in response if len(r) > 0]
		status = response[0]
		if status == "ERR_BAD_CMD_READ":
			sleep(0.05)

	num_responses = response[1].strip()
	num_responses = int(num_responses)
	recv_responses = len(response[2:])
	data = " ".join(response[2:])
	while recv_responses < num_responses:
		response = s.recv(1024)
		data += response.decode('utf8')
		recv_responses = len(data.split(' '))
	s.close()
	return [d for d in data.split(' ') if len(d) > 0]

def withdraw(service, port, hostname=socket.gethostname()):
	
	_val_service(service)

	cmd = "{:<8}".format("WITHDRAW")
	payload = "%s:%d:%s," % (hostname, port, service)
	l = "{:<4}".format(len(payload))
	
	response = rawsend(cmd + l + payload)

	if response == "OK":
		return True
	else:
		raise Exception(response)
	
