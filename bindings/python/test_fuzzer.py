#!/usr/bin/env python3

import unittest

from random import choice
from string import ascii_letters
from dst import rawsend, puck

class TestFuzz(unittest.TestCase):
	def test_lotsofzeros512(self):
		payload = '\x00'*512
		rawsend(payload)
		self.assertTrue(puck())

	def test_lotsofzeros1024(self):
		payload = '\x00'*1024
		rawsend(payload)
		self.assertTrue(puck())

	def test_lotsofzeros512k(self):
		payload = '\x00'*1024*512
		rawsend(payload)
		self.assertTrue(puck())

	def test_random_alphanumeric512(self):
		payload = ''.join(choice(ascii_letters) for x in range(512))
		rawsend(payload)
		self.assertTrue(puck())
		

if __name__ == "__main__":
	unittest.main()	
