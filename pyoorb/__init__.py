import os
import pkg_resources
from .ext import pyoorb

# The OORB_DATA environment variable overrides oorb's default search path for data
# files.  If it is not already set, then set it.
if 'OORB_DATA' not in os.environ:
    os.environ['OORB_DATA'] = pkg_resources.resource_filename(
        'pyoorb.data', '')

__version__ = (pkg_resources.resource_stream('pyoorb', 'VERSION')
               .read().strip().decode())

# clean namespace
del os, pkg_resources
