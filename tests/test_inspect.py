import pytest
from squirrel import ns, Snippet, const

@pytest.mark.parametrize('source, expected', [
    ('',   Snippet('%s',   ('',), True, True)),
    ('fx', Snippet('%s', ('fx',), True, True)),
    (None, Snippet('%s', (None,), True, True)),
    (35,   Snippet('%s',   (35,), True, True)),

    (ns.hello.world, Snippet('`hello`.`world`', (), True, True)),
    (ns.STAR, Snippet('*', (), True, True)),

    (const.LPAREN, Snippet('(', (), True, False)),
    (const.RPAREN, Snippet(')', (), False, True)),
])
def test_inspect(source, expected):
    # Test this via Snippet.from_inspect since it covers everything neatly
    got = Snippet.from_inspect(source)
    assert isinstance(got.args, tuple)
    assert isinstance(expected.args, tuple)
    assert got == expected
