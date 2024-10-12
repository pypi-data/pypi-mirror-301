from collections import defaultdict
from datetime import datetime
from typing import Iterable, Type, Any

from asyncache import cached
from cachetools import TTLCache
from cachetools.keys import hashkey
from sqlalchemy import (
    Column,
    BinaryExpression,
    ColumnOperators,
    Sequence,
    Row,
    RowMapping, func, Select, select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from ..interface.crud import BaseDbModelType
from ..interface.crud import BaseSchemaType, BaseSchema


def remove_self(*argv, **kwarg):
    # убираем первый параметр - сессия
    return hashkey(*argv[1:], **kwarg)

@cached(TTLCache(maxsize=1024, ttl=300), key=remove_self)
async def get_record_count(session: AsyncSession, stmt: Select) -> int:
    stmt = select(func.count()).select_from(stmt)
    return (await session.scalars(stmt)).first()

def clause_for_column(field: Column, val) -> BinaryExpression | ColumnOperators:
    """Формирует условие для where()
    Если передано единичное значение или строка, то Column == val
    Если итерируемый объект, то Column.in_(val)
    Args:
        field: колонка
        val: значение
    Returns:
        BinaryExpression | ColumnOperators
    """
    if isinstance(val, Iterable) and not isinstance(val, str):
        vals = list(val)
        if (
            len(vals) == 2
            and isinstance(vals[0], datetime)
            and isinstance(vals[1], datetime)
        ):
            return field.between(vals[0], vals[1])
        return field.in_(val)
    elif isinstance(val, str) and "%" in val:
        return field.ilike(val)
    else:
        return field == val


def process_fields_to_model_and_relation(fields: tuple[str, ...]) -> (set, dict):
    """Преобразует набор полей в:
      - множество (set) полей непосредственно модели ("field")
      - словарь отношений [модель][поле] ("model.field")
    Args:
        fields: набор полей в формате "field" или "model.field"
    Returns:
        (множество полей модели, словарь отношений)
    """
    model = set()
    relation = defaultdict(dict)
    for f in fields:
        if "." in f:
            model_, field = f.split(".", 1)
            relation[model_][field] = 1
        else:
            model.add(f)
    return model, relation


def instance_to_model(
    instance: BaseSchema,
    model: BaseDbModelType,
    exclude_fields: set | None = None,
    update_fields: set | None = None,
) -> BaseDbModelType:
    """Преобразует Pydantic экземпляр в модель SqlAlchemy
    Args:
        instance: Pydantic экземпляр
        model: модель таблицы SqlAlchemy
        exclude_fields: поля которые исключаются из model_dump
        update_fields: если передано - то только эти поля будут выгружены  в модель SqlAlchemy

    Returns:
        экземпляр модели SqlAlchemy
    """
    if not exclude_fields:
        exclude_fields = {}
    # возьмем только те поля которые есть в модели SqlAlchemy
    include_fields: set = model.attribute_names()
    # если заданы update_fields (обновить только эти поля) - берем пересечение с полями модели
    if update_fields:
        include_fields.intersection(update_fields)
    instance = model(
        **instance.model_dump(exclude=exclude_fields, include=include_fields)
    )
    return instance


def prepare_update_data(
    instance: BaseSchema,
    model: BaseDbModelType,
    exclude_fields: tuple[str, ...] | None = None,
    update_fields: tuple[str, ...] | None = None,
) -> dict:
    """Преобразует Pydantic экземпляр в словарь для метода
     update() используемый для обновления данных в БД
    Args:
        instance: Pydantic экземпляр
        model: модель таблицы SqlAlchemy
        exclude_fields: поля которые исключаются из model_dump()
        update_fields: если передано - то только эти поля будут
         выгружены  в модель SqlAlchemy
    Returns:
        dict
    """

    update_data = instance.model_dump()
    for field, value in list(update_data.items()):
        if not hasattr(model, field):
            del update_data[field]
        if not isinstance(value, dict):
            continue
        submodel_ = getattr(model, field).entity.class_
        for subfield in list(update_data[field].keys()):
            if hasattr(submodel_, subfield):
                continue
            del update_data[field][subfield]

    result = defaultdict(dict)
    if update_fields:
        for f in update_fields:
            if "." in f:
                model_, field = f.split(".", 1)
                result[model_][field] = update_data[model_][field]
            else:
                result[f] = update_data[f]
        return result
    if exclude_fields:
        for f in exclude_fields:
            if "." in f:
                model_, field = f.split(".", 1)
                if model_ in update_data and field in update_data[model_]:
                    del update_data[model_][field]
            else:
                if f in update_data:
                    del update_data[f]

    return update_data


def prepare_where_clause(
    model: BaseDbModelType,
    filters: dict,
) -> (list, dict):
    """Формирует список условий поиска для where()
    Ищет поля, в том числе в relations модели SqlAlchemy
    Args:
        model: SqlAlchemy модель таблицы
        filters: список полей и значений для условий (словарь) или список полей
    Returns:
        список условий поиска
    """
    clause = []
    relationships = defaultdict(dict)
    options = dict()

    # Parse filters for direct attributes and relationships
    for attr, value in filters.items():
        if "." in attr:
            # It"s a relationship field
            rel_attr, rel_field = attr.split(".", 1)
            relationships[rel_attr][rel_field] = value
        else:
            # It"s a direct attribute of the model
            column = getattr(model, attr, None)
            clause.append(clause_for_column(column, value))

    # Для загрузки relation будем использовать
    # join совместно contains_eager
    for rel_attr, rel_filter in relationships.items():
        relation = getattr(model, rel_attr)
        options[relation] = contains_eager(relation)

        for attr, value in rel_filter.items():
            column = getattr(relation.property.mapper.class_, attr)
            clause.append(relation.has(clause_for_column(column, value)))

    return clause, options


def update_row(
    schema: BaseSchemaType, row: Row | RowMapping | Any, data: dict
) -> BaseSchemaType:
    for field, value in data.items():
        # обновим зависимости
        if isinstance(value, dict):
            if not hasattr(row, field):
                raise ValueError(f"Row {row} has no relation {field} from {data=}")
            relation = getattr(row, field)
            for subfield, subvalue in data[field].items():
                setattr(relation, subfield, subvalue)
            continue
        # обновим данные модели
        if not hasattr(row, field):
            raise ValueError(f"Row {row} has no field {field} from {data=}")
        setattr(row, field, value)
    return schema.model_validate(row)


def update_rows(
    schema: BaseSchemaType, rows: Sequence[Row | RowMapping | Any], data: dict
) -> list[BaseSchema]:
    results = []
    for row in rows:
        results.append(update_row(schema, row, data))
    return results
