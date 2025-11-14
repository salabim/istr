import math
import itertools
import os
import sys
import re

if __name__ == "__main__":  # to make the tests run without the pytest cli
    import os, sys  # three lines to use the local package and chdir

    os.chdir(os.path.dirname(__file__))
    sys.path.insert(0, os.path.dirname(__file__) + "/../" + os.path.dirname(__file__).split(os.sep)[-2])

import pytest

import istr

istr.equals = lambda self, other: type(self) is type(other) and (str(self) == str(other))
# this method tests whether self and other are exactly the same

minus_one = istr(-1)
zero = istr(0)
one = istr(1)
two = istr(2)
three = istr(3)
four = istr(4)
five = istr(5)
six = istr(6)
seven = istr(7)
eight = istr(8)
nine = istr(9)
ten = istr(10)
eleven = istr(11)
twelve = istr(12)
thirteen = istr(13)
one_to_twelve = istr.range(1, thirteen)


def test_arithmetic():
    assert two + three == "5"
    assert two + three == five
    assert 2 + three == five
    assert two + 3 == five

    assert two - three == "-1"
    assert two - three == minus_one
    assert 2 - three == minus_one
    assert two - 3 == minus_one

    assert two * three == "6"
    assert two * three == six
    assert 2 * three == six
    assert two * 3 == six

    assert twelve // three == "4"
    assert twelve // three == four
    assert 12 // three == four
    assert twelve // 3 == four

    assert twelve / three == "4"
    assert twelve / three == four
    assert 12 / three == four
    assert twelve / 3 == four

    assert thirteen / three == "4"
    assert thirteen / three == four
    assert 13 / three == four
    assert thirteen / 3 == four

    assert twelve % five == 2
    assert twelve % 5 == 2
    assert 12 % five == 2

    assert twelve % five == "2"
    assert twelve % 5 == "2"
    assert 12 % five == "2"

    assert two**three == "8"
    assert two**3 == "8"
    assert 2**three == "8"


def test_lt():
    assert type(two < three) is bool
    assert two < three
    assert 2 < three
    assert two < 3

    assert not three < two
    assert not 3 < two
    assert not three < 2

    assert not two < two
    assert not 2 < two
    assert not two < 2


def test_le():
    assert type(two <= three) is bool
    assert two <= three
    assert 2 <= three
    assert two <= 3

    assert two <= two
    assert 2 <= two
    assert two <= two


def test_gt():
    assert type(three > two) is bool
    assert three > two
    assert 3 > two
    assert three > 2

    assert not two > three
    assert not 2 > three
    assert not two > 3

    assert not three > three
    assert not 3 > three
    assert not three > 3


def test_ge():
    assert type(three >= two) is bool
    assert three >= two
    assert 3 >= two
    assert three >= 2

    assert three >= three
    assert 3 >= three
    assert three >= three


def test_eq():
    assert two == istr("2")
    assert two == 2
    assert two == "2"
    assert 2 == two
    assert "2" == two

    assert not two == "ab"
    assert not two == istr


def test_ne():
    assert not two != istr("2")
    assert not two != 2
    assert not two != "2"
    assert not 2 != two
    assert not "2" != two

    assert two != "ab"
    assert two != istr


def test_order():
    assert " ".join(sorted(("1 2 5 4 100 10").split())) == "1 10 100 2 4 5"  # just to see the difference
    assert " ".join(sorted(istr(("1 2 5 4 100 10").split()))) == "1 2 4 5 10 100"


def test_concat():
    c = list(istr.concat(((1, 2), (3, 4))))
    assert c == istr(["12", "34"])
    c = list(istr.concat(itertools.permutations(range(3), 2)))
    assert c == [istr("01"), istr("02"), istr("10"), istr("12"), istr("20"), istr("21")]


