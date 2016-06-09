from overload import *
from types import FunctionType


# @overload
# def bar(): return (9)

class testclass():
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		return type(self).__qualname__ + '({})'.format(self.val)

	@overload
	def add(self, val):
		self.val += val
		return self
	print('@')
	@overload
	def add(self, val1, val2):
		self.val += val1 * val2
		return self
foo = testclass(9)
print(foo.add(3,4))
