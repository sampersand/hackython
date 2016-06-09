from types import FunctionType
import inspect
"""
I've decided that arguments that were optional in the main function are required in the helper ones.
"""
class _func_info():
	def __init__(self, func):
		self.func = func
		self.fullargspec = inspect.getfullargspec(func)
		if not self.fullargspec.defaults: self.args, self.kwargs = tuple(self.fullargspec.args), {}
		else: self.args, self.kwargs = self.args[:len(defaults)], dict(zip(self.args[-len(defaults):], defaults))
		self.varargs = self.fullargspec.varargs
		self.varkw = self.fullargspec.varkw
		self.kwargsonly = self.fullargspec.kwonlydefaults or {}
		self.kwargskeys = frozenset(self.kwargs)
		self.kwargsonlykeys = frozenset(self.kwargsonly)
	
	def __hash__(self):
		#kwonly can be frozenset because only membership is needed
		return hash((self.args, self.kwargskeys, self.varargs,
					self.varkw, self.kwargsonlykeys)) 
	def matches(self, args, kwargs):
		return self.matches(args, kwargs, frozenset(kwargs))
	def _matches(self, args, kwargs, kwargskeys):
		"""
		imagine you have this function:
			def funcname(p1, p2, p3, kw1=..., kw2=..., kw3=..., *agss, kwo1=..., kwo2=..., kwo3=..., **kwargs)
		you can call it like such: 
			funcname(..., ..., ...)
			funcname(..., ..., p3 = ...)
			funcname(..., p2 = ..., p3 = ...)
			etc
		--
		Section 1:
		First, to check to see if the amount of passed args is larger than the amount of the function's args and kwargs
		combined, and that there is no varpos (ie `*args`). If that is true, than its obviously not a fit.
		--
		Section 2:
		Check that all the function's positinal arguments exist, either by being passed as `args` or being specified
		in `kwargs`.
		--
		Section 3:
		Check the passed kwargs, and see if any of them aren't defnied, and varkw isnt defined.
		"""
		print(args, kwargs)
		print(self.args, self.kwargs)

		# Section 1: checking length of passed args
		if len(args) > len(self.args) + len(self.kwargs) and not self.varargs:
			return False
		
		# Section 2: positional arguments
		positional_kwargs = self.args[len(args):]
		for arg in positional_kwargs:
			if arg not in kwargskeys: # aka, if the positional argument isnt at the right spot
				return False

		# Section 3: kwargs
		if not self.varkw:
			if kwargskeys - self.kwargskeys - frozenset(positional_kwargs) - self.kwargsonlykeys: #maybe break into multiple if statements
				# aka, if 
				return False
		return True


class _overloaded_function(dict):
	def __new__(self, func, check_for_duplicates):
		return super().__new__(self, {})
	def __init__(self, func, check_for_duplicates):
		super().__init__({})
		self + func
		self.check_for_duplicates = check_for_duplicates
	def __add__(self, func):
		finfo = _func_info(func)
		if finfo in self:
			print("Warning: function '{}' already exists!".format(finfo))
		self[finfo] = finfo
		return self
	def __call__(self, *args, **kwargs):
		lastmatched = None
		kwargskeys = frozenset(kwargs)
		for finfo in self.values():
			if finfo._matches(args, kwargs, kwargskeys):
				if lastmatched:
					raise SyntaxError("Two possibilities for the given args")
				lastmatched = finfo
				if not self.check_for_duplicates:
					break
		if lastmatched == None:
			raise SyntaxError("No function found for the arguments: args={}, kwargs={}".format(args, kwargs))
		return lastmatched.func(*args, **kwargs)

def _getfunc(func, check_for_duplicates):
	locals = inspect.currentframe().f_back.f_back.f_locals
	if func.__qualname__ in locals and isinstance(locals[func.__qualname__], _overloaded_function):
		return locals[func.__qualname__] + func
	return _overloaded_function(func, check_for_duplicates)

def overload(func = None, check_for_duplicates = True):
	if isinstance(func, FunctionType):
		return _getfunc(func, check_for_duplicates)
	return lambda func: _getfunc(func, check_for_duplicates)

@overload
def foo(a, b, c):
	print('foo(a,b): %s'%locals())
@overload
def foo(a, *args):
	print('no')
foo(1, 2, c= 3,)
# # def printme(parg1, parg2, *pargs, kwonlyarg1 = 4, kwonlyarg2 = 5, **kwargs):
# def printme(parg1, parg2, parg3, kwarg1 = 1, kwarg2 = 2, kwarg3 = 3, *pargs, kwonlyarg1 = 4, kwonlyarg2 = 5, kwonlyarg3 = 6, **kwargs):
# 	print('printme(alot):' + str(locals()))

# @overload
# def printme(*args):
# 	print('printme(*args):' + str(args))