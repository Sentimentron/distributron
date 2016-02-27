#!/usr/bin/env python3

import unittest
import socket
from distrib import register, withdraw, broker, clearall


class TestWithdraw(unittest.TestCase):
    """
    The WITHDRAW command used to declare that a service isn't
    listening any more.
    """
    def setUp(self):
        clearall()

    def test_withdraw(self):
        """
        Check that withdrawn services are no longer visible in BROKER.
        """
        response = register("testService1", 12311)
        self.assertEqual(response, "OK")

        svcs = list(broker("testService1"))
        self.assertEqual(len(svcs), 1)

        withdraw("testService1", 12311)

        svcs = list(broker("testService1"))
        self.assertEqual(len(svcs), 0)


if __name__ == "__main__":
    unittest.main()
