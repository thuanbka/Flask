# test_app.py
import unittest
import json
from my_app import create_app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app  = create_app()
        app.config["TESTING"] = True
        app.config["SUPPORT_FRONT_END"] = False
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["message"], 'WELLCOME HOME!!')

    def test_welcome(self):
        response = self.app.get('/welcome')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["message"], 'WELCOME to WELCOME')

if __name__ == '__main__':
    unittest.main()

