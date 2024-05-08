 <img src="https://www.salabim.org/istr_logo.png" width=500>

### Introduction

With  `istr` is possible to interpret strings as if they were integers.

This can be very handy for solving puzzles, but also for other purposes.
For instance the famous send more money puzzle, where each letter has to be replaced by a unique digit (0-9)

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
        print(f' {s|e|n|d}')
        print(f' {m|o|r|e}')
        print('-----')
        print(f'{m|o|n|e|y}')
```

Of, if we want to add all the digits in a string:

```
sum_digits = sum(istr('9282334'))  # answer 31
```

And the module is a demonstration of extending a class (str) with extra and changed functionality.

### Installation
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

### Usage
#### Start

Just start with

```
from istr import istr
```

#### Use istrs as if the were int

We can define an istr:
```
four = istr('4')
five = istr('5')
```
The variables `four`  and `five` can now be used as if they were int:

```
twenty = four * five
```
, after which x is `istr('20')`

The same can be done with

```
twenty = 4 * five
```

or

```
twenty = four * 5
```

And now `twenty` can be used as if it was an int as well. So

```
twenty - four
```

is `istr('16')`

We can do all the usual arithmetic operations on istrs, e.g.

```
-four + (twenty / 2)
```

is `istr('6')`

And we can test for equality. So:

```
twenty == 20
```
is True.

But istrs are also strings. So

```
twenty == '20'
```

is also True!

For the order comparisons (<=, <, >, >=), the istr is always interpreted as an int:

That means that  both
```
twenty < 30
twenty >= '10' # here '10' is converted to 10 for the comparison
```
are `True`.

In contrast to an ordinary string
```
print(four + five)
```
prints `9`, as istr are treated as ints (if possible).

Please note that `four`  could have also been initialized with
```
four = istr(4)
```
or even
```
four, five = istr(4, 5)
```

##### Important
>
> All calculations are strictly integer calculations. That means that if a float or decimal variable is ever produced it will be converted to an int.
> Also divisions are always floor divisions!

#### Use istrs as string

We should realize that istrs are in fact strings.

In order to concatenate two istrs (or an istr and a str), we cannot use the `+` operator (remember `four + five` is `istr('9')`).

In order to concatenate istrs,  we use the or operator (`|`). So

```
four | five
```
will be `istr(`45`).

And
```
(four | five) / 3
```
is `istr('9')`.

