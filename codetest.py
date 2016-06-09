from overload
if __name__ == '__main__':
	class testclass():
		def __init__(self, v):
			self.v = v
		@overload
		def add(self, v):
			self.v += v
		def add1(self, v1, v2):
			self.v += v1 * v2
		add = overload(add1, 'add')
	t = testclass(1)
	print(t.add(9))
	print(t.v)
	# @overload
	# def foo(a, b, c):
	# 	print('foo(a,b): %s'%locals())
	# def fooa(a, *args):
	# 	print('no')
	# foo = overload(fooa, 'foo', 0)

	# foo(1, 2, 3)












