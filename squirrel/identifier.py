class Identifier(object):
    args = ()
    def __str__(self):
        return f'`{self.value}`'

    def __init__(self, value):
        self.value = value

class Chain(tuple):
    args = ()
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
