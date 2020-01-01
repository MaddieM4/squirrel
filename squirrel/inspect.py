def text(source):
    if hasattr(source, 'args'):
        return str(source)
    return '%s'

def args(source):
    if hasattr(source, 'args'):
        return source.args
    return (source,)

def pad_left(source):
    return getattr(source, 'pad_left', True)

def pad_right(source):
    return getattr(source, 'pad_right', True)
