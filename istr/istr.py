import functools
import math

#     _       _
#    (_) ___ | |_  _ __
#    | |/ __|| __|| '__|
#    | |\__ \| |_ | |
#    |_||___/ \__||_|
# strings you can count on

__version__ = "0.1" # only x.y here!
import functools
import math

"""
changelog

version 0.1.2  2024-04-26  
-------------------------
Added all relevant string methods to return istrs or data structures with istrs.
Added corresponding tests.

version 0.1.0  2024-04-22  
-------------------------
Changed the way istr.range is implemennted.

Changed the context manager istr.format() to be used directly without the with statement.
Also, noww istr.format() works without any argument and then returns the current format.

istr class now uses __slots__

All internal values and methods now start with an underscore.

Introduced istr.repr_mode()

Introduced istr.base()

Extended tests for new functionality


version 0.0.8  2024-04-18  
-------------------------
initial version with changelog
"""


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
            istr("8") ==> istr("8")
        if numeric, the value will be interpreted as an int
            istr(8) ==> istr("8")
        if a dict (or subtype of dict), the same type dict will be returned with all values istr"ed
            istr({0: 0, 1: 1, 2: 4}) ==> {0: istr("0"), 1: istr("1"), 2: istr("4")}
        if an iterator, the iterator will be mapped with istr
            istr(i * i for i in range(3)) ==> <map object>
            list(istr(i * i for i in range(3))) ==> [istr("0"), istr("1"), istr("4")]
        if an iterable, the same type will be returned with all elements istr"ed
            istr([0, 1, 4]) ==> [istr("0"), istr("1"), istr("4")]
            istr((0, 1, 4)) ==> (istr("0"), istr("1"), istr("4"))
            istr({0, 1, 4}) ==> {istr("4"), istr("0"), istr("1")} # or similar
        if a range, an istr.range instance will be returned
            istr(range(3)) ==> istr.range(3)
            list(istr(range(3))) ==> [istr("0"), istr("1"), istr("2")]
            len(istr(range(3))) ==> 3

        it is possible to give more than one parameter, in which case a tuple
        of the istrs of the parameters will be returned, which can be handy
        to multiple assign, e.g.
            a, b, c = istr(5, 6, 7) ==> a=istr("5") , b=istr("6"), c=istr("7")"""

    __slots__ = ("_as_int", "_as_repr")

    _format = ""
    _mode = "istr"
    _base = 10

    @staticmethod
    def _to_base(number, base):
        if number < 0:
            raise ValueError(f"negative numbers are not allowed for base {base}")
        result = ""
        while number:
            result += "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[number % base]
            number //= base
        return result[::-1] or "0"

    @classmethod
    def _to_int(cls, value):
        try:
            if cls._base != 10 and isinstance(value, str):
                return int(value, cls._base)
            else:
                return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"unable to convert {repr(value)} to int (base {cls._base})")

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
        if value == "":
            as_str = ""
            as_int = 0
        else:
            as_int = cls._to_int(value)
            if (cls._format == "" or cls._base != 10) and not isinstance(value, istr):
                if isinstance(value, str):
                    as_str = value
                else:
                    if cls._base == 10:
                        as_str = str(as_int)
                    else:
                        as_str = istr._to_base(as_int, cls._base)
            else:
                as_str = f"{as_int:{cls._format}}"

        self = super().__new__(cls, as_str)
        self._as_int = as_int
        if self._mode == "istr":
            self._as_repr = f"{cls.__name__}({repr(as_str)})"
        elif self._mode == "int":
            self._as_repr = repr(as_int)
        else:
            self._as_repr = repr(as_str)
        return self

    def __hash__(self):
        return hash((self.__class__, str(self)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._as_int == other._as_int
        if isinstance(other, str):
            return super().__eq__(other)
        try:
            return self._as_int == self._to_int(other)
        except Exception:
            return False

    def __ne__(self, other):
        return not self == other

    def __contains__(self, other):
        return super().__contains__(str(other))

    def __repr__(self):
        return self._as_repr

    def __le__(self, other):
        return self._as_int <= self._to_int(other)

    def __lt__(self, other):
        return self._as_int < self._to_int(other)

    def __ge__(self, other):
        return self._as_int >= self._to_int(other)

    def __gt__(self, other):
        return self._as_int > self._to_int(other)

    def __bool__(self):
        return bool(self._as_int)

    def __add__(self, other):
        return self.__class__(self._as_int + self._to_int(other))

    def __sub__(self, other):
        return self.__class__(self._as_int - self._to_int(other))

    def __mul__(self, other):
        return self.__class__(self._as_int * self._to_int(other))

    def __floordiv__(self, other):
        return self.__class__(self._as_int // self._to_int(other))

    def __rfloordiv__(self, other):
        return self.__class__(self._to_int(other) // self._as_int)

    def __truediv__(self, other):
        return self.__class__(self._as_int // self._to_int(other))

    def __rtruediv__(self, other):
        return self.__class__(self._to_int(other) // self._as_int)

    def __pow__(self, other):
        return self.__class__(self._as_int ** self._to_int(other))

    def __rpow__(self, other):
        return self.__class__(self._to_int(other) ** self._as_int)

    def __radd__(self, other):
        return self.__class__(self._to_int(other) + self._as_int)

    def __rsub__(self, other):
        return self.__class__(self._to_int(other) - self._as_int)

    def __rmul__(self, other):
        return self.__class__(self._to_int(other) * self._as_int)

    def __mod__(self, other):
        return self.__class__(self._as_int % self._to_int(other))

    def __rmod__(self, other):
        return self.__class__(self._to_int(other) % self._as_int)

    def __or__(self, other):
        return self.__class__("".join((self, self.__class__(other))))

    def __ror__(self, other):
        return self.__class__("".join((self.__class__(other), self)))

    def __int__(self):
        return int(self._as_int)

    def __round__(self):
        return self.__class__(round(self._as_int))

    def __trunc__(self):
        return self.__class__(math.trunc(self._as_int))

    def __floor__(self):
        return self.__class__(math.floor(self._as_int))

    def __ceil__(self):
        return self.__class__(math.ceil(self._as_int))

    def __matmul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rmatmul__(self, other):
        return self.__class__(super().__rmul__(other))

    def __divmod__(self, other):
        return self.__class__(divmod(self._as_int, self._to_int(other)))

    def __rdivmod__(self, other):
        return self.__class__(divmod(self._to_int(other), self._as_int))

    def __neg__(self):
        return self.__class__(-self._as_int)

    def __pos__(self):
        return self

    def __abs__(self):
        return self.__class__(abs(self._as_int))

    def is_even(self):
        return self._as_int % 2 == 0

    def is_odd(self):
        return self._as_int % 2 == 1

    def reversed(self):
        return self[::-1]

    def __getitem__(self, key):
        return self.__class__(super().__getitem__(key))

    @classmethod
    def concat(cls, iterable):
        return map(lambda x: istr("").join(x), istr(iterable))

    @classmethod
    def enumerate(cls, iterable, start=0):
        for i, value in enumerate(iterable, start):
            yield cls(i), value

    @classmethod
    class format:
        def __new__(cls, cls_format, format=None):
            if format is None:
                return cls_format._format
            return super().__new__(cls)

        def __init__(self, cls, format):
            self.saved_format = cls._format
            self.saved_cls = cls
            if not (isinstance(format, str) and all(x in "0123456789" for x in format)):
                raise ValueError(f"{repr(format)} is incorrect format")

            cls._format = format

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._format = self.saved_format

    @classmethod
    class repr_mode:
        def __new__(cls, cls_mode, mode=None):
            if mode is None:
                return cls_mode._mode
            if mode in ("istr", "str", "int"):
                return super().__new__(cls)
            raise TypeError(f"mode not 'istr', 'str' or 'int', but {repr(mode)}")

        def __init__(self, cls, mode):
            self.saved_mode = cls._mode
            self.saved_cls = cls
            cls._mode = mode

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._mode = self.saved_mode

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

    def capitalize1(self, *args, **kwargs):
        return self.__class__(super().capitalize(*args, **kwargs))

    def casefold(self, *args, **kwargs):
        return self.__class__(super().casefold(*args, **kwargs))

    def center(self, *args, **kwargs):
        return self.__class__(super().center(*args, **kwargs))

    def expandtabs(self, *args, **kwargs):
        return self.__class__(super().expandtabs(*args, **kwargs))

    def join(self, *args, **kwargs):
        return self.__class__(super().join(*args, **kwargs))

    def ljust(self, *args, **kwargs):
        return self.__class__(super().ljust(*args, **kwargs))

    def lower(self, *args, **kwargs):
        return self.__class__(super().lower(*args, **kwargs))

    def lstrip(self, *args, **kwargs):
        return self.__class__(super().lstrip(*args, **kwargs))

    def partition(self, *args, **kwargs):
        return self.__class__(super().partition(*args, **kwargs))

    def removeprefix(self, *args, **kwargs):
        return self.__class__(super().removeprefix(*args, **kwargs))

    def removesuffix(self, *args, **kwargs):
        return self.__class__(super().removesuffix(*args, **kwargs))

    def replace(self, *args, **kwargs):
        return self.__class__(super().replace(*args, **kwargs))

    def rjust(self, *args, **kwargs):
        return self.__class__(super().rjust(*args, **kwargs))

    def rpartition(self, *args, **kwargs):
        return self.__class__(super().rpartition(*args, **kwargs))

    def rsplit(self, *args, **kwargs):
        return self.__class__(super().rsplit(*args, **kwargs))

    def rstrip(self, *args, **kwargs):
        return self.__class__(super().rstrip(*args, **kwargs))

    def split(self, *args, **kwargs):
        return self.__class__(super().split(*args, **kwargs))

    def strip(self, *args, **kwargs):
        return self.__class__(super().strip(*args, **kwargs))

    def swapcase(self, *args, **kwargs):
        return self.__class__(super().swapcase(*args, **kwargs))

    def title(self, *args, **kwargs):
        return self.__class__(super().title(*args, **kwargs))

    def translate(self, *args, **kwargs):
        return self.__class__(super().translate(*args, **kwargs))

    def upper(self, *args, **kwargs):
        return self.__class__(super().upper(*args, **kwargs))

    def zfill(self, *args, **kwargs):
        return self.__class__(super().zfill(*args, **kwargs))

    f = "capitalize"
    exec(
        f"""
def {f}(self, *args, **kwargs):
        return self.__class__(super(istr,self).{f}(*args, **kwargs)) 
""",
        globals(),
        locals(),
    )


def main():
    a = istr("123123")
    print(repr(a.capitalize()))


if __name__ == "__main__":
    main()

