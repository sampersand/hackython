from overload import *
from types import FunctionType

@overload
def printargs(func):
	return printargs(func, '{', ', ', '}')
@overload
def printargs(func, start, sep, end):
	def pr(*args, **kwargs):
		print(start,func.__qualname__, args, kwargs, end, sep = sep)
		return func(*args, **kwargs)
	return pr
@overload
def printargs(a, b, start = '{', sep = ', ', end = '}'):
	return lambda func: printargs(func = func, start = start, sep = sep,end = end)

# @printargs(1, 2, '\n--','\n', '--\n')
@printargs
def domath(a, b, c):
	return a * b ** c

domath(1,2,3)
# class intv2(int):
	# @overload
	# def __add__(self, val):
	# 	return intv2(super().__add__(val))
	# @overload
	# def __add__(self, ):
	# 	return 
# foo = intv2(9)
# print(foo + 1)