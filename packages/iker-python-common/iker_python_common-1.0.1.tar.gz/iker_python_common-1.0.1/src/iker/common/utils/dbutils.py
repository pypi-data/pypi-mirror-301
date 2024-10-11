import contextlib
import dataclasses
import datetime
import urllib.parse
from typing import Any, ContextManager, Type

import psycopg2
import psycopg2.extensions
import sqlalchemy
import sqlalchemy.ext.compiler
import sqlalchemy.orm

from iker.common.utils.funcutils import singleton
from iker.common.utils.sequtils import head_or_none
from iker.common.utils.strutils import is_blank

__all__ = [
    "DBAdapter",
    "orm_to_dict",
    "orm_clone",
    "to_pg_date",
    "to_pg_time",
    "to_pg_ts",
    "to_pg_ts",
    "pg_date_max",
    "pg_ts_max",
    "mysql_insert_ignore",
    "postgresql_insert_on_conflict_do_nothing",
]


class DBAdapter(object):
    """
    Database adapter
    """

    class Drivers:
        Mysql = "mysql+mysqldb"
        Postgresql = "postgresql+psycopg2"

    def __init__(
        self,
        driver: str,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        engine_opts: dict[str, Any] | None = None,
        session_opts: dict[str, Any] | None = None,
    ):
        self.driver = driver
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.engine_opts = engine_opts or {}
        self.session_opts = session_opts or {}

    @property
    def connection_string(self) -> str:
        port_part = "" if self.port is None else (":%d" % self.port)
        user_part = urllib.parse.quote(self.user, safe="")
        password_part = "" if is_blank(self.password) else (":%s" % urllib.parse.quote(self.password, safe=""))
        database_part = urllib.parse.quote(self.database, safe="")

        return f"{self.driver}://{user_part}{password_part}@{self.host}{port_part}/{database_part}"

    @property
    def engine(self) -> sqlalchemy.Engine:
        return sqlalchemy.create_engine(self.connection_string, **self.engine_opts)

    def make_connection(self):
        return self.engine.connect()

    def make_session(self, **kwargs) -> ContextManager[sqlalchemy.orm.Session]:
        return contextlib.closing(sqlalchemy.orm.sessionmaker(self.engine, **{**self.session_opts, **kwargs})())

    def create_model(self, orm_base: Type[sqlalchemy.orm.DeclarativeBase]):
        orm_base.metadata.create_all(self.engine)

    def drop_model(self, orm_base: Type[sqlalchemy.orm.DeclarativeBase]):
        orm_base.metadata.drop_all(self.engine)

    def execute(self, sql: str, **params):
        """
        Executes the given SQL statement with the specific parameters

        :param sql: SQL statement to execute
        :param params: parameters dict
        """
        with self.make_connection() as connection:
            connection.execute(sqlalchemy.text(sql), params)
            connection.commit()

    def query_all(self, sql: str, **params) -> list[tuple]:
        """
        Executes the given SQL query with the specific parameters and returns all the results

        :param sql: SQL query to execute
        :param params: parameters dict
        :return: result tuples list
        """
        with self.make_connection() as connection:
            with contextlib.closing(connection.execute(sqlalchemy.text(sql), params)) as proxy:
                return [item for item in proxy.fetchall()]

    def query_first(self, sql: str, **params) -> tuple | None:
        """
        Executes the given SQL query with the specific parameters and returns the first result tuple

        :param sql: SQL query to execute
        :param params: parameters dict
        :return: the first result tuple
        """
        return head_or_none(self.query_all(sql, **params))


def orm_to_dict(orm: sqlalchemy.orm.DeclarativeBase, exclude: set[str] = None) -> dict[str, Any]:
    if not isinstance(orm, sqlalchemy.orm.DeclarativeBase):
        raise TypeError('not a SQLAlchemy ORM declarative base')

    mapper = sqlalchemy.inspect(type(orm))
    return dict((c.key, getattr(orm, c.key)) for c in mapper.columns if c.key not in (exclude or set()))


def orm_clone(orm: sqlalchemy.orm.DeclarativeBase, exclude: set[str] = None, no_autoincrement: bool = False):
    if not isinstance(orm, sqlalchemy.orm.DeclarativeBase):
        raise TypeError('not a SQLAlchemy ORM declarative base')

    mapper = sqlalchemy.inspect(type(orm))
    exclude = exclude or (set(c.key for c in mapper.columns if c.autoincrement is True) if no_autoincrement else set())
    fields = orm_to_dict(orm, exclude)

    if not dataclasses.is_dataclass(orm):
        return type(orm)(**fields)

    init_fields = dict((field.name, fields.get(field.name)) for field in dataclasses.fields(orm) if field.init)

    new_orm = type(orm)(**init_fields)
    for name, value in fields.items():
        if name not in init_fields:
            setattr(new_orm, name, value)
    return new_orm


def to_pg_date(dt: datetime.datetime | datetime.date | int | float):
    if isinstance(dt, (datetime.datetime, datetime.date)):
        return psycopg2.extensions.DateFromPy(dt)
    elif isinstance(dt, (int, float)):
        return psycopg2.DateFromTicks(dt)
    raise TypeError("should be one of 'datetime.datetime', 'datetime.date', 'int', 'float'")


def to_pg_time(dt: datetime.time | int | float):
    if isinstance(dt, datetime.time):
        return psycopg2.extensions.TimeFromPy(dt)
    elif isinstance(dt, (int, float)):
        return psycopg2.TimeFromTicks(dt)
    raise TypeError("should be one of 'datetime.time', 'int', 'float'")


def to_pg_ts(dt: datetime.datetime | datetime.date | int | float):
    if isinstance(dt, (datetime.datetime, datetime.date)):
        return psycopg2.extensions.TimestampFromPy(dt)
    elif isinstance(dt, (int, float)):
        return psycopg2.TimestampFromTicks(dt)
    raise TypeError("should be one of 'datetime.datetime', 'datetime.date', 'int', 'float'")


@singleton
def pg_date_max():
    return psycopg2.Date(9999, 12, 31)


@singleton
def pg_ts_max():
    return psycopg2.Timestamp(9999, 12, 31, 23, 59, 59.999, tzinfo=datetime.timezone.utc)


def mysql_insert_ignore(enabled: bool = True):
    @sqlalchemy.ext.compiler.compiles(sqlalchemy.sql.Insert, "mysql")
    def dispatch(insert: sqlalchemy.sql.Insert, compiler: sqlalchemy.sql.compiler.SQLCompiler, **kwargs) -> str:
        if not enabled:
            return compiler.visit_insert(insert, **kwargs)

        return compiler.visit_insert(insert.prefix_with("IGNORE"), **kwargs)


def postgresql_insert_on_conflict_do_nothing(enabled: bool = True):
    @sqlalchemy.ext.compiler.compiles(sqlalchemy.sql.Insert, "postgresql")
    def dispatch(insert: sqlalchemy.sql.Insert, compiler: sqlalchemy.sql.compiler.SQLCompiler, **kwargs) -> str:
        if not enabled:
            return compiler.visit_insert(insert, **kwargs)

        statement = compiler.visit_insert(insert, **kwargs)
        # If we have a "RETURNING" clause, we must insert before it
        returning_position = statement.find("RETURNING")
        if returning_position >= 0:
            return statement[:returning_position] + " ON CONFLICT DO NOTHING " + statement[returning_position:]
        else:
            return statement + " ON CONFLICT DO NOTHING"
