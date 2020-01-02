import pytest
from squirrel import SQL, Chain, Snippet, ns

s = lambda text: Snippet.from_sql(text, pad_left=False, pad_right=False)

@pytest.mark.parametrize('source, expected', [
    ('', []),
    ('SELECT * FROM table', [s('SELECT * FROM table')]),
    ('SELECT * FROM table WHERE first={first}', [s('SELECT * FROM table WHERE first='), 1]),
    ('SELECT * FROM table WHERE first={first} AND second={second}',
        [s('SELECT * FROM table WHERE first='), 1, s(' AND second='), '2nd']),
])
def test_format(source, expected):
    assert SQL(source, first=1, second='2nd') == Chain(expected)

def test_padding():
    """
    Usually, format-created strings already have exactly the padding the user wants.
    We don't want to break that padding in unintuitive ways.
    """
    got = SQL('SELECT * FROM {table} WHERE {table}.id={id}', table=ns.widgets, id=7)
    assert got.text == 'SELECT * FROM `widgets` WHERE `widgets`.id=%s'
    assert got.args == (7,)