In order to repeat a string in the usual sense, you cannot use the `*` operator (remember `3 * four` is `istr(12)`. 

In order to repeat we use the matrix multiplication operator (`@`). So

 `3 @ four`

 is `istr('444')`

And 

```four @ 3```

is also `istr('444')`

##### Note

>
> It is not allowed to use the `@` operator for two istrs. So, `four @ five` raises a TypeError.
#### istrs that can't be interpreted as an int


Although usualy, istrs are to be interpreted as an int, that's not a requirement.

So

```
istr('abc')
```

or

```
istr('1,2,3')
```

are accepted.

But, we can't do any arithmetic with them. 

If we try

```
istr('abc') + 5
```

a `TypeError` will be raised.

That holds for any arithmetic we try.

If we want to test if an istr can be interpreted (and thus used in an arithmetic expression). we can use the `is_int()` method. So

```ìstr(20).is_int()```

is `True`, whereas

```ìstr('abc').is_int()```

is `False`.



The `bool` operator works normally on the integer value of an istr. So

`bool(istr('0'))` ==> `False`
`bool(istr('1'))` ==> `True`

If the istr can't be interpreted as an int, the string value will be used to test. So

`bool(istr('abc'))` ==> `True`
`bool(istr(''))` ==> `False`

#### Other operators

For the `in` operator, an istr is treated as an ordinary string, although it is possible to use ints as well:

```
'34' in istr(1234)
34 in istr(1234)

```
On the left hand side an istr is always treated as a string:
```
istr(1234) in '01234566890ABCDEF'
```

Sorting a list of istrs is based on the integer value, not the string. So

```
' '.join(sorted('1 3 2 4 5 6 11 7 9 8 10 12 0'.split()))
```

is

```
'0 1 10 11 2 3 4 5 6 7 8 9'
```

,whereas

```
' '.join(sorted(istr('1 3 2 4 5 6 11 7 9 8 10 12 0'.split()))
```

is 

```
'0 1 2 3 4 5 6 7 8 9 10 11'
```
#### Using values that are neither string or numeric to initialize istr

Apart from with numeric (to be interpreted as an int) or str, istr can be initialized with
several other types:


- if a dict (or subtype of dict), the same type dict will be returned with all *values* istr'ed

- if an iterator, the iterator will be mapped with istr

- if an iterable, the same type will be returned with all elements istr'ed

```
    istr([0, 1, 4]) ==> [istr('0'), istr('1'), istr('4')]
    istr((0, 1, 4)) ==> (istr('0'), istr('1'), istr('4'))
    istr({0, 1, 4}) ==> `{istr('4'), istr('0'), istr('1')}  # or similar  
```

- if a range, an istr.range instance will be returned
  
```
  istr(range(3)) ==> istr.range(3)
  list(istr(range(3))) ==> [istr('0'), istr('1'), istr('2')]
  len(istr(range(3))) ==> 3
```

- if an istr.range instance, the same istr.range will be returned

- if an istr, the same istr will be used

  ```
    istr(istr('4')) ==> istr ('4')
  ```

#### More than one parameter for istr
It is possible to give more than one parameter, in which case a tuple
of the istrs of the parameters will be returned, which can be handy
to unpack multiple values, e.g.

```
a, b, c = istr(5, 6, 7) ==> a=istr('5') , b=istr('6'), c=istr('7') 
```

#### test for even/odd
It is possible to test for even/odd (provided the istr can be interpreted as an int) with the

`is_even` and `is_odd` method, e.g.

```
istr(4).is_even()) ==> True
istr(5).is_odd()) ==> True
```
#### test whether all characters are distinct

With the `all_distinct` method, it is possible to test whether all characters are distinct (i.e. no character appearts more than once).

```
istr('01234').all_distict() ==> True
istr('012340').all_distict() ==> False
n98 = istr(98)
n100 = n98 + 2
istr(n98).all_distinct() ==> True
istr(n100).all_distinct() ==> False
```

#### reverse an istr

The method `istr.reversed()` will return an istr with the reversed content:
```
istr(456).reversed() ==> istr('654')
istr('0456').reversed() ==> istr('6540')
```
The same can -of course- be achieved with
```
istr(456)[::-1] ==> istr('654')
istr('0456')[::-1] ==> istr('6540')
```
##### Note
>
> It is possible to reverse a negative istr, but the result can't be interpreted as an int anymore.
>
> ```
> istr(-456).reversed() ==> TypeError
> ```

#### enumerate with istrs

The `istr.enumerate` method can be used just as the builtin enumerate function.
The iteration counter however is an istr rather than an int. E.g. 

```
for i, c in istr.enumerate('abc'):
    print(f'{repr(i)} {c}')
```
prints
```
istr('0') a
istr('1') b
istr('2') c
```

#### concatenate an iterable

The `istr.concat` method can be useful to map all items of an iterable
to `istr` and then concatenate these.

`

```
list(istr.concat(((1,2),(3,4))) ==> istr([12,34])
list(istr.concat(itertools.permutations(range(3),2))) ==> 
    [istr('01'), istr('02'), istr('10'), istr('12'), istr('20'), istr('21')] 
```

#### generate istr with digits

The class method `digits` can be used to return an istr of digits according to a given specification.
The method takes either no or a number of arguments.

If no arguments are given, the result will be `istr('0123456789')`.

The given argument(s) result in a range of digits.

- `<n>` ==> n
- `<n-m>` ==> n, n+1, ..., m
- `-n>` ==> 0, 1, ... n
- `n->` ==> n, n+1, ..., 9 if n is numeric (0-9), n, n+1, ... Z if n is a letter
- `'-'` ==> 0, 1, ..., 9
- `''` ==> 0, 1, ..., 9

(n and m must be digits between 0 and 9 or letters letters between A and Z)

When no stop value is specified, it will be

* 9 if the start value is between 0 and 9
* Z if the start value is between A and Z 

The final result is an istr composed of the given range(s).

Here are some examples:

```
istr.digits() ==> istr('0123456789')
istr.digits('') ==> istr('0123456789')
istr.digits('1') ==> istr('1')
istr.digits('3-') ==> istr('3456789')
istr.digits('-3') ==> istr('0123')
istr('1-4', '6', '8-9') ==> istr('1234689')
istr('1', '1-2', '1-3') ==> istr('11213')
istr.digits('-z') ==> istr('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
istr.digits('A-F') ==> istr('ABCDEF')
istr.digits('C') ==> istr('C')
istr.digits('3-') ==> istr('34567879')
istr.digits('X-') ==> istr('XYZ')
```


#### Subclassing istr
When a class is derived from istr, all methods will return that newly derived class. 

