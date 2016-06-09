from time import clock

def func1():
	@overload
def func2():
	{1,2,3} 
	
def timesforfunc(func, trials = 100000):
	for x in range(trials):
		c = clock(); func()
		yield clock() - c
def timefunc(func, trials = 100000):
	return sum(timesforfunc(func, trials))
def compare(func1, func2, trials = 100000):
	return timefunc(func1, trials) / timefunc(func2, trials)
# print(timefunc(lambda: {1,2,3} - set()))
print(compare(func1, func2, int(1e5)))