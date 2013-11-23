from flask import render_template, g, abort
from webassets.loaders import PythonLoader
from flask.ext.assets import Environment, Bundle
from flask.ext.login import current_user
from flask.ext.login import login_required
from functools import wraps

from login_setup import setup_login


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function



def setup_views(app):
    assets = Environment(app)
    bundles = PythonLoader('assetbundle').load_bundles()
    for name, bundle in bundles.iteritems():
        assets.register(name, bundle)

    setup_login(app)

    @app.before_request
    def before_request():
        g.user = current_user

    @app.route('/')
    def index():
        return render_template("base.html")

    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/admin')
    @login_required
    @admin_required
    def admin():
        return render_template("admin.html")