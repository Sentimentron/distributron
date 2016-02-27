#!/usr/bin/env python3

from distrib import broker, clearall, register
import unittest


class ClearTests(unittest.TestCase):
    """
        Test that the CLEAR command responds correctly.
    """

    def test_cmd(self):
        """
            Check that the command returns OK, which it always should.
        """
        self.assertEqual(clearall(), "OK")

    def test_cmd_invalidates(self):
        """
            Check that the command invalidates everything previously
            registered and that nothing is returned for previously
            valid command.
        """
        response = register("clearTestService", 1101)
        if response != "OK":
            raise ValueError(response)
        svcs = list(broker("clearTestService"))
        if len(svcs) != 1:
            raise ValueError(len(svcs))
        self.assertEqual(clearall(), "OK")
        svcs = list(broker("clearTestService"))
        self.assertEqual(len(svcs), 0)


if __name__ == "__main__":
    unittest.main()
