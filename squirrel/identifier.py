from squirrel import inspect

class Identifier(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'`{self.value}`'

    def __repr__(self):
        return f'<Identifier {self}>'

class Chain(tuple):
    # TODO: handle these in a way that doesn't overlap with getattr access...
    args = ()
    pad_left = True
    pad_right = True

    def __str__(self):
        return '.'.join(str(ident) for ident in self)

    def __getitem__(self, k):
        return Chain([*self, Identifier(k)])

    def __getattr__(self, k):
        return self[k]

    @property
    def STAR(self):
        "Explicitly adds the string '*' rather than a wrapped identifier."
        return Chain([*self, '*'])
