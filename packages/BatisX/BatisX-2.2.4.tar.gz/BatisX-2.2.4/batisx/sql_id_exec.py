from . import dbx
from mysqlx.sql_id_exec import SqlExec as _SqlExec
from sqlexecx.page_exec import PageExec


class SqlExec(_SqlExec):

    def save_select_key(self, select_key: str, *args, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.exec.save_select_key(select_key, self.sql, *args, **kwargs)


def sql(sql: str) :
    assert sql, "Parameter 'sql' must not be none"
    return SqlExec(dbx, sql)


def page(page_num: int, page_size: int) :
    return PageExec(dbx, page_num, page_size)