def test_range():
    assert one_to_twelve == istr.range("1", "13")
    assert one_to_twelve == istr.range(one, thirteen, one)
    assert one_to_twelve == istr(range(1, 13))

    assert len(one_to_twelve) == 12
    assert 2 in one_to_twelve
    assert "2" in one_to_twelve
    assert two in one_to_twelve

    assert 13 not in one_to_twelve
    assert "13" not in one_to_twelve
    assert thirteen not in one_to_twelve

    assert one_to_twelve[2] == 3
    assert one_to_twelve[2] == "3"
    assert one_to_twelve[2] == three

    assert one_to_twelve[2:4] == istr.range(3, 5)

    with pytest.raises(IndexError):
        one_to_twelve[12]
        
    assert str(list(istr.range(5, base=2, repr_mode='str'))) == "['0', '1', '10', '11', '100']"


def test_misc():
    assert istr("") == ""
    assert istr("") != 0

    assert istr(istr(6)) == "6"
    assert istr(" 12 ") == " 12 "
    with istr.int_format("03"):
        assert istr("   12  ") == "   12  "
        assert istr("") == ""


def test_divmod():
    assert divmod(eleven, three) == (istr(3), istr(2))
    assert divmod(11, three) == (istr(3), istr(2))
    assert divmod(eleven, 3) == (istr(3), istr(2))
    assert divmod(11, 3) == (3, 2)  # just for reference


def test_iter():
    assert [x for x in istr.range(3)] == [istr(0), istr(1), istr(2)]


def test_reversed():
    assert [x for x in reversed(istr.range(3))] == [istr(2), istr(1), istr(0)]


def test_lazy():
    for x in istr.range(10000000000000000000000000):
        if x == four:
            break
    assert x == 4

    for x in istr(range(10000000000000000000)):
        if x == four:
            break
    assert x == 4


def test_str_repr():
    assert one.equals(istr("1"))
    assert str(one) == "1"
    assert f"{one}" == "1"
    assert repr(one_to_twelve) == "istr.range(1, 13)"
    assert repr(istr.range(10)) == "istr.range(0, 10)"
    assert repr(istr.range(one, two, three)) == "istr.range(1, 2, 3)"

    assert str(one_to_twelve) == "istr.range(1, 13)"
    assert str(istr.range(10)) == "istr.range(0, 10)"
    assert str(istr.range(one, two, three)) == "istr.range(1, 2, 3)"


def test_index():
    assert (one_to_twelve.index(2)) == 1
    assert (one_to_twelve.index(two)) == 1
    assert (one_to_twelve.index("2")) == 1
    with pytest.raises(ValueError):
        one_to_twelve.index(13)
    with pytest.raises(ValueError):
        one_to_twelve.index(thirteen)
    with pytest.raises(ValueError):
        one_to_twelve.index("13")


def test_count():
    assert one_to_twelve.count(2) == 1
    assert one_to_twelve.count(two) == 1
    assert one_to_twelve.count("2") == 1
    assert one_to_twelve.count(13) == 0
    assert one_to_twelve.count(thirteen) == 0
    assert one_to_twelve.count("13") == 0


def test_hash():
    assert hash(istr.range(1, 13)) == hash(one_to_twelve)
    assert hash(istr.range(1, 12)) != hash(one_to_twelve)


def test_int_format():
    assert istr(" 1 ") == " 1 "
    with istr.int_format("0"):
        assert istr(" 1 ") == " 1 "
    with istr.int_format("03"):
        assert istr(1) == "001"
        assert istr(1234) == "1234"
    with istr.int_format("3"):
        assert istr(1) == "  1"
        assert istr(1234) == "1234"
    with istr.int_format(""):
        assert istr(1234) == "1234"
    with istr.int_format("003"):
        assert istr(1) == "001"
    with pytest.raises(ValueError):
        with istr.int_format(" 1"):
            ...
    with pytest.raises(ValueError):
        with istr.int_format("1 "):
            ...
    with pytest.raises(ValueError):
        with istr.int_format("a"):
            ...
    with pytest.raises(ValueError):
        with istr.int_format(1):
            ...
    with istr.int_format("0"):
        assert istr(" 3 ") == " 3 "
    assert istr.int_format() == ""
    istr.int_format("03")
    assert istr.int_format() == "03"
    assert istr("  8 ") == "  8 "
    istr.int_format("")
    assert istr(" 8 ") == " 8 "


