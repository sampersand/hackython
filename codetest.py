from overload import *
from types import MethodType
from inspect import currentframe, stack
def _overload(func):
	def call(self, *args, **kwargs):
		return overload(func).__call__(*([self]+list(args)), **kwargs)
	return call
class testclass():
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		return type(self).__qualname__ + '({})'.format(self.val)
	@_overload
	def add(self, val):
		self.val += val
		return self
	# @_overload
	# def add1(self, val1, val2):
	# 	self.val += val1 * val2
@_overload
def bar(self, val):
	return (self, val, 9)
print(bar(1,2))
foo = testclass(val = 9)
print(foo.add(3))

# def addnotmethod(self, val):
# 	self.val += val
# 	return self.val
# cli1 = testclass(1)
# cli2 = testclass(100)
# cli1.addv2 = MethodType(addnotmethod, cli1)
# cli2.addv2 = MethodType(addnotmethod, cli2)
# print(MethodType(testclass.add, cli1) == cli1.add)
# print(cli1.addv2(2), 'cli1')
# print(cli2.addv2(3), 'cli2')
# print(cli1.v, cli2.v)
