#!/usr/bin/env python3

"""

	Compute the inverse, Ai, of the matrix A ( A @ Ai = I ).

		1) Compute LU decomposition of A to speed up step 2

					LU = PA

		2) Solve for Ai using A @ xi = ei,
			where ei is the ith column of the identity matrix, I. 
			And where xi is the ith column of Ai.

"""

__filename__ = "inverse.py"
__author__ = "L.J. Brown"

# internal
import logging

# external
import numpy as np
import scipy.linalg

# initilize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inverse(A, tol=10**(-14), inplace=False):
	""" 
		Compute the inverse of the matrix A and store in place if specified. 

		:param A: nxn non-singular matrix to compute the inverse of.
		:param tol: Defualt set to 10^(-14), consider  values bellow this threshold to be zero.
		:param inplace: Defualt set to False. Store Ai (A inverse) in parameter A when True, create new matrix when set to False, return Ai in either case.
		:returns: Ai (A inverse).
	"""
	n = A.shape[0]

	# LU decomposition -- raise ValueError for singular matrix A
	try:
		LU, piv = scipy.linalg.lu_factor(A)

		# enforce magnitude of diagonal values are above given tolernce (round off)
		for di in np.diag(LU):
			if abs(di) <= tol: raise ValueError

	except ValueError:
		logger.error("Error 'Singular Matrix' passed method: %s" % inverse.__name__)

	# initalize Ai depending on paramter 'inplace'
	if not inplace:
		Ai = np.empty(A.shape)
	else:
		Ai = A 				# Ai is refrence to A

	# initilize column vector of identity matrix to zeros 
	ei = np.zeros(shape=(n,))

	# solve for A^-1 and store in A
	for i in range(n):
		ei[i] = 1
		Ai[:,i] = scipy.linalg.lu_solve((LU, piv), ei)
		ei[i] = 0

	# return Ai (A inverse)
	return Ai

def inverse_solve(A, b, tol=10**(-14)):
	""" 
	Compute the inverse of the matrix A and solve for x in the system,

							Ax = b

	:param A: nxn non-singular matrix to compute the inverse of.
	:param b: vector of length n on the right hand side of the above equation
	:param tol: Defualt set to 10^(-14), consider  values bellow this threshold to be zero.
	:returns: solution vector of length n (x).
	"""
	Ai = inverse(A, tol=tol)
	x = Ai @ b
	return x
