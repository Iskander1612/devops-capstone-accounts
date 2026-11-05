"""Security policy contract tests."""
from unittest import TestCase
from service import app


class TestSecurity(TestCase):
    """Verify headers and browser access policies."""

    def test_headers(self):
        """It should emit Talisman security headers."""
        response = app.test_client().get('/health')
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn("default-src 'self'", response.headers['Content-Security-Policy'])

    def test_cors(self):
        """It should support CORS and preflight without credentials."""
        client = app.test_client()
        origin = 'https://example.com'
        response = client.get('/accounts', headers={'Origin': origin})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], origin)
        response = client.options('/accounts', headers={
            'Origin': origin, 'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('POST', response.headers['Access-Control-Allow-Methods'])
        self.assertNotIn('Access-Control-Allow-Credentials', response.headers)
