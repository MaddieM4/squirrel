class SQL(object):
    def __init__(self, text, *args, pad_left=True, pad_right=True):
        assert isinstance(text, str)
        self.text = text
        self.args = tuple(args)
        self.pad_left = pad_left
        self.pad_right = pad_right

    @classmethod
    def Arg(cls, value):
        return cls('%s', value)

    @classmethod
    def cast(cls, value):
        if isinstance(value, cls):
            return value
        if hasattr(value, 'args'):
            return cls(str(value), *value.args)
        return cls(str(value))

    def __add__(self, other):
        other = SQL.cast(other)
        padding = ' ' if (self.pad_right and other.pad_left) else ''
        return SQL(self.text + padding + other.text, *(self.args + other.args))

    def __str__(self):
        return self.text

class Identifier(object):
    args = ()
    def __init__(self, text='', literal=''):
        self.text = literal or f'`{text}`'

    def __str__(self):
        return self.text

    def __getitem__(self, k):
        if self.text:
            return Identifier(literal=f'{self.text}.`{k}`')
        return Identifier(k)

    def __getattr__(self, k):
        return self[k]

    def __add__(self, other):
        return SQL.cast(self) + other

    @property
    def _star(self):
        return Identifier(literal=f'{self.text}.*')

schema = Identifier('')
schema.text = ''

SQL.comma = SQL(',', pad_left=False, pad_right=True)
SQL.empty = SQL('',  pad_left=False, pad_right=False)
SQL.SELECT = SQL('SELECT', pad_left=False, pad_right=True)
SQL.FROM   = SQL('FROM',   pad_left=True,  pad_right=True)

class Query(object):
    def __init__(self, verb, table):
        self.verb  = verb
        self.table = table
        self.components = []

    @classmethod
    def select(cls, table):
        return cls(SQL.SELECT, table)

    def columns(self, sql):
        self.components.append({'columns': SQL.cast(sql)})
        return self

    def order(self, sql, *extra):
        for item in extra:
            sql = sql + item
        self.components.append({'order': SQL.cast(sql)})
        return self

    def limit(self, n):
        assert isinstance(n, int) and n >= 0
        self.components.append({'limit': str(n)})
        return self

    def find(self, key):
        for component in self.components:
            if key in component:
                yield component[key]

    def incorporate(self, key, separator=SQL.comma, prefix=SQL.empty, empty_value=SQL.empty):
        sql = SQL('')
        for item in self.find(key):
            if sql.text:
                sql = sql + separator + item
            else:
                sql = item
        if sql.text:
            return SQL.cast(prefix) + sql
        else:
            return SQL.cast(empty_value)

    def last(self, key, prefix=SQL.empty, empty_value=SQL.empty):
        found = None
        for item in self.find(key):
            found = item
        if found is not None:
            return SQL.cast(prefix) + found
        return SQL.cast(empty_value)

    @property
    def sql(self):
        return SQL.cast(self.verb) \
            + self.incorporate('columns', empty_value=self.table._star) \
            + 'FROM' + self.table \
            + self.incorporate('order', prefix='ORDER BY') \
            + self.last('limit', prefix='LIMIT')

# -----------------------------------------------------------------------------
# Sanity test stuff
# -----------------------------------------------------------------------------
example = SQL.cast(schema.hello.world)
assert example.text == '`hello`.`world`', example.text
assert example.args == (), example.args

SELECT = SQL('SELECT')
FROM   = SQL('FROM')

query = SELECT + schema.name_id + FROM + schema.jrnl + 'ORDER BY t_created'
assert query.text == 'SELECT `name_id` FROM `jrnl` ORDER BY t_created', query.text
assert query.args == (), query.args

ASC  = SQL('ASC')
DESC = SQL('DESC')
j = schema.jrnl
query = Query.select(j).order(j.t_created, DESC).order(j.jrnl_id, ASC)
print(query.sql)