E.g.
```
class jstr(istr):
    ...
    
print(repr(jstr(4) * jstr(5)))
```
will print `jstr('20')`

#### Changing the way repr works

It is possible to control the way an `istr` instance will be repr'ed.

By default, `istr(5)` is represented as `istr('5')`.

With the `istr.repr_mode()` context manager, that can be changed:
```
with istr.repr_mode('str'):
    five = istr(5)
    print(repr(five))
with istr.repr_mode('int'):
    five = istr(5)
    print(repr(five))
with istr.repr_mode('istr'):
    five = istr(5)
    print(repr(five))
```
This will print
```
'5'
5
istr('5')
```
If the repr_mode is `'int'` and the istr can't be interpreted as an int the string `?` will be returned:

```
 with istr.repr_mode('int'):
    abc = istr('abc')
    print(repr(abc))
```

This will print

```
?
```

##### Note
>
> The way an `istr` is represented is determined at initialization.

It is also possible to set the repr mode without a context manager:

```
istr.repr_mode('str')
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

#### Changing the base system

By default, `istr` works in base 10. However it is possible to change the base system with the `istr.base()` context manager / method.

Any base between 2 and 36 may be used.

Note that the integer is **always** stored in base 10 mode, but the string
representation will reflect the chosen base (at time of initialization).

Some examples:
```
with istr.base(16):
    a = istr('7fff')
    print(int(a))

    b = istr(127)
    print(repr(b))
```
This will result in
```
32767
istr('7F')
```
All calculations are done in the decimal 10 system.

Note that the way an `istr` is interpreted is determined at initialization.

It is also possible to set the repr mode without a context manager:
```
istr.base(16)
print(int(istr('7fff')))
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

#### Changing the format of the string

When an  istr is initialized with a string the istr will be always stored as such.

```
repr('4')) ==> istr('4')
repr(' 4')) ==> istr(' 4')
repr('4  ')) ==> istr('4  ')
```

For initializing with an int (or other numeric) value, the string is by default simply the str representation

```
repr(4)) ==> istr('4')
```

With the `istr.int_format()` context manager this behavior can be changed.
If the format specifier is a number, most likely a single digit, that
will be the minimum number of characters in the string:

```
with istr.int_format('3'):
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
with istr.int_format('03'):
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

##### Note
>
> For bases other than 10, the string will never be reformatted!

### Overview of operations

The table below shows whether the string or the int version of istr is applied.

```
operator/function   int  str   Example
-----------------------------------------------------------------------------------------
+                    x         istr(20) + 3 ==> istr('23')
_                    x         istr(20) - 3 ==> istr('17')
*                    x         istr(20) * 3 ==> istr('60')
/                    x         istr(20) / 3 ==> istr('6')
//                   x         istr(20) // 3 ==> istr('6')
%                    x         istr(20) % 3 ==> istr('2')
divmod               x         divmod(istr(20), 3) ==> (istr('6'), istr('2'))
**                   x         istr(2) ** 3 ==> istr('8')
@                         x    istr(20) @ 3 ==> istr('202020')
==                   x    x    istr(20) == 20 ==> True | istr(20) == '20' ==> True
|                         x    istr(20) | 5 ==> istr('205')
abs                  x         abs(istr(-20)) ==> istr('20')
bool                 x    x *) bool(istr(' 0 ')) ==> False | istr('') ==> False
<=, <, >, >=         x         istr('100') > istr('2') ==> True
slicing                   x    istr(12345)[1:3] ==> istr('23')
iterate                   x    [x for x in istr(20)] ==> [istr('2'), istr('0')
len                       x    len(istr(' 20 ')) ==> 4
count                     x    istr(100),count('0') ==> 2
index                     x    istr(' 100 ').index('0') ==> 2
split                     x    istr('1 2').split() ==> (istr('1'), istr('2'))
other string methods      x    istr('aAbBcC').lower() ==> istr('aabbcc')
                               istr('aAbBcC').islower() ==> False
                               istr('  abc   ').strip() ==> istr('abc')
-----------------------------------------------------------------------------------------
*) str is applied if is_int() is False
```
### Test script
There's an extensive pytest script in the `\tests` directory.

This script also shows clearly the ways istr can be used, including several edge cases. Highly recommended to have a look at.



### Badges
![PyPI](https://img.shields.io/pypi/v/istr-python) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/istr-python) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/istr-python)

![PyPI - License](https://img.shields.io/pypi/l/istr-python) ![Black](https://img.shields.io/badge/code%20style-black-000000.svg) 
![GitHub last commit](https://img.shields.io/github/last-commit/salabim/istr)
