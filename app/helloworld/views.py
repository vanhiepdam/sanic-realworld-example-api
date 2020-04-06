# -*- coding: utf-8 -*-

from app.base.base_view import ViewBaseMixin


class HelloWorldViewMixin(ViewBaseMixin):
    @classmethod
    def get_hello_world(cls):
        return {
            'hello': 'world'
        }
