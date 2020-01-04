from squirrel import inspect, snippet

class Identifier(str):
    @property
    def text(self):
        return f'`{self}`'

    def __repr__(self):
        return f'<Identifier "{self}">'

class Chain(tuple):
    # TODO: handle these in a way that doesn't overlap with getattr access...
    args = ()

    @property
    def text(self):
        return '.'.join(inspect.text(ident) for ident in self)

    @property
    def pad_left(self): return bool(self)

    @property
    def pad_right(self): return bool(self)

    def __str__(self):
        return self.text

    def __getitem__(self, k):
        return Chain([*self, Identifier(k)])

    def __getattr__(self, k):
        return self[k]

    def __eq__(self, other):
        from .chain import Chain as SQLChain
        from .snippet import Const
        if other is None:
            return SQLChain([self, Const.IS, Const.NULL])
        if isinstance(other, list):
            return SQLChain([self, Const.IN, other])

        # Deliberately not isinstance(other, tuple).
        # We only want to handle plain tuples this way,
        # not any of our lovely subclasses.
        if type(other) == tuple and len(other) == 2:
            op, value = other
            assert op in ('>', '<', '=', '<=', '>=', '!='), f"{op!r} must be an operator"
            return SQLChain([self, snippet.Snippet.from_sql(op), value])

        return SQLChain([self, Const.EQUALS, other])

    @property
    def STAR(self):
        "Explicitly adds the string '*' rather than a wrapped identifier."
        return Chain([*self, snippet.Const.STAR])

    @property
    def ASC(self):
        from .chain import Chain as SQLChain
        return SQLChain([self, snippet.Const.ASC])

    @property
    def DESC(self):
        from .chain import Chain as SQLChain
        return SQLChain([self, snippet.Const.DESC])

ns = Chain()
