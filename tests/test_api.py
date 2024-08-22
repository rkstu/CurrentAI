import unittest
from app import create_app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_add_user(self):
        response = self.client.post('/api/add_user', json={
            "emailId": "test@example.com",
            "password": "test123",
            "first_name": "Test",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 201)
    
    def test_sentiment_analysis(self):
        response = self.client.post('/api/sentiment', json={
            "sentences": ["I love programming.", "I hate bugs."]
        })
        self.assertEqual(response.status_code, 200)
    
    # Add more tests for other endpoints

if __name__ == '__main__':
    unittest.main()
