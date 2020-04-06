from tests.base_test import TestBase


class HelloWorldTest(TestBase):
    def test_helloworld(self):
        request, response = self.app.test_client.get('/api/1/')

        self.assertEqual(response.status_code, 200)
