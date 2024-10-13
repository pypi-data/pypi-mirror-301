import io
import logging
import json
from unittest import TestCase
from contextlib import redirect_stderr
from src.gcp_microservice_utils import setup_cloud_logging


class TestLogging(TestCase):
    def test_structured_log(self):
        with redirect_stderr(io.StringIO()) as mock_stderr:
            setup_cloud_logging()
            logging.warning('Structured log test')

        for msg in mock_stderr.getvalue().splitlines():
            self.assertIn('logging.googleapis.com/labels', json.loads(msg))
