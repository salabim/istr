import math
import itertools

if __name__ == "__main__":  # to make the tests run without the pytest cli
    import sys

    sys.path = ["../istr"] + sys.path

import pytest

from istr import istr

istr.equals = lambda self, other: type(self) == type(other) and (str(self) == str(other))
# this method tests whether self and other are exactly the same

for i, name in enumerate("minus_one zero one two three four five six seven eight nine ten eleven twelve thirteen".split(), -1):
    globals()[name] = istr(i)
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
    assert two <= three
    assert 2 <= three
    assert two <= 3

    assert two <= two
    assert 2 <= two
    assert two <= two


def test_gt():
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
    assert " ".join(sorted(istr.range(1, 13))) == "1 2 3 4 5 6 7 8 9 10 11 12"
    assert " ".join(sorted(map(istr, range(1, 13)))) == "1 2 3 4 5 6 7 8 9 10 11 12"

def test_concat():
    c = list(istr.concat(((1,2),(3,4))))
    assert c == istr(['12','34'])
    c=list(istr.concat(itertools.permutations(range(3),2)))
    assert c == [istr('01'), istr('02'), istr('10'), istr('12'), istr('20'), istr('21')]
    
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
        a = one_to_twelve[12]


def test_misc():
    assert istr("") == ""
    assert istr("") == 0
    with pytest.raises(ValueError):
        istr(" ")
    assert istr(istr(6)) == "6"
    assert istr(" 12 ") == " 12 "
    with istr.format("03"):
        assert istr("   12  ") == "012"
        assert istr("") == ""


def test_divmod():
    assert divmod(eleven, three) == (istr(3), istr(2))
    assert divmod(11, three) == (istr(3), istr(2))
    assert divmod(eleven, 3) == (istr(3), istr(2))
    assert divmod(11, 3) == (3, 2)


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


def test_format():
    assert istr(" 1 ") == " 1 "
    with istr.format("0"):
        assert istr(" 1 ") == "1"
    with istr.format("03"):
        assert istr(1) == "001"
        assert istr(1234) == "1234"
    with istr.format("3"):
        assert istr(1) == "  1"
        assert istr(1234) == "1234"
    with istr.format(""):
        assert istr(1234) == "1234"
    with istr.format("003"):
        assert istr(1) == "001"
    with pytest.raises(ValueError):
        with istr.format(" 1"):
            ...
    with pytest.raises(ValueError):
        with istr.format("1 "):
            ...
    with pytest.raises(ValueError):
        with istr.format("a"):
            ...
    with pytest.raises(ValueError):
        with istr.format(1):
            ...
    with istr.format("0"):
        assert istr(" 3 ") == "3"
    assert istr.format() == ""
    istr.format("03")
    assert istr.format() == "03"
    assert istr("  8 ") == "008"
    istr.format("")
    assert istr(" 8 ") == " 8 "


def test_range_format():
    r = istr.range(11)
    assert repr(r) == "istr.range(0, 11)"
    assert " ".join(r) == "0 1 2 3 4 5 6 7 8 9 10"
    r = istr.range(11)
    with istr.format("02"):
        assert " ".join(r) == "00 01 02 03 04 05 06 07 08 09 10"


def test_even_odd():
    assert istr(1).is_odd()
    assert not istr(1).is_even()

    assert istr(12345678).is_even()
    assert not istr(12345678).is_odd()


def test_join():
    s = "".join(istr(("4", "5", "6")))
    assert s == "456"
    assert type(s) == str

    s = istr("").join(("4", "5", "6"))
    assert s == "456"
    assert s == 456
    assert type(s) == istr

    s = istr("").join(istr(("4", "5", "6")))
    assert s == "456"
    assert s == 456
    assert type(s) == istr

    s = istr("").join(istr(("", "", "6")))
    assert s == "6"
    assert s == 6
    assert type(s) == istr


def test_matmul():
    assert (five @ 3).equals(istr("555"))
    assert (3 @ five).equals(istr("555"))

    with pytest.raises(TypeError):
        three @ five
    with pytest.raises(TypeError):
        three @ "5"
    with pytest.raises(TypeError):
        "3" @ five


def test_str():
    assert repr(str(five)) == "'5'"


def test_trunc_and_friends():
    assert math.trunc(one).equals(istr("1"))
    assert math.ceil(one).equals(istr("1"))
    assert math.floor(one).equals(istr("1"))
    assert round(one).equals(istr("1"))


