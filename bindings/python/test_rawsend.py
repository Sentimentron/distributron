#!/usr/bin/env python3

import unittest
from dst import rawsend

class TestRawSend(unittest.TestCase):
	
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
	
	def test_badpayload_mismatched_size(self):
		cmd = "{:<8}".format("BROKER")
		payload = "127.0.0.1:1811:SomeService"
		l = len(payload)*2
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEquals(response, "ERR_BAD_PAYLOAD")

	def test_everything_correct(self):
		cmd = "{:<8}".format("BROKER")
		payload = "127.0.0.1:1811:SomeService"
		l = len(payload)
		size = "{:<4}".format(l)
		response = rawsend(cmd + size + payload)
		self.assertEquals(response, "OK")

if __name__ == "__main__":
	unittest.main()	
