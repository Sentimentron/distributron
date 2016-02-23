#!/usr/bin/env python3

from dst import broker, clearall, register
import unittest

class ClearTests(unittest.TestCase):
	
	def test_cmd(self):
		self.assertEqual(clearall(), "OK")

	def test_cmd_invalidates(self):
		response = register("clearTestService", 1101)
		if response != "OK":
			raise ValueError(response)
		svcs = list(broker("clearTestService"))
		if len(svcs) != 1:
			raise ValueError(len(svcs))
		self.assertEqual(clearall(),"OK")
		svcs = list(broker("clearTestService"))
		self.assertEqual(len(svcs), 0)

if __name__ == "__main__":
	unittest.main()	
