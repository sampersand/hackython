import functiming

from overload import *
# help(functiming)
@overload(check_for_duplicates = 0)
def foo():
	return dict()

print(functiming.compare(lambda: dict(), foo))
# print(functiming.compare(lambda: dict(), overload(lambda: dict(), check_for_duplicates = 0)))