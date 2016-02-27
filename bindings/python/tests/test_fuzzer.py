#!/usr/bin/env python3

import unittest

from random import choice
from string import ascii_letters
from distrib import rawsend, puck


class TestFuzz(unittest.TestCase):
    """
    TestFuzz checks that some obviously badly-formatted commands don't
    crash the server.
    """
    def test_lotsofzeros512(self):
        """
        Send a payload of 512 zeros.
        """
        payload = '\x00' * 512
        rawsend(payload)
        # Check that the server is still alive.
        self.assertTrue(puck())

    def test_lotsofzeros1024(self):
        """
        Send a payload of 512 zeros.
        """
        payload = '\x00' * 1024
        rawsend(payload)
        self.assertTrue(puck())

    def test_lotsofzeros512k(self):
        """
        Send a payload of 512 KB of zeros.
        """
        payload = '\x00' * 1024 * 512
        rawsend(payload)
        self.assertTrue(puck())

    def test_random_alphanumeric512(self):
        """
        Send a payload of 512 random characters.
        """
        payload = ''.join(choice(ascii_letters) for x in range(512))
        rawsend(payload)
        self.assertTrue(puck())


if __name__ == "__main__":
    unittest.main()
