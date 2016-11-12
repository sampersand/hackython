from types import ModuleType
from sys import modules
from .from_stack import from_stack
class ModuleAttribute():
	__slots__ = ('__obj__',)

	def __init__(self, obj):
		self.__obj__ = obj

	def __get__(self, instance, parent):
		return self.__obj__

def _create_module():
	return type('MutableModule', (ModuleType,), {'__doc__':
        '''
        Base class for custom modules.

        Each MutableModule is a unique class, which allows them to be modified
        without affecting other instances

        Note that this means that they will not be the same object:
        	import module_a
        	import module_a
        	assert type(module_a) is type(module_b) # good so far

        	convert_module(module_a) # these are done in-place
        	convert_module(module_b)

        	assert type(module_a) is type(module_b) # will fail
        '''}) 
def convert_module(module = None):
	''' Converts a module into a MutableModule IN PLACE.

	All _MutableModuleTypes objects will be "promoted" from module attributes to
	the module class's attributes
	Arguments:
		module -- The module to convert.
		            None       - The module will be automatically determined
		                         (unstable) (default)
		            str        - Module will be obtained from sys.modules. 
		            ModuleType - Used directly
	Returns:
		None, as the operation is done in place.
	Throws:
		TypeError -- If a non-None/str/ModuleType is passed for module.
		NameError -- If the moudle with the specified name cannot be found in 
		             sys.modules
	'''
	if module is None:
		module = current_module(stack_level = 3)
	if isinstance(module, str):
		module = get_module(module)

	if not isinstance(module, ModuleType):
		raise TypeError('Expected ModuleType, not {}'.format(mcls))

	# a copy is used so the changes to this MutableModule don't affect others.
	mcls = _create_module()

	assert issubclass(mcls, ModuleType), mcls

	for name, value in dict(module.__dict__).items():
		if isinstance(value, ModuleAttribute):
			setattr(mcls, name, value.__get__(module, type(module)))
			delattr(module, name) #removes them from module

	module.__class__ = mcls

def get_module(name):
	if name not in modules:
		raise NameError(name)
	return modules[name]

def current_module(*, stack_level = 2):
	name = from_stack('__name__', stack_level)
	assert name, name
	return get_module(name)

cm = current_module
mattr = ModuleAttribute
__all__ = ('ModuleAttribute', 'mattr',
           'convert_module', 'current_module', 'get_module', 'cm')












