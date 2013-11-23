import os
from flask import Flask
from database import init_db
from polliste.api import create_api
from polliste.views import setup_views

API_VERSION = 'v1'

def create_app(db_url):

    path = os.path.dirname(os.path.abspath(__file__))
    tmpl_dir = os.path.join(path, 'polliste/templates')
    static_dir = os.path.join(path, 'polliste/static')

    app = Flask(__name__, template_folder=tmpl_dir, static_folder=static_dir)
    app.secret_key = os.environ.get('SECRET_KEY', 'development_fallback')

    (app.db_session, app.db_metadata, app.db_engine) = init_db(db_url)



    @app.teardown_request
    def shutdown_session(exception=None):
        app.db_session.remove()

    setup_views(app)
    create_api(app, API_VERSION)
    return app			

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app = create_app(os.environ.get(
        'DATABASE_URL',
        'sqlite:////tmp/polliste.db')
    )
    app.run(host='0.0.0.0', port=port, debug=True)