from types import ModuleType

def convert_module(module):
	if not isinstance(module, ModuleType):
		raise TypeError('Expected ModuleType, not ' + str(module.__class__.__qualname__))

	return type(type(module))(module.__name__,
	                      module.__class__.__bases__,
	                      module.__dict__)()
class ModuleMethod(classmethod):
	pass
	# def __get__(self, instance, parent):
	# 	ret = super().__get__(instance, parent)
	# 	print(ret, 'ret')
	# 	print(dir(ret))
	# 	return ret













