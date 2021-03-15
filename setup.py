#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
from glob import glob
import shutil
from numpy.distutils.core import setup, Extension as NumpyExtension
from numpy.distutils.command.build_ext import build_ext

import subprocess


class PyoorbBuildExt(build_ext):
    def run(self):
        self.configure()
        self.make()
        self.download_ephem()
        self.copy_files()
        super().run()

    def configure(self):
        cmd = [
            './configure',
            'gfortran',
            'opt',
        ]
        subprocess.check_call(cmd, cwd='oorb')

    def make(self):
        cmd = ['make', '-j']
        subprocess.check_call(cmd, cwd='oorb')

    def download_ephem(self):
        cmd = ['make', 'ephem']
        subprocess.check_call(cmd, cwd='oorb')

    def copy_files(self):
        """Copies fortran-python interface and supporting files."""
        if not os.path.exists('src'):
            os.mkdir('src')
        files = [
            'oorb/build/planetary_data.mod',
            'oorb/build/base_cl.mod',
            'oorb/build/time_cl.mod',
            'oorb/build/sphericalcoordinates_cl.mod',
            'oorb/build/observatories_cl.mod',
            'oorb/build/orbit_cl.mod',
            'oorb/build/stochasticorbit_cl.mod',
            'oorb/build/physicalparameters_cl.mod',
            'oorb/python/pyoorb.f90',
        ]
        for f in files:
            shutil.copy(f, 'src')


def version():
    """Generate version using oorb script."""
    cmd = ['./build-tools/compute-version.sh']
    return subprocess.check_output(cmd, cwd='oorb').decode().strip()


setup(
    version=version(),
    cmdclass={
        'build_ext': PyoorbBuildExt
    },
    ext_modules=[NumpyExtension(
        'pyoorb.ext', ['src/pyoorb.f90'],
        libraries=['lapack'],
        extra_objects=['oorb/lib/liboorb.a']
    )],
    data_files=[
        ('oorb', glob('oorb/data/*.dat') + ['oorb/VERSION'])
    ]
)
