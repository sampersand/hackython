import functiming

from .overload_fast import foverload
from .overload import overload
# help(functiming)
@foverload(_locals = locals())
def with_foverload():
	return dict()
@overload(_locals = locals())
def with_overload():
	return dict()
def without_foverload():
	return dict()

print(functiming.compare(with_foverload, with_overload))
