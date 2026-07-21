#     _       _
#    (_) ___ | |_  _ __
#    | |/ __|| __|| '__|
#    | |\__ \| |_ | |
#    |_||___/ \__||_|
# strings you can count on

__version__ = "1.1.33"
import functools
import itertools
import types
import sys
import inspect
import math
import operator
import copy
import bisect
import collections
import numbers

"""
Note: the changelog is in changelog.md

You can view the changelog on www.salabim.org/istr/changelog

The readme can be viewed on www.salabim.org/istr/
"""

_0_to_Z = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class _range:
    """
    based on https://codereview.stackexchange.com/questions/229073/pure-python-range-implementation
    """

    def __init__(self, cls, start, stop, step, length, base, int_format, repr_mode):
        self.start, self.stop, self.step = process_start_stop_step_length(start, stop, step, length)
        if self.step == 0:
            raise ValueError(f"step must not be zero, not {self.step}")
        if self.step < 0:
            step_sign = -1
        else:
            step_sign = 1
        self._len = max(1 + (self.stop - self.start - step_sign) // self.step, 0)
        self.parent_cls = cls
        self.base = cls._base if base is None else base
        self.int_format = cls._int_format if int_format is None else int_format
        self.repr_mode = cls._repr_mode if repr_mode is None else repr_mode
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
            return self.parent_cls.range(
                self.start + self.step * start,
                self.start + self.step * stop,
                self.step * step,
                base=self.base,
                int_format=self.int_format,
                repr_mode=self.repr_mode,
            )
        index = int(index)
        if index < 0:
            index += self._len
        if not 0 <= index < self._len:
            raise IndexError("range object index out of range")
        return self.parent_cls(self.start + self.step * index, base=self.base, int_format=self.int_format, repr_mode=self.repr_mode)

    def __hash__(self):
        if self._len == 0:
            return id(self.parent_cls.range)
        return hash((self._len, self.start, int(self[-1])))

    def __iter__(self):
        value = self.start
        if self.step > 0:
            while value < self.stop:
                yield self.parent_cls(value, base=self.base, int_format=self.int_format, repr_mode=self.repr_mode)
                value += self.step
        else:
            while value > self.stop:
                yield self.parent_cls(value, base=self.base, int_format=self.int_format, repr_mode=self.repr_mode)
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
        if str, the value will to be interpreted as an int
            istr('8') ==> istr('8')
        if numeric, the value will be interpreted as an int
            istr(8) ==> istr('8')
        if str and starts with '=', the value will be retrieved from letter variables and other characters unprocessed, e.g.
            if a=4 and b=32, istr('=ab1') will be istr'('4321')
        if str and starts with ':=', the value will be retrieved from letter variables. And the corresponding value will be set, e.g.
            if a=4 and b=32, istr(':=ab') will be istr'('432') and ab will be assigned that value too.
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
            a, b, c = istr(5, 6, 7) ==> a=istr('5') , b=istr('6'), c=istr('7')
    """

    __slots__ = ("_as_int", "_this_base", "_this_int_format", "_this_repr_mode")

    _int_format = ""
    _repr_mode = "istr"
    _base = 10
    _nan = object()
    _digits_cache = {}

    @classmethod
    def _to_base(cls, number, base):
        if number < 0:
            raise ValueError(f"negative numbers are not allowed for base {base}")
        result = ""
        while number:
            result += _0_to_Z[number % base]
            number //= base
        return result[::-1] or "0"

    @classmethod
    def _to_int(cls, value, base=10):
        try:
            if base != 10 and isinstance(value, str):
                return int(value, base)
            else:
                return int(value)
        except Exception:
            return cls._nan

    def __new__(cls, *value, namespace=None, base=None, int_format=None, repr_mode=None):
        base = cls._base if base is None else base
        int_format = cls._int_format if int_format is None else int_format
        repr_mode = cls._repr_mode if repr_mode is None else repr_mode
        if len(value) == 1:
            value = value[0]  # normal case of 1 parameter
        elif len(value) == 0:
            raise TypeError("no parameter given")

        match value:
            case range():
                return cls.range(value.start, value.stop, value.step, base=base, int_format=int_format, repr_mode=repr_mode)
            case _range():
                return value
            case cls():
                if value.is_int():
                    return cls(value._as_int, base=base, int_format=int_format, repr_mode=repr_mode)
                else:
                    return copy.copy(value)
            case dict():
                return type(value)(
                    (k, cls(v, base=base, int_format=int_format, repr_mode=repr_mode, namespace=get_namespace(namespace))) for k, v in value.items()
                )

            case _ if not isinstance(value, (str, type)) and hasattr(value, "__iter__"):
                if hasattr(value, "__next__"):
                    return map(lambda v: cls(v, base=base, int_format=int_format, repr_mode=repr_mode, namespace=get_namespace(namespace)), value)
                return type(value)(map(lambda v: cls(v, base=base, int_format=int_format, repr_mode=repr_mode, namespace=get_namespace(namespace)), value))

        if isinstance(value, str) and (any(value.startswith(s) and value != s for s in ("=", ":="))):
            if value[0] == "=":
                value = str(cls.compose(value[1:], namespace=get_namespace(namespace)))
            else:  # it's :=
                var_name = value[2:]
                if not var_name.isidentifier():
                    raise ValueError(f"{var_name!r} is not a valid identifier")
                value = str(cls.compose(var_name, namespace=get_namespace(namespace)))
                get_namespace(namespace)[var_name] = cls(value)
        as_int = cls._to_int(value, base)
        if as_int is cls._nan or isinstance(value, str):
            as_str = value
        else:
            if int_format == "" or base != 10:
                if base == 10:
                    as_str = str(as_int)
                else:
                    as_str = cls._to_base(as_int, base)
            else:
                as_str = f"{as_int:{int_format}}"

        self = super().__new__(cls, as_str)
        self._as_int = as_int
        self._this_base = base
        self._this_int_format = int_format
        self._this_repr_mode = repr_mode
        return self

    def __iter__(self):
        yield from self.__class__(super().__iter__())

    def __hash__(self):
        return hash((self.__class__, str(self)))

    def __eq__(self, other):
        if isinstance(other, istr):
            if self.is_int() and other.is_int():
                return self._as_int == other._as_int
        if isinstance(other, str):
            return super().__eq__(other)
        if self.is_int():
            try:
                return self._as_int == int(other)
            except Exception:
                return False
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        match self._this_repr_mode:
            case "istr":
                return f"{self.__class__.__name__}({repr(str(self))})"
            case "int":
                return "?" if self._as_int is self._nan else repr(self._as_int)
            case _:
                return repr(str(self))

    def __bool__(self):
        if self.is_int():
            return bool(self._as_int)
        return bool(str(self))

    def _frepr(self, obj):
        # like repr, but if obj is an istr, the as_repr is not used to make sure the
        # the returned value is istr(...) and not infuenced by the repr mode
        if isinstance(obj, self.__class__):
            return f"{obj.__class__.__name__}({super(istr, obj).__repr__()})"
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
            raise ValueError(f"invalid literal for int(): {self._frepr(self)}")
        return int(self._as_int)

    def __float__(self):
        if not self.is_int():
            raise ValueError(f"invalid literal for float(): {self._frepr(self)}")
        return float(self._as_int)

    def __complex__(self):
        if not self.is_int():
            raise ValueError(f"invalid literal for complex(): {self._frepr(self)}")
        return complex(self._as_int)

    def is_even(self):
        return istr.is_divisible_by(self, 2)

    def is_odd(self):
        return not istr.is_divisible_by(self, 2)

    def is_palindrome(self):
        self_as_str = istr.interpret_as_str(self)
        return self_as_str == self_as_str[::-1]

    def is_non_decreasing(self):
        self_as_str = istr.interpret_as_str(self)
        return all(i0 <= i1 for i0, i1 in zip(self_as_str, self_as_str[1:]))

    def is_non_increasing(self):
        self_as_str = istr.interpret_as_str(self)
        return all(i0 >= i1 for i0, i1 in zip(self_as_str, self_as_str[1:]))

    def is_increasing(self):
        self_as_str = istr.interpret_as_str(self)
        return all(i0 < i1 for i0, i1 in zip(self_as_str, self_as_str[1:]))

    def is_decreasing(self):
        self_as_str = istr.interpret_as_str(self)
        return all(i0 > i1 for i0, i1 in zip(self_as_str, self_as_str[1:]))

    def is_divisible_by(self, divisor):
        return istr.divided_by(self, divisor) is not None

    def divided_by(self, divisor, fallback=None):
        if divisor == 0:
            return fallback
        quotient, remainder = divmod(istr.interpret_as_int(self), int(divisor))
        return istr(quotient) if remainder == 0 else fallback

    def is_prime(self):
        n = istr.interpret_as_int(self)
        if n < 1_000_000:
            return n in istr._primes_up_to_1_000_000_as_set()

        if not n & 1:
            return False

        for x in range(3, int(n**0.5) + 1, 2):
            if n % x == 0:
                return False
        return True

    @classmethod
    def primes(cls, start=None, stop=None, /, length=None, cache=True):
        """
        returns all primes up to a given upperbound or between a given lowerbound and upperbound
        alternatively, the length can be given
        """
        start, stop, step = process_start_stop_step_length(start, stop, 1, length)
        if (cls, "primes", start, stop) in _cache:
            return _cache[cls, "primes", start, stop]

        if stop <= 1_000_000:
            result = in_range(cls._primes_up_to_1_000_000(), start, stop)
        else:
            result = cls._primes(start, stop)
        if cache:
            _cache[cls, "primes", start, stop] = result
        return result

    @classmethod
    def _primes(cls, start, stop):
        sieve = bytearray(b"\x01") * (stop + 1)
        sieve[0:2] = b"\x00\x00"

        for i in range(2, int(stop**0.5) + 1):
            if sieve[i]:
                sieve[i * i : stop + 1 : i] = b"\x00" * (((stop - i * i) // i) + 1)

        return list(map(cls, ([i for i, is_prime in enumerate(sieve) if is_prime and start <= i < stop])))  # range check just to be sure

    @classmethod
    @functools.lru_cache
    def _primes_up_to_1_000_000(cls):
        return cls._primes(0, 1_000_000)

    @classmethod
    @functools.lru_cache
    def _primes_up_to_1_000_000_as_set(cls):
        return set(map(int, cls._primes_up_to_1_000_000()))

    def is_square(self):
        return istr.is_power_of(self, 2)

    def is_cube(self):
        return istr.is_power_of(self, 3)

    def is_power_of(self, exponent):
        n = istr.interpret_as_int(self)
        exponent = check_integer(exponent, "exponent")
        if n < 0:
            if exponent % 2 == 0:
                return False
            else:
                n = -n
        match exponent:
            case 0:
                return n == 1
            case 1:
                return True
            case x if x < 0:
                raise ValueError(f"exponent must be >=0; not {exponent}")
            case _ if n < 1_000_000:
                return n in istr._power_ofs_up_to_1_000_000_as_set(exponent)
            case _:
                ...
        return n == round(n ** (1 / exponent)) ** exponent

    @classmethod
    def squares(cls, start=None, stop=None, /, length=None, cache=True):
        """
        returns all squares up to a given stop or between a given start and stop
        alternatively, the length can be given
        """
        return cls.power_ofs(2, start, stop, length=length, cache=cache)

    @classmethod
    def cubes(cls, start=None, stop=None, /, length=None, cache=True):
        """
        returns all cubes up to a given stop or between a given start and stop
        alternatively, the length can be given
        """
        return cls.power_ofs(3, start, stop, length=length, cache=cache)

    @classmethod
    def power_ofs(cls, exponent, start=None, stop=None, /, length=None, cache=True):
        """
        returns all power of n up to a given stop or between a given start and stop
        alternatively, the length can be given
        """
        start, stop, step = process_start_stop_step_length(start, stop, 1, length)
        exponent = check_integer(exponent, "exponent")

        if (cls, "power_ofs", exponent, start, stop) in _cache:
            return _cache[cls, "power_ofs", exponent, start, stop]
        match exponent:
            case 0:
                if start <= 1 < stop:
                    result = [istr(1)]
                else:
                    result = []
            case 1:
                result = cls(list(range(start, stop)))
            case x if (x % 2 == 0 or start >= 0) and stop <= 1_000_000:
                result = in_range(cls._power_ofs_up_to_1_000_000(exponent), start, stop)
            case _:
                result = cls._power_ofs(exponent, start, stop)
        if cache:
            _cache[cls, "power_ofs", exponent, start, stop] = result
        return result

    @classmethod
    def _power_ofs(cls, exponent, start, stop):
        if exponent % 2 == 0:
            start = max(0, start)
        match exponent:
            case 0:
                if start <= 1 < stop:
                    result = [1]
                else:
                    result = []
            case 1:
                result = [*range(start, stop)]
            case _:
                result = []
                if start < 0:  # can't be the case for even n (because of above limiting)
                    i = -int((-start) ** (1 / exponent))
                else:
                    i = int(start ** (1 / exponent))
                while (i_n := i**exponent) < stop:
                    if i_n >= start:  # just to be sure
                        result.append(i_n)
                    i += 1

        return list(map(cls, result))

    @classmethod
    @functools.lru_cache
    def _power_ofs_up_to_1_000_000(cls, n):
        return cls._power_ofs(n, 0, 1_000_000)

    @classmethod
    @functools.lru_cache
    def _power_ofs_up_to_1_000_000_as_set(cls, n):
        return set(map(int, cls._power_ofs_up_to_1_000_000(n)))

    def decompose(self, letters, namespace=None):
        """
        decompose one-letter variables into global variables
        each one-letter variable must represent just one character
        same one-letter variables represent the the same character
        the istr must have the same length as the letters
        """
        namespace = get_namespace(namespace)

        lookup = {}

        if len(letters) != len(self):
            raise ValueError(f"incorrect number of variables {len(letters)}; should be {len(self)}")

        for letter, ch in zip(letters, self):
            if letter in lookup and lookup[letter] != ch:
                raise ValueError(f"multiple values found for variable {letter}")
            if not letter.isidentifier():
                raise ValueError(f"{repr(letter)} cannot be used as a variable")
            lookup[str(letter)] = ch
        namespace.update(lookup)

    @classmethod
    def compose(cls, letters, namespace=None):
        """
        compose an istr from individual letter variables
        """
        namespace = get_namespace(namespace)
        result = []
        for letter in letters:
            if letter.isidentifier():
                if letter not in namespace:
                    raise ValueError(f"variable {repr(letter)} not defined")
                result.append(str(namespace[letter]))
            else:
                result.append(letter)
        return cls("".join(result))

    def __or__(self, other):
        if isinstance(other, str):
            return self.__class__(str(self).__add__(other))
        else:
            raise TypeError(f"unsupported operand type(s) for |: {self._frepr(self)} and {self._frepr(other)}")

    def __ror__(self, other):
        if isinstance(other, str):
            return self.__class__(other.__add__(str(self)))
        else:
            raise TypeError(f"unsupported operand type(s) for |: {self._frepr(other)} and {self._frepr(self)}")

    def __matmul__(self, other):
        try:
            return self.__class__(super().__mul__(other))
        except Exception:  # TypeError:
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

    def is_consecutive(self):
        s = istr.interpret_as_str(self)
        if len(s) <= 1:
            return False
        c0 = s[0]
        for c1 in s[1:]:
            if ord(c1) - ord(c0) != 1:
                return False
            c0 = c1
        return True

    def is_triangular(self):
        n = istr.interpret_as_int(self)
        if n <= 0:
            return False
        return istr.is_square(n * 8 + 1)

    def reversed(self):
        return self[::-1]

    def ceil(self, divisible_by=1):
        if divisible_by <= 0:
            raise ValueError(f"step has to be >0, not {divisible_by}")
        if divisible_by != int(divisible_by):
            raise ValueError(f"step has to be an integer value, not {divisible_by}")
        n = istr.interpret_as_float(self)
        return istr((math.ceil(n / divisible_by)) * divisible_by)

    def floor(self, divisible_by=1):
        if divisible_by <= 0:
            raise ValueError(f"step has to be >0, not {divisible_by}")
        if divisible_by != int(divisible_by):
            raise ValueError(f"step has to be an integer value, not {divisible_by}")
        return istr((math.floor(self / divisible_by)) * divisible_by)

    def interpret_as_int(self):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as int: {self._frepr(self)}")
            return self._as_int
        if isinstance(self, collections.abc.Iterable) and not isinstance(self, str):
            return int(istr.join(self))

        return int(self)

    def interpret_as_float(self):
        if isinstance(self, istr):
            if not self.is_int():
                raise TypeError(f"not interpretable as float: {self._frepr(self)}")
            return self._as_int
        if isinstance(self, collections.abc.Iterable) and not isinstance(self, str):
            return float(istr.join(self))

        return float(self)

    def interpret_as_str(self):
        if isinstance(self, collections.abc.Iterable) and not isinstance(self, str):
            return istr.join(self)

        return str(self)

    def _str_method(self, name, *args, **kwargs):
        return self.__class__(getattr(super(), name)(*args, **kwargs))

    for name in (
        "capitalize casefold center expandtabs format join ljust lower lstrip partition removeprefix "
        "removesuffix replace rjust rpartition rsplit rstrip split strip swapcase title translate upper zfill"
    ).split():
        locals()[name] = functools.partialmethod(_str_method, name)

    @classmethod
    def zip(cls, *iterables, strict=False, join=False):
        if join:
            return cls.concat(cls(zip(*iterables, strict=strict)))
        else:
            return cls(zip(*iterables, strict=strict))

    @classmethod
    def batched(cls, iterable, n, *, strict=False, join=False):  # will be overridden if in itertools and not Python 3.12
        if n < 1:
            raise ValueError("n must be at least one")
        iterator = iter(iterable)
        while batch := tuple(itertools.islice(iterator, n)):
            if strict and len(batch) != n:
                raise ValueError("istr.batched(): incomplete batch")
            if join:
                yield cls.join(cls(batch))
            else:
                yield cls(batch)

    @classmethod
    def _itertools_method(cls, name, *args, **kwargs):
        return cls(getattr(itertools, name)(*args, **kwargs))

    @classmethod
    def _itertools_join_method(cls, name, *args, join=False, **kwargs):
        res = cls(getattr(itertools, name)(*args, **kwargs))
        return map(cls.join, res) if join else res

    for name in dir(itertools):
        if not name.startswith("_") and not name == "count":  # count has its own method
            match name:
                case "groupby" | "tee":
                    locals()[name] = getattr(itertools, name)
                case "permutations" | "combinations" | "combinations_with_replacement" | "product" | "batched" | "pairwise" | "zip_longest":
                    if name == "batched" and sys.version_info[:2] == (3, 12):
                        continue  # version 3.12 does not support the strict parameter, so, we don't use the itertools method
                    locals()[name] = functools.partialmethod(_itertools_join_method, name)
                case _:
                    locals()[name] = functools.partialmethod(_itertools_method, name)

    def count(*args):
        if len(args) >= 2 and isinstance(args[0], istr):
            return str(args[0]).count(str(args[1]), *map(int, args[2:]))
        else:
            return istr(itertools.count(*args))

    def is_int(self):
        return self._as_int is not self._nan

    def join(self, iterable=None):
        if isinstance(self, istr):
            return self.__class__(str(self).join(iterable))
        if iterable is None:
            return istr("").join(self)
        if not isinstance(self, str):
            raise TypeError(f"{self!r} should be istr, str or iterable, not {type(self)}")
        return istr(self).join(iterable)

    @classmethod
    def concat(cls, iterable):
        return map(cls.join, cls(iterable))

    def prod(self, *, start=1):
        return math.prod(self, start=istr(start))

    @classmethod
    def sumprod(cls, p, q, /, strict=True):
        if "sumprod" in math.__dict__ and strict:
            return cls(math.sumprod(p, q))
        return sum(_map(operator.__mul__, cls(p), cls(q), strict=strict))

    @classmethod
    def enumerate(cls, iterable, start=0):
        for i, value in enumerate(iterable, int(start)):
            yield cls(i), value

    def this_base(self):
        return self._this_base

    def this_int_format(self):
        return self._this_int_format

    def this_repr_mode(self):
        return self._this_repr_mode

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

        def __enter__(self): ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._int_format = self.saved_int_format

    @classmethod
    class repr_mode:
        def __new__(cls, cls_repr_mode, mode=None):
            if mode is None:
                return cls_repr_mode._repr_mode
            if mode is int:
                mode = "int"
            if mode in ("istr", "str", "int"):  # istr is used only for TypeErrors
                return super().__new__(cls)
            raise TypeError(f"mode not 'istr', 'str' or 'int', but {repr(mode)}")

        def __init__(self, cls, mode):
            self.saved_repr_mode = cls._repr_mode
            self.saved_cls = cls
            cls._repr_mode = mode

        def __enter__(self): ...

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

        def __enter__(self): ...

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.saved_cls._base = self.saved_base

    @classmethod
    def range(cls, start=None, stop=None, step=1, /, length=None, base=None, int_format=None, repr_mode=None):
        return _range(cls, start, stop, step, length, base=base, int_format=int_format, repr_mode=repr_mode)

    @classmethod
    def digits(cls, *args):
        """
        return an istr of istr'ed digits as specified with args

        if no args, 0-9 will be used

        all given args will be used
        each arg has to be either null string, <digit>, <digit>-<digit>, <digit>- or -<digit>

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

        result = cls("".join(result))
        cls._digits_cache[key] = result
        return result


def _map(func, *iterables, strict=False):
    """
    like map, but with a strict parameter (also for Python < 3.14)
    """
    if sys.version_info >= (3, 14):
        yield from map(func, *iterables, strict=strict)
        return

    if not strict:
        yield from map(func, *iterables)
        return

    iterators = [iter(it) for it in iterables]

    while True:
        values = []
        exhausted = []
        for it in iterators:
            try:
                v = next(it)
                values.append(v)
                exhausted.append(False)
            except StopIteration:
                values.append(None)
                exhausted.append(True)

        if all(exhausted):
            return

        if any(exhausted) and not all(exhausted):
            raise ValueError("map_strict: iterables have different lengths")

        yield func(*values)


_cache = {}


def in_range(lst, start, stop):
    """
    this function will give all values of lst in the range [start, stop)

    Parameters
    ----------
    lst : list
        must be sorted!

    start : int (or istr)
        lowerbound

    stop : int (or istr)
        non inclusive upperbound

    Returns
    -------
    list of all items in [start, stop)

    Note
    ----
    Equivalent to
    [item for item in lst if start <= item < stop], but more efficient.
    """
    start = int(start)
    stop = int(stop)
    left = bisect.bisect_left(lst, start)
    right = bisect.bisect_left(lst, stop)
    return lst[left:right]


def check_integer(value, value_description):

    if not isinstance(value, numbers.Number):
        try:
            return int(value)
        except TypeError:
            raise ValueError(f"{value_description} should be an integer, not {value}")

    if value != int(value):
        raise ValueError(f"{value_description} should be an integer, not {value}")
    return int(value)


def process_start_stop_step_length(start, stop, step, length):
    if start is None and length is None:
        raise ValueError("no bound(s) or length specified")
    if length is not None:
        if start is not None:
            raise ValueError("both bound(s) and length specified")
        length = check_integer(length, "length")
        if length < 1:
            raise ValueError(f"length must be >=1, not {length}")
        start = 10 ** (length - 1)
        stop = start * 10
    else:
        start, stop = (0, start) if stop is None else (start, stop)
    start = check_integer(start, "start")
    stop = check_integer(stop, "upperbound")
    step = check_integer(step, "step")
    return start, stop, step


def get_namespace(namespace):
    if namespace is None:
        frame = real_caller_frame()
        namespace = frame.f_globals
    return namespace


def real_caller_frame():
    # this will return the frame of the first frame on the stack that does not belong to this module,
    # so in the 'user' space
    frame = inspect.currentframe()
    frame_name = frame.f_globals.get("__name__")
    frame = frame.f_back
    while frame is not None and frame_name == frame.f_globals.get("__name__"):
        frame = frame.f_back
    return frame


istr.type = type(istr(0))


class istrModule(types.ModuleType):
    def __call__(self, *args, **kwargs):
        return istr(*args, **kwargs)

    def __setattr__(self, item, value):
        setattr(istr, item, value)

    def __getattr__(self, item):
        return getattr(istr, item)


if __name__ != "__main__":
    sys.modules["istr"].__class__ = istrModule
