from overload import *
from types import MethodType
def addnotmethod(self, v):
	self.v += v
	return self.v
class clname():
	def __init__(self, v):
		self.v = v
	def __repr__(self):
		return type(self).__qualname__ + '({})'.format(self.v)
	# @overload
	def add(self, v):
		self.v += v
	# @overload
	# def add1(self, v1, v2):
	# 	self.v += v1 * v2
cli1 = clname(1)
cli2 = clname(100)
print(type(clname.add), t)
cli1.addv2 = MethodType(addnotmethod, cli1)
print(cli1.addv2(2), 'cli1')
print(cli2.addv2(3), 'cli2')
print(cli1.v, cli2.v)






































# @overload
# def foo(a, b, c):
# 	print('foo(a,b): %s'%locals())
# def fooa(a, *args):
# 	print('no')
# foo = overload(fooa, 'foo', 0)

# foo(1, 2, 3)












