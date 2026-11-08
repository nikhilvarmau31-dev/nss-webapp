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
        import sys
        path_info = environ.get('PATH_INFO', '')
        query_string = environ.get('QUERY_STRING', '')
        print(f"ENV_DEBUG_RAW: PATH_INFO='{path_info}' QUERY_STRING='{query_string}'", file=sys.stderr)

        # In Vercel serverless runtime, query string might be baked into PATH_INFO
        if '?' in path_info:
            path_part, _, qs_part = path_info.partition('?')
            path_info = path_part
            if not query_string:
                query_string = qs_part
            else:
                query_string = f"{qs_part}&{query_string}"

        if '__path=' in query_string:
            params = parse_qs(query_string, keep_blank_values=True)
            if '__path' in params:
                raw_path = params.pop('__path')[0]
                path_info = ('/' + raw_path.lstrip('/')) if raw_path else '/'
                query_string = urlencode(params, doseq=True)
        elif path_info in ('/api/index', '/api/index/'):
            path_info = '/'

        print(f"ENV_DEBUG_FINAL: PATH_INFO='{path_info}' QUERY_STRING='{query_string}'", file=sys.stderr)

        environ['PATH_INFO'] = path_info
        environ['QUERY_STRING'] = query_string
        environ['SCRIPT_NAME'] = ''

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelWSGIMiddleware(app.wsgi_app)
