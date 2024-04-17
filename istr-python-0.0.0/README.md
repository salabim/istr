# Introduction

The istrlib module has exactly one class: istr.

With this it is possible to interpret string as if they were integers. This can be very handy for solving 
puzzles, but also for other purposes.

# Installation
Installing istrlib with pip is easy.
```
$ pip install istrlib
```
or when you want to upgrade,
```
$ pip install istrlib --upgrade
```

Alternatively, istrlib.py can be just copied into you current work directory from GitHub (https://github.com/salabim/istrlib).

No dependencies!

# Usage
Just start with

```
from istrlib import istr
```

Now we can define some istrs:
```
four = istr("4")
five = istr("5")
```
Them we can do
```
x= four * five
```
, after which x is `istr("40")`

And now we can do
```
print(x == 40)
print(x == "40")
```
resulting in two times `True`. That's because istr instances are treated as int, although they are strings.

That means that we can also say
```
print(x < 50)
print(x >= "30")
```
again resulting in two times `True`.

In contrast to an ordinary string
```
print(four + five)
```
prints `9`, as istr are treated as ints.

So, how can we concatenate istrs? Just use the or operator (|): 
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

In order to multiply a string in the usual sense, you cannot use `3 * four`, as that will be `12`. 

We use the matrix multiplication operator (@) for this. So `3 @ four` is `444`.

Also allowed are
```
abs(four)
-four 
```

For the in operator a istr is treated as an ordinary string, although it is possible to use ints as well:
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
That is to allow for istr("").join(i for i in "01234"

Sorting a list of istrs is based on the integer value, not the string. So

`' '.join(sorted('1 3 2 4 5 6 11 7 9 8 10 12 0'.split()))`

is

`'0 1 10 11 2 3 4 5 6 7 8 9'`

,whereas

`' '.join(sorted(istr('1 3 2 4 5 6 11 7 9 8 10 12 0'.split())))`

is 

`'0 1 2 3 4 5 6 7 8 9 10 11'`

