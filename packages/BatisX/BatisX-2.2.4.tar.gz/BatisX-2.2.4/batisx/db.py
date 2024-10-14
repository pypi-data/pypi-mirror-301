from mysqlx import sql_support
# Don't remove. Import for not repetitive implementation
from sqlexecx import save_select_key, do_save_sql_select_key
from mysqlx.db import insert, save, execute, batch_insert, batch_execute, get, query, query_one, select, select_one, \
    do_execute, do_get, do_query, do_query_one, do_select, do_select_one, do_select_page, do_query_page, select_page, query_page,\
    do_save_sql, drop_table, truncate_table, sql, table, page


def save_sql(sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.

    Examples
    --------
    >>> import sqlexecx as db
    >>> sql = 'INSERT INTO person(name, age) VALUES(?, ?)'
    >>> db.save_sql(sql, '张三', 20)
    3
    >>> sql = 'INSERT INTO person(name, age) VALUES(:name, :age)'
    >>> db.save_sql(sql, name='张三', age=20)
    3
    """
    
    sql, args = sql_support.try_dynamic_sql('batisx.db.save_sql', sql, *args, **kwargs)
    return do_save_sql(sql, *args)


def save_sql_select_key(select_key: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.

    :param select_key: sql for select primary key
    :param sql: SQL
    :return: Primary key

    Examples
    --------
    >>> import sqlexecx as db
    >>> select_key = 'SELECT LAST_INSERT_ID()'
    >>> sql = 'INSERT INTO person(name, age) VALUES(?, ?)'
    >>> db.save_sql_select_key(select_key, sql, '张三', 20)
    3
    >>> sql = 'INSERT INTO person(name, age) VALUES(:name, :age)'
    >>> db.save_sql_select_key(select_key, sql, name='张三', age=20)
    3
    """
    
    sql, args = sql_support.try_dynamic_sql('batisx.db.save_sql', sql, *args, **kwargs)
    return do_save_sql_select_key(select_key, sql, *args)


from .sql_page_exec import sql, page
