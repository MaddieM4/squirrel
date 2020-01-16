class SquirrelBase(object):
    '''
    This is a mixin to provide some common functionality across our various
    classes. I may also restructure the classes soon too, to reduce their surface
    area.
    '''

    def wrap(self):
        from .chain import Chain
        from .snippet import Const
        return Chain([ Const.LPAREN, self, Const.RPAREN ])

    def __eq__(self, other):
        from .chain import Chain
        from .snippet import Const, Snippet

        if other is None:
            return Chain([self, Const.IS, Const.NULL])
        if isinstance(other, list):
            return Chain([self, Const.IN, other])

        # Deliberately not isinstance(other, tuple).
        # We only want to handle plain tuples this way,
        # not any of our lovely subclasses.
        if type(other) == tuple and len(other) == 2:
            op, value = other
            assert op in ('>', '<', '=', '<=', '>=', '!='), repr(op)+" must be an operator"
            return Chain([self, Snippet.from_sql(op), value])

        return Chain([self, Const.EQUALS, other])

    def __lt__(self, other): return self == ('<',  other)
    def __le__(self, other): return self == ('<=', other)
    def __gt__(self, other): return self == ('>',  other)
    def __ge__(self, other): return self == ('>=', other)
    def __ne__(self, other): return self == ('!=', other)
