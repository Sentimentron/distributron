#!/usr/bin/env python3

from dst import broker
import unittest

class BrokerTests(unittest.TestCase):
	
	def test_cmd(self):
		broker("ReservedTestService")
		
