from time import clock
def compare(func1, func2, trials = 100000):
	def timefunction(f):
		for x in range(trials):
			c = clock(); f()
			yield clock() - c
	return sum(timefunction(func1)) / sum(timefunction(func2))