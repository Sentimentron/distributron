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

    def test_withdraw_nonexistent(self):
        """
        Even if a service wasn't registered, you should be able to WITHDRAW it.
        """
        self.assertTrue(withdraw("testServiceNonExistent", 12311))

    def test_withdraw_altport(self):
        """
        Withdrawing services on other ports should not affect this one,
        even if they have the same name.
        """
        response = register("testService1", 12311)
        self.assertEqual(response, "OK")

        response = register("testService1", 12312)
        self.assertEqual(response, "OK")

        svcs = list(broker("testService1"))
        self.assertEqual(len(svcs), 2)

        withdraw("testService1", 12312)

        svcs = list(broker("testService1"))
        self.assertEqual(len(svcs), 1)

    def tearDown(self):
        clearall()

if __name__ == "__main__":
    unittest.main()
