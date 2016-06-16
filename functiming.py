from time import clock
from typing import Callable
from types import GeneratorType
__doc__ = """This module provides varius functions to determine the speed of functions

The functions to run time tests on should accept no arguments; the return value (if any) will be ignored.

Note: Run time is somewhat random by nature, as processes other than just Python may also be running at the runtime. 
	  Large trial amounts will minimize the impact this intrinsic randomness has.
"""

def times(func: Callable, trials: int = 100000) -> GeneratorType:
	"""A generator for the speed it takes for the function to run, where each yielded value is a single trial.

	func -- The function that will be called repeatedly, and whose run time will be yielded.
	trials -- The amount of times that `func` will be called.
	
	return -- The time it took for a single trial to take place.
	"""
	for x in range(trials):
		c = clock(); func()
		yield clock() - c
def average_time(func: Callable, trials: int = 100000) -> float:
	"""Finds the average time it takes for a function to run.

	func -- The function that will be called repeatedly, and the resulting times will be averaged
	trials -- The amount of times that `func` will be called.

	return -- The average time it took for the function to run.
	"""
	return sum(times(func, trials)) / trials

def compare(func1: Callable, func2: Callable, trials: int = 100000) -> float:
	"""Compares two functions together, and returns a proportion of the two's average times.
	
	func1 -- The first function that will be run, and whose times will be averaged.
	func2 -- The second function that will be run, and whose times will be averaged.
	trials -- The amount of times that the functions will be run.
	
	return -- 
	"""
	return average_time(func1, trials) / average_time(func2, trials)

__all__ = ['times', 'average_time', 'compare']
