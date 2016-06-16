import functiming

from overload import *
# help(functiming)
@overload(check_for_duplicates = 1)
def foo():
	return dict()

# print(foo.__call__())
print(functiming.compare(lambda: dict(), foo))
