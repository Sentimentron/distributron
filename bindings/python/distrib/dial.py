#!/bin/env python3

import socket
from time import sleep


def _val_service(s):
    """
    Checks that the service name doesn't contain reserved characters.
    Raises a ValueError if something's wrong.
    :param s: The service to check.
    :return:
    """
    if ":" in s:
        raise ValueError("service names cannot include ':'")
    if "," in s:
        raise ValueError("service names cannot include ','")
    if " " in s:
        raise ValueError("service names cannot include ' '")


def rawsend(payload):
    """
    Sends the payload string to the server without additional
    validation or formatting.
    :param payload: The string to send.
    :return: The first element of the response.
    """
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


def puck():
    """
    Checks that the server is alive.
    :return: True if the server is responding.
    """
    try:
        return rawsend("{:<8}".format("PUCK")) == "OK"
    except:
        return False


def clearall():
    """
    Deletes all of the registered service entries.
    :return: 'OK' if the deletion succeeded.
    """
    return rawsend("{:<8}".format("CLEARALL"))


def register(service, port):
    """
    Registers :service: at the given :port:.
    :param service: The service name to register.
    :param port: The TCP/IP or UDP port the service is listening on.
    :return: 'OK' if the registration succeeded.
    """
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
    """
    Looks up services beginning with :prefix:. Because the response to
    SEARCH can include duplicates, we return a set object, which filters them.
    :param prefix: The lookup prefix.
    :return: A set of matching services.
    """
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
        status, _, response = response.partition(' ')
        if status == "OK":
            num_responses, _, response = response.partition(' ')
        elif status == "ERR_BAD_CMD_READ":
            sleep(0.05)

    num_responses = int(num_responses)
    recv_responses = len(response.split(' '))
    data = response
    while recv_responses < num_responses:
        response = s.recv(1024)
        data += response.rstrip(b'\x00').decode('utf8')
        recv_responses = len(data.split(' '))
    s.close()
    return set([d for d in data.split(' ') if len(d) > 0])


def broker(service):
    """
    BROKER yields a list of hosts and TCP/UDP ports that are providing
    a given :service:.
    :param service: The service to look up.
    :return: A generator containing (host, port) tuples.
    """
    _val_service(service)

    # Format arguments
    cmd = "{:<8}".format("BROKER")
    l = len(service)
    payload = service
    l = "{:<4}".format(l)
    payload = cmd + l + payload

    # Open the socket, manually decode the response
    status = "ERR_BAD_CMD_READ"
    try:
        while status == "ERR_BAD_CMD_READ":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 11818))
            s.sendall(payload.encode('utf8'))
            response = s.recv(1024).decode('utf8')
            status, _, response = response.partition(' ')
            if status == "OK":
                num_responses, _, response = response.partition(' ')
            elif status == "ERR_BAD_CMD_READ":
                sleep(0.05)

        num_responses = int(num_responses)
        recv_responses = len(response.split(' '))
        data = response
        while recv_responses < num_responses:
            response = s.recv(1024)
            data += response.rstrip(b'\x00').decode('utf8')
            recv_responses = len(data.split(' '))
        for d in data.split(' '):
            if len(d) == 0:
                continue
            host, _, port = d.partition(':')
            yield host, int(port)
    finally:
        s.close()


def withdraw(service, port, hostname=socket.gethostname()):
    """
    Declares that service :service: running on :port: running on :hostname:
    is no longer listening.
    :param service: The service to withdraw.
    :param port: The port that :service: is listening on.
    :param hostname: The host that :service: is listening on.
    :return: 'OK' if the withdraw succeeded.
    """
    _val_service(service)

    cmd = "{:<8}".format("WITHDRAW")
    payload = "%s:%d:%s," % (hostname, port, service)
    l = "{:<4}".format(len(payload))

    response = rawsend(cmd + l + payload)

    if response == "OK":
        return True
    else:
        raise Exception(response)
