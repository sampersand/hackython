from inspect import stack
def from_stack(name, stack_level = -1, *, _locals = True, _globals = True):
	assert _locals or _globals #not required, but no reason for them not to be.

	frame = stack()[stack_level]
	fr = frame.frame

	if _locals and name in fr.f_locals:
		return fr.f_locals[name]
	if _globals and name in fr.f_globals:
		return fr.f_globals[name]
	raise NameError("{} doesn't exist at stack frame {}".format(name, frame))
__all__ = 'from_stack', 