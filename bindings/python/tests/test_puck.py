#!/usr/bin/env python3

import unittest
from distrib import puck


class TestPuck(unittest.TestCase):
    """
    The PUCK command is used to check that the server is alive.
    """

    def test_puck(self):
        """
        The puck command should always return True.
        """
        self.assertTrue(puck())


if __name__ == "__main__":
    unittest.main()
