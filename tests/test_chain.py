from squirrel.chain import Chain
from squirrel.snippet import Snippet

def test_chain():
    c = Chain(['hello', Snippet.from_sql('='), 'world'])
    assert c[0] == 'hello'
    assert c.text == '%s = %s'
    assert c.args == ('hello', 'world')
    assert getattr(c, 'text') == '%s = %s'
