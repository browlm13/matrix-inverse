#!/usr/bin/env python3

"""

Solve System Using Two Different Methods


Method 1) Compute the inverse matrix Ai and solve : 
					
					x = Ai @ b

Method 2) Perform LU decomposition and solve two equations 
		  (with forward and backward substitution):

					(1) Ly = b,
					(2) Ux = y
								
				* note: Permuation matrices not mentioned

Compare Methods

	- Time
	- Relative Error

"""

__filename__ = "test_inv.py"
__author__ = "L.J. Brown"

# internal
import logging

# external
import numpy as np
import scipy.linalg

# my lib
from function_performance_timer import time_function
from inverse import inverse_solve

# initilize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#
# Test Settings
#

SIZES = [125, 250, 500, 1000] 	# each element is a size n for creating a random nxn matrix
MAX_VAL, MIN_VAL = 1000, -1000

#
# Helper Methods
#

def random_matrix(shape=(1,1), max_value=1, min_value=0):
	""" 
		Return random matrix.

		:param shape: integer tuple of size two containing dimensions of Matrix. ex: shape=(n,m).
		:param max_value: Maximum value an element of the generated matrix can take.
		:param min_value: Minimum value an element of the generated matrix can take.
		:returns: Randomly generated matrix.
	"""
	n, m = shape
	R = np.random.rand(n,m)*np.random.randint(low=min_value, high=max_value)
	return R

def random_vector(n, min_value=0, max_value=1):
	""" 
		Return random matrix.

		:param n: integer length containing number of elements for the generated vector.
		:param max_value: Maximum value an element of the generated vector can take.
		:param min_value: Minimum value an element of the generated vector can take.
		:returns: Randomly generated vector.
	"""
	x = np.random.rand(n)*np.random.randint(low=min_value, high=max_value)
	return x

def lu_solve(A,b,tol=10**(-14)):
	"""
		Scipy lu_solve wrapper. Solve for the vector x in the equation,

								Ax = b

		:param A: nxn non-singular matrix.
		:param b: vector of length n.
		:param tol: Defualt set to 10^(-14), consider values bellow this threshold to be zero.
		:returns: Solution vector x of length n.
	"""

	# LU decomposition -- raise ValueError for singular matrix A
	try:
		LU, piv = scipy.linalg.lu_factor(A)

		# enforce magnitude of diagonal values are above given tolernce (round off)
		for di in np.diag(LU):
			if abs(di) <= tol: raise ValueError

	except ValueError:
		logger.error("Error 'Singular Matrix' passed method: %s" % inverse.__name__)

	# Use decomposition to solve for x
	x = scipy.linalg.lu_solve((LU, piv), b)

	# return solution vector x
	return x

def vector_relative_error(x_true, x_comp):
	"""
		Return relative error between computed solution and true solution vectors.

					|| x_true - x_comp ||
					---------------------
						|| x_true ||

		:param x_true: True solution vector.
		:parama x_comp: Computed solution vector.
		:returns: Float representing the relative error.
	"""
	absolute_difference = np.absolute( x_true - x_comp ).sum(axis=0).sum()
	denominator = np.absolute( x_true ).sum(axis=0).sum()
	r_error = np.divide(absolute_difference,denominator)
	return r_error

#
# Run Tests 
#

if __name__ == "__main__":

	for n in SIZES:

		# generate random matrix A of size nxn
		A = random_matrix(shape=(n,n), min_value=MIN_VAL, max_value=MAX_VAL)

		# generate random solution vector x for : Ax = b
		x = random_vector(n, min_value=MIN_VAL, max_value=MAX_VAL)

		# compute b for : Ax = b
		b = A @ x

		#
		# 			Solve System Using Two Different Methods
		#
		#
		# 	Method 1) Compute the inverse matrix Ai and solve : 
		#						
		#						x = Ai @ b
		#
		#   Method 2) Perform LU decomposition and solve two equations 
		#			  (with forward and backward substitution):
		#
		#						(1) Ly = b,
		#						(2) Ux = y
		#									
		#					* note: Permuation matrices not mentioned

		# Time methods
		time_1, x1 = time_function(inverse_solve, np.copy(A), b, return_function_output=True)
		time_2, x2 = time_function(lu_solve, np.copy(A), b, return_function_output=True)

		# Compute relative errors for each method
		r_error_1 = vector_relative_error(x, x1)
		r_error_2 = vector_relative_error(x, x2)

		# display runtime and relative error of both methods for size n
		logger.info("Size (%sx%s):" % (n,n))
		logger.info("\tInverse Solve: \t time: %s, \t relative error %s" % (time_1,r_error_1))
		logger.info("\tLU Solve: \t time: %s, \t relative error %s" % (time_2,r_error_2))
