import os
import app

def setup_app():
    the_app = app.create_app(
        os.environ.get("TEST_DATABASE_URL", 'sqlite:////tmp/polliste_test_default.db')
    )
    the_app.config['TESTING'] = True
    the_app.debug = True
    client = the_app.test_client()
    return the_app, client

def remove_app(the_app):
    the_app.db_session.remove()
    the_app.db_metadata.drop_all(the_app.db_engine)