def test_range_int_format():
    r = istr.range(11)
    assert repr(r) == "istr.range(0, 11)"
    assert " ".join(r) == "0 1 2 3 4 5 6 7 8 9 10"

    with istr.int_format("02"):
        r = istr.range(11)
        assert " ".join(r) == "00 01 02 03 04 05 06 07 08 09 10"
    r = istr.range(11, int_format="03")
    assert " ".join(r) == "000 001 002 003 004 005 006 007 008 009 010"


def test_even_odd():
    assert istr(1).is_odd()
    assert not istr(1).is_even()

    assert istr(12345678).is_even()
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_odd()
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_even()

    assert istr.is_odd(1)
    assert not istr.is_even(1)
    assert istr.is_even(12345678)
    assert istr.is_odd(11111111)


def test_is_divisible_by():
    assert istr(18).is_divisible_by(3)
    assert istr(18).is_divisible_by(istr(3))
    assert not istr(19).is_divisible_by(3)
    assert not istr(19).is_divisible_by(istr(3))
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_divisible_by(3)
    assert istr.is_divisible_by(18, 3)
    assert not istr.is_divisible_by(19, 3)


def test_is_square():
    assert not istr(-1).is_square()
    assert istr(0).is_square()
    assert istr(1).is_square()
    assert not istr(2).is_square()
    assert istr(4).is_square()
    assert istr(16).is_square()
    assert not istr(99).is_square()
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_square()
    assert istr.is_square(0)
    assert istr.is_square(1)
    assert not istr.is_square(2)
    assert istr.is_square(4)
    assert istr.is_square(16)


def test_is_cube():
    assert not istr(-1).is_cube()
    assert istr(0).is_cube()
    assert istr(1).is_cube()
    assert not istr(2).is_cube()
    assert istr(8).is_cube()
    assert istr(27).is_cube()
    assert not istr(99).is_cube()
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_cube()
    assert istr.is_cube(0)
    assert istr.is_cube(1)
    assert not istr.is_cube(2)
    assert istr.is_cube(8)
    assert istr.is_cube(27)


def test_is_power_of():
    assert not istr(-1).is_power_of(3)
    assert istr(0).is_power_of(3)
    assert istr(1).is_power_of(3)
    assert not istr(2).is_power_of(3)
    assert istr(8).is_power_of(3)
    assert istr(27).is_power_of(3)
    assert not istr(99).is_power_of(3)
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_power_of(3)
    assert istr.is_power_of(0, 3)
    assert istr.is_power_of(1, 3)
    assert not istr.is_power_of(2, 3)
    assert istr.is_power_of(8, 3)
    assert istr.is_power_of(27, 3)
    with pytest.raises(TypeError):
        istr(1).is_power_of(3.1)
    with pytest.raises(ValueError):
        istr(1).is_power_of(-1)


def test_is_prime():
    assert not istr(0).is_prime()
    assert not istr(1).is_prime()
    assert istr(2).is_prime()
    assert istr(3).is_prime()
    assert not istr(4).is_prime()
    assert istr(97).is_prime()
    assert not istr(99).is_prime()
    with pytest.raises(TypeError, match=re.escape(f"not interpretable as int")):
        istr("a").is_prime()
    assert not istr.is_prime(0)
    assert not istr.is_prime(1)
    assert istr.is_prime(2)
    assert istr.is_prime(3)
    assert not istr.is_prime(4)
    assert istr.is_prime(97)
    assert not istr.is_prime(99)


def test_join():
    s = "".join(istr(("4", "5", "6")))
    assert s == "456"
    assert type(s) is str

    s = istr("").join(("4", "5", "6"))
    assert s == "456"
    assert s == 456
    assert type(s) is istr.type

    s = istr("").join(istr(("4", "5", "6")))
    assert s == "456"
    assert s == 456
    assert type(s) is istr.type

    s = istr("").join(istr(("", "", "6")))
    assert s == "6"
    assert s == 6
    assert type(s) is istr.type


def test_or():
    assert (eleven | twelve).equals(istr("1112"))
    assert ("11" | twelve).equals(istr("1112"))
    assert (eleven | "12").equals(istr("1112"))
    with pytest.raises(TypeError):
        11 | twelve
    with pytest.raises(TypeError, match=re.escape("unsupported operand type(s) for |: 11 and istr('12')")):
        11 | twelve
    with pytest.raises(TypeError, match=re.escape("unsupported operand type(s) for |: istr('11') and 12")):
        eleven | 12


def test_matmul():
    assert (five @ 3).equals(istr("555"))
    assert (3 @ five).equals(istr("555"))

    with pytest.raises(TypeError):
        three @ five
    with pytest.raises(TypeError):
        three @ "5"
    with pytest.raises(TypeError):
        "3" @ five


def test_is_int():
    for operator in "+ - * / // % **".split():
        with pytest.raises(TypeError, match=re.escape(f"unsupported operand for {operator}: istr('a') and 1")):
            eval(f"istr('a'){operator}1")
        with pytest.raises(TypeError, match=re.escape(f"unsupported operand for {operator}: 1 and istr('a')")):
            eval(f"1{operator}istr('a')")
    for operator in "<= < > >=".split():
        with pytest.raises(TypeError, match=re.escape(f"unsupported operand for {operator}: istr('a') and 1")):
            eval(f"istr('a'){operator}1")
        roperator = {"<": ">", ">": "<"}[operator[0]] + operator[1:]
        with pytest.raises(TypeError, match=re.escape(f"unsupported operand for {roperator}: istr('a') and 1")):
            eval(f"1{operator}istr('a')")
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for divmod: istr('a') and 2")):
        divmod(istr("a"), 2)
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for divmod: 2 and istr('a')")):
        divmod(2, istr("a"))
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for round: istr('a')")):
        round(istr("a"))
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for trunc: istr('a')")):
        math.trunc(istr("a"))
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for floor: istr('a')")):
        math.floor(istr("a"))
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for ceil: istr('a')")):
        math.ceil(istr("a"))
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for abs: istr('a')")):
        abs(istr("a"))
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for +: istr('a')")):
        +istr("a")
    with pytest.raises(TypeError, match=re.escape(f"unsupported operand for -: istr('a')")):
        -istr("a")
    with pytest.raises(TypeError):
        istr("a").is_odd()
    with pytest.raises(TypeError):
        istr("a").is_even()
    assert istr(1).is_int()
    assert not istr("a").is_int()

    with pytest.raises(TypeError, match=f"istr"):
        istr("a") + 1
    with pytest.raises(TypeError, match=f"istr"):
        with istr.repr_mode("int"):  # error message should not use the standard repr
            istr("a") + 1
    with pytest.raises(TypeError, match=f"istr"):
        with istr.repr_mode("str"):  # error message should not use the standard repr
            istr("a") + 1


def test_str():
    assert repr(str(five)) == "'5'"
    assert f"|{istr(1234):6}|" == "|1234  |"
    with pytest.raises(ValueError):
        f"{istr(1234):d}"


def test_bool():
    assert bool(istr(0)) is False
    assert bool(istr(1)) is True
    assert bool(istr("0")) is False
    assert bool(istr("a")) is True
    assert bool(istr("")) is False


def test_trunc_and_friends():
    assert math.trunc(one).equals(istr("1"))
    assert math.ceil(one).equals(istr("1"))
    assert math.floor(one).equals(istr("1"))
    assert round(one).equals(istr("1"))


def test_data_structures():
    assert istr(list(range(1, 4))) == [istr("1"), istr("2"), istr("3")]
    assert istr(tuple(range(1, 4))) == (istr("1"), istr("2"), istr("3"))
    assert istr(set(range(1, 4))) == {istr(1), istr(2), istr(3)}

    assert list(istr(range(1, 4))) == [istr("1"), istr("2"), istr("3")]

    assert list(istr.enumerate("abc")) == [(istr("0"), "a"), (istr("1"), "b"), (istr("2"), "c")]
    assert list(istr.enumerate("abc", 1)) == [(istr("1"), "a"), (istr("2"), "b"), (istr("3"), "c")]

    assert istr(dict(zero=0, one=1, two=4)) == {"zero": istr("0"), "one": istr("1"), "two": istr("4")}


def test_indexing():
    a = istr(12345)
    assert a[0].equals(istr(1))
    assert a[:2].equals(istr(12))
    assert a[::-1].equals(istr(54321))
    assert a[-2:].equals(istr(45))


def test_reverse():
    a = istr(12345)
    assert a.reversed().equals(istr(54321))
    a = istr(-123)
    assert a.reversed().equals(istr("321-"))


def test_edge_cases():
    with pytest.raises(TypeError):
        istr(istr)
    assert istr(istr(one)).equals(istr("1"))
    with pytest.raises(TypeError):
        istr()
    rng = istr.range(5)
    assert rng is istr(rng)


def test_unpacking():
    a = istr("123")
    x, y, z = istr(*a)
    assert x.equals(istr(1))
    assert y.equals(istr(2))
    assert z.equals(istr(3))
    del x, y, z

    x, y, z = a
    assert x.equals(istr(1))
    assert y.equals(istr(2))
    assert z == "3"


def test_repr_mode():
    hundred = istr(100)
    assert repr(hundred) == "istr('100')"

    with istr.repr_mode("istr"):
        hundred = istr(100)
    assert repr(hundred) == "istr('100')"

    with istr.repr_mode("int"):
        assert istr.repr_mode() == "int"
        hundred = istr(100)
    assert repr(hundred) == "100"
    with istr.repr_mode("str"):
        hundred = istr(100)
    assert repr(hundred) == "'100'"
    hundred = istr(100)
    assert repr(hundred) == "istr('100')"

    with istr.repr_mode("int"):
        a = istr("abc")
    assert repr(a) == "?"

    assert istr.repr_mode() == "istr"

    with pytest.raises(TypeError):
        istr.repr_mode("no")


def test_str_methods():
    a = " abcABC "
    assert istr(a).capitalize().equals(istr(a.capitalize()))
    assert istr(a).casefold().equals(istr(a.casefold()))
    assert istr(a).center(20).equals(istr(a.center(20)))
    assert istr(a).expandtabs(4).equals(istr(a.expandtabs(4)))
    assert istr("{:4}").format(2).equals(istr("   2"))
    assert istr("").join(("0", "1", "2")).equals(istr("012"))
    assert istr(a.ljust(20)).equals(istr(a).ljust(20))
    assert istr(a.lower()).equals(istr(a).lower())
    assert istr(a.lstrip()).equals(istr(a).lstrip())
    assert istr(a).partition("a") == istr(a.partition("a"))
    assert istr(a.removeprefix(" ab")).equals(istr(a).removeprefix(" ab"))
    assert istr(a.removesuffix("BC ")).equals(istr(a).removesuffix("BC "))
    assert istr(a.rjust(20)).equals(istr(a).rjust(20))
    assert istr(a).rpartition("a") == istr(a.rpartition("a"))
    assert istr(a.rsplit("b")) == istr(a).rsplit("b")
    assert istr(a.rstrip()).equals(istr(a).rstrip())
    assert istr(a).swapcase().equals(istr(a.swapcase()))
    assert istr(a).title().equals(istr(a.title()))
    assert istr(a).translate({65: 66}).equals(istr(a.translate({65: 66})))
    assert istr(a.upper()).equals(istr(a).upper())
    assert istr(a.zfill(10)).equals(istr(a).zfill(10))


