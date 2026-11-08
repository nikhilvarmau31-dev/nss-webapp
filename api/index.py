import sys
import os

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class VercelPathFixer:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched_path = (
            environ.get('HTTP_X_MATCHED_PATH') or
            environ.get('HTTP_X_FORWARDED_URI') or
            environ.get('HTTP_X_VERCEL_MATCHED_PATH')
        )

        if matched_path and matched_path not in ('/api/index', '/api/index/'):
            environ['PATH_INFO'] = matched_path.split('?')[0]
        elif environ.get('PATH_INFO', '') in ('/api/index', '/api/index/'):
            environ['PATH_INFO'] = '/'
        elif environ.get('PATH_INFO', '').startswith('/api/index/'):
            environ['PATH_INFO'] = environ['PATH_INFO'][len('/api/index'):]

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathFixer(app.wsgi_app)
