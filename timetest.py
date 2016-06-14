from time import clock

def func1():
	['abcdefghijklmnopqrstuvwxyz'[i] for i in range(26)]# if i in {2,3,5,7,11,13,17,23}]
def func2():
	alpha = 'abcdefghijklmnopqrstuvwxyz'
	[alpha[i] for i in range(26)]# if i in {2,3,5,7,11,13,17,23}]

	
def timesforfunc(func, trials = 100000):
	for x in range(trials):
		c = clock(); func()
		yield clock() - c
def timefunc(func, trials = 100000):
	return sum(timesforfunc(func, trials))
def compare(func1, func2, trials = 100000):
	return timefunc(func1, trials) / timefunc(func2, trials)
if __name__ == '__main__':
	print(compare(func1, func2, int(1e5)))