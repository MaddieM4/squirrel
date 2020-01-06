from functools import singledispatch

@singledispatch
def text(source):
    return getattr(source, 'text', '%s')

@singledispatch
def args(source):
    return getattr(source, 'args', (source,))

def pad_left(source):
    return getattr(source, 'pad_left', True)

def pad_right(source):
    return getattr(source, 'pad_right', True)

@text.register(list)
def list_text(source):
    inner = ', '.join((text(item) for item in source))
    return '(' + inner + ')'

@args.register(list)
def list_args(source):
    result = []
    for item in source:
        result.extend(args(item))
    return tuple(result)
