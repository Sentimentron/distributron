#!/usr/bin/env python3

from dst import broker, clearall, register
import socket
import unittest

class BrokerTests(unittest.TestCase):
	
	def setUp(self):
		clearall()
		register("ReservedTestService", 11819)
		register("AnotherReservedTestService", 11820)
		register("MultiReservedTestService", 11821)
		register("MultiReservedTestService", 11822)

	def test_cmd_1(self):
		svcs = list(broker("ReservedTestService"))
		self.assertEqual(len(svcs), 1)
		self.assertEqual(svcs[0][0], socket.gethostname())
		self.assertEqual(svcs[0][1], 11819)
		self.assertEqual(svcs[0][2], "ReservedTestService")
	
	def test_cmd_2(self):
		svcs = list(broker("AnotherReservedTestService"))	
		self.assertEqual(len(svcs), 1)
		self.assertEqual(svcs[0][0], socket.gethostname())
		self.assertEqual(svcs[0][1], 11820)
		self.assertEqual(svcs[0][2], "AnotherReservedTestService")

	def test_cmd_multi(self):
		svcs = list(broker("MultiReservedTestService"))
		self.assertEqual(len(svcs), 2)
		self.assertEqual(svcs[0][0], socket.gethostname())	
		self.assertEqual(svcs[1][0], socket.gethostname())	
		self.assertEqual(svcs[0][2], "MultiReservedTestService")
		self.assertEqual(svcs[1][2], "MultiReservedTestService")

if __name__ == "__main__":
	unittest.main()
