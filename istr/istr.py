#     _       _
#    (_) ___ | |_  _ __
#    | |/ __|| __|| '__|
#    | |\__ \| |_ | |
#    |_||___/ \__||_|
# strings you can count on

__version__ = "1.1.3"
import functools
import math
import itertools
import types
import sys

"""
Note: the changelog is now in changelog.md

You can view the changelog on www.salabim.org/istr/changelog.html

The readme can be viewed on www.salabim.org/istr/
"""

_0_to_Z = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class _range:
    """
    based on https://codereview.stackexchange.com/questions/229073/pure-python-range-implementation
    """

    def __init__(self, cls, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        self.start, self.stop, self.step = (int(obj) for obj in (start, stop, step))
        if step == 0:
            raise ValueError("range() arg 3 must not be zero")
        if self.step < 0:
            step_sign = -1
        else:
            step_sign = 1
        self._len = max(1 + (self.stop - self.start - step_sign) // self.step, 0)
        self.parent_cls = cls
        self.init_done = True

    def __setattr__(self, name, value):
        if getattr(self, "init_done", False):
            raise AttributeError()
        super().__setattr__(name, value)

    def __contains__(self, value):
        if isinstance(value, int):
            return self._index(value) != -1
        return any(n == value for n in self)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if self._len != len(other):
            return False
        if self._len == 0:
            return True
        if self.start != other.start:
            return False
        if self[-1] == other[-1]:
            return True
        return False

    def __getitem__(self, index):
        def adjust_indices(length, start, stop, step):
            if step is None:
                step = 1
            else:
                step = int(step)

            if start is None:
                start = length - 1 if step < 0 else 0
            else:
                start = int(start)
                if start < 0:
                    start += length
                    if start < 0:
                        start = -1 if step < 0 else 0
                elif start >= length:
                    start = length - 1 if step < 0 else length

            if stop is None:
                stop = -1 if step < 0 else length
            else:
                stop = int(stop)
                if stop < 0:
                    stop += length
                    if stop < 0:
                        stop = -1 if step < 0 else 0
                elif stop >= length:
                    stop = length - 1 if step < 0 else length

            return start, stop, step

        if isinstance(index, slice):
            start, stop, step = adjust_indices(self._len, index.start, index.stop, index.step)
            return self.parent_cls.range(self.start + self.step * start, self.start + self.step * stop, self.step * step)
        index = int(index)
        if index < 0:
            index += self._len
        if not 0 <= index < self._len:
            raise IndexError("range object index out of range")
        return self.parent_cls(self.start + self.step * index)

    def __hash__(self):
        if self._len == 0:
            return id(self.parent_cls.range)
        return hash((self._len, self.start, int(self[-1])))

    def __iter__(self):
        value = self.start
        if self.step > 0:
            while value < self.stop:
                yield self.parent_cls(value)
                value += self.step
        else:
            while value > self.stop:
                yield self.parent_cls(value)
                value += self.step

    def __len__(self):
        return self._len

    def __repr__(self):
        if self.step == 1:
            return f"{self.parent_cls.__name__}.range({self.start}, {self.stop})"
        return f"{self.parent_cls.__name__}.range({self.start}, {self.stop}, {self.step})"

    def __reversed__(self):
        return iter(self[::-1])

    def _index(self, value):
        index_mul_step = value - self.start
        if index_mul_step % self.step:
            return -1
        index = index_mul_step // self.step
        if 0 <= index < self._len:
            return index
        return -1

    def count(self, value):
        """
        Rangeobject.count(value) -> integer
        Return number of occurrences of value.
        """
        return sum(1 for n in self if int(n) == int(value))

    def index(self, value, start=0, stop=None):
        if start < 0:
            start = max(self._len + start, 0)
        if stop is None:
            stop = self._len
        if stop < 0:
            stop += self._len

        if isinstance(value, int):
            index = self._index(value)
            if start <= index < stop:
                return index
            raise ValueError(f"{value} is not in range")

        i = start
        n = self.start + self.step * i
        while i < stop:
            if n == int(value):
                return i
            i += 1
            n += self.step
        raise ValueError(f"{value} is not in range")


class istr(str):
    """
    istr object

    Parameters
    ----------
    value : any
        if str the value will to be interpreted as an int
            istr('8') ==> istr('8')
        if numeric, the value will be interpreted as an int
            istr(8) ==> istr('8')
        if a dict (or subtype of dict), the same type dict will be returned with all values istr'ed
            istr({0: 0, 1: 1, 2: 4}) ==> {0: istr('0'), 1: istr('1'), 2: istr('4')}
        if an iterator, the iterator will be mapped with istr
            istr(i * i for i in range(3)) ==> <map object>
            list(istr(i * i for i in range(3))) ==> [istr('0'), istr('1'), istr('4')]
        if an iterable, the same type will be returned with all elements istr'ed
            istr([0, 1, 4]) ==> [istr('0'), istr('1'), istr('4')]
            istr((0, 1, 4)) ==> (istr('0'), istr('1'), istr('4'))
            istr({0, 1, 4}) ==> {istr('4'), istr('0'), istr('1')} # or similar
        if a range, an istr.range instance will be returned
            istr(range(3)) ==> istr.range(3)
            list(istr(range(3))) ==> [istr('0'), istr('1'), istr('2')]
            len(istr(range(3))) ==> 3
        if an istr, the same istr will be returned istr(istr('2')) ==> istr('2')

        it is possible to give more than one parameter, in which case a tuple
        of the istrs of the parameters will be returned, which can be handy
        to multiple assign, e.g.
            a, b, c = istr(5, 6, 7) ==> a=istr('5') , b=istr('6'), c=istr('7')"""

    __slots__ = ("_as_int", "_as_repr")

    _int_format = ""
    _repr_mode = "istr"
    _base = 10
    _nan = object()
    _digits_cache = {}

    @staticmethod
    def _to_base(number, base):
        if number < 0:
            raise ValueError(f"negative numbers are not allowed for base {base}")
        result = ""
        while number:
            result += _0_to_Z[number % base]
            number //= base
        return result[::-1] or "0"

    @classmethod
    def _to_int(cls, value):
        try:
            if cls._base != 10 and isinstance(value, str):
                return int(value, cls._base)
            else:
                return int(value)
        except:
            return cls._nan

    def __new__(cls, *value):
        if len(value) == 0:
            raise TypeError("no parameter given")
        if len(value) == 1:
            value = value[0]  # normal case of 1 parameter
        if isinstance(value, range):
            return cls.range(value.start, value.stop, value.step)
        if isinstance(value, _range):
            return value
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return type(value)((k, cls(v)) for k, v in value.items())
        if not isinstance(value, (str, type)) and hasattr(value, "__iter__"):
            if hasattr(value, "__next__"):
                return map(functools.partial(cls), value)
            return type(value)(map(functools.partial(cls), value))
        as_int = cls._to_int(value)
        if isinstance(value, str):
            as_str = value
        else:
            if as_int is cls._nan:
                raise TypeError(f"incorrect value for {cls.__name__}: {repr(value)}")
            if cls._int_format == "" or cls._base != 10:
                if cls._base == 10:
                    as_str = str(as_int)
                else:
                    as_str = istr._to_base(as_int, cls._base)
            else:
                as_str = f"{as_int:{cls._int_format}}"

        self = super().__new__(cls, as_str)
        self._as_int = as_int
        if self._repr_mode == "istr":
            self._as_repr = f"{cls.__name__}({repr(as_str)})"
        elif self._repr_mode == "int":
            self._as_repr = "?" if as_int is self._nan else repr(as_int)
        else:
            self._as_repr = repr(as_str)
        return self

    def __iter__(self):
        yield from self.__class__(super().__iter__())

    def __hash__(self):
        return hash((self.__class__, str(self)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.is_int() and other.is_int():
                return self._as_int == other._as_int
        if isinstance(other, str):
            return super().__eq__(other)
        try:
            return self._as_int == self._to_int(other)
        except Exception:
            return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self._as_repr

    def __bool__(self):
        if self.is_int():
            return bool(self._as_int)
        return bool(str(self))

    def _frepr(self, obj):
        # like repr, but if obj is an istr, the as_repr is not used to make sure the
        # the returned value is istr(...) and not infuenced by the repr mode
        if isinstance(obj, self.__class__):
            return f"{obj.__class__.__name__}({super(istr,obj).__repr__()})"
        return repr(obj)

    def _int_method(self, name, op, *args):
        if len(args) == 1:
            other = args[0]
            if not self.is_int() or self._to_int(other) is self._nan:
                if name.startswith("__r"):
                    raise TypeError(f"unsupported operand for {op}: {self._frepr(other)} and {self._frepr(self)}")
                else:
                    raise TypeError(f"unsupported operand for {op}: {self._frepr(self)} and {self._frepr(other)}")
            if "<" in op or ">" in op:
                return getattr(self._as_int, name)(self._to_int(other))
            else:
                return self.__class__(getattr(self._as_int, name)(self._to_int(other)))
        else:
            if not self.is_int():
                raise TypeError(f"unsupported operand for {op}: {self._frepr(self)}")
            return self.__class__(getattr(self._as_int, name)())

    for name_op in (
        "__add__+ __radd__+ __sub__- __rsub__- __mul__* __rmul__* __floordiv__// __rfloordiv__// "
        "__truediv__/ __rtruediv__/ __pow__** __rpow__** __mod__% __rmod__% "
        "__divmod__divmod __rdivmod__divmod "
        "__le__<= __lt__< __gt__> __ge__>= "
        "__round__round __trunc__trunc __floor__floor __ceil__ceil __neg__- __pos__+ "
        "__invert__~ __abs__abs "
    ).split():
        i = len(name_op) - "".join(reversed(name_op)).find("_")  # pos of last _
        name = name_op[:i]
        op = name_op[i:]

        locals()[name] = functools.partialmethod(_int_method, name, op)

    def __int__(self):
        if not self.is_int():
            raise ValueError(f"invalid literal for int() with base 10: {self._frepr(self)}")
        return int(self._as_int)

    def is_even(self):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as int: {self._frepr(self)}")
            n = self._as_int
        else:
            n = int(self)

        return n % 2 == 0

    def is_odd(self):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as int: {self._frepr(self)}")
            n = self._as_int
        else:
            n = int(self)

        return n % 2 == 1

    def is_square(self):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as int: {self._frepr(self)}")
            n = self._as_int
        else:
            n = int(self)

        return n >= 0 and self == math.isqrt(n) ** 2

    def is_prime(self):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as int: {self._frepr(self)}")
            n = self._as_int
        else:
            n = int(self)

        if n < 2:
            return False
        if n == 2:
            return True
        if not n & 1:
            return False

        for x in range(3, int(n**0.5) + 1, 2):
            if n % x == 0:
                return False
        return True

    def __or__(self, other):
        try:
            return self.__class__(str(self).__add__(other))
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for |: {self._frepr(self)} and {self._frepr(other)}")

    def __ror__(self, other):
        try:
            return self.__class__(other.__add__(str(self)))
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for |: {self._frepr(other)} and {self._frepr(self)}")

    def __matmul__(self, other):
        try:
            return self.__class__(super().__mul__(other))
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for @: {self._frepr(self)}  and {self._frepr(other)}")

    def __rmatmul__(self, other):
        try:
            return self.__class__(super().__rmul__(other))
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for @|: {self._frepr(other)}  and {self._frepr(self)}")

    def __getitem__(self, key):
        return self.__class__(super().__getitem__(key))

    def all_distinct(self):
        return len(self) == len(set(self))

    def reversed(self):
        return self[::-1]

    def is_divisible_by(self, divisor):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as int: {self._frepr(self)}")
            n = self._as_int
        else:
            n = int(self)
        return n % int(divisor) == 0

    def _str_method(self, name, *args, **kwargs):
        return self.__class__(getattr(super(), name)(*args, **kwargs))

    for name in (
        "capitalize casefold center expandtabs format join ljust lower lstrip partition removeprefix "
        "removesuffix replace rjust rpartition rsplit rstrip split strip swapcase title translate upper zfill"
    ).split():
        locals()[name] = functools.partialmethod(_str_method, name)

    @classmethod
    def _itertools_method(cls, name, *args, **kwargs):
        return cls(getattr(itertools, name)(*args, **kwargs))

    for name in dir(itertools):
        if not name.startswith("__"):
            if name in ("groupby", "tee"):
                locals()[name] = getattr(itertools, name)
            else:
                locals()[name] = functools.partialmethod(_itertools_method, name)

    def is_int(self):
        return self._as_int is not self._nan

    @classmethod
    def concat(cls, iterable):
        return map(lambda x: istr("").join(x), istr(iterable))

    @classmethod
    def enumerate(cls, iterable, start=0):
        for i, value in enumerate(iterable, start):
            yield cls(i), value

    @classmethod
    class int_format:
        def __new__(cls, cls_int_format, int_format=None):
            if int_format is None:
                return cls_int_format._int_format
            return super().__new__(cls)

        def __init__(self, cls, int_format):
            self.saved_int_format = cls._int_format
            self.saved_cls = cls
            if not (isinstance(int_format, str) and all(x in "0123456789" for x in int_format)):
                raise ValueError(f"{repr(int_format)} is incorrect int_format")

            cls._int_format = int_format

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._int_format = self.saved_int_format

    @classmethod
    class repr_mode:
        def __new__(cls, cls_repr_mode, mode=None):
            if mode is None:
                return cls_repr_mode._repr_mode
            if mode in ("istr", "str", "int"):  # _istr is used only for TypeErrors
                return super().__new__(cls)
            raise TypeError(f"mode not 'istr', 'str' or 'int', but {repr(mode)}")

        def __init__(self, cls, mode):
            self.saved_repr_mode = cls._repr_mode
            self.saved_cls = cls
            cls._repr_mode = mode

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._repr_mode = self.saved_repr_mode

    @classmethod
    class base:
        def __new__(cls, cls_base, base=None):
            if base is None:
                return cls_base._base
            if 2 <= base <= 36:
                return super().__new__(cls)
            raise ValueError(f"base not between 2 and 36, but {base}")

        def __init__(self, cls, base):
            self.saved_base = cls._base
            self.saved_cls = cls
            cls._base = base

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._base = self.saved_base

    @classmethod
    def range(cls, start, stop=None, step=1):
        return _range(cls, start, stop, step)

    @classmethod
    def digits(cls, *args):
        """
        return an istr of istr'ed digits as specified with args

        if no args, 0-9 will be used

        all given args will be used
        each arg has to be either null string, <digit>, <digit>-<digit> or -<digit>

        the digits may be '0' through '9' and 'A' through 'Z' (not case sensitive)
        The returned value will always be in uppercase (if applicable).

        Examples
        --------
        istr.digits() ==> istr('0123456789')
        istr.digits('') ==> istr('0123456789')
        istr.digits('1') ==> istr('1')
        istr.digits('3-') ==> istr('3456789')
        istr.digits('-3') ==> istr('0123')
        istr('1-4', '6', '8-9') ==> istr('1234689')
        istr('1', '1-2', '1-3') ==> istr('11213')
        istr.digits('-z') ==> istr('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        istr.digits('C') ==> istr('C')
        istr.digits('A-F') ==> istr('ABCDEF')
        istr.digits('X-') ==> istr('XYZ')

        Note
        ----
        A digit can occur more than once.
        """
        key = (args, cls._base, cls._int_format, cls._repr_mode)
        if key in cls._digits_cache:
            return cls._digits_cache[key]
        result = []
        if not args:
            args = ["0-9"]
        for arg in args:
            if arg.strip() == "":
                arg = "0-9"
            pre, *post = arg.split("-", 1)
            if pre.strip() == "":
                pre = "0"
            pre = pre.upper()
            if len(pre) > 1 or pre not in _0_to_Z:
                raise ValueError(f"incorrect specifier: {repr(arg)}")
            start = _0_to_Z.index(pre)

            if post:
                post = post[0]
                if post.strip() == "":
                    if pre in "0123456789":
                        post = "9"
                    else:
                        post = "Z"
                post = post.upper()
                if len(post) > 1 or post not in _0_to_Z:
                    raise ValueError(f"incorrect specifier: {repr(arg)}")
                stop = _0_to_Z.index(post)
                if start > stop:
                    raise ValueError(f"incorrect specifier: {repr(arg)}")
            else:
                stop = start
            result.extend(_0_to_Z[i] for i in range(start, stop + 1))

        result = istr("".join(result))
        cls._digits_cache[key] = result
        return result
        
istr.type=type(istr(0))


def main():
    ...

class istrModule(types.ModuleType):
    def __call__(self, *args, **kwargs):
        return istr.__call__(*args, **kwargs)
    def __setattr__(self, item, value):
        setattr(istr,item,value)
    def __getattr__(self, item,):
        return getattr(istr,item)

sys.modules["istr"].__class__ = istrModule

if __name__ == "__main__":
    main()

