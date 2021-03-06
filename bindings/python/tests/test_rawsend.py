#!/usr/bin/env python3

import unittest
from distrib import rawsend, clearall

class TestRawSend(unittest.TestCase):
	def setUp(self):
		clearall()

	def test_badcmd(self):
		payload = "{:<1024}".format("Hi there!")
		cmd = "{:<8}".format("HI")
		response = rawsend(cmd+payload)
		self.assertEqual(response, "ERR_BAD_CMD")

	def test_badcmd_tooshort(self):
		payload = "{:<1024}".format("Hi there!")
		cmd = "BROKER"
		response = rawsend(cmd+payload)
		self.assertEqual(response, "ERR_BAD_CMD")

	def test_badcmd_toolong(self):
		cmd = "BROKERBROKER"
		payload = "{:<1024}".format("Hi there!")
		response = rawsend(cmd+payload)
		self.assertEqual(response, "ERR_BAD_CMD")

	def test_badpayload(self):
		cmd = "{:<8}".format("BROKER")
		response = rawsend(cmd)
		self.assertEqual(response, "ERR_BAD_PAYLOAD_SIZE")

	def test_badpayload_missingsize(self):
		cmd = "{:<8}".format("BROKER")
		payload = "{:<1024}".format("BLAH BLAH")
		response = rawsend(cmd + payload)
		self.assertEqual(response, "ERR_BAD_PAYLOAD_SIZE")

	def test_badpayload_smallsize(self):
		cmd = "{:<8}".format("BROKER")
		payload = "{:<1024}".format("BLAH BLAH")
		size = "{:<4}".format(0)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_PAYLOAD_SIZE")

	def test_badpayload_negativesize(self):
		cmd = "{:<8}".format("BROKER")
		payload = "{:<1024}".format("BLAH BLAH")
		size = "{:<4}".format(-40)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_PAYLOAD_SIZE")

	def test_badpayload_mismatched_size(self):
		cmd = "{:<8}".format("BROKER")
		payload = "127.0.0.1:1811:SomeService"
		l = len(payload)*2
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_PAYLOAD")

	def test_everything_correct(self):
		cmd = "{:<8}".format("BROKER")
		payload = "SomeService"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "OK 0")

	def test_bad_delim(self):
		cmd = "{:<8}".format("REGISTER")
		payload = "127:1811:SomeService"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_DELIM")

	def test_bad_host(self):
		cmd = "{:<8}".format("REGISTER")
		payload = "1:1811:SomeService,"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_HOST")

	def test_bad_service(self):
		cmd = "{:<8}".format("REGISTER")
		payload = "127.0.0.1:1811:,"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_SRV")

	def test_bad_port(self):
		cmd = "{:<8}".format("REGISTER")
		payload = "127.0.0.1::,"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_PORT")

	def test_bad_port_toosmall(self):
		cmd = "{:<8}".format("REGISTER")
		payload = "127.0.0.1:-128:sp,"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEqual(response, "ERR_BAD_PORT")

if __name__ == "__main__":
	unittest.main()