def test_data_structures():
    assert repr(istr(list(range(1, 4)))) == "[istr('1'), istr('2'), istr('3')]"
    assert repr(istr(tuple(range(1, 4)))) == "(istr('1'), istr('2'), istr('3'))"
    assert istr(set(range(1, 4))) == {istr(1), istr(2), istr(3)}

    assert repr(list(istr(range(1, 4)))) == "[istr('1'), istr('2'), istr('3')]"

    assert repr(list(istr.enumerate("abc"))) == "[(istr('0'), 'a'), (istr('1'), 'b'), (istr('2'), 'c')]"
    assert repr(list(istr.enumerate("abc", 1))) == "[(istr('1'), 'a'), (istr('2'), 'b'), (istr('3'), 'c')]"

    assert repr(istr(dict(zero=0, one=1, two=4))) == "{'zero': istr('0'), 'one': istr('1'), 'two': istr('4')}"


def test_indexing():
    a = istr(12345)
    assert a[0].equals(istr(1))
    assert a[:2].equals(istr(12))
    assert a[::-1].equals(istr(54321))
    assert a[-2:].equals(istr(45))


def test_reverse():
    a = istr(12345)
    assert a.reversed(), same(istr(54321))


def test_edge_cases():
    with pytest.raises(ValueError):
        istr("ab")
    with pytest.raises(ValueError):
        istr(istr)
    assert istr(istr(one)).equals(istr("1"))
    with pytest.raises(TypeError):
        istr()
    rng=istr.range(5)
    assert rng is istr(rng)

def test_unpacking():
    a = istr("123")
    x, y, z = istr(*a)
    assert x.equals(istr(1))
    assert y.equals(istr(2))
    assert z.equals(istr(3))


def test_repr_mode():
    hundred = istr(100)
    assert repr(hundred) == "istr('100')"

    with istr.repr_mode("istr"):
        hundred = istr(100)
    assert repr(hundred) == "istr('100')"

    with istr.repr_mode("int"):
        hundred = istr(100)
    assert repr(hundred) == "100"
    with istr.repr_mode("str"):
        hundred = istr(100)
    assert repr(hundred) == "'100'"
    hundred = istr(100)
    assert repr(hundred) == "istr('100')"

    assert istr.repr_mode() == "istr"

    with pytest.raises(TypeError):
        istr.repr_mode("no")

def test_str_methods():
    a=istr("   123123 ")
    b=istr("123123")
    assert a.capitalize().equals(a)
    assert a.casefold().equals(a)
    assert a.center(20).equals(istr('        123123      '))
    assert a.expandtabs(4).equals(a)
    assert istr("").join(("0","1","2")).equals(istr("012"))
    assert a.ljust(20).equals(istr('   123123           '))
    assert a.lower().equals(a)
    assert a.lstrip().equals(istr('123123 '))
    assert a.partition("3")==(istr('   12'), istr('3'), istr('123 '))
    assert a.removeprefix("   12").equals(istr("3123 "))
    assert a.removesuffix("23 ").equals(istr("   1231"))
    assert a.replace("1","9").equals(istr("   923923 "))
    assert a.rjust(20).equals(istr('             123123 '))
    assert b.partition("2")==(istr('1'), istr('2'), istr('3123'))
    assert b.rpartition("2")==(istr('1231'), istr('2'), istr('3'))
    assert b.rsplit("1")==[istr(''), istr('23'), istr('23')]
    assert a.rstrip().equals(istr('   123123'))
    assert b.split("1")==[istr(''), istr('23'), istr('23')]
    assert a.strip().equals(istr('123123'))
    assert a.swapcase().equals(a)
    assert a.title().equals(a)
    assert a.translate({49:  52}).equals(istr('   423423 '))
    assert a.upper().equals(a)
    assert b.zfill(10).equals(istr('0000123123'))

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
    with pytest.raises(ValueError):
        assert a | a # FF can't be converted to base 10
        
    



def test_subclassing():
    class jstr(istr):
        ...

    assert jstr(5).equals(jstr(5))
    assert repr(jstr(*range(3))) == "(jstr('0'), jstr('1'), jstr('2'))"


if __name__ == "__main__":
    pytest.main(["-vv", "-s", "-x", __file__])

