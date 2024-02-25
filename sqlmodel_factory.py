from typing import List, Union, Generic, TypeVar
from sqlmodel.sql.sqltypes import AutoString
from sqlalchemy import Column, types
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

T = TypeVar("T")


class SQLModelFactory(SQLAlchemyFactory[T]):
    __is_base_factory__ = True
    @classmethod
    def get_type_from_column(cls, column: Column) -> type:
        column_type = type(column.type)

        annotation = None
        if column_type == AutoString:
            annotation = str
        if annotation:
            return annotation

        if column_type in cls.get_sqlalchemy_types():
            annotation = column_type
        elif issubclass(column_type, types.ARRAY):
            annotation = List[column.type.item_type.python_type]  # type: ignore[assignment,name-defined]
        else:
            annotation = column.type.python_type
        if column.nullable:
            annotation = Union[annotation, None]  # type: ignore[assignment]

        return annotation
