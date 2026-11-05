"""Test JSON errors and database configuration defaults."""
from unittest import TestCase
from service import app
from service.common.error_handlers import internal_server_error


class TestErrorHandlers(TestCase):
    """API errors remain machine-readable."""

    def test_server_error(self):
        """It should format internal failures as a JSON 500 response."""
        with app.app_context():
            response, code = internal_server_error(RuntimeError('test failure'))
            self.assertEqual(code, 500)
            self.assertEqual(response.get_json()['error'], 'Internal Server Error')
