from functools import singledispatch

@singledispatch
def to_sql(param):
    return str(param)

@singledispatch
def to_args(param):
    return []
