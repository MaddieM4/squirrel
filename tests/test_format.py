import pytest
from squirrel import SQL, Chain, Snippet

s = Snippet.from_sql

@pytest.mark.parametrize('source, expected', [
    ('', []),
    ('SELECT * FROM table', [s('SELECT * FROM table')]),
    ('SELECT * FROM table WHERE first={first}', [s('SELECT * FROM table WHERE first='), 1]),
    ('SELECT * FROM table WHERE first={first} AND second={second}',
        [s('SELECT * FROM table WHERE first='), 1, s(' AND second='), '2nd']),
])
def test_format(source, expected):
    assert SQL(source, first=1, second='2nd') == Chain(expected)
