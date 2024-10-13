'''
this module define a class `MyNamespace`. This class acts like whatever value it is initialized with, but also a namespace.
'''
from .mydict import MyDict

class MyNamespace(object):
    def __init__(self, mydict: MyDict, splitter: str = "/"):
        self.__dict__["_mydict"] = MyDict( mydict )
        self.__dict__["_splitter"] = str( splitter )

    @property
    def _value(self):
        return self._mydict.get("")
    
    def __getattr__(self, name):
        if name in ["_mydict", "_splitter", "_value"]:
            return object.__getattribute__(self, name)

        myd = self._mydict
        sub_d = myd(name, splitter = self._splitter)
        if len(sub_d) == 0: # don't have sub namespace
            return getattr(self._value, name)
        
        return MyNamespace(sub_d, splitter = self._splitter)

        
    def __setattr__(self, name, value):
        self._mydict[name] = value

    def to_dict(self):
        return dict( self._mydict )

    def __add__(self, other): return self._value + other
    def __sub__(self, other): return self._value - other
    def __mul__(self, other): return self._value * other
    def __truediv__(self, other): return self._value / other
    def __floordiv__(self, other): return self._value // other
    def __mod__(self, other): return self._value % other
    def __pow__(self, other): return self._value ** other
    def __lshift__(self, other): return self._value << other
    def __rshift__(self, other): return self._value >> other
    def __and__(self, other): return self._value & other
    def __or__(self, other): return self._value | other
    def __xor__(self, other): return self._value ^ other
    def __invert__(self): return ~self._value
    def __radd__(self, other): return other + self._value
    def __rsub__(self, other): return other - self._value
    def __rmul__(self, other): return other * self._value
    def __rtruediv__(self, other): return other / self._value
    def __rfloordiv__(self, other): return other // self._value
    def __rmod__(self, other): return other % self._value
    def __rpow__(self, other): return other ** self._value
    def __iadd__(self, other): self._value += other; return self
    def __isub__(self, other): self._value -= other; return self
    def __imul__(self, other): self._value *= other; return self
    def __itruediv__(self, other): self._value /= other; return self
    def __ifloordiv__(self, other): self._value //= other; return self
    def __imod__(self, other): self._value %= other; return self
    def __ipow__(self, other): self._value **= other; return self
    def __eq__(self, other): return self._value == other
    def __ne__(self, other): return self._value != other
    def __lt__(self, other): return self._value < other
    def __le__(self, other): return self._value <= other
    def __gt__(self, other): return self._value > other
    def __ge__(self, other): return self._value >= other
    def __int__(self): return int(self._value)
    def __float__(self): return float(self._value)
    def __complex__(self): return complex(self._value)
    def __round__(self, n=None): return round(self._value, n)
    def __trunc__(self): return self._value.__trunc__()
    def __floor__(self): return self._value.__floor__()
    def __ceil__(self): return self._value.__ceil__()
    def __str__(self): return str(self._value)
    def __repr__(self): return repr(self._value)
    def __bytes__(self): return bytes(self._value)
    def __bool__(self): return bool(self._value)
    def __len__(self): return len(self._value)
    def __enter__(self): return self._value.__enter__()
    def __exit__(self, exc_type, exc_value, traceback): return self._value.__exit__(exc_type, exc_value, traceback)
    def __iter__(self): return iter(self._value)
    def __next__(self): return next(self._value)
    def __call__(self, *args, **kwargs): return self._value(*args, **kwargs)
    def __getitem__(self, key): return self._value[key]
    def __setitem__(self, key, value): self._value[key] = value
    def __delitem__(self, key): del self._value[key]

