import pytest
import sql

@pytest.mark.parametrize('data,expected', [
    ('some text', 'some text'),
    (5, '5'),
])
def test_to_sql(data, expected):
    assert sql.to_sql(data) == expected

@pytest.mark.parametrize('data,expected', [
    ('some text', []),
])
def test_to_args(data, expected):
    assert sql.to_args(data) == expected
