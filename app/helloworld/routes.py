# -*- coding: utf-8 -*-
from app.helloworld.views import HelloWorldViewMixin
from app.middlewares import to_json_response, add_cors_header, prevent_xss


def setup_v1(base_url, app):
    hello_url = base_url + "/"

    @app.route(hello_url + '', methods=['GET'])
    @prevent_xss
    @add_cors_header(app)
    @to_json_response
    async def hello_word(request):
        return HelloWorldViewMixin.get_hello_world(), 200
