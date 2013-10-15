# -*- coding: utf-8 -*-
# _bplogsmooth.py
# Module providing the bplogsmooth function
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

"""Module providing the bplogsmooth() function, which smooths an fft and 
converts it to dB.
"""

import numpy as np
from numpy.linalg import norm

from ._dbp import dbp

def bplogsmooth(X, tbin, f0):
	"""f, p = bplogsmooth(X, tbin, f0)
	Smooth the fft, X, and convert it to dB.
	Use 8 bins from the bin corresponding to f0 to tbin and again as far. 
	Thereafter increase bin sizes by a factor of 1.1, staying less than 2^10.
	For tbin, group the bins together. TBIN IS ASSUMED TO BE IN THE UPPER SIDEBAND!
	Use this for nice double-sided log-log plots.
	"""
	if hasattr(X, 'shape') and len(X.shape) == 2 and \
	   not X.shape[0]*X.shape[1] == max(X.shape):
		raise VelueError, "The X vector is not unidimensional: " + str(X.shape)
	N = max(X.shape) if hasattr(X, 'shape') else len(X)
	tbin = int(tbin)
	n = 8

	bin0 = np.round(f0*N, 0)
	bin1 = ((tbin - bin0) % n) + bin0
	bind = bin1 - bin0
	usb1 = np.concatenate((np.arange(bin1, tbin+1, n), 
	                       np.arange(tbin+3, tbin+bind+1, 8)
	                     ))
	m = usb1[-1] + n
	while m + n/2. < N/2.:
		usb1 = np.concatenate((usb1, np.array((m,))))
		n = min(n*1.1, 2**10)
		m = m + n
	usb2 = np.concatenate((usb1[1:]-1, np.array((N/2.,))))

	n = 8
	lsb2 = np.arange(bin1, bin1 - 2*bind + 1, -n) - 1
	m = lsb2[-1] - n
	while m - n/2. > 1:
		lsb2 = np.concatenate((lsb2, np.array((m,))))
		n = min(n*1.1, 2**10)
		m = m - n
	lsb1 = np.concatenate((lsb2[1:] + 1, np.ones((1,))))

	startbin = np.concatenate((lsb1[::-1], usb1)) - 1
	stopbin = np.concatenate((lsb2[::-1], usb2)) - 1

	f = ((startbin + stopbin)/2. - 1.)/N - f0
	p = np.zeros(f.shape)
	for i in range(f.shape[0]):
		p[i] = dbp(
		           norm(X[startbin[i]:stopbin[i]+1]**2. /
		                (stopbin[i] - startbin[i] + 1.)
		               )
		          )
	return f, p

def test_bplogsmooth():
	"""Test function.
	"""
	# FIXME WRITE PROPER TEST
	bplogsmooth(np.arange(100), 100, 50)
	
if __name__ == '__main__':
	test_bplogsmooth()