## changelog of istr | strings you can count on |

#### For the full documentation, see www.salabim.org/istr .

#### version 1.1.40 2026-07-21

- Introduced the method `long_multiplication`, which gives a list of all lines to do a long multiplication.

  E.g. `print(istr.long_multiplication(1234,567)` will print 

  `[istr('1234'), istr('567'), istr('8638'), istr('7404'), istr('6170'), istr('699678')]`
  
  The method has an optional parameter `as_str`, that can be used t0 get a nice representation of the long multiplication lines.
  
  E.g. `print(istr.long_multiplication(1234,567, as_str=True)` will print
  ```
    1234
     567
  ------ x
    8638
   7404
  6170
  ------
  699678  
  ```
  
- Introduced the method `long_division`, which gives a list of all lines to do a long division (note that the divisor and dividend count as separate lines).

  E.g. `print(istr.long_division(1395, 45)` will print 

  [istr('31'), istr('45'), istr('1395'), istr('135'), istr('45'), istr('45'), istr('0')]
  
  The method has an optional parameter `as_str`, that can be used to get a nice representation of the long division lines.
  
  E.g. `print(istr.long_division(1395, 45, as_str=True)` will print 
  ```
         31
       ----
  45 ) 1395
       135
       ---
         45
         45
         --
          0
  ```
  
  ```
  
  ```

#### version 1.1.39 2026-07-19

- The method `long_sqrt`, does not insert a trailing 0 anymore.

- The method `long_sqrt`, now has an optional parameter `as_str`, that can be used to get a nice string representation of the long square root lines.
  
  E.g. `print(istr.long_sqrt(123 ** 2, as_str=True))` will print
  ```
    1 2 3
    -----
  \/15129
    1
    -
     51
     44
     --
      729
      729
      ---
        0 
  ```
  
#### version 1.1.38 2026-07-18

- Introduced the method `long_sqrt`, which is gives a list of  the lines of a long square root. Both the result (root) and the original number, possibly with a trailing 0 are returned, along with the calculated values.
  E.g. `istr.long_sqrt(123 ** 2)` results in
  
  `[istr('123'), istr('15129'), istr('1'), istr('51'), istr('44'), istr('729'), istr('729'), istr('0')]`
  
#### version 1.1.37 2026-07-13

- Introduced the method `sum`, which is equivalent to the builtin sum function. It is primarily used to be similar to the `prod` method.
  ```
  istr(1234).sum() ==> istr('10')
  istr.sum(1234) ==> istr('10')
  istr.sum('1234') ==> istr('10')
  ```

#### version 1.1.36 2026-06-29

- Introduced the methods `sqrt`, `cbrt`, `nth_root` to provide the square root, cubic root and nth root of an istr. If there is no integer root, the fallback value (default `istr('0')` will be returned.

  ```
  istr(64).sqrt() ==> istr('8')
  istr(65).sqrt() ==> istr('0')
  istr(1234**3).cbrt() ==> istr('1234')
  istr(1234**3+1).cbrt() ==> istr('0')
  istr(1234**5).nth_root(5) ==> istr('1234')
  istr(1234**5+1).nth_root(5) ==> istr('0')
  istr(1234**5+1).nth_root(5, 1) ==> istr('1')
  istr(1234**5+1).nth_root(5, None) ==> None
  
  istr.sqrt(64) ==> istr('8')
  ```
	- `istr(None)` is now `None` (was: `istr('None')) 

#### version 1.1.35 2026-06-28

- The fallback value for `divided_by` is now `istr('0')`, instead of `istr('')`.

- `is_power_of` can now also be called without an exponent. In that case, True will be returned if the given value is a perfect power, False otherwise.
  
  ```
  istr(2**10).is_power_of() ==> True
  istr(-3**3).is_power_of() ==> True
  istr(34).is_power_of() ==> False
  ```
  
- Introduced `divisors`, which will generate all divisors of a number.
  Normally, the divisors are sorted, but if the sorted flag is False, the order is not necessarily maintained (this is slightly more efficient).
  ```
  istr(18).divisors() ==> [istr('1'), istr('2'), istr('3'), istr('6'), istr('9'), istr('18')]
  istr(19).divisors() ==> [istr('1'), istr('19')]  
  istr(18).divisors(sorted=False) ==> [istr('1'), istr('18'), istr('2'), istr('9'), istr('3'), istr('6')]  
  ```
  This method can also be used with an int. E.g.:  
  ```
  istr.divisors(18) ==> [istr('1'), istr('2'), istr('3'), istr('6'), istr('9'), istr('18')]
  istr.divisors(19) ==> [istr('1'), istr('19')]  
  istr.divisors(18, False) ==> [istr('1'), istr('18'), istr('2'), istr('9'), istr('3'), istr('6')]  
  ```

#### version 1.1.34 2026-06-20

- Introduced `istr.getitem`, which is essentially, a safe version of indexing an istr.
  If the index is within the bounds of the istr, `getitem` just works like indexing. Otherwise, where normally an IndexError would be raised, the fallback value (default istr('')) will be returned.
  Note that the result will always be istr-ed, except when fallback is None.
  
  Examples:
  ```
  istr(1234).getitem(2) ==> istr('3')
  istr(1234).getitem(-2) ==> istr('3')
  istr(1234).getitem(5) ==> istr('')
  istr(1234).getitem(5, '0') ==> istr('0')
  istr(1234).getitem(5, None) ==> None
  ```
  This method can also be used with a str. E.g.:
  ```
  istr.getitem('1234', 2) ==> istr('3')
  istr.getitem('1234', -2) ==> istr('3')
  istr.getitem('1234', 5) ==> istr('')
  istr.getitem('1234',5, '0') ==> istr('0')
  istr.getitem('1234',5, None) ==> None
  ```
  Note that this method has also the advantage that it can accept an istr as index, in contrast to normal indexing.

- The fallback value for `divided_by` is now `istr('')`, instead of `None`. Also the result is always istr-ed, except for None.

#### version 1.1.33 2026-06-13

- `istr.primes`, `istr.squares`, `istr.cubes` and `istr.power_ofs` now have a keyword only parameter `length`, that can be used instead of of bound(s). E.g.
  ```
  print(*istr.squares(length=2))
  print(*istr.cubes(length=2) )
  print(*istr.power_ofs(5,length=4)   )
  print(*istr.primes(length=2))
  ```
  will print
  ```
  16 25 36 49 64 81
  27 64
  1024 3125 7776
  11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97  
  ```
  It is not allowed to specifiy both bound(s) and length.
  
- `istr.primes`, `istr.squares`, `istr.cubes` and `istr.power_ofs now check more aggresively if parameters are correct.

- `istr.range` now also support a keyword only parameter `length`, that can be used instead of bound(s):
  
  ```
  print(*istr.range(length=2))
  ```
  will print
  ```
  10 11 12 13 ... 98 99
  ```
  It is not allowed to specify both bound(s) and length.

#### version 1.1.32 2026-06-02

- `istr.is_consecutive` now also accepts an iterable, which is joined prior to the test (see 1.1.31).
- `istr.permutations`, `istr.combinations`, `istr.combinations_with_replacement`, `istr.product`, `istr.pairwise`, `istr.zip_longest` and `istr.batched` now have a keyword argument `join`, which is False by default. If False, the methods just produce an iterable returning tuples. If True, the tuples are joined to make an istr. E.g.
  ```
  for s in istr.product('12', '34'):
      print(s)
  ```
  results in
  ```
  (istr('1'), istr('3'))
  (istr('1'), istr('4'))
  (istr('2'), istr('3'))
  (istr('2'), istr('4'))
  ```
  , whereas
  ```
  for s in istr.product('12','34', join=True):
      print(s)
  ```
  results in
  ```
  istr('13')
  istr('14')
  istr('23')
  istr('24')
  ```
- `istr.batched` is now available for Python < 3.12. And under Python 3.12 `istr.batched` now also supports the strict flag. 
- Introduced `istr.zip`, which is the equivalent of the zip builtin, but applies istr to each element. `istr.zip` also supports the join parameter:
  ```
  print(list(istr.zip('12', '345')))
  print(list(istr.zip('12', '345', join=True)))
  print(list(istr.zip('12', '345', strict=True)))
  ```
  results in
  ```
  [(istr('1'), istr('3')), (istr('2'), istr('4'))]
  [istr('13'), istr('24')]
  ValueError: zip() argument 2 is longer than argument 1
  ```

#### version 1.1.31 2026-05-20

- `istr.is_odd`, `istr.is_even`, `istr.is_divisible_by`, `istr.is_square`, `istr.is_cube`,  `istr.is_power_of`, `istr.is_triangular`, `istr.is_palindrome`, `istr.is_increasing`, `istr.is_non_decreasing`, `istr.is_decreasing` and `istr.is_non_increasing` now also accepts an iterable, which is joined prior to the test.
   This is particularly useful to filter tuples yielded from permutations, combinations and products.
   So, now we can do
   
   ```
   map(istr.join,filter(istr.prime, istr.combinations(range(10),2)))
       ==> istr('02'), istr('03'), ... istr('89')
   ```
   
#### version 1.1.30 2026-05-19

- Introduced `istr.ceil` to find he smallest integer, divisible by a given number (divisible_by), greater than or equal to the value. 
  This can be useful to step through all multiples of n, >= m, like:

  ```
  for i in istr.range(istr(1000/3, 10000, 3)) ==> # 1002, 1005, ... 9999
  for i in istr.count(int(istr,ceil(1000/3)), 3))  ==> 1002, 1005, ...
  ```
  Examples:

  ```
  istr(1000).ceil() ==> 1000 # divisible_by is 1 by default
  istr(1000).ceil(2) ==> 1000
  istr(1000).ceil(3) ==> 1002
  ```

  It is also possible to use the ceil method for floats or ints:

  ```
  istr.ceil(1000.2) ==> 1001
  istr.ceil(1000.2, 2)  ==> 1002
  istr.ceil(1000.2, 3 ==> 1002
  ```

- Introduced  `istr.floor`to find the largest integer, divisible by a given number (divisible_by), smaller than or equal to the value.

  Examples:

  ```
  istr(1000).floor() ==> 1000 # divisible_by is 1 by default
  istr(1000).floor(2) ==> 1000
  istr(1000).floor(3) ==> 999
  ```

  It is also possible to use the ceil method for floats or ints:

  ```
  istr.floor(1000.2) ==> 1000
  istr.floor(1000.2, 2)  ==> 1000
  istr.floor(1000.2, 3 ==> 999
  ```

#### version 1.1.29 2026-05-17

- `istr.compose` now correctly handles strings that contain letters that can't be identifiers. These letters are left as is in the resulting string.
  So:
  
  ```
  x = 1
  y = 0
  _ = "_"
  istr.compose("xy") ==> istr("10")
  istr.compose("10=(xy)") ==> istr("10=(10)")
  istr.compose("x_000)") ==> istr("1_000")
  istr.compose("z") ==> ValueError
  
  istr("=xy") ==> istr("10")
  istr("=10=(xy)") ==> istr("10=(10)")
  istr("=x_000)") ==> istr("1_000")
  istr("=z") ==> ValueError
  ```
  

#### version 1.1.28 2026-03-22

- Introduced `istr.is_increasing()`, `istr.is_decreasing()`, `istr.is_non_increasing()` and `istr.is_non_decreasing()`
  So:
  
  ```
  istr(1223).is_increasing() ==> False
  istr(1223).is_non_decreasing() ==> True
  istr(3221).is_decreasing() ==> False
  istr(3221).is_non_increasing ==> True
  ```
  It is also possible to test for 'increasingness' and friends for anything that can be converted to a str:
  ```
  istr.is_increasing(123) ==> True  
  ```

#### version 1.1.27 2026-03-12
- In contrast to the readme, `istr.count` did not work on istr, but instead used always the itertools count.
  This has been fixed. So, now it is possible to do:
  
  ```
  istr(100).count(0) ==> 2
  istr(100).count(0, 1) ==>2
  istr(100).count("a") ==> 0
  ```
  If called like `istr.count()`, the itertools version is used:
  ```
  istr.count() ==> istr('0'), istr('1'), istr('2'), ...
  istr.count(10) ==> istr('10'), istr('11'), istr('12'), ...
  istr.count(10,3) ==> istr('10'), istr('13'), istr('16'), ...
  ```
  Note that `istr.count(istr(10))` results in `istr('10'), istr('11'), istr('12'), ...`, but
  `istr.count(istr(10),1)` is in fact the str version and thus returns `1`.

#### version 1.1.26 2026-03-08
- Introduced `istr.is_palindrome()` to check whether an istr is palindromic:
```
istr(12321).is_palindrome() ==> True
istr('aba').is_palindrome() ==> True
istr(123).is_palindrome() ==> False
```
It is also possible to test for a palindrome for anything that can be converted to a str:
```
istr.is_palindrome(121) ==> True
istr.is_palindrome('no devil lived on') ==> True
istr.is_palindrome(min) ==> False
```

#### version 1.1.25 2026-02-17

- Internal change: caller frame now assessed via the new 'standard' function real_caller_frame()

#### version 1.1.24 2026-01-27

-  `__new__` reorganized (now uses match/case)

-  an istr can now be initialized with any expression, even if it can't be evaluated as an int, like `5 + 6j` or `min` . Or course, these istr-s can't be used as int.

-  the `repr` of an istr is not set upon initialization, but rather be constructed when required, resulting in faster initialization.

- getting namespace is now more reliable.

#### version 1.1.23 2026-01-24

- Python 3.10 is now a minimum requirement (because match/case statements are now used).

- `istr.primes` did not work properly for lower or upper bounds that were an istr. Fixed.

- optimized `istr,primes`, `istr.squares`, `istr.cubes` and `istr.power_ofs` for upper bounds up to 1_000_000 .

- the `start` parameter of `istr.enumerate` could not be an `istr`. Fixed.


#### version 1.1.21 2026-01-21

- `istr.power_ofs` now correctly supports negative lower and upper bounds.
- `istr.is_power_of` now correctly supports negative values.

#### version 1.1.20 2026-01-20

- `istr.compose` now also accepts digits. So
  
  ```
  a=1
  b=2
  print(istr.compose('ab3'))
  print(istr('=a9'))
  print(istr('=9a'))
  print(istr(':=a9'))
  print(a9)
  print(istr(':=9a'))
  ```
  will print
  ```
  123
  19
  91
  19
  19
  ValueError: '9a' is not a valid identifier
  ```

#### version 1.1.19  2026-01-17

- `istr.divided_by`has a new parameter, *fallback* which will be retured if the (integer) division is not possible. The default is None.
  
  ```
  istr(19).divided_by(3) ==> None
  istr(19).divided_by(3, 0) ==> 0
  ```
  
#### version 1.1.18  2026-01-16

- introduced `istr.divided_by`, which will return None if not divisible by the given divisor, otherwise the result of the division. Example:
  
  ```
  istr(18).divided_by(3) ==> 6
  istr(19).divided_by(3) ==> None
  ```
  
  So, it combines `is_divisible_by` and the actual division.
  
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

- `istr.squares`, `istr.cubes` and `istr.primes` now caches the result, so it's no problem to call multiple times. The caching can be disabled with the `cache=False` parameter

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
