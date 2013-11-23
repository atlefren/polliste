import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

import unittest
from api_tests.brewery_api_test import *
from api_tests.pol_api_test import *

if __name__ == "__main__":
    unittest.main()