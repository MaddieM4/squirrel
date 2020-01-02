def text(source):
    return getattr(source, 'text', '%s')

def args(source):
    return getattr(source, 'args', (source,))

def pad_left(source):
    return getattr(source, 'pad_left', True)

def pad_right(source):
    return getattr(source, 'pad_right', True)
