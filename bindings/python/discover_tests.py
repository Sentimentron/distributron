"""
Compatibility shim so you can run python3 setup.py test to run the tests.

Credit: http://stackoverflow.com/a/17004409/854911
"""

import os
import sys
import unittest

def additional_tests():
    setup_file = sys.modules['__main__'].__file__
    setup_dir = os.path.abspath(os.path.dirname(setup_file))
    test_dir = os.path.join(setup_dir, 'tests')
    return unittest.defaultTestLoader.discover(test_dir)


