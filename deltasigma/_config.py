# -*- coding: utf-8 -*-
# _config.py
# Module providing configuration switches
# Copyright 2013 Giuseppe Venturini
# This file is part of python-deltasigma.
#
# python-deltasigma is a 1:1 Python replacement of Richard Schreier's
# MATLAB delta sigma toolbox (aka "delsigma"), upon which it is heavily based.
# The delta sigma toolbox is (c) 2009, Richard Schreier.
#
# python-deltasigma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LICENSE file for the licensing terms.

"""Module providing configuration switches.
"""

import os
import sys
from warnings import warn

import numpy as np
from scipy.linalg import get_blas_funcs

# should synthesizeNTF run the optimization routine?
optimize_NTF = True

# how many iterations should be allowed in NTF synthesis?
# see synthesizeNTF() for more
itn_limit = 500

# debug
_debug = False

# get blas information to compile the cython extensions
try:
    get_blas_funcs(["gemm"])
    blas_info = True
except ValueError:
    blas_info = False
    if _debug:
        warn("Scipy did not detect the BLAS library in the system")

setup_args = {"script_args": []}
lib_include = [np.get_include()]

if not blas_info:
    warn(
        "Cannot find the BLAS library. You may set it using the environment variable "
        "BLAS_H.\nNOTE: You need to pass the path to the directories where the "
        "header files are, not the path to the files."
    )
setup_args.update({"include_dirs": list(set(lib_include))})
