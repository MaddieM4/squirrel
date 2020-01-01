from collections import namedtuple
Inspection = namedtuple('Inspection', 'str, args, pad_left, pad_right')

def flatten(source):
    return Inspection(
        str  = stringify(source),
        args = get_args(source),
        pad_left  = pad_left(source),
        pad_right = pad_right(source),
    )

def stringify(source):
    if hasattr(source, 'args'):
        return str(source)
    return '%s'

def get_args(source):
    if hasattr(source, 'args'):
        return source.args
    return (source,)

def pad_left(source):
    return getattr(source, 'pad_left', True)

def pad_right(source):
    return getattr(source, 'pad_right', True)
