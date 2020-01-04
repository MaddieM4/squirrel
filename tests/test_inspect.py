import pytest
from squirrel import ns, Snippet, const, Chain
from squirrel.helpers import *

@pytest.mark.parametrize('source, expected', [
    ('',   Snippet('%s',   ('',), True, True)),
    ('fx', Snippet('%s', ('fx',), True, True)),
    (None, Snippet('%s', (None,), True, True)),
    (35,   Snippet('%s',   (35,), True, True)),
    ([35, 'yo', ns.wexford],   Snippet('(%s, %s, `wexford`)', (35,'yo'), True, True)),

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
    (ns.hello.world == None, Snippet('`hello`.`world` IS NULL', (), True, True)),
    (ns.hello.world == [1,2,3], Snippet('`hello`.`world` IN (%s, %s, %s)', (1,2,3), True, True)),
    (ns.hello.world == [], Snippet('`hello`.`world` IN ()', (), True, True)),
    (ns.hello.world == ('>=', 7), Snippet('`hello`.`world` >= %s', (7,), True, True)),
    (ns.hello.world == ns.goodnight.moon, Snippet('`hello`.`world` = `goodnight`.`moon`', (), True, True)),

    (WHERE(ns.foo, bar='baz'), Snippet('WHERE `foo`.`bar` = %s', ('baz',), True, True)),
    (WHERE('foo', first=1, second=2), Snippet('WHERE `foo`.`first` = %s AND `foo`.`second` = %s', (1,2), True, True)),
    (WHERE(ns.foo.bar == 5, ns.foo.baz == 'xyz'), Snippet('WHERE `foo`.`bar` = %s AND `foo`.`baz` = %s', (5,'xyz'), True, True)),
    (WHERE('mytable', ns.foo.bar == 5, ns.foo.baz == 'xyz', myfield=9),
        Snippet('WHERE `foo`.`bar` = %s AND `foo`.`baz` = %s AND `mytable`.`myfield` = %s', (5,'xyz',9), True, True)),
    (WHERE('mytable', id=[4,5,6]), Snippet('WHERE `mytable`.`id` IN (%s, %s, %s)', (4,5,6), True, True)),
    (WHERE('mytable', id=('>', 5)), Snippet('WHERE `mytable`.`id` > %s', (5,), True, True)),

    (JOIN('x','y', 'a b c d'),
        Snippet('JOIN `y` ON `y`.`a` = `x`.`a` AND `y`.`b` = `x`.`b` AND `y`.`c` = `x`.`c` AND `y`.`d` = `x`.`d`', (), True, True)),
    (JOIN('x','y', 'a','b', c='hello', d='world'),
        Snippet('JOIN `y` ON `y`.`a` = `x`.`a` AND `y`.`b` = `x`.`b` AND `y`.`c` = %s AND `y`.`d` = %s', ('hello', 'world'), True, True)),
    (JOIN('x','y', id=('>', 180)),
        Snippet('JOIN `y` ON `y`.`id` > %s', (180,), True, True)),

    (GROUP_BY(), Snippet('', (), False, False)),
    (GROUP_BY(None), Snippet('', (), False, False)),
    (GROUP_BY(0), Snippet('GROUP BY %s', (0,), True, True)),
    (GROUP_BY(ns.foo.bar), Snippet('GROUP BY `foo`.`bar`', (), True, True)),

    (ORDER_BY(), Snippet('', (), False, False)),
    (ORDER_BY(None), Snippet('', (), False, False)),
    (ORDER_BY(0), Snippet('ORDER BY %s', (0,), True, True)),
    (ORDER_BY(ns.foo.bar, const.ASC), Snippet('ORDER BY `foo`.`bar` ASCENDING', (), True, True)),
    (ORDER_BY(ns.foo.bar.ASC), Snippet('ORDER BY `foo`.`bar` ASCENDING', (), True, True)),
    (ORDER_BY(ns.foo.bar.DESC), Snippet('ORDER BY `foo`.`bar` DESCENDING', (), True, True)),

    (LIMIT(), Snippet('', (), False, False)),
    (LIMIT(None), Snippet('', (), False, False)),
    (LIMIT(0), Snippet('LIMIT %s', (0,), True, True)),

    (OFFSET(), Snippet('', (), False, False)),
    (OFFSET(None), Snippet('', (), False, False)),
    (OFFSET(0), Snippet('OFFSET %s', (0,), True, True)),

    (fn.UCASE(ns.title), Snippet('UCASE(`title`)', (), True, True)),
    (fn.COALESCE(1, 2, 3, 4), Snippet('COALESCE(%s, %s, %s, %s)', (1,2,3,4), True, True)),
    (fn.CAST(1, AS='UNSIGNED'), Snippet('CAST(%s AS UNSIGNED)', (1,), True, True)),
])
def test_inspect(source, expected):
    # Test this via Snippet.from_inspect since it covers everything neatly
    got = Snippet.from_inspect(source)
    assert isinstance(got.args, tuple)
    assert isinstance(expected.args, tuple)
    assert got == expected

def test_operator_assert():
    with pytest.raises(AssertionError, match="'xyz' must be an operator"):
        ns.foo == ('xyz', 7)
    # This should be fine
    ns.foo == ('>', 7)

def test_join_clause_assert():
    with pytest.raises(AssertionError, match="JOIN must have clauses"):
        JOIN('x', 'y')
