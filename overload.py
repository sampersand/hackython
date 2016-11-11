import types, typing, inspect
#####
#I've decided that arguments that were optional in the main function are required in the helper ones.
#####

class _func_info():
	def __init__(self: __qualname__,
				 func: types.FunctionType) -> None:
		self.func = func
		fullargspec = inspect.getfullargspec(func)
		if not fullargspec.defaults:
			self.args, self.kwargs = tuple(fullargspec.args), {}
		else:
			self.args, self.kwargs = fullargspec.args[:len(fullargspec.defaults)],\
				dict(zip(fullargspec.args[-len(fullargspec.defaults):], fullargspec.defaults))
		self.varargs = fullargspec.varargs
		self.varkw = fullargspec.varkw
		self.kwargsonly = fullargspec.kwonlydefaults or {}
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
		varargs = len(args) > len(self.args) + len(self.kwargs) and not self.varargs
		varargs_that_are_kwargs = any(arg not in kwargskeys for arg in self.args[len(args):])
		kwargs = kwargskeys - self.kwargskeys - frozenset(self.args[len(args):]) - self.kwargsonlykeys and not self.varkw
		if True: #annotations
			# print(kwargs)
			annotations = False
			# quit()
		else:
			annotations = False
		return not(varargs or varargs_that_are_kwargs or kwargs) # Section 3
	def __repr__(self: __qualname__) -> str:
		return '{}({})'.format(type(self).__qualname__, self.func)
	def __str__(self: __qualname__) -> str:
		return str(list(self))

class overloaded_function(dict):
	def __new__(self: __qualname__,
				func: types.FunctionType,
				check_for_duplicates: bool,
				smart: bool) -> __qualname__:
		return super().__new__(self, {})
	def __init__(self: __qualname__,
				 func: types.FunctionType,
				 check_for_duplicates: bool,
				 smart: bool) -> None:
		super().__init__({})
		self + func
		self.check_for_duplicates = check_for_duplicates
		self.smart = smart

	def __add__(self: __qualname__,
				func: types.FunctionType) -> __qualname__:
		finfo = _func_info(func)
		if finfo in self:
			print("Warning: function '{}' already exists!".format(finfo))
		self[finfo] = finfo
		return self
	def _smartcall(self: __qualname__,
				   matched: list,
				   args: tuple,
				   kwargs: dict) -> typing.Any:
		if len(matched) == 1:
			return matched[0].func(*args, **kwargs)
		'''
		annotations beyond here
		'''
		from hackython import verify
		matched_annotations = []
		for func in matched:
			try:
				verify(func = func.func, shouldwarn = False)(*args, **kwargs)
				matched_annotations.append(func)
			except TypeError as e:
				pass
		if len(matched_annotations) == 1:
			return matched_annotations[0].func(*args, **kwargs)
		raise SyntaxError("Not currently known how to smartcall args={}, kwargs = {} for functions:\n{}".format(args, kwargs, matched))

	def __call__(self: __qualname__,
				*args: tuple,
			   **kwargs: dict) -> typing.Any:
		lastmatched = []
		kwargskeys = frozenset(kwargs)
		for finfo in self.values():
			if finfo._matches(args, kwargs, kwargskeys):
				if lastmatched and not self.smart:
					raise SyntaxError("Two possibilities for the given args: args={}, kwargs = {}".format(args, kwargs))
				lastmatched.append(finfo)
				if not self.check_for_duplicates:
					return lastmatched[0].func(*args, **kwargs)
		if not lastmatched:
			raise SyntaxError("No function found for the arguments: args={}, kwargs={}".format(args, kwargs))
		return self._smartcall(lastmatched, args, kwargs)
		# return lastmatched.func(*args, **kwargs)

	def __str__(self: __qualname__) -> str:
		return '{{}}'.format(', '.join(':'.join((str(k), str(v))) for k, v in self.items()))

def _getfunc(func: types.FunctionType,
			 name: str,
			 check_for_duplicates: bool,
			 locals: dict,
			 delete: bool,
			 smart: bool) -> types.FunctionType:
	if name in locals and (isinstance(locals[name], overloaded_function)
									or isinstance(locals[name], types.FunctionType) and
									hasattr(locals[name], '__func__')):
		if hasattr(locals[name], '__func__'):
			locals[name] = locals[name].__func__
		if check_for_duplicates != locals[name].check_for_duplicates:
			locals[name].check_for_duplicates = check_for_duplicates
		if smart != locals[name].smart:
			locals[name].smart = smart
		ret = locals[name] + func
		if delete:
			del locals[func.__name__]
	else:
		ret = overloaded_function(func, check_for_duplicates, smart)
	def call(*args, **kwargs):
		return ret(*args, **kwargs)
	call.__func__ = ret
	return call

def overload(func: types.FunctionType = None,
			 name: str = None,
			 delete: bool = True,
			 smart: bool = True,
			 check_for_duplicates: bool = True,
			 _locals: dict = None) -> types.FunctionType:
	"""
	Enables `overloading` a function. 
	func (default=None) :: If None, the program will check for any other functions with the same name as the function
		that this is being called on, and overload those. Specifying `func` will only overload the passed function. Note that
		`func` has to be of type `types.FunctionType` or `overloaded_function`.
	name (default=None) :: If None, then `func.__qualname__` will be used to determine what to overload.
		Otherwise, name will be.
	check_for_duplicates (default=True) :: If False, the program will call and return the first valid function it finds.
		If True, then it will continue searching until there are no more valid functions, or it finds another match.
		In the case of another match, a SyntaxError will be thrown.
	_locals (default=None) :: If set to None, the locals where overload was called will be used
		(e.g. the locals at `foo = overload()`); Otherwise, _locals will be used.
	delete (default=True) :: If True, and `func.__name__` isn't equal to `name`, then func will be deleted
		out of `_locals`.
	"""
	_locals = _locals or inspect.currentframe().f_back.f_locals
	if isinstance(func, types.FunctionType) and hasattr(func, '__func__'):
		func = func.__func__
	if isinstance(func, (types.FunctionType, overloaded_function)):
		return _getfunc(func, name or func.__name__, check_for_duplicates, _locals, delete, smart)
	return lambda func: _getfunc(func, name or func.__name__, check_for_duplicates, _locals, delete, smart)

__all__ = ['overload']























