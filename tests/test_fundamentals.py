import pytest
import sql

@pytest.mark.parametrize('param,expected_sql,expected_args', [
    ('some text', 'some text', []),
    (5, '5', []),
    (
        { 'hello': 'world' }, 
        '(hello=%s)',
        ['world'],
    ),
    (
        { 'a':'A', 'b':'B', 'c':'C', 'number':3}, 
        '(a=%s AND b=%s AND c=%s AND number=%s)',
        ['A','B','C', 3],
    ),
])
def test_to_pair(param, expected_sql, expected_args):
    got_sql, got_args = sql.to_pair(param)
    assert got_sql  == expected_sql
    assert got_args == expected_args
