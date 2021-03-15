This repository is a demo to make a pip-installable pyoorb.  pyoorb is the python interface to [OpenOrb](https://github.com/oorb/oorb), an orbit computation package.  The original pyoorb source is distributed with OpenOrb.

Only the default ephemeris data are downloaded.

## Install

pip can install directly from this repo:
```
pip install git+https://github.com/mkelley/pyoorb-experiment
```

Otherwise, checkout the source, download the oorb submodule, and install:
```
git clone https://github.com/mkelley/pyoorb-experiment
cd pyoorb-experiment
git submodule update --init
python3 setup.py install
```


## Implementation

OpenOrb is included as a git submodule.  A custom setuptools build_ext command configures OpenOrb to use gfortran, build the libraries, and download the de430 ephemeris.  Numpy is used to build the FORTRAN extension library.  This was always the case with pyoorb included with OpenOrb, but here we use setup.py to build the FORTRAN signature file and library, rather than build it with a Makefile.  In order to compile the extension, the relevant files are copied from the OpenOrb source tree to a local `src` directory.