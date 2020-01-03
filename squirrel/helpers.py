from .identifier import ns
from .snippet import Const as const
from .chain import Chain

def SELECT(table, *cols):
    if isinstance(table, str):
        table = ns[table]
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

def AND(*sections):
    return Chain.join(const.AND, sections)

def OR(*sections):
    return Chain.join(const.OR, sections)
