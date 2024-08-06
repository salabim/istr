## changelog of istr | strings you can count on |

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
