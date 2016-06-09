from overload import *
from types import MethodType as mt
def q(s, v):
	print(s, v)
	s.v += v
class tc():
	def __init__(s, v): s.v = v
	def __repr__(s): return type(s).__qualname__ + '({})'.format(s.v)
	def a(s, v):
		s.v += v
	def a1(s, v1, v2):
		s.v += v1 * v2
t = tc(1)
tc.a2 = mt(q, t)
print(tc.a2(9))
print(t.v)






































# @overload
# def foo(a, b, c):
# 	print('foo(a,b): %s'%locals())
# def fooa(a, *args):
# 	print('no')
# foo = overload(fooa, 'foo', 0)

# foo(1, 2, 3)












