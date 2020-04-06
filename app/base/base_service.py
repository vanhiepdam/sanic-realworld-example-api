# -*- coding: utf-8 -*-
import copy

from app.database import session_connect


class ServiceBaseMixin(object):
    model = None

    @classmethod
    def get_queryset(cls, criteria=None):
        """
        criteria format:
        {
            column: :VALUE | [:OPERATOR, :VALUE],
            limit: :LIMIT, (OPTIONAL)
            offset: :OFFSET (OPTIONAL)
        }
        :OPERATOR: sqlalchemy's operator
        """
        with session_connect() as session:
            queryset = session.query(cls.model)
            if criteria is not None:
                for field_name in criteria:
                    try:
                        field = getattr(cls.model, field_name)
                        if isinstance(criteria[field_name], list) \
                                and len(criteria[field_name]) == 2:
                            operator, filter_value = criteria[field_name]
                            queryset = queryset.filter(
                                getattr(field, operator)(filter_value)
                            )
                        else:
                            queryset = queryset.filter(field == criteria[field_name])
                    except AttributeError:
                        continue
        return queryset

    @classmethod
    def paginate_query(cls, queryset, limit, offset):
        if offset:
            queryset = queryset.offset(offset)
        if limit:
            queryset = queryset.limit(limit)

        return queryset

    @classmethod
    def list(cls, criteria=None):
        instances = cls.get_queryset(criteria=criteria)

        return instances

    @classmethod
    def get_by_id(cls, obj_id: str):
        with session_connect() as session:
            instance = session.query(cls.model).get(obj_id)
        return instance

    @classmethod
    def update_by_id(cls, obj_id, data: dict):
        with session_connect() as session:
            instance = session.query(cls.model).get(obj_id)
            instance.fill(data)

        return instance

    @classmethod
    def create(cls, data):
        with session_connect() as session:
            instance = cls.model(**data)
            session.add(instance)
            session.flush()
            instance_copy = copy.deepcopy(instance)
        return instance_copy

    @classmethod
    def delete(cls, ids: list):
        if not isinstance(ids, list):
            ids = [ids]
        with session_connect() as session:
            instances = session.query(cls.model).filter(cls.model.id.in_(ids))
            instances.delete(synchronize_session=None)
        return ids

    @classmethod
    def count_items(cls, criteria=None):
        queryset = cls.get_queryset(criteria)

        return queryset.count()
