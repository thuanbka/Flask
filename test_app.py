# test_app.py
import unittest
import json
from demo_jwt import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
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

