from types import FunctionType
import inspect
#####
#I've decided that arguments that were optional in the main function are required in the helper ones.
#####

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
	
	def __iter__(self):
		return iter((self.args, self.kwargskeys, self.varargs, self.varkw, self.kwargsonlykeys))
	def __hash__(self):
		#kwonly can be frozenset because only membership is needed
		return hash(iter(self)) 
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

		
		return not(len(args) > len(self.args) + len(self.kwargs) and not self.varargs or # Section 1
		   any(arg not in kwargskeys for arg in self.args[len(args):]) or # Section 2
		   kwargskeys - self.kwargskeys - frozenset(self.args[len(args):]) - self.kwargsonlykeys and not self.varkw) # Section 3
	def __repr__(self):
		return '_func_info({})'.format(self.func)
	def __str__(self):
		return str(list(self))

class overloaded_function(dict):
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
		print(self)
		lastmatched = None
		kwargskeys = frozenset(kwargs)
		for finfo in self.values():
			if finfo._matches(args, kwargs, kwargskeys):
				if lastmatched:
					raise SyntaxError("Two possibilities for the given args: args={}, kwargs = {}".format(args, kwargs))
				lastmatched = finfo
				if not self.check_for_duplicates:
					break
		if lastmatched == None:
			raise SyntaxError("No function found for the arguments: args={}, kwargs={}".format(args, kwargs))
		return lastmatched.func(*args, **kwargs)
	def __str__(self):
		return '{' + ', '.join(':'.join((str(k), str(v))) for k, v in self.items()) + '}'
def _getfunc(func, function_name, check_for_duplicates, locals):
	if function_name in locals and isinstance(locals[function_name], overloaded_function):
		return locals[function_name] + func
	return overloaded_function(func, check_for_duplicates)

def overload(func = None, function_name = None, check_for_duplicates = True, _locals = None):
	"""
	Enables `overloading` a function. 
	func (default=None) :: If None, the program will check for any other functions with the same name as the function
		that this is being called on, and overload those. Specifying `func` will only overload the passed function. Note that
		`func` has to be of type `types.FunctionType` or `overloaded_function`.
	function_name (default=None) :: If None, then `func.__qualname__` will be used to determine what to overload.
		Otherwise, function_name will be.
	check_for_duplicates (default=True) :: If False, the program will call and return the first valid function it finds.
		If True, then it will continue searching until there are no more valid functions, or it finds another match.
		In the case of another match, a SyntaxError will be thrown.
	_locals (default=None) :: If set to None, the locals where overload was called will be used
		(e.g. the locals at `foo = overload()`); Otherwise, _locals will be used.

	"""
	_locals = _locals or inspect.currentframe().f_back.f_locals
	if isinstance(func, (FunctionType, overloaded_function)):
		return _getfunc(func, function_name or func.__qualname__, check_for_duplicates, _locals)
	return lambda func: _getfunc(func, function_name or func.__qualname__, check_for_duplicates, _locals)

__all__ = ['overload', 'overloaded_function']

if __name__ == '__main__':
	class testclass():
		@overload
		def __init__(self, a):
			self.a = a
			self.b = None
		@overload
		def __init__(self, a, b):
			self.a = a
			self.b = b
	t = testclass(1)
	print(t.a)
	# @overload
	# def foo(a, b, c):
	# 	print('foo(a,b): %s'%locals())
	# @overload
	# def foo(a, *args):
	# 	print('no')
	# # foo(1, 2)
	# def foo(a, *args):
	# 	print(a, args)
	# foo(1, *args)












