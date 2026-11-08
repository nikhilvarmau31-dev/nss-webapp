import sys
import os
from urllib.parse import parse_qs, urlencode

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class VercelWSGIMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get('QUERY_STRING', '')
        if '__path=' in qs:
            params = parse_qs(qs, keep_blank_values=True)
            if '__path' in params:
                raw_path = params.pop('__path')[0]
                environ['PATH_INFO'] = ('/' + raw_path.lstrip('/')) if raw_path else '/'
                environ['QUERY_STRING'] = urlencode(params, doseq=True)
        elif environ.get('PATH_INFO', '') in ('/api/index', '/api/index/'):
            environ['PATH_INFO'] = '/'

        environ['SCRIPT_NAME'] = ''

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelWSGIMiddleware(app.wsgi_app)
