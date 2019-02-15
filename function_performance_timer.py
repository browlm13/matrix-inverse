#!/usr/bin/env

"""
Timer - function performance evaulation
[Notes]:
	Deprecated of time.time() since version 3.3: 
		Behaviour platform specific.
		usage:
			time.process_time() # process-wide timing
			time.perf_counter() # system-wide timing
		for well defined behaviour.
	More detailed specs can be found using profile in standard lib:
		usage: 
			import profile
			profile.run('func()')
"""

__filename__ = "function_performance_timer.py"
__author__ = "L.J. Brown"

import time

# time function duration and return time in milliseconds
def time_function( function, *args, return_function_output=False ):

	#time function
	start = time.time()
	function_output = function(*args)
	end = time.time()

	#time in milliseconds
	ex_duration = (end-start) * 1000.0

	if return_function_output:
		return ex_duration, function_output

	return ex_duration

# time function n times return average in milliseconds
def average_runtime( n, function, *args ):

	#function trials
	runtimes = []
	for i in range(n): 
		runtimes.append( time_function(function,*args) )

	#average duration in milliseconds
	avg = sum(runtimes)/n
	return avg

if __name__ == '__main__':

    #
    # example usage
    #

    # output
    header_string = """
    \n     Demonstrating methods in timer module...
   	\n\tRunning test on dummy function.
   	(Approximation of the number e)
   	"""
    print(header_string)

    # define test function
    from math import factorial
    e_approx = lambda n: sum([ 1/factorial(i) for i in range(0, n) ]) 

    # time function one trial
    print("Running test on single execution... ")
    n_taylor_terms = 10**3
    single_execution_time, results = time_function( e_approx, n_taylor_terms, return_function_output=True )
    print("Single Execution Time: %s milliseconds" % single_execution_time )

    # time function average over 4 trials trial
    print("\nRunning average runtime test... ")
    num_trials = 4
    average_execution_time = average_runtime( num_trials, e_approx, n_taylor_terms )
    print("Average Execution Time (%s trials): %s milliseconds" % ( num_trials, average_execution_time ) )

    # output dummy results
    print("\nApproximation of e: %s\n\n\t\tEnd of script.\n" % results)
