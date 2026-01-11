## changelog of istr | strings you can count on |

#### version 1.1.17  2026-01-11

- some internal changes and added tests
  
#### version 1.1.16  2026-01-10

- introduced `istr.power_ofs`, which can be used to get all numbers up to a given upperbound or between a given lowerbound and upperbound that are a power of a given number, like
  `istr.power_ofs (4, 100)`  returns `[istr('0'), istr('1'), istr('16'), istr('81')]`

- `istr.squares` and `istr.cubes` now delegate to `istr.power_ofs` 

- `istr.primes`, `istr.squares`, `istr.cubes` and `istr.power_ofs` now have a keyword argument cache, which is True by default. If False, the result is not cached.

- `istr.primes`, `istr.squares`, `istr.cubes` and `istr.power_ofs` now have a non inclusive upper bound (in line with Python's common behaviour),

  ```
  istr.squares(16) ==> [istr('0'), istr('1'), istr('4'), istr('9')]  # 16 is excluded
  ```

- `istr.is_divisible_by` now correctly returns False if called with a 0 as divisor.

- error message for `istr.compose` and `istr.decompose` improved.

#### version 1.1.15  2026-01-06

- `istr.squares`, `istr.cubes` and `istr.primes` now caches the result, so it's no problem to call multiple times.

#### version 1.1.14  2026-01-05

- `istr.is_square`, `istr.is_cube` and `istr.is_prime` now uses a (once) precomputed set for numbers <=1_000_000, thus improving performance in many cases.
- Introduced `istr.squares` , `istr.cubes` and `istr.primes` .to get all squares, cubes or primes up to a given upperbound or between a given lowerbound and upperbound:
  `istr.squares (100)` returns a list of all squares <=100
  `istr.squares(50, 100)` return a list of all squares >=50 and <=100
  The same functionality is available for cubes and primes 

#### version 1.1.13  2026-01-04

- `istr.join` may now also be used as a class method, like
  `istr.join(("1", "2", "3"))` ==> `istr("123")` (`""` is applied as separator)

  `istr.join("0", ("1", "2", "3"))` ==> `istr("10203")`)

- Tests for this new functionality have been added.

#### version 1.1.12 | 2025-12-05
- Introduced `is_consecutive()`
  This method checks whether all (string) elements of an istr are consecutive (distance 1):
  `istr(123).is_consecutive()` is True, whereas `istr(124).is_consecutive()` is False.
  Note that this method can also be used for non-istr-s, like `istr.is_consecutive(123)`

- Introduced `is_triangular()`
  This method checks whether a number is a triangular number:
  `istr(6).is_triangular()` is True, whereas `istr(7).is_triangular()` is False.
  Note that this method can also be used for non-istr-s, like `istr.is_triangular(6)`

#### version 1.1.11 | 2025-11-15
- A new way to compose an istr from global one-letter variables is introduced: by starting a string with := as an argument to istr, the rest of the argument will be used to compose the istr from the one-letter variables, just like when the string started with =.
  But, now, the evaluated will also be assigned to a variable composed of the names of the one-letter variables. E.g.
  
  ```
  x=4
  y=7
  if istr(":=xy").is_prime():
      print(f"{xy=}")  
  ```
  This will print `xy=47`. This is particularly useful when combined with peek.
  
#### version 1.1.10 | 2025-11-14
- From now on, when istr() is applied to an istr, the current base, repr_mode and int_format will be used to determine the representation.
  This can be handy to reformat an istr.
- istr now has three more keyword arguments: `base`, `int_format` and `repr_mode`. So these attributes can now be set easily on an individual instance.
  So, `repr(istr(12, base==36))` is  `istr('C')`
- `istr.range` now has three more keyword arguments: `base`, `int_format` and `repr_mode`.
  So, `list(istr.range(4, base=2))` is `[istr('0', istr('1'), istr('10'), istr('11')`
- The `base`, `int_format` and `repr_mode` of an istr can now be queried with the methods `this_base()`, `this_int_format` and `this_repr_mode`. E.g.
  `istr(12, base=36).this_base()` is 36 and
- The builtins `float()` and `complex()` now support istr-s as well.


#### version 1.1.9 | 2025-11-09
- The namespace keyword argument now propagates to embedded istr-s.
  So, for instance

  ```
  x, y, z = 1, 2, 3
  istr(["=xy", "=yz"])
  ```
  evaluates to `[istr("12"), istr("23")]`
  
  And
  ```
  istr(["=xy", "=yz"], namespace=dict(x=3, y=4, z="z")
  ```
  evaluates to `[istr("34"), istr("4z")]`

  For more examples, see the test suite.

- `istr("=")` now evaluates to an istr with one = character, rather than compose to an empty istr.

