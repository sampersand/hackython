import re
import types
try:
	from warnings import warn
except ImportError as e:
	print("Warning: Cannot import the 'warn' function; defaulting to raising Exceptions. Cause:", e)


def verify(func = None, shouldwarn = 'warn' in globals(), allowexprs = True, allowstrs = True):
	""" if allowstrs, the __qualname__ has to match exactuly"""
	if func == None:
		return lambda pfunc: verify(pfunc, shouldwarn, allowexprs, allowstrs)

	if type(func) != types.FunctionType:
		return lambda pfunc: verify(pfunc, shouldwarn = func, allowexprs = shouldwarn, allowstrs = allowexprs)

	def _alert(msg):
		if shouldwarn:
			warn(msg, RuntimeWarning, stacklevel = 3)
		else:
			raise TypeError(msg)

	def _check_arg(passedarg, annotation):
		if allowexprs and isinstance(annotation, types.FunctionType):
			return annotation(passedarg)
		if isinstance(annotation, (list, tuple, set)):
			for annot in annotation:
				if _check_arg(passedarg, annot):
					return True
			return False
		if isinstance(annotation, str):
			if not allowstrs:
				raise ValueError("String expressions aren't allowed, however '{}' is a string!".format(annotation))
			return type(passedarg).__qualname__ == annotation
		return issubclass(type(passedarg), annotation)

	def _check_function(*args, **kwargs):
		if not hasattr(func, '__annotations__'):
			return func(*args, **kwargs)
		annot = func.__annotations__
		allargs = dict(zip(func.__code__.co_varnames, args))
		allargs.update(kwargs)
		for name, value in allargs.items(): #might wanna make this sorted
			if name in annot and not _check_arg(value, annot[name]):
				_alert("'{}' expected \"{}\" for variable '{}', not \"{}\" ({})".format(func.__name__, annot[name], name, value, type(value)))
		ret = func(*args, **kwargs)
		if 'return' in annot and not _check_arg(ret, annot['return']):
			_alert("Expected return value type of \"{}\" from '{}', not \"{}\" ({})".format(annot['return'], func.__name__, ret, type(ret)))
		return ret
	return _check_function

def test(arg):
	return 

@verify(True)
def testfunc(a: int, b: (int, bool, float), c:bool = False, d:dict = {}) -> str:
	return str(a * b)

print(testfunc(2, 3.4, c = 1j))













