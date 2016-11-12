import sys
import typing
from types import ModuleType

from .from_stack import from_stack

class ModuleAttribute():
	''' The class representing a Module Attribute
	
	This is meant to be used as a decorator inside modules.	Examples:

	# in a file called 'spam'

		@ModuleAttribute
		def __str__(self):
			return '<my module named {!r}>'.format(self)

		_do_i_want_ham = False

		@ModuleAttribute
		@property
		def ham(self):
			return _do_i_want_ham

		@ModuleAttribute
		@ham.setter
		def ham(self, doiwant):
			self._do_i_want_ham = doiwant

		convert_module(current_module())

	# in a file called 'eggs'
		
		import spam
		print(spam)
			# <my module named 'spam'>

		print(spam.ham)
			# False
		print(spam._do_i_want_ham)
			# False
		
		spam.ham = True

		print(spam.ham)
			# True
		print(spam._do_i_want_ham)
			# True
	'''
	__slots__ = ('__obj__',)

	def __init__(self, obj: typing.Any) -> None:
		''' Initialize self by setting 'self.__obj__' to 'obj'
		'''
		self.__obj__ = obj

	def __get__(self, instance: typing.Type,
					  parent: typing.Type) -> typing.Any:
		''' Return 'self.__obj__'.
		
		This is used internally to just obtain the object - any __get__,
		__set__, or __delete__ methods should be defined as in __obj__, not
		this class.
		'''
		return self.__obj__


	def __getattr__(self, attr: typing.Any) -> typing.Any:
		''' Reroute all unknown attributes to self.__obj__ '''
		return getattr(self.__obj__, attr)

def _new_module_type() -> ModuleType:
	''' **Internal** Creates a unique ModuleType subclass called MutableModule.
	
	The default properties of each MutableModule are identical, but their memory
	location isn't. This is to allow for modification of one instance without
	disturbing the others.

	Returns:
		A new subclass of ModuleType, called MutableModule
	'''
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

def convert_module(module: ModuleType) -> None:
	''' Converts a module into a MutableModule IN PLACE.

	All ModuleAttribute objects will be "promoted" from module attributes to
	the module class's attributes.

	Arguments:
		module -- The module to convert. (expected type: ModuleType)
	Returns:
		None, as the operation is done in place.
	Throws:
		TypeError -- If a ModuleType is passed for module.

	'''
	if not isinstance(module, ModuleType):
		raise TypeError('Expected ModuleType, not {}'.format(mcls))

	# a copy is used so the changes to this MutableModule don't affect others.
	mcls = _new_module_type()

	assert issubclass(mcls, ModuleType), mcls

	for name, value in dict(module.__dict__).items():
		if isinstance(value, ModuleAttribute):
			setattr(mcls, name, value.__get__(module, type(module)))
			delattr(module, name) #removes them from module

	module.__class__ = mcls

def get_module(name: str) -> ModuleType:
	'''	Gets the module with the specified name.
	
	This is done by looking at sys.modules

	Arguments:
		name      -- The name of the desired module

	Returns:
		The module corresponding to 'name' in sys.modules.

	Throws:
		KeyError -- If the moudle with the specified name cannot be found in 
		            sys.modules
	'''
	if name not in sys.modules:
		raise KeyError(name) # preemptive raise
	return sys.modules[name]

def current_module(*, stack_level: int = 2) -> ModuleType:
	''' Obtains the module from which this function was called.

	This function obtains the '__name__' attribtue from the specified
	stack_level, then passes it to get_module

	Arguments:
		stack_level -- The amount of stackframes to go up to find '__name__'. 
		               Defaults to the frame where current_module was called
		               (default: 2) (expected type: int)
	Returns:
		(see get_module)
		The result of 'get_module(name)' 
	Throws:
		NameError  -- If '__name__' cannot be found in the specified stackfrme.
		ValueError -- if 'stack_level' is not an int.

	'''
	name = from_stack('__name__', stack_level)
	assert name, name
	return get_module(name) # shouldn't crash, cant test w/o a try/except

cm = current_module
mattr = ModuleAttribute
__all__ = ('mattr', 'cm', 'convert_module',
           'get_module', 'current_module', 'ModuleAttribute')












