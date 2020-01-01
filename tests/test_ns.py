import pytest
import squirrel as sq

@pytest.mark.parametrize('chain, expected', [
    (sq.ns.hello, '`hello`'),
    (sq.ns.hello.world, '`hello`.`world`'),
    (sq.ns.hello.STAR, '`hello`.*'),
    (sq.ns.STAR, '*'),
])
def test_chain(chain, expected):
    assert chain.args == ()
    assert str(chain) == expected

def test_import():
    from squirrel.ns import STAR, foo
    assert str(STAR) == '*'
    assert str(foo) == '`foo`'

    from squirrel.ns import long_cumbersome_name as lcn
    assert str(lcn) == '`long_cumbersome_name`'

    # TODO: Support deeper path imports
