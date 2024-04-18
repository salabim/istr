from functools import partial
import math
import contextlib

#   _       _
#  (_) ___ | |_  _ __
#  | |/ __|| __|| '__|
#  | |\__ \| |_ | |
#  |_||___/ \__||_|    use strings as integers

__version__ = "0.0.8"

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
            a, b, c = istr(5, 6, 7) ==> a=istr("5") , b=istr("6"), c=istr("7")
"""

    _format = ""

    @classmethod
    def toint(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"unable to convert {repr(value)} to int")

    @classmethod
    def check_format(cls, format):
        if format is None:
            return cls._format
        if not (isinstance(format, str) and all(x in "0123456789" for x in format)):
            raise ValueError(f"{repr(format)} is incorrect format")
        return format

    def __new__(cls, *value):
        if len(value) == 0:
            raise TypeError("no parameter given")
        if len(value) == 1:
            value = value[0]  # normal case of 1 parameter
        if isinstance(value, range):
            return cls.range(value.start, value.stop, value.step)
        if isinstance(value, dict):
            return type(value)((k, cls(v)) for k, v in value.items())
        if not isinstance(value, (str, type)) and hasattr(value, "__iter__"):
            if hasattr(value, "__next__") or type(value) == range:
                return map(partial(cls), value)
            return type(value)(map(partial(cls), value))
        if value == "":
            asstr = ""
            asint = 0
        else:
            asint = cls.toint(value)
            if cls._format == "":
                if isinstance(value, str):
                    asstr = value
                else:
                    asstr = str(asint)
            else:
                asstr = f"{asint:{cls._format}}"

        self = super().__new__(cls, asstr)
        self.asint = asint
        return self

    def __hash__(self):
        return hash((self.__class__, str(self)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.asint == other.asint
        if isinstance(other, str):
            return super().__eq__(other)
        try:
            return self.asint == self.toint(other)
        except Exception:
            return False

    def __ne__(self, other):
        return not self == other

    def __contains__(self, other):
        return super().__contains__(str(other))

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __le__(self, other):
        return self.asint <= self.toint(other)

    def __lt__(self, other):
        return self.asint < self.toint(other)

    def __ge__(self, other):
        return self.asint >= self.toint(other)

    def __gt__(self, other):
        return self.asint > self.toint(other)

    def __bool__(self):
        return bool(self.asint)

    def __add__(self, other):
        return self.__class__(self.asint + self.toint(other))

    def __sub__(self, other):
        return self.__class__(self.asint - self.toint(other))

    def __mul__(self, other):
        return self.__class__(self.asint * self.toint(other))

    def __floordiv__(self, other):
        return self.__class__(self.asint // self.toint(other))

    def __rfloordiv__(self, other):
        return self.__class__(self.toint(other) // self.asint)

    def __truediv__(self, other):
        return self.__class__(self.asint // self.toint(other))

    def __rtruediv__(self, other):
        return self.__class__(self.toint(other) // self.asint)

    def __pow__(self, other):
        return self.__class__(self.asint ** self.toint(other))

    def __rpow__(self, other):
        return self.__class__(self.toint(other) ** self.asint)

    def __radd__(self, other):
        return self.__class__(self.toint(other) + self.asint)

    def __rsub__(self, other):
        return self.__class__(self.toint(other) - self.asint)

    def __rmul__(self, other):
        return self.__class__(self.toint(other) * self.asint)

    def __mod__(self, other):
        return self.__class__(self.asint % self.toint(other))

    def __rmod__(self, other):
        return self.__class__(self.toint(other) % self.asint)

    def __or__(self, other):
        return self.__class__("".join((self, self.__class__(other))))

    def __ror__(self, other):
        return self.__class__("".join((self.__class__(other), self)))

    def __int__(self):
        return int(self.asint)

    def __round__(self):
        return self.__class__(round(self.asint))

    def __trunc__(self):
        return self.__class__(math.trunc(self.asint))

    def __floor__(self):
        return self.__class__(math.floor(self.asint))

    def __ceil__(self):
        return self.__class__(math.ceil(self.asint))

    def __matmul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rmatmul__(self, other):
        return self.__class__(super().__rmul__(other))

    def __divmod__(self, other):
        return self.__class__(divmod(self.asint, self.toint(other)))

    def __rdivmod__(self, other):
        return self.__class__(divmod(self.toint(other), self.asint))

    def __neg__(self):
        return self.__class__(-self.asint)

    def __pos__(self):
        return self

    def __abs__(self):
        return self.__class__(abs(self.asint))

    def is_even(self):
        return self.asint % 2 == 0

    def is_odd(self):
        return self.asint % 2 == 1

    def join(self, iterable):
        s = super().join(iterable)
        return self.__class__(s)

    def reversed(self):
        return self[::-1]

    def __getitem__(self, key):
        return self.__class__(super().__getitem__(key))

    @classmethod
    def enumerate(cls, iterable, start=0):
        for i, value in enumerate(iterable, start):
            yield cls(i), value

    @classmethod
    @contextlib.contextmanager
    def format(cls, format):
        saved_format = cls._format
        cls._format = cls.check_format(format)
        yield
        cls._format = saved_format

    @classmethod
    def default_format(cls, format=None):
        if format is not None:
            cls._format = cls.check_format(format)
        return cls._format

    @classmethod
    class range:
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


def main():
    for i,c in istr.enumerate("abc"):
        print(f"{i!r} {c}")

if __name__ == "__main__":
    main()
