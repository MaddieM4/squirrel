from functools import singledispatch

def to_pair(param):
    return to_sql(param), to_args(param)

@singledispatch
def to_sql(param):
    return str(param)

@singledispatch
def to_args(param):
    return []

def AND(iterable):
    elements = ' AND '.join(iterable)
    return f'({elements})'

@to_sql.register(dict)
def dict_to_sql(param):
    return AND(k+'=%s' for k in param)

@to_args.register(dict)
def dict_to_args(param):
    return [v for v in param.values()]
