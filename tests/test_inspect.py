import pytest
from squirrel.inspect import *
from squirrel import ns

@pytest.mark.parametrize('source, expected', [
    ('',   Inspection('%s',   ('',), True, True)),
    ('fx', Inspection('%s', ('fx',), True, True)),
    (None, Inspection('%s', (None,), True, True)),
    (35,   Inspection('%s',   (35,), True, True)),
    (ns.hello.world, Inspection('`hello`.`world`', (), True, True)),
    (ns.STAR, Inspection('*', (), True, True)),
])
def test_flatten(source, expected):
    got = flatten(source)
    assert isinstance(got.args, tuple)
    assert isinstance(expected.args, tuple)
    assert got == expected
