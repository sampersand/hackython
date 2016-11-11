from inspect import stack
def from_stack(name, stack_level = -1):
	frame = stack()[stack_level]
	fr = frame.frame
	if name in fr.f_locals:
		return fr.f_locals[name]
	if name in fr.f_globals:
		return fr.f_globals[name]
	raise NameError("{} doesn't exist at stack frame {}".format(name, frame))