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
resulting in two times `True`. That's because istr instances are treated as int, although they are strings.

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
```
if istr("0"):
    print("True")
else:
    print("False")
```
this will print `False`

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

# Using other values for istr than int or str
Apart from with simple int or str, istr can be initialized with

- if a dict (or subtype of dict), the same type dict will be returned with all values istr"ed

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

# Subclassing istr
When a class is derived from istr, all methods will return that newly derived class. 

E.g.
```
class jstr(istr):
    ...
    
print(repr(jstr(4) * jstr(5)))
```
will print `jstr('20')`

# Test script
There's an extensive pytest script in the \test directory.

This script also shows clearly the ways istr can be used.
