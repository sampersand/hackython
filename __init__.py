from .overload import *
from .switch import *
from .functiming import *
from .module_hacks import *
modulemethod = ModuleMethod
__all__ = ('overload',
		   'switch', 'case', 'default', 'fallthrough', 'cont', 'ft', 
           'times', 'avg_speed', 'compare_speeds',
           'convert_module', 'modulemethod'
           )