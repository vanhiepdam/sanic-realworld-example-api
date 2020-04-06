# -*- coding: utf-8 -*-
import json

from tests.base_test import TestBase


class AuthTest(TestBase):
    def test_register(self):
        request, response = self.app.test_client.post('/api/1/register', data=json.dumps({
            'username': 'user_test',
            'password': 'test',
            'email': 'test@test.com'
        }))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
