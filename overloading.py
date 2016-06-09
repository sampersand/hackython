import inspect
class func_info():
	def __init__(self, func):
		self.func = func
		args, self.var_arg, self.kw_arg, defaults, _, self.kwonlyargs, _ = inspect.getfullargspec(self.func)
		if not self.kwonlyargs:
			self.kwonlyargs = {}
		if not defaults:
			self.kwargs = ()
			self.kwargs_defaults = {}
			self.pargs = tuple(args)
		else:
			self.kwargs = tuple(args[-len(defaults):])
			self.kwargs_defaults = {self.kwargs[d] : defaults[d] for d in range(len(defaults))}
			self.pargs = tuple(args[:len(args) - len(self.kwargs)])
	def __iter__(self):
		return iter((self.pargs, tuple(self.kwargs), self.var_arg, self.kw_arg))

	def matches(self, pargs, kwargs):
		if len(pargs) < len(self.pargs):
			return False
		args = self.kwargs_defaults.copy()
		args.update(self.kwonlyargs)
		""" first, go thru passed pargs, and match them up."""
		for pos in range(len(pargs)):
			if pos < len(self.pargs):
				if '$pargs' not in args:
					args['$pargs'] = []
				args['$pargs'].append(pargs[pos])
			else:
				if pos < len(self.pargs) + len(self.kwargs):
					args[self.kwargs[pos - len(self.pargs)]] = pargs[pos]
				elif self.var_arg:
					if '$var_arg' not in args:
						args['$var_arg'] = []
					args['$var_arg'].append(pargs[pos])
				else:
					return False #aka too many pargs

		""" Then go and look at kwargs, and match them up"""
		for kwarg, val in kwargs.items():
			if kwarg not in args:
				if self.kw_arg:
					if '$kw_arg' not in args:
						args['$kw_arg'] = {}
					args['$kw_arg'][kwarg] = val
				else:
					return False
			else:
				args[kwarg] = val
		return args, self.func

class func_info_fast():
	def __init__(self, func):
		self.func = func
		args, self.var_arg, self.kw_arg, defaults, _, _, _ = inspect.getfullargspec(self.func)
		args, defaults = tuple(args), defaults or ()
		self.kwargs = args[-len(defaults):]
		self.pargs = args[:len(args) - len(self.kwargs)]

	def __iter__(self):
		return iter((self.pargs, self.kwargs, self.var_arg, self.kw_arg))

		def matches(self, pargs, kwargs): return len(pargs) >= len(self.pargs) and (self.var_arg or len(pargs) <= len(self.pargs) + len(self.kwargs)) and (self.kw_arg or all(kwarg in self.kwargs for kwarg in kwargs)) and self.func

class overloaded_function(dict):
	def __new__(self, enforce): return super().__new__(self, {})
	def __init__(self, enforce):
		super().__init__({})
		self.enforce = enforce
	def __add__(self, other):
		finfo = self.enforce and func_info(other) or func_info_fast(other)
		self[tuple(finfo)] = finfo
		return self
	def __call__(self, *pargs, **kwargs):
		matches = []
		for ftuple, finfo in self.items():
			match = finfo.matches(pargs, kwargs)
			if match != False:
				if not self.enforce:
					return match(*pargs, **kwargs)
				matches.append(match)
		if len(matches) == 0:
			raise TypeError('Unable to find a valid function given the given arguments. pargs: {}, kwargs: {}'.format(pargs, kwargs))
		"""

		"""
		print(matches)
def overload(ovlfunc = None, enforce = True):
	def getfunc(func):
		return (ovlfunc or overloaded_function(enforce)) + func
	return getfunc

__all__ = ['overload']
# @overload(enforce = True)
# # def foo(a): # foo(x) or foo(a = x)
# def foo(a, b, c, d = 1, e = 2, f = 3, *pargs, g = 4, h = 5, i = 6, **kwargs): # foo(x) or foo(a = x)
# 	return 'foo*: ' + ', '.join(str(x) for x in [a, b, c, d, e, f, pargs, g, h, i, kwargs])

# @overload(foo)
# def foo(a, b, c = 1, d = 2): # foo(x, b = y)
# 	return 'fooabcd: ' + str(a) + str(b) + str(c) + str(d)

# @overload(foo)
# def foo(a, b = 1): # foo(x, b = y)
# 	return 'fooab=:%s, %s' % (a, b)
# @overload(foo)
# def foo(a, b): # foo(x, y)
# 	return 'fooab:%s, %s' % (a, b)

# @overload(foo)
# def foo(*args, n = 1): # foo(x, y, z, ..., n = w)
# 	return 'foo*:' + str(args)
# @overload(foo)
# def foo(n, **kwargs): # foo(w, a = x, b = y, c = z, ...)
# 	return 'foo**:' + str(kwargs)



# print(foo(9, 8, 7, 6))








