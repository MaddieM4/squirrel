from collections import namedtuple

class Comparison(namedtuple('Comparison', ['field_name', 'comparison', 'value'])):
    def __repr__(self):
        return f'CMP<{self.field_name!r} {self.comparison} {self.value!r}>'

    def __and__(self, other):
        return AND([self, other])

class OR(list):
    def __repr__(self):
        return 'OR:' + list.__repr__(self)

    def __and__(self, other):
        return AND(self + [other])
        if isinstance(other, AND):
            return AND(self + other)
        else:
            clone = AND(self)
            clone.append(other)
            return clone

    def __or__(self, other):
        return OR(self + [other])

class AND(list):
    def __repr__(self):
        return 'AND:' + list.__repr__(self)

    def __and__(self, other):
        if isinstance(other, AND):
            return AND(self + other)
        else:
            clone = AND(self)
            clone.append(other)
            return clone

    def __or__(self, other):
        return OR(self, other)

def EQ(fn, v): return Comparison(fn, '=', v)
def NE(fn, v): return Comparison(fn,'!=', v)
def GT(fn, v): return Comparison(fn,'>' , v)
def GE(fn, v): return Comparison(fn,'>=', v)
def LT(fn, v): return Comparison(fn,'<' , v)
def LE(fn, v): return Comparison(fn,'<=', v)

class Tables(object):
    def __getattr__(self, t):
        return Table(t)

class Table(str):
    def __repr__(self):
        return f"T`{str(self)}`"

    def __getattr__(self, f):
        return Field(self, f)

class Field(namedtuple('Field', ['table', 'field'])):
    def __repr__(self):
        if self.table:
            return f"`{str(self.table)}`.`{self.field}`"
        return f"F`{self.field}`"

    def __eq__(self, value):
        return EQ(self, value)

tables = Tables()
