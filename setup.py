#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
from glob import glob
import shutil
import setuptools
from numpy.distutils.core import setup, Extension as NumpyExtension
from numpy.distutils.command.build_src import build_src

import subprocess


class PyoorbBuildSrc(build_src):
    def run(self):
        self.env = os.environ.copy()
        self.find_gfortran()
        self.configure()
        self.make()
        # self.download_ephem()
        self.copy_files()
        super().run()

    def find_gfortran(self):
        """Find a gfortran executable."""
        if os.environ.get("FC_GFORTRAN") is not None:
            gfortran = shutil.which(name)
        else:
            for name in ("gfortran", "gfortran-11", "gfortran-12", "gfortran-10"):
                gfortran = shutil.which(name)
                if gfortran is not None:
                    break

        if gfortran is None:
            fc = (
                ""
                if os.environ.get("FC_GFORTRAN") is None
                else f"  FC_GFORTRAN = {os.environ.get('FC_GFORTRAN')}"
            )
            raise FileNotFoundError("Cannot find gfortran executable." + fc)

        self.env["FC_GFORTRAN"] = gfortran

    def configure(self):
        """Configures oorb to build with gfortran and optimization."""
        if not os.path.exists("oorb/Makefile.include"):
            cmd = [
                "./configure",
                "gfortran" "opt",
            ]
            subprocess.check_call(cmd, cwd="oorb", env=self.env)

    def make(self):
        """Builds oorb, required to build the pyoorb extension."""
        if not os.path.exists("oorb/lib/liboorb.a"):
            cmd = ["make", "-j"]
            subprocess.check_call(cmd, cwd="oorb", env=self.env)

    def download_ephem(self):
        """Downloads the default oorb ephemeris."""
        if not os.path.exists("oorb/data/de430.dat"):
            cmd = ["make", "ephem"]
            subprocess.check_call(cmd, cwd="oorb", env=self.env)

    def copy_files(self):
        """Copies fortran-python interface and data files."""
        if not os.path.exists("src"):
            os.mkdir("src")
        files = [
            "oorb/build/planetary_data.mod",
            "oorb/build/base_cl.mod",
            "oorb/build/time_cl.mod",
            "oorb/build/sphericalcoordinates_cl.mod",
            "oorb/build/observatories_cl.mod",
            "oorb/build/orbit_cl.mod",
            "oorb/build/stochasticorbit_cl.mod",
            "oorb/build/physicalparameters_cl.mod",
            "oorb/python/pyoorb.f90",
        ]
        for f in files:
            if not os.path.exists(os.path.join("src", os.path.basename(f))):
                shutil.copy(f, "src")

        path = "pyoorb/data"
        for f in glob("oorb/data/*.dat"):
            if not os.path.exists(os.path.join(path, os.path.basename(f))):
                shutil.copy(f, path)

        shutil.copy("oorb/VERSION", "pyoorb")


def version():
    """Generate version using oorb script."""
    cmd = ["./build-tools/compute-version.sh"]
    return subprocess.check_output(cmd, cwd="oorb").decode().strip()


setup(
    version=version(),
    cmdclass={"build_src": PyoorbBuildSrc},
    ext_modules=[
        NumpyExtension(
            "pyoorb.ext",
            ["src/pyoorb.f90"],
            libraries=["lapack"],
            extra_objects=["oorb/lib/liboorb.a"],
        )
    ],
    # install data files
    package_data={"pyoorb": ["data/*.dat", "VERSION"]},
)
