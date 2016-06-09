from overload import *

class foo():
    @overload
    def __init__(self, a):
        self.__init__(a, 9)
    @overload
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __str__(self):
        return str(self.a) + ' ' + str(self.b)
print(foo(3))
quit()

@overload
def printargs(a, b, start = '{', sep = ', ', end = '}'):
	return lambda func: printargs(func = func, start = start, sep = sep,end = end)

@overload
def printargs(func):
	return printargs(func, '{', ', ', '}')

@overload
def printargs(func, start, sep, end):
	def pr(*args, **kwargs):
		print(start,func.__qualname__, args, kwargs, end, sep = sep)
		return func(*args, **kwargs)
	return pr

@printargs
def domath(a, b, c):
	return a * b ** c

def foo(a, *args):
	print(a, args)
foo.__call__({'a':'19', })
# domath(1,2,3)
# class intv2(int):
	# @overload
	# def __add__(self, val):
	# 	return intv2(super().__add__(val))
	# @overload
	# def __add__(self, ):
	# 	return 
# foo = intv2(9)
# print(foo + 1)








@overload
def foo(a, b): foo(a, b, 9)

@overload
def foo(a, b, c): print(a, b, c)

@overload
def foo(a): foo(a,6)

foo(3)

















