<img src="https://www.salabim.org/istr_logo.png" width=500>

# Introduction

The istr module has exactly one class: istr.

With this it is possible to interpret strings as if they were integers.

This can be very handy for solving puzzles, but also for other purposes. For instance the
famous send more money puzzle
```
  S E N D
  M O R E
--------- +
M O N E Y
```
can be nicely, albeit not very efficient, coded as:
```
import itertools
from istr import istr

for s, e, n, d, m, o, r, y in istr(itertools.permutations(range(10), 8)):
    if m and ((s|e|n|d) + (m|o|r|e) == (m|o|n|e|y)):
        print(f" {s|e|n|d}")
        print(f" {m|o|r|e}")
        print("-----")
        print(f"{m|o|n|e|y}")
```

And it is a nice demonstration of extending a class (str) with extra and changed functionality.

# Installation
Installing istr with pip is easy.
```
$ pip install istr-python
```
or when you want to upgrade,
```
$ pip install istr-python --upgrade
```
Alternatively, istr.py can be just copied into you current work directory from GitHub (https://github.com/salabim/istr).

No dependencies!

# Usage
Just start with

```
from istr import istr
```

Now we can define some istrs:
```
four = istr("4")
five = istr("5")
```
Then we can do
```
x= four * five
```
, after which x is `istr("20")`

And now we can do
```
print(x == 20)
print(x == "20")
```
resulting in two times `True`. That's because istrs instances are treated as int, although they are strings.

That means that we can also say
```
print(x < 30)
print(x >= "10")
```
again resulting in two times `True`.

In contrast to an ordinary string
```
print(four + five)
```
prints `9`, as istr are treated as ints.

Please note that `four` and `five` could have also be initialized with
```
four = istr(4)
five = istr(5)
```
or even
```
four, five = istr(4, 5)
```

But how can we concatenate istrs? Just use the or operator (|): 
```
print(four | five)
```
will output `45`.

And the result is again an istr.

That means that
```
(four | five) / 3
```
is `istr("9")`.

In order to repeat a string in the usual sense, you cannot use `3 * four`, as that woud be `12`. 

We use the matrix multiplication operator (@) for this. So `3 @ four` is `444`. As is `four @ 3`.

Also allowed are
```
abs(four)
-four 
```

The bool operator works on the integer value of an istr. So
`bool("0")` ==> `False`
`bool("1")` ==> `True`
The code
```
if istr("0"):
    print("True")
else:
    print("False")
```
will print `False`

For the in operator, an istr is treated as an ordinary string, although it is possible to use ints as well:
```
"34" in istr(1234)
34 in istr(1234)
```
On the left hand side an istr is always treated as a string:
```
istr(1234) in "01234566890ABCDEF"
```

Note that all calculations are strictly integer calculations. That means that if a float variale is ever produced it will be converted to an int.
Also divisions are always floor divisions!

There's a special case for `istr("")`. This is a proper empty string, but also represents the value of 0.
That is to allow for `istr("").join(i for i in "01234)"`, resulting in `istr("01234")`.

Sorting a list of istrs is based on the integer value, not the string. So

`" ".join(sorted("1 3 2 4 5 6 11 7 9 8 10 12 0".split()))`

is

`"0 1 10 11 2 3 4 5 6 7 8 9"`

,whereas

`" ".join(sorted(istr("1 3 2 4 5 6 11 7 9 8 10 12 0".split())))`

is 

`"0 1 2 3 4 5 6 7 8 9 10 11"`

# Using other values for istr than numeric value or str
Apart from with simple numeric (to be interpreted as an int) or str, istr can be initialized with
several other types:

- if a dict (or subtype of dict), the same type dict will be returned with all values istr'ed

    `istr({0: 0, 1: 1, 2: 4})` ==> `{0: istr("0"), 1: istr("1"), 2: istr("4")}`

- if an iterator, the iterator will be mapped with istr

    `istr(i * i for i in range(3))` ==> `<map object>`

    `list(istr(i * i for i in range(3)))` ==> `[istr("0"), istr("1"), istr("4")]`

- if an iterable, the same type will be returned with all elements istr'ed

    `istr([0, 1, 4])` ==> `[istr("0"), istr("1"), istr("4")]`

    `istr((0, 1, 4))` ==> `(istr("0"), istr("1"), istr("4"))`

    `istr({0, 1, 4})` ==> `{istr("4"), istr("0"), istr("1")} # or similar`

- if a range, an istr.range instance will be returned
    
    `istr(range(3))` ==> `istr.range(3)`

    `list(istr(range(3)))` ==> `[istr("0"), istr("1"), istr("2")]`

    `len(istr(range(3)))` ==> `3`

- if an istr.range instance, the same istr.range will be returned

# More than one parameter for istr
It is possible to give more than one parameter, in which case a tuple
of the istrs of the parameters will be returned, which can be handy
to unpack multiple values, e.g.

`a, b, c = istr(5, 6, 7)` ==> `a=istr("5") , b=istr("6"), c=istr("7")`

# test for even/odd
It is possible to test for even/odd with the

`is_even` and `is_odd` method, e.g.

```
print(istr(4).is_even())
print(istr(5).is_odd())
```
This will print `True` twice.

# reverse an istr
The method `istr.reversed()` will return the an istr with the reversed content:
```
print(repr(istr(456).reversed()))
print(repr(istr("0456").reversed()))
```
result:
```
istr("654")
istr("6540")
```
The same can -of course- be achieved with
```
print(repr(istr(456)[::-1]))
print(repr(istr("0456")[::-1]))
```
Note that is impossible to reverse a negative istr.

# enumerate with istrs

The `istr.enumerate` method can be used just as the builtin enumerate function.
The iteration counter however is an istr rather than an int. E.g. 
```
    for i,c in istr.enumerate("abc"):
        print(f"{repr(i)} {c}")
```
prints
```
istr('0') a
istr('1') b
istr('2') c
```

# concatenate an iterable

The `istr.concat1 method can be useful to map all items of an iterable
to `istr` and then concatenate these.

`list(istr.concat(((1,2),(3,4)))` ==> `istr([12,34])`

`list(istr.concat(itertools.permutations(range(3),2)))` ==> `[istr('01'), istr('02'), istr('10'), istr('12'), istr('20'), istr('21')]` 

# Subclassing istr
When a class is derived from istr, all methods will return that newly derived class. 

E.g.
```
class jstr(istr):
    ...
    
print(repr(jstr(4) * jstr(5)))
```
will print `jstr('20')`

# Changing the way repr works

It is possible to control the way an `istr` instance will be repr'ed.

By default, the `istr('5')` is represented as `istr('5')`.

With the istr.repr_mode() context manager, that can be changed:
```
with istr.repr_mode("str"):
    five = istr('5')
    print(repr(five))
with istr.repr_mode("int"):
    five = istr('5')
    print(repr(five))
with istr.repr_mode("istr"):
    five = istr('5')
    print(repr(five))
```
This will print
```
'5'
5
istr('5')
```
Note that the way an `istr` is represented is determined at initialization.

It is also possible to set the repr mode without a context manager:

```
istr.repr_mode("str")
five = istr('5')
print(repr(five))
```
This will print
```
'5'
```
Finally, the current repr mode can be queried with `istr.repr_mode()`. So upon start:
```
print(repr(istr.repr_mode()))
```
will output `istr`.

# Changing the base system

By default, `istr` works in base 10. However it is possible to change the base system with the `istr.base()` context manager / method.

Any base between 2 and 36 may be used.

Note that the integer is always stored in base 10 mode, but the string
representation will reflect the chosen base (at time of initialization).

Some examples:
```
with istr.base(16):
    a = istr("7fff")
    print(int(a))

    b = istr(15)
    print(repr(b))
```
This will result in
```
32767
istr('F')
```
All calculations are done in the decimal 10 system.

Note that the way an `istr` is interpreted is determined at initialization.

It is also possible to set the repr mode without a context manager:
```
istr.base(16)
print(int(istr("7fff")))
```
This will print
```
32767
```
Finally, the current base can be queried with `istr.base()`, so upon start:
```
print(istr.base())
```
will result in `10`.

# Changing the format of the string

By default, `istr` does not change the way an istr is stored when a str is to initialize:

`repr('4'))` ==> `istr('4')`

`repr(' 4'))` ==> `istr(' 4')`

`repr('4  '))` ==> `istr('4  ')`

For initializing with an int (or other numeric) value, the string is simply the str representation

`repr(4))` ==> `istr('4')`

With the `istr.format()` context manager this behavior can be changed.
If the format specifier is a number, most likely a single digit, that
will be the minimum number of characters in the string:
```
with istr.format("3"):
    print(repr(istr(1)))
    print(repr(istr(12)))
    print(repr(istr(123)))
    print(repr(istr(1234)))
```
will print
```
istr('  1')
istr(' 12')
istr('123')
istr('1234')
```
If the string starts with a `0`, the string will be zero filled:
```
with istr.format("03"):
    print(repr(istr(1)))
    print(repr(istr(12)))
    print(repr(istr(123)))
    print(repr(istr(1234)))
```
will print
```
istr('001')
istr('012')
istr('123')
istr('1234')
```
Note that if a format other than the default `''` is used, the string will reformatted even if the `istr` is specified with a string:
```
with istr.format("03"):
    print(repr(istr("  12 ")))
```
will result in `istr('0012')`

Remark: For bases other than 10, the string will never be reformatted!

# Test script
There's an extensive pytest script in the `\tests` directory.

This script also shows clearly the ways istr can be used.

![PyPI](https://img.shields.io/pypi/v/istr) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/istr) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/istr)

![PyPI - License](https://img.shields.io/pypi/l/istr) ![Black](https://img.shields.io/badge/code%20style-black-000000.svg) 
 ![GitHub last commit](https://img.shields.io/github/last-commit/salabim/istr)