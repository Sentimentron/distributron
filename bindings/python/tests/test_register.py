#!/usr/bin/env python3

import unittest
from distrib import register


class TestRegister(unittest.TestCase):
    """
    The REGISTER command is used to declare services.
    """
    def test_register(self):
        """
        Check that we can register a basic service.
        """
        response = register("testService", 12311)
        self.assertEqual(response, "OK")

    def test_register_everything(self):
        """
        Check that we can register a service which listens
        on multiple ports.
        """
        for i in range(64):
            response = register("testService", 12312 + i)
            self.assertEqual(response, "OK")


if __name__ == "__main__":
    unittest.main()
