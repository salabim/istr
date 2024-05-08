#     _       _
#    (_) ___ | |_  _ __
#    | |/ __|| __|| '__|
#    | |\__ \| |_ | |
#    |_||___/ \__||_|
# strings you can count on

__version__ = "1.0.2"
import functools
import math

"""
Note: the changelog is now in changelog.md

You can view the changelog on www.salabim/istr_changelog.html
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

    _int_format = ""
    _repr_mode = "istr"
    _base = 10
    _nan = object()
    _force_istr_repr = False
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

    def _check_is_int(self, *args, right=False):
        operator = args[len(args) == 2]
        if len(args) == 2:
            other = args[0]
            if not self.is_int() or self._to_int(other) is self._nan:
                self.__class__._force_istr_repr = True
                if right:
                    message = f"unsupported operand for {operator}: {repr(other)} and {repr(self)}"
                else:
                    message = f"unsupported operand for {operator}: {repr(self)} and {repr(other)}"
                self.__class__._force_istr_repr = False
                raise TypeError(message)
        else:
            if not self.is_int():
                self.__class__._force_istr_repr = True
                message = f"unsupported operand for {operator}: {repr(self)}"
                self.__class__._force_istr_repr = False
                raise TypeError(message)

    def _rcheck_is_int(self, *args):
        self._check_is_int(*args, right=True)

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

    def __contains__(self, other):
        return super().__contains__(str(other))

    def __repr__(self):
        if self._force_istr_repr:
            return f"{self.__class__.__name__}({super().__repr__()})"
        return self._as_repr

    def __le__(self, other):
        self._check_is_int(other, "<=")
        return self._as_int <= self._to_int(other)

    def __lt__(self, other):
        self._check_is_int(other, "<")
        return self._as_int < self._to_int(other)

    def __ge__(self, other):
        self._check_is_int(other, ">=")
        return self._as_int >= self._to_int(other)

    def __gt__(self, other):
        self._check_is_int(other, ">")
        return self._as_int > self._to_int(other)

    def __bool__(self):
        if self.is_int():
            return bool(self._as_int)
        return bool(str(self))

    def __add__(self, other):
        self._check_is_int(other, "+")
        return self.__class__(self._as_int + self._to_int(other))

    def __radd__(self, other):
        self._rcheck_is_int(other, "+")
        return self.__class__(self._to_int(other) + self._as_int)

    def __sub__(self, other):
        self._check_is_int(other, "-")
        return self.__class__(self._as_int - self._to_int(other))

    def __rsub__(self, other):
        self._rcheck_is_int(other, "-")
        return self.__class__(self._to_int(other) - self._as_int)

    def __mul__(self, other):
        self._check_is_int(other, "*")
        return self.__class__(self._as_int * self._to_int(other))

    def __rmul__(self, other):
        self._rcheck_is_int(other, "*")
        return self.__class__(self._to_int(other) * self._as_int)

    def __floordiv__(self, other):
        self._check_is_int(other, "//")
        return self.__class__(self._as_int // self._to_int(other))

    def __rfloordiv__(self, other):
        self._rcheck_is_int(other, "//")
        return self.__class__(self._to_int(other) // self._as_int)

    def __truediv__(self, other):
        self._check_is_int(other, "/")
        return self.__class__(self._as_int // self._to_int(other))

    def __rtruediv__(self, other):
        self._rcheck_is_int(other, "/")
        return self.__class__(self._to_int(other) // self._as_int)

    def __pow__(self, other):
        self._check_is_int(other, "**")
        return self.__class__(self._as_int ** self._to_int(other))

    def __rpow__(self, other):
        self._rcheck_is_int(other, "**")
        return self.__class__(self._to_int(other) ** self._as_int)

    def __mod__(self, other):
        self._check_is_int(other, "%")
        return self.__class__(self._as_int % self._to_int(other))

    def __rmod__(self, other):
        self._rcheck_is_int(other, "%")
        return self.__class__(self._to_int(other) % self._as_int)

    def __or__(self, other):
        return self.__class__("".join((self, self.__class__(other))))

    def __ror__(self, other):
        return self.__class__("".join((self.__class__(other), self)))

    def __round__(self):
        self._check_is_int("round")
        return self.__class__(round(self._as_int))

    def __int__(self):
        if not self.is_int():
            raise ValueError(f"invalid literal for int() with base 10: {repr(self)}")
        return int(self._as_int)

    def __trunc__(self):
        self._check_is_int("trunc")
        return self.__class__(math.trunc(self._as_int))

    def __floor__(self):
        self._check_is_int("floor")
        return self.__class__(math.floor(self._as_int))

    def __ceil__(self):
        self._check_is_int("ceil")
        return self.__class__(math.ceil(self._as_int))

    def __matmul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rmatmul__(self, other):
        return self.__class__(super().__rmul__(other))

    def __divmod__(self, other):
        self._check_is_int(other, "divmod")
        return self.__class__(divmod(self._as_int, self._to_int(other)))

    def __rdivmod__(self, other):
        self._rcheck_is_int(other, "divmod")
        return self.__class__(divmod(self._to_int(other), self._as_int))

    def __neg__(self):
        self._check_is_int("-")
        return self.__class__(-self._as_int)

    def __pos__(self):
        self._check_is_int("+")
        return self

    def __abs__(self):
        self._check_is_int("abs")
        return self.__class__(abs(self._as_int))

    def is_even(self):
        self._check_is_int("is_even")
        return self._as_int % 2 == 0

    def is_odd(self):
        self._check_is_int("is_odd")
        return self._as_int % 2 == 1

    def all_distinct(self):
        return len(self) == len(set(self))

    def is_int(self):
        return self._as_int is not self._nan

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
            return cls.digits_cache[key]
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

    def capitalize(self, *args, **kwargs):
        return self.__class__(super().capitalize(*args, **kwargs))

    def casefold(self, *args, **kwargs):
        return self.__class__(super().casefold(*args, **kwargs))

    def center(self, *args, **kwargs):
        return self.__class__(super().center(*args, **kwargs))

    def expandtabs(self, *args, **kwargs):
        return self.__class__(super().expandtabs(*args, **kwargs))

    def format(self, *args, **kwargs):
        return self.__class__(super().format(*args, **kwargs))

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


def main():
    with istr.repr_mode("int"):
        print(repr(istr(3)))
        print(repr(istr("a")))
        with istr.int_format("4"):
            print(repr(istr(3)))
            print(repr(istr("a")))
        with istr.int_format("04"):
            print(repr(istr(3)))
            print(repr(istr("a")))

if __name__ == "__main__":
    main()
