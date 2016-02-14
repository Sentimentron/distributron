#!/usr/bin/env python3

import unittest
from dst import register

class TestRegister(unittest.TestCase):
	
	def test_register(self):
		response = register("testService", 12311)
		self.assertEqual(response, "OK")

	def test_register_everything(self):
		for i in range(64):
			response = register("testService", 12312 + i)
			self.assertEqual(response, "OK")


if __name__ == "__main__":
	unittest.main()	
