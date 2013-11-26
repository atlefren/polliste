from flask import render_template, g, abort
from webassets.loaders import PythonLoader
from flask.ext.assets import Environment, Bundle
from flask.ext.login import current_user
from flask.ext.login import login_required
from functools import wraps

from models import Pol, Observation
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
        pol = app.db_session.query(Pol).all()
        print pol
        return render_template("index.html", pol_list=pol)

    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/pol/<int:pol_id>')
    def pol(pol_id):
        pol = app.db_session.query(Pol).get(pol_id)

        observations = app.db_session.query(Observation).filter(Observation.pol==pol).all()

        print observations

        if pol is None:
            abort(404)
        return render_template("pol.html", pol=pol, observations=observations)

    @app.route('/admin')
    @login_required
    @admin_required
    def admin():
        return render_template("admin.html")