from collections import namedtuple
from squirrel import inspect

class Snippet(namedtuple('Snippet', 'text, args, pad_left, pad_right')):
    '''
    Represents a piece of arbitrary SQL, potentially with placeholders
    and parameterized arguments. The padding information matters for
    SQL chains.
    '''
    def __str__(self):
        return self.text

    @classmethod
    def from_inspect(cls, source):
        return cls(
            text = inspect.text(source),
            args = inspect.args(source),
            pad_left  = inspect.pad_left(source),
            pad_right = inspect.pad_right(source),
        )

    @classmethod
    def from_sql(cls, text, args=(), pad_left=True, pad_right=True):
        return cls(text, args, pad_left, pad_right)

    # Possible TODO: Snippet.from_raw which escapes placeholders?
    # Not sure there's any value to that...

class Const(object):
    "Just a namespace of helpful snippets."

    LPAREN = Snippet.from_sql('(', pad_right=False)
    RPAREN = Snippet.from_sql(')', pad_left=False)
    COMMA  = Snippet.from_sql(',', pad_left=False)
    EQUALS = Snippet.from_sql('=')
    TRUE   = Snippet.from_sql('(1=1)')
    FALSE  = Snippet.from_sql('(1=0)')
    STAR = Snippet.from_sql('*')
    NULL = Snippet.from_sql('NULL')

    AND = Snippet.from_sql('AND')
    OR  = Snippet.from_sql('OR')
    IS  = Snippet.from_sql('IS')
    IN  = Snippet.from_sql('IN')
    ON  = Snippet.from_sql('ON')

    SELECT = Snippet.from_sql('SELECT')
    FROM   = Snippet.from_sql('FROM')
    WHERE  = Snippet.from_sql('WHERE')
    JOIN   = Snippet.from_sql('JOIN')

    GROUP_BY = Snippet.from_sql('GROUP BY')
    ORDER_BY = Snippet.from_sql('ORDER BY')
    LIMIT    = Snippet.from_sql('LIMIT')
    OFFSET   = Snippet.from_sql('OFFSET')
    ASC  = Snippet.from_sql('ASCENDING')
    DESC = Snippet.from_sql('DESCENDING')
