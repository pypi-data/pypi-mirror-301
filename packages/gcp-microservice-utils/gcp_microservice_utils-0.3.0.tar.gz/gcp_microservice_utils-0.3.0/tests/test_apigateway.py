import base64
import json
from unittest import TestCase
from flask import Flask, request
from src.gcp_microservice_utils import setup_apigateway


class TestApiGateway(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        setup_apigateway(self.app)

        self.client = self.app.test_client()

    def test_before_request_with_valid_userinfo(self):
        userinfo = {'sub': '12345', 'email': 'test@example.com'}
        userinfo_encoded = base64.urlsafe_b64encode(json.dumps(userinfo).encode()).decode()

        with self.client:
            self.client.get("/test", headers={'X-Apigateway-Api-Userinfo': userinfo_encoded})

            self.assertEqual(request.user_token, userinfo)

    def test_before_request_with_invalid_userinfo(self):
        with self.client:
            self.client.get("/test", headers={'X-Apigateway-Api-Userinfo': 'invalid'})

            self.assertIsNone(request.user_token)

    def test_before_request_without_userinfo(self):
        with self.client:
            self.client.get("/test")

            self.assertIsNone(request.user_token)
