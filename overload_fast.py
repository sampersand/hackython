import types, typing, inspect
#####
#I've decided that arguments that were optional in the main function are required in the helper ones.
#####

class _func_info():
	def __init__(self: __qualname__,
	             func: types.FunctionType) -> None:
		self.func = func
		args, self.varargs, self.varkw, defaults, _, kwargsonly, _ = inspect.getfullargspec(func)
		self.args = tuple(args)
		if defaults:
			self.args, self.kwargs = args[:len(defaults)], dict(zip(args[-len(defaults):], defaults))
		else:
			self.kwargs = {}
		self.kwargsonly = kwargsonly or {}
		self.kwargskeys = frozenset(self.kwargs)
		self.kwargsonlykeys = frozenset(self.kwargsonly)
	
	def __iter__(self: __qualname__) -> 'how to describe?':
		return iter((self.args, self.kwargskeys, self.varargs, self.varkw, self.kwargsonlykeys))

	def __hash__(self: __qualname__) -> int:
		return hash(iter(self))
	
	def _matches(self: __qualname__,
	             args: tuple,
	             kwargs: dict,
	             kwargskeys: frozenset) -> bool:
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
		return not(len(args) > len(self.args) + len(self.kwargs) and not self.varargs or
		any(arg not in kwargskeys for arg in self.args[len(args):]) or
		 kwargskeys - self.kwargskeys - frozenset(self.args[len(args):]) - self.kwargsonlykeys and not self.varkw)
	# def __repr__(self: __qualname__) -> str:
	# 	return '{}({})'.format(type(self).__qualname__, self.func)
	# def __str__(self: __qualname__) -> str:
	# 	return str(list(self))

class overloaded_function(dict):
	def __new__(self: __qualname__, func: types.FunctionType) -> __qualname__:
		return super().__new__(self, {})
	def __init__(self: __qualname__, func: types.FunctionType) -> None:
		super().__init__({})
		self += func

	def __iadd__(self: __qualname__, func: types.FunctionType) -> __qualname__:
		finfo = _func_info(func)
		self[finfo] = finfo
		del finfo
		return self

	def __call__(self: __qualname__,
				*args: tuple,
			   **kwargs: dict) -> typing.Any:
		kwargskeys = frozenset(kwargs)
		for finfo in self.values():
			if finfo._matches(args, kwargs, kwargskeys):
				return finfo.func(*args, **kwargs)
		raise SyntaxError("No function found for the arguments: args={}, kwargs={}".format(args, kwargs))

	# def __str__(self: __qualname__) -> str:
	# 	return '{{}}'.format(', '.join(':'.join((str(k), str(v))) for k, v in self.items()))

def _getfunc(func: types.FunctionType, name: str, locals: dict) -> types.FunctionType:
	if name in locals and (isinstance(locals[name], overloaded_function)
	                                or isinstance(locals[name], types.FunctionType) and
	                                hasattr(locals[name], '__func__')):
		if hasattr(locals[name], '__func__'):
			locals[name] = locals[name].__func__
		ret = locals[name] + func
	else:
		ret = overloaded_function(func)
	def call(*args, **kwargs):
		return ret(*args, **kwargs)
	call.__func__ = ret
	return call

def foverload(func: types.FunctionType = None, name: str = None, _locals: dict = None) -> types.FunctionType:
	"""
	Enables `overloading` a function. 
	func (default=None) :: If None, the program will check for any other functions with the same name as the function
		that this is being called on, and overload those. Specifying `func` will only overload the passed function. Note that
		`func` has to be of type `types.FunctionType` or `overloaded_function`.
	name (default=None) :: If None, then `func.__qualname__` will be used to determine what to overload.
		Otherwise, name will be.
	_locals (default=None) :: If set to None, the locals where overload was called will be used
		(e.g. the locals at `foo = overload()`); Otherwise, _locals will be used.
	"""
	if isinstance(func, types.FunctionType) and hasattr(func, '__func__'):
		func = func.__func__
	if isinstance(func, (types.FunctionType, overloaded_function)):
		return _getfunc(func, name or func.__name__, _locals or inspect.currentframe().f_back.f_locals)
	return lambda func: _getfunc(func, name or func.__name__, _locals or inspect.currentframe().f_back.f_locals)

__all__ = ['foverload', 'overloaded_function']























