#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import sys
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
import subprocess


class PyoorbBuild(build_ext):
    def run(self):
        # super().run(self)
        self.configure()
        self.make()
        self.download_ephem()

    def configure(self):
        cmd = [
            './configure',
            'gfortran',
            'opt',
            '--with-pyoorb',
            f'--prefix={sys.prefix}'
        ]
        subprocess.check_call(cmd, cwd='oorb')

    def make(self):
        cmd = ['make', '-j']
        subprocess.check_call(cmd, cwd='oorb')

    def download_ephem(self):
        cmd = ['make', 'ephem']
        subprocess.check_call(cmd, cwd='oorb')


class PyoorbInstall(install):
    def run(self):
        cmd = ['make', 'install']
        subprocess.check_call(cmd, cwd='oorb')


setup(
    cmdclass={
        'build_ext': PyoorbBuild,
        'install': PyoorbInstall
    }
)
