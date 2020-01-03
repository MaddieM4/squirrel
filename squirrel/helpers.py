from .identifier import ns
from .snippet import Const as const
from .chain import Chain

def AND(*sections):
    return Chain.join(const.AND, sections)

def OR(*sections):
    return Chain.join(const.OR, sections)

def _ensure_table(table):
    if isinstance(table, str):
        return ns[table]
    return table

def SELECT(table, *cols):
    table = _ensure_table(table)
    if not cols:
        cols = (const.STAR,)

    if len(cols) == 1 and ' ' in cols[0]:
        cols = cols[0].split()

    def fix_col(col):
        if isinstance(col, str):
            return table[col]
        return col

    return Chain([
        const.SELECT,
        Chain.join(const.COMMA, map(fix_col, cols)),
        const.FROM,
        table
    ])

def WHERE(*args, **kwargs):
    clauses = args
    if kwargs:
        table = _ensure_table(args[0])
        clauses = list(args[1:]) + [table[k] == v for k,v in kwargs.items()]
    return Chain([ const.WHERE, AND(*clauses) ])
