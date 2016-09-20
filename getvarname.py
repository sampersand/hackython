# # def varname(var):
# #   import inspect
# #   frame = inspect.currentframe()
# #   for name in frame.f_back.f_locals.keys():
# #     try:
# #       if eval(name) is var:
# #         return(name)
# #     except:
# #       pass
# # a = 1
# # b = 1
# # print(varname(a) if 1 == 1 else 0)

# import inspect
# def varname():
#     f = inspect.currentframe().f_back
#     frame = type(f)
#     print(dir(inspect))
#     print(inspect.inspect(f))
#     quit()
#     return f.f_code
# print('hello') or exec(varname())

from functools import reduce

class _factors(list):
    def __sub__(self, other):
        s = self[:]
        for x in other:
            if x in s:
                s.pop(s.index(x))
        return _factors(s)
    def __int__(self):
        return reduce(lambda q,w: q * w, self) if self else 0

def find(factors, tolookfor):
    factors = _factors(factors)
    for pos in range(1 << len(factors)):
        a = _factors([factors[x] for x in range(len(factors)) if (1 << x) & pos])
        b = factors - a
        # if not a or not b:
            # continue
        if int(a) + int(b) == tolookfor:
            return int(a), int(b)




print(find([-1, 2, 2, 3, 3, 3], -12))




















