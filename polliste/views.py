from flask import render_template
from webassets.loaders import PythonLoader
from flask.ext.assets import Environment, Bundle

def setup_views(app):
    assets = Environment(app)
    bundles = PythonLoader('assetbundle').load_bundles()
    for name, bundle in bundles.iteritems():
        assets.register(name, bundle)


    @app.route('/')
    def hello_world():
        return render_template("base.html")
