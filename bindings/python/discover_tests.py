import os
import sys
import unittest

def additional_tests():
    setup_file = sys.modules['__main__'].__file__
    setup_dir = os.path.abspath(os.path.dirname(setup_file))
    test_dir = os.path.join(setup_dir, 'tests')
    return unittest.defaultTestLoader.discover(test_dir)