- In the test suite, the variables `minus_one` to `thirteen` are now explicitly defined, instead of via a clever patch loop. This is to avoid excessive ruff warnings reported.

- Bug in `istr.__eq__()` made that peek crashed when peeking a non-int istr. Fixed.

#### version 1.1.8 | 2025-11-08
Introduced `istr.prod()`, which is equivalent to `math.prod()`, but results in an istr.
Thus, `istr.prod(range(1,5))` is `istr(24)`
And `istr.prod((1,2,3), start=4)` is also `istr(24)`.

It is also possible to apply `prod` on an istr:
`istr(1234).prod()` is `istr(24)`
`istr("123").prod(start=4)` is `istr(24)`



Introduced `istr.sumprod()`, which is equivalent to `math.sumprod()`, but applies  istr to both iterables.
Note that this method is available even in Python < 3.12 .
Thus, `istr.sumprod("12", (3,4))` is `istr(11)`
In contrast to `math.sumprod()`, `istr.sumprod()` supports a `strict` parameter (True by default)
Thus, `istr.sumprod("12", (3,4,5), strict=False)` is `istr(11)`, whereas `istr.sumprod("12", (3,4,5))` 
raises a ValueError. 



Python 3.7 is no longer supported. So, from now on Python >= 3.8 is required.

#### version 1.1.7 | 2025-11-06

A new way to compose an istr from global one-letter variables is introduced: by starting a string with = as an argument to istr, the rest of the argument will be used to compose the istr  from the one-letter variables:

```
x=4
y=7
z=0
assert istr("=xyz") == istr.compose("xyz")
```

Not so much a change in istr, but a remark: To decompose an istr into individual variables, istr.decompose() can be used,
But it is arguably easier and safer to unpack the istr, like
```
a, b, c = istr(934)
```
, which is functionally equivalent to
```
istr(934).decompose("abc")
```
#### version 1.1.6 | 2025-11-05

Refactored `istr.is_square`(),  `istr.is_cube()`,  `istr.is_power_of()`,  `istr.is_odd()`,  `istr.is_even()`,  `istr.is_prime()` and `istr.is_disible_by()`.

#### version 1.1.5 | 2025-11-04

Added `istr.is_cube()` and `istr.is_power_of()`.

Internal change: `is_square()` now delegates to `istr._is_power_off`, which is used also for `istr.is_cube()` and `istr.is_power_of()`.

#### version 1.1.4 | 2025-10-26

Introduced compose and decompose methods.

With `decompose`, one-letter global variables can be set from an istr, e.g.
```
istr(934).decompose("abc")
```
will result in the global variables a=9, b=3 and c=4.

With `compose`, an istr will be constructed based on the values of one letter global variables, e.g.
```
x=4
y=7
z=0
s = istr.compose("xyz")
```
will assign istr(470) to s.

#### version 1.1.3 | 2025-03-09

Readme updated

#### version 1.1.2 | 2024-11-07

At last, the short form of importing (`import istr`) works properly!

#### version 1.1.1 | 2024-11-06

The new way of importing istr didn't work properly. So, importing should be done with from `istr import istr` (again).

#### version 1.1.0 | 2024-11-03

With this version is possible to just use
`import istr`
instead of
`from istr import istr`

All functionality is maintained.

The only functional difference is that istr cannot be use as a type in subclassing anymore. In order to still be able to subclass, use istr.type instead. So

```
class jstr(istr.type):
   ...
```

#### version 1.0.12 | 2024-08-06

The methods `istr.is_even`, `istr.is_odd`, `istr.is_square`, `istr.is_prime` and `istr.is_divisible_by` can now also be used with an ordinary int. E.g.:

```
istr.is_even(4) ==> True
istr.is_odd(4) ==> False
istr.is_square(4) ==> True
istr.is_prime(4) ==> False
istr.is_divisible_by(4, 2) ==> True
```

#### version 1.0.11 | 2024-08-05

Introduced `istr.is_square` and `istr.is_prime` methods. Examples:

```
istr(4).is_square() ==> True
istr(5).is_square()) ==> False

istr(4).is_prime() ==> False
istr(5).is_prime()) ==> True
```

#### version 1.0.9 | 2024-06-15

Introduced `istr.is_divisible_by`  method.
For example:

```
    istr(18).is_divisible_by(3) ==> True
    istr(18).is_divisible_by(istr(3)) ==> True
    istr(19).is_divisible_by(3) ==> False
    istr(19).is_divisible_by(istr(3)) == False   
```

#### version 1.0.8 | 2024-06-01
Instead of using istr in the internal methods _int_method and _str_method, the proper class is now used.
This makes inheriting from istr more correct.

#### version 1.0.7 | 2024-05-29
When comparing istrs with <=, <, > and >= the type of the result is now bool, instead of istr,
which is more logical.

