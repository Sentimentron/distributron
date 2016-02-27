#!/usr/bin/env python3

from distrib import search, clearall, register
import unittest


class SearchTests(unittest.TestCase):
    """
    The SEARCH command is used to retrieve services based on a prefix.
    """
    def setUp(self):
        clearall()

    def test_search(self):
        """
        Test that when we have 400 services (test/0, test/1 etc)
        that we search for "test/", we can get them all.
        """
        test_svcs = ["test/{}".format(i) for i in range(400)]
        for svc in test_svcs:
            response = register(svc, 1211)
            if response != "OK":
                raise ValueError(response)
        response_svcs = search("test/")
        self.assertEqual(set(response_svcs), set(test_svcs))

    def tearDown(self):
        clearall()


if __name__ == "__main__":
    unittest.main()
