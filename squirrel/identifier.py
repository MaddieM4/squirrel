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

    @property
    def STAR(self):
        "Explicitly adds the string '*' rather than a wrapped identifier."
        return Chain([*self, snippet.Const.STAR])
