import types
import inspect
class func_info():
	def __init__(self, func):
		#_ignore is kwonlyargs.values()
		self.func = func
		args, self.var_arg, self.kw_arg, defaults, _ignore, self.kwonlyargs, self.annot = inspect.getfullargspec(self.func)
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

	def consolidate(self, args):
		""" warning: this modifies args"""
		pargs = []
		if '$pargs' in args:
			pargs = args['$pargs']
			if '$var_arg' in args:
				pargs.append(args['$var_arg'])
				del args['$var_arg']
			del args['$pargs']
		if '$kw_args' in args:
			args.update(args['$kw_args'])
			del args['$kw_args']
		return (pargs, args)
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
"""
name(v1, v2, v3, kw=1, kw=2, kw=3, *args, kwo=4, kwo=5, **kwargs)
name(args, kwargs, *args, kwoargs, **kwags)
"""
		# """ first, update any of the things which are keyword only arguments. """
		# for kwonlyarg, value in self.kwonlyargs.items():
		# 	if kwonlyarg not in args:
		# 		args[kwonlyarg] = value
		# """ next, find any passed kwarg that """
		# for pargpos in range(len(pargs)): #first, put all the guarenteed thigns in
		# 	if pargpos > len(self.pargs) - 1: # if the current number is too far, then put it into 
		# 		if not self.var_arg: #means too many arguments
		# 			return False 
		# 		if '$var_arg' not in args:
		# 			args['$var_arg'] = []
		# 		args['$var_arg'].append(pargs[pargpos])
		# 	args[self.pargs[pargpos]] = pargs[pargpos]
		# print(args)
		# for parg in self.pargs

class overloaded_function(dict):
	def __new__(self): return super().__new__(self, {})
	def __init__(self):
		super().__init__({})
		self.name = None
	def __add__(self, other):
		if not isinstance(other, types.FunctionType):
			return NotImplemented
		finfo = func_info(other)
		if self.name == None:
			self.name = other.__qualname__
		elif other.__qualname__ != self.name:
			raise TypeError("This class only accepts functions named '{}', not '{}'".format(self.name, other.__qualname__))
		self[tuple(finfo)] = finfo
		return self
	def __call__(self, *pargs, **kwargs):
		for ftuple, finfo in self.items():
			match = finfo.matches(pargs, kwargs)
			if match != False:
				consolidated = finfo.consolidate(match[0])
				return match[1](*pargs, **kwargs)#*consolidated[0], **consolidated[1])
		raise TypeError('Unable to find a valid function given the given arguments. pargs: {}, kwargs: {}'.format(pargs, kwargs))
def overload(ovlfunc = None):
	if ovlfunc == None: ovlfunc = overloaded_function()
	def obtainfunc(passedfunc): return ovlfunc + passedfunc
	return obtainfunc

@overload()
# def foo(a): # foo(x) or foo(a = x)
def foo(a, b, c, d = 1, e = 2, f = 3, *pargs, g = 4, h = 5, i = 6, **kwargs): # foo(x) or foo(a = x)
	return 'foo*: ' + ', '.join(str(x) for x in [a, b, c, d, e, f, pargs, g, h, i, kwargs])

@overload(foo)
def foo(a, b = 1, c = 2): # foo(x, b = y)
	pass

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












