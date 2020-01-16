from squirrel import inspect, Snippet

PADDING = ' '

class Chain(tuple):
    @property
    def text(self):
        return ''.join(self._gen_text())

    def _gen_text(self):
        pad_right = False
        for item in self:
            if pad_right and inspect.pad_left(item):
                yield PADDING
            yield inspect.text(item)
            pad_right = inspect.pad_right(item)

    @property
    def args(self):
        return tuple(self._gen_args())

    def _gen_args(self):
        for item in self:
            yield from inspect.args(item)

    @property
    def pad_left(self):
        if not len(self):
            return False
        return inspect.pad_left(self[0])

    @property
    def pad_right(self):
        if not len(self):
            return True
        return inspect.pad_right(self[-1])

    @classmethod
    def join(cls, sep, items):
        return cls(cls._gen_join(sep, items))

    def _gen_join(sep, items):
        emit_sep = False
        for item in items:
            if emit_sep:
                yield sep
            yield item
            emit_sep = True

    def to_snippet(self):
        return Snippet.from_inspect(self)
