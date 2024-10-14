import os
import sqlexecx
import functools
from .log_support import logger
from mysqlx.support import SqlAction, DBError
from mysqlx.sql_support import simple_sql, get_named_sql_args
from mysqlx.sql_holder import get_sql_model, do_get_sql, build_sql_id
from mysqlx.sql_mapper import get_exec_func, get_select_func, before

_UPDATE_ACTIONS = (SqlAction.INSERT.value, SqlAction.UPDATE.value, SqlAction.DELETE.value, SqlAction.CALL.value)


def mapper(namespace: str = None, sql_id: str = None, batch=False, return_key=False, select_key=None):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            param_names = func.__code__.co_varnames
            full_sql_id, func_name = before(func, namespace, sql_id, *args, **kwargs)
            sql_model = get_sql_model(full_sql_id)
            exec_func = get_exec_func(func, sql_model.action, batch)
            if return_key:
                use_select_key = select_key
                use_sql, args = do_get_sql(sql_model, batch, param_names, *args, **kwargs)
                if use_select_key is None:
                    use_select_key = sql_model.select_key
                    if use_select_key is None:
                        try:
                            use_select_key = sqlexecx.Dialect.get_select_key(sql=use_sql)
                        except NotImplementedError:
                            return DBError(
                                f"Expect 'select_key' but not. you can set it in mapper file with 'selectKey', or @mapper with 'select_key'")
                return sqlexecx.do_save_sql_select_key(use_select_key, use_sql, *args)
            if batch:
                if kwargs:
                    logger.warning("Batch exec sql better use like '{}(args)' or '{}(*args)' then '{}(args=args)'".format(func_name, func_name, func_name))
                    args = list(kwargs.values())[0]
                use_sql, _ = do_get_sql(sql_model, batch, param_names, *args)
            else:
                use_sql, args = do_get_sql(sql_model, batch, param_names, *args, **kwargs)
            return exec_func(use_sql, *args)

        return _wrapper

    return _decorator


def sql(value: str, batch=False, return_key=False, select_key=None):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_sql = value
            low_sql = value.lower()
            if any([action in low_sql for action in _UPDATE_ACTIONS]):
                if batch:
                    if kwargs:
                        args = list(kwargs.values())[0]
                    return sqlexecx.batch_execute(use_sql, *args)
                if return_key:
                    use_select_key = select_key
                    if use_select_key is None:
                        try:
                            use_select_key = sqlexecx.Dialect.get_select_key(sql=use_sql)
                        except NotImplementedError:
                            return DBError(f"Expect 'select_key' but not in func '{func.__name__}' at file: '{func.__code__.co_filename}', line {func.__code__.co_firstlineno}. you can set it @sql with 'select_key'")
                    assert SqlAction.INSERT.value in low_sql, 'Only insert sql can return primary key.'
                    if kwargs:
                        use_sql, args = get_named_sql_args(use_sql, **kwargs)
                    return sqlexecx.do_save_sql_select_key(use_select_key, use_sql, *args)

                if kwargs:
                    use_sql, args = get_named_sql_args(use_sql, **kwargs)
                return sqlexecx.do_execute(use_sql, *args)
            elif SqlAction.SELECT.value in low_sql:
                select_func = get_select_func(func)
                use_sql, args = simple_sql(use_sql, *args, **kwargs)
                return select_func(use_sql, *args)
            else:
                return ValueError("Invalid sql: {}.".format(sql))

        return _wrapper

    return _decorator
