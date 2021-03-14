#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import sys
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
import subprocess


class PyoorbBuild(build_py):
    def run(self):
        self.run_command('build_ext')
        return super().run()


class PyoorbBuildExt(build_ext):
    def run(self):
        self.configure()
        self.make()
        self.download_ephem()
        return super().run()

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
        'build': PyoorbBuild,
        'build_ext': PyoorbBuildExt,
        'install': PyoorbInstall
    }
)