#### version 1.0.6 | 2024-05-29
All methods in itertools are now available directly from istr.
For example:

```
list(istr.repeat(1, 4)) ==> [istr('1'), istr('1'), istr('1'), istr('1')]
next(istr.count(3)) ==> istr('3')
```

This can be handy as these methods don't have to be imported from itertools anymore.

Added tests for these new class methods.

#### version 1.0.5 | 2024-05-24
Serious bug with caching istr.digits() fixed.
Added tests for properly caching istr.digits().

#### version 1.0.4 | 2024-05-24
Serious bug with the or (|) operator fixed.
Added tests for the or (|) operator.

#### version 1.0.3 | 2024-05-13
The class istr.range is now immutable.

The dunder int methods that were previously all defined separately are now defined with
a simple loop that uses partialmethod (this does not change the functionality in any way).

The string methods that were previously all defined separately are now defined with
a simple loop that uses partialmethod (this does not change the functionality in any way).

Generating TypeError messages for incompatible types is now direct (via _frepr method) instead of
with a tricky force_repr boolean.

The in operator now relies on the __contains__ method inherited from str (in other words
it is not overridden anymore).

#### version 1.0.2 | 2024-05-08

When a string that can't be interpreted as an int is created when istr.repr_mode is 'int', the repr of that file will be `?` (was: `nan`):

```
with istr.repr_mode('int'):
    a = istr('abc')
print(a)
```

will print

```
?
```

#### version 1.0.1 | 2024-05-07

From now on, the changelog is not anymore part of the istr.py file, but is in a separate `changelog.md` file.

`istr.digits` now also supports the letters from *A* through *Z*, making it possible to generate digits for bases >10.

```
  istr.digits('-z') ==> istr('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  istr.digits('A-F') ==> istr('ABCDEF')
  istr.digits('C') ==> istr('C')
```

Note that the default stop value is *9* when the start is a numeric digit.
If start is a letter, the default stop value is *Z*. So

```
  istr.digits('3-') ==> istr('34567879')
  istr.digits('X-') ==> istr('XYZ')
```

Technical detail: caching digits is now implemented with a custom cache dict instead of lru_cache to be able to include _base, _int_format and _int_repr_mode in the key.



Introduced a new method: `all_distinct`.

This can be handy for quite a few puzzles.

```
  istr('01234').all_distinct() ==> True
  istr('012340').all_distint() ==> False
  istr('thequickbrown').all_distinct() ==> True
```

#### version 1.0.0 | 2024-05-06

With this version, istrs do not have to be interpretable as an int anymore.
Only when arithmetic and friends are to be carried with an istr, that's a requirement.

So now we can say

```
  a = istr('1 2 3')
  print(a.split())
```

and get

```
  [istr('1'), istr('2'), istr('3')]
```

But

```
  a = istr('1 2 3')
  b = a + 1
```

will raise

```
  TypeError: unsupported operand for +: istr('1 2 3') and 1
```

  It is possible to check whether an istr can be interpreted as an int with the `is_int` method:

```
  a = istr('1 2 3')
  print(a.is_int()) 
```

will give

```
  False 
```

This also means that there is no reason for `istr('')` to be interpreted as *0*. So it isn't anymore.

And `reversed()` now also works with negative numbers, although the result can't be used in calculations.



The method / context manager `format` has been renamed to `int_format`.



The bool method now operates on the *string* if it can not be interpreted as an *int*.

That means that `bool(istr(''))` is `False`. For any other istr where is_int() is True, bool will be True.

#### version 0.2.0 | 2024-04-30

Added `__iter__` method .

So now,

```
    for c in istr('123'):
        ...
```

results in c values that are istrs 



Added `istr.digits` method:

#### Examples

```
istr.digits() ==> istr('0123456789')
istr.digits('') ==> istr('0123456789')
istr.digits('1') ==> istr('1')
istr.digits('3-') ==> istr('3456789')
istr.digits('-3') ==> istr('0123')
istr('1-4', '6', '8-9') ==> istr('1234689')
istr.digits('1', '1-2', '1-3') ==> istr('112123')
```

  Note that a digit can occur more than once.

#### version 0.1.2  | 2024-04-26  

Added all relevant string methods to return istrs or data structures with istrs.

Added corresponding tests.

#### version 0.1.0  | 2024-04-22  

Changed the way `istr.range` is implemented.



Changed the context manager `istr.format()` to be used directly without the with statement.

Also, now `istr.format()` works without any argument and then returns the current format.



istr class now uses `__slots__`.



All internal values and methods now start with an underscore.



Introduced `istr.repr_mode()`



Introduced `istr.base()`



Extended tests for new functionality

#### version 0.0.8  |2024-04-18  

initial version with changelog