def test_base():
    assert istr.base() == 10
    with istr.base(16):
        a = istr("7fff")
        assert a == 32767
        assert a == "7fff"
        b = istr("3fff")
        c = a - b
        assert c == istr("4000")
        assert c == 2**14
    assert istr.base() == 10
    with istr.base(36):
        a = istr("PA7")
        assert a == 32767

    with istr.base(2):
        a = istr("111")
        assert a == 7
        b = a - istr("110")
        assert repr(b) == "istr('1')"

    with pytest.raises(ValueError):
        istr.base(1)
    with pytest.raises(ValueError):
        istr.base(37)

    with pytest.raises(ValueError):
        with istr.base(16):
            istr(-1)

    with istr.base(16):
        a = istr(15)
    with istr.base(10):
        assert a * a == 225

    a = istr(255)
    x = istr("?")
    with istr.base(16):
        assert istr(a) == "FF"
        assert istr(a, base=36) == "73"
        assert istr(x) == "?"
        assert istr(x, base=36) == "?"
        
def test_this_queries():
    a = istr(12, base=36, int_format="04", repr_mode="str")
    assert repr(a)=="'C'"
    assert a.this_base()==36
    assert a.this_int_format()=='04'
    assert a.this_repr_mode()=='str'

    a = istr(12, int_format="04", repr_mode="str")
    assert repr(a)=="'0012'"
    assert a.this_base()==10
    assert a.this_int_format()=='04'
    assert a.this_repr_mode()=='str'
    
def test_digits():
    assert istr.digits().equals(istr("0123456789"))
    assert istr.digits("").equals(istr("0123456789"))
    assert istr.digits("1").equals(istr("1"))
    assert istr.digits("3-").equals(istr("3456789"))
    assert istr.digits("-3").equals(istr("0123"))
    assert istr.digits("1-4", "6", "8-9").equals(istr("1234689"))
    assert istr.digits("1", "1-2", "1-3").equals(istr("112123"))
    a = istr.digits("a")
    assert a.equals(istr("A"))
    assert not a.is_int()
    with istr.base(36):
        a = istr.digits("a")
        assert a == 10
        assert a == "A"
        assert istr.digits("-a").equals(istr("0123456789A"))
        assert istr.digits("x-").equals(istr("XYZ"))
        assert istr.digits("B-d").equals(istr("BCD"))
        assert istr.digits("-").equals(istr("0123456789"))
    with istr.base(16):
        ef = istr.digits("e-f")
        assert (ef + 1).equals(istr("F0"))
        assert ef == 239


def test_digits_cache():
    d = istr.digits()
    assert id(d) == id(istr.digits())
    assert int(d) == 123456789

    with istr.base(16):
        d = istr.digits()
        assert id(d) == id(istr.digits())
    assert int(d) == 4886718345


def test_itertools():
    def list100(it):
        # just iterates over the first 100 elements in the iterable
        return [next(it) for _ in range(100)]

    assert list(istr.accumulate((1, 3, 4))) == [istr("1"), istr("4"), istr("8")]
    assert list(istr.chain(range(2), range(2, 5))) == [istr("0"), istr("1"), istr("2"), istr("3"), istr("4")]
    assert list(istr.combinations(range(5), r=3)) == list(istr(itertools.combinations(range(5), r=3)))
    assert list(istr.combinations_with_replacement(range(5), r=3)) == list(istr(itertools.combinations_with_replacement(range(5), r=3)))
    assert list(istr.compress("123456", [1, 0, 1, 0, 1, 1])) == [istr("1"), istr("3"), istr("5"), istr("6")]
    assert list100(istr.count()) == list100(istr(itertools.count()))
    assert list100(istr.cycle(range(10))) == list100(istr(itertools.cycle(range(10))))
    assert list(istr.dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1])) == [istr("6"), istr("4"), istr("1")]
    assert list(istr.filterfalse(lambda x: x % 2, range(10))) == [istr("0"), istr("2"), istr("4"), istr("6"), istr("8")]
    assert list(istr.islice("123456", 2)) == [istr("1"), istr("2")]
    assert list(istr.permutations(range(5), 3)) == list(istr(itertools.permutations(range(5), 3)))
    assert list(istr.product(range(5), range(4))) == list(istr(itertools.product(range(5), range(4))))
    assert list100(istr.repeat(10)) == list100(istr(itertools.repeat(10)))
    assert list(istr.starmap(pow, [(2, 5), (3, 2), (10, 3)])) == [istr("32"), istr("9"), istr("1000")]
    assert list(istr.takewhile(lambda x: x < 5, [1, 4, 6, 3, 8])) == [istr("1"), istr("4")]
    assert list(istr.zip_longest("123", "56", fillvalue="0")) == [(istr("1"), istr("5")), (istr("2"), istr("6")), (istr("3"), istr("0"))]
    if sys.version_info >= (3, 10):
        assert list(istr.pairwise("1234")) == [(istr("1"), istr("2")), (istr("2"), istr("3")), (istr("3"), istr("4"))]
    if sys.version_info >= (3, 12):
        assert list(istr.batched("12345", n=2)) == [(istr("1"), istr("2")), (istr("3"), istr("4")), (istr("5"),)]


