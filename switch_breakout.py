from types import CodeType
import inspect
class attrdict(dict):
    def __getattr__(self, attr):
    	return self[attr]

class case():
    def __init__(self, *labels, value = None, breakout = False, code = False):
        self.labels = set(labels)
        self.value = value
        self.breakout = breakout
        self.iscode = code
    def __eq__(self, other): return other in self.labels
    def _value(self, _globals, _locals):
        if self.iscode and isinstance(self.value, (str, bytes, bytearray)):
            exec(compile(self.value, [], 'exec'), _globals, _locals)
            return attrdict(_locals)
        if isinstance(self.value, CodeType):
            exec(self.value, _globals, attrdict(_locals))
            return attrdict(_locals)
        return self.value
    def __str__(self): return '{} : {}'.format(self.labels, self.value)
    def __repr__(self): return '{}({}{}{}{})'.format(type(self).__qualname__, repr(self.labels),
                                            self.value != None and ', value=' + repr(self.value) or '',
                                            self.breakout != False and ', breakout=' + repr(self.breakout) or '',
                                            self.iscode != False and ', code=' + repr(self.iscode) or '',)

class _default_case(case):
    def __init__(self): super().__init__(None)
    def __eq__(self, other): return True
    def __str__(self): return 'default : {}'.format(self.value)

class _switch_statement(list):
    class _breakout_class():
        pass
    def __new__(self, varname = None, dothrow = False): return super().__new__(self, [])
    def __init__(self, varname = None, dothrow = False):
        self.varname = varname
        self.dothrow = dothrow
    def __getitem__(self, item):
        if isinstance(item, slice) and isinstance(item.start, case):
            item = (item,)
        if isinstance(item, tuple):
            for casevalue in item: # item should be plural haha
                if isinstance(casevalue, slice):
                    self.append(casevalue.start)
                    self[-1].value = casevalue.stop
                    if isinstance(casevalue.step, _switch_statement._breakout_class):
                        self[-1].breakout = True
                elif isinstance(casevalue, _switch_statement._breakout_class):
                    self[-1].breakout = True
                elif isinstance(casevalue, case):
                    self.append(casevalue)
            return self
        return super().__getitem__(item)

    def __call__(self, control_var, _globals = None, _locals = None):
            if control_var not in self:
                if self.dothrow:
                    raise IndexError("Case not found: {}".format(control_var))
                else:
                    return None
            if _globals == None:
                _globals = inspect.stack()[1].frame.f_globals
            if _locals == None:
                _locals = inspect.stack()[1].frame.f_locals
            if self.varname != None:
                _locals[self.varname] = control_var
            for _case in self[self.index(control_var):]:
                ret = _case._value(_globals, _locals)
                if _case.breakout: return ret
            return ret #should exist because otherwise error would have been called

class switch_class():
    def __call__(self, varname = None, dothrow = False):
        return _switch_statement(varname, dothrow)
    def __getitem__(self, item):
        return _switch_statement()[item]


switch = switch_class()
default = _default_case()
breakout = _switch_statement._breakout_class()
br = breakout
__all__ = ['switch', 'default', 'breakout', 'br', 'case']




