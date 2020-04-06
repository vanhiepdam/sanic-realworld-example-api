# -*- coding: utf-8 -*-
class ViewBaseMixin:
    LIMIT = 10
    OFFSET = 0

    @staticmethod
    def get_pagination_result(items, total, limit, offset):
        return {
            'items': items,
            'total': total,
            'limit': limit,
            'offset': offset
        }

    @staticmethod
    def deleted_message(obj_id):
        return {
            'id': obj_id,
            'deleted': 'ok'
        }
