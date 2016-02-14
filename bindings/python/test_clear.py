#!/usr/bin/env python3

from dst import broker, clearall
import unittest

class ClearTests(unittest.TestCase):
	
	def test_cmd(self):
		self.assertEqual(clearall(), "OK")

if __name__ == "__main__":
	unittest.main()	
