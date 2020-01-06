import pytest
from squirrel import SELECT, ns

def test_new():
    q = SELECT('foo')
    assert q.table == ns.foo

@pytest.mark.parametrize('q, sql', [
    (SELECT('foo'), 'SELECT * FROM `foo`'),
    (SELECT('foo', id=7), 'SELECT * FROM `foo` WHERE `foo`.`id` = %s'),
    (SELECT('foo', 'a b cd'), 'SELECT `foo`.`a`, `foo`.`b`, `foo`.`cd` FROM `foo`'),
    (SELECT('foo', 'a').WHERE(), 'SELECT `foo`.`a` FROM `foo`'),
    (SELECT('foo', 'a').WHERE(b=5), 'SELECT `foo`.`a` FROM `foo` WHERE `foo`.`b` = %s'),
    (SELECT('foo', 'a').WHERE(ns.foo.cd == 'apple', b=5), 'SELECT `foo`.`a` FROM `foo` WHERE `foo`.`cd` = %s AND `foo`.`b` = %s'),
    (SELECT('foo', 'a').WHERE(id=('>', 4)), 'SELECT `foo`.`a` FROM `foo` WHERE `foo`.`id` > %s'),
    (SELECT('foo').WHERE(id=('>', 4)).LIMIT(5), 'SELECT * FROM `foo` WHERE `foo`.`id` > %s LIMIT %s'),
    (SELECT('foo').WHERE(first=1).WHERE(second=2), 'SELECT * FROM `foo` WHERE `foo`.`first` = %s AND `foo`.`second` = %s'),
    (SELECT('foo').LIMIT(5), 'SELECT * FROM `foo` LIMIT %s'),
    (SELECT('foo').LIMIT(5).OFFSET(10), 'SELECT * FROM `foo` LIMIT %s OFFSET %s'),
    (SELECT('foo').LIMIT(5, 10), 'SELECT * FROM `foo` LIMIT %s, %s'),

    (SELECT('foo').JOIN('bar', 'product_id category', quality=('>', 10)),
        'SELECT * FROM `foo` JOIN `bar` ON `bar`.`product_id` = `foo`.`product_id` AND `bar`.`category` = `foo`.`category` AND `bar`.`quality` > %s'),
    (SELECT('foo').JOIN('bar', 'id').JOIN('baz', 'baz_id').WHERE(id = 5),
        'SELECT * FROM `foo` JOIN `bar` ON `bar`.`id` = `foo`.`id` JOIN `baz` ON `baz`.`baz_id` = `foo`.`baz_id` WHERE `foo`.`id` = %s'),
])
def test_sql(q, sql):
    assert q.text == sql
