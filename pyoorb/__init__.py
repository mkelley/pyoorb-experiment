from .ext import pyoorb

import os
import sys
__version__ = open(
    os.path.join(sys.prefix, 'share', 'oorb', 'VERSION'),
    'r').read(-1).strip()
del os, sys