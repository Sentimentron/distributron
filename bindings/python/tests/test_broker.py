#!/usr/bin/env python3

from distrib import broker, clearall, register
import socket
import unittest


class BrokerTests(unittest.TestCase):
    """
        Test that the BROKER command is functioning.

            The BROKER command looks up the locations that a service is running.
    """
    def setUp(self):
        clearall()
        register("ReservedTestService", 11819)
        register("AnotherReservedTestService", 11820)
        register("MultiReservedTestService", 11821)
        register("MultiReservedTestService", 11822)

    def test_cmd_1(self):
        """
        Tests that the ReservedTestService created in setUp can be found.
        """
        svcs = list(broker("ReservedTestService"))
        self.assertEqual(len(svcs), 1)
        self.assertEqual(svcs[0][0], socket.gethostname())
        self.assertEqual(svcs[0][1], 11819)

    def test_cmd_2(self):
        """
        Tests that BROKER can correctly distinguish between services.
        """
        svcs = list(broker("AnotherReservedTestService"))
        self.assertEqual(len(svcs), 1)
        self.assertEqual(svcs[0][0], socket.gethostname())
        self.assertEqual(svcs[0][1], 11820)

    def test_cmd_multi(self):
        """
        Tests that BROKER can correctly return multiple results.
        """
        svcs = list(broker("MultiReservedTestService"))
        self.assertEqual(len(svcs), 2)
        self.assertEqual(svcs[0][0], socket.gethostname())
        self.assertEqual(svcs[1][0], socket.gethostname())


if __name__ == "__main__":
    unittest.main()
