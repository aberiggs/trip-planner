"""Module adding backend/src into the system path"""

import sys
from os.path import dirname as d
from os.path import abspath, join

root_dir = join(d(d(abspath(__file__))), "src")
sys.path.append(root_dir)


root_dir = join(d(d(abspath(__file__))), "tests")
sys.path.append(root_dir)
