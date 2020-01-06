from collections import namedtuple
from squirrel import helpers, const, Chain

class SELECT(object):
    def __init__(self, table, *cols, **where):
        self.table = helpers._ensure_table(table)
        self.cols = cols
        self.joins = []
        self.where = helpers._comparisons(self.table, **where)
        self.limit = None
        self.offset = None

    def JOIN(self, table, *args, **kwargs):
        self.joins.append(helpers.JOIN(self.table, table, *args, **kwargs))
        return self

    def WHERE(self, *args, **kwargs):
        self.where += list(args)
        self.where += helpers._comparisons(self.table, **kwargs)
        return self

    def LIMIT(self, amount, second_arg=None):
        if second_arg is not None:
            self.limit = Chain([amount, const.COMMA, second_arg])
        else:
            self.limit = amount
        return self

    def OFFSET(self, amount):
        self.offset = amount
        return self

    def to_chain(self):
        return Chain([
            helpers.SELECT(self.table, *self.cols),
            Chain(self.joins),
            helpers._if_content(const.WHERE, helpers.AND(*self.where)),
            helpers.LIMIT(self.limit),
            helpers.OFFSET(self.offset),
        ])

    @property
    def text(self):
        return self.to_chain().text