def test_all_distinct():
    assert istr("abcdef").all_distinct()
    assert not istr("aabcdef").all_distinct()
    assert istr("").all_distinct()


def test_prod():
    assert istr.prod(range(1, 5)).equals(istr(24))
    assert istr.prod((1, 2, 3), start=4).equals(istr(24))
    assert istr("1234").prod().equals(istr(24))
    assert istr("123").prod(start=4).equals(istr(24))


def test_sumprod():
    assert istr.sumprod((1, 2), (3, 4)).equals(istr(11))
    assert istr.sumprod(istr("12"), (3, 4)).equals(istr(11))
    assert istr.sumprod(istr("12"), "34").equals(istr(11))
    assert istr.sumprod(istr("12"), "34", strict=False).equals(istr(11))
    assert istr.sumprod(istr("12"), "345", strict=False).equals(istr(11))
    with pytest.raises(ValueError):
        istr.sumprod((1, 2), (3, 4, 5))
    with pytest.raises(ValueError):
        istr.sumprod((1, 2), (3, 4, 5), strict=True)


def test_subclassing():
    class jstr(istr.type):
        ...

    assert jstr(5).equals(jstr(5))
    assert repr(jstr(*range(3))) == "(jstr('0'), jstr('1'), jstr('2'))"


def test_decompose():
    istr("123").decompose("xyz")
    assert x == 1
    assert y == 2
    assert z == 3
    istr(456).decompose("xyz")
    assert x == 4
    assert y == 5
    assert z == 6
    istr(1231).decompose("xyzx")
    assert x == 1
    assert y == 2
    assert z == 3
    namespace = {}
    istr(123).decompose("xyz", namespace=namespace)
    assert namespace == dict(x=istr(1), y=istr(2), z=istr(3))

    with pytest.raises(ValueError):
        istr(1234).decompose("xyzx")
    with pytest.raises(ValueError):
        istr(1234).decompose("xyz")
    with pytest.raises(ValueError):
        istr(12).decompose("xyz")
    with pytest.raises(ValueError):
        istr(123).decompose("xy1")


def test_compose():
    global x, y, z
    x = 1
    y = "2"
    z = istr(3)
    assert istr.compose("xyz").equals(istr(123))
    with pytest.raises(ValueError):
        istr.compose("wxyz")  # w is not defined
    assert istr.compose("xyz", namespace=dict(x=3, y=istr(4), z="5")).equals(istr(345))
    assert istr("=xyz").equals(istr(123))
    assert istr("=xyz", "=x") == (istr(123), istr(1))
    assert istr("=") == "="

    assert istr(["=xyz", "=y"]) == [istr(123), istr(2)]
    assert istr(("=xyz", "=y")) == (istr(123), istr(2))
    assert istr({"=xyz", "=y"}) == {istr(123), istr(2)}

    assert istr(dict(xyz="=xyz", y="=y")) == {"xyz": istr(123), "y": istr(2)}
    assert istr(dict(xyz="=xyz", y="=y"), namespace=dict(x=3, y=4, z="z")) == {"xyz": istr("34z"), "y": istr(4)}

    assert istr(istr("=xyz")) == istr(123)


if __name__ == "__main__":
    pytest.main(["-vv", "-s", "-x", __file__])

