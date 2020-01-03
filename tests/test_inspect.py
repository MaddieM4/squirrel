import pytest
from squirrel import ns, Snippet, const, Chain
from squirrel.helpers import *

@pytest.mark.parametrize('source, expected', [
    ('',   Snippet('%s',   ('',), True, True)),
    ('fx', Snippet('%s', ('fx',), True, True)),
    (None, Snippet('%s', (None,), True, True)),
    (35,   Snippet('%s',   (35,), True, True)),

    (ns.hello.world, Snippet('`hello`.`world`', (), True, True)),
    (ns.STAR, Snippet('*', (), True, True)),

    (const.LPAREN, Snippet('(', (), True, False)),
    (const.RPAREN, Snippet(')', (), False, True)),
    (Chain(['hello', 'world']), Snippet('%s %s', ('hello', 'world'), True, True)),
    (Chain([ns.foo, const.EQUALS, ns.bar.baz]), Snippet('`foo` = `bar`.`baz`', (), True, True)),
    (Chain([ns.foo, const.EQUALS, const.LPAREN]), Snippet('`foo` = (', (), True, False)),
    (Chain([const.RPAREN, ns.foo]), Snippet(') `foo`', (), False, True)),
    (Chain([const.LPAREN, ns.foo, const.RPAREN]), Snippet('(`foo`)', (), True, True)),
    (Chain([]), Snippet('', (), False, False)),
    (ns, Snippet('', (), False, False)),

    (SELECT(ns.foo), Snippet('SELECT * FROM `foo`', (), True, True)),
    (SELECT('mytable', 'x','y','z'), Snippet('SELECT `mytable`.`x`, `mytable`.`y`, `mytable`.`z` FROM `mytable`', (), True, True)),
    (SELECT('mytable', 'x y z'), Snippet('SELECT `mytable`.`x`, `mytable`.`y`, `mytable`.`z` FROM `mytable`', (), True, True)),

    (AND(), Snippet('', (), False, False)),
    (AND(1,2,3), Snippet('%s AND %s AND %s', (1, 2, 3), True, True)),
    (OR(ns.foo, ns.bar), Snippet('`foo` OR `bar`', (), True, True)),

    (ns.hello.world == 5, Snippet('`hello`.`world` = %s', (5,), True, True)),

    (WHERE(ns.foo, bar='baz'), Snippet('WHERE `foo`.`bar` = %s', ('baz',), True, True)),
    (WHERE('foo', first=1, second=2), Snippet('WHERE `foo`.`first` = %s AND `foo`.`second` = %s', (1,2), True, True)),
    (WHERE(ns.foo.bar == 5, ns.foo.baz == 'xyz'), Snippet('WHERE `foo`.`bar` = %s AND `foo`.`baz` = %s', (5,'xyz'), True, True)),
    (WHERE('mytable', ns.foo.bar == 5, ns.foo.baz == 'xyz', myfield=9),
        Snippet('WHERE `foo`.`bar` = %s AND `foo`.`baz` = %s AND `mytable`.`myfield` = %s', (5,'xyz',9), True, True)),
])
def test_inspect(source, expected):
    # Test this via Snippet.from_inspect since it covers everything neatly
    got = Snippet.from_inspect(source)
    assert isinstance(got.args, tuple)
    assert isinstance(expected.args, tuple)
    assert got == expected
