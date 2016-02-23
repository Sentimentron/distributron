#!/usr/bin/env python3

import unittest
from dst import puck

class TestPuck(unittest.TestCase):
		
	def test_puck(self):
		self.assertTrue(puck())


if __name__ == "__main__":
	unittest.main()	
