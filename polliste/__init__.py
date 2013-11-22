from flask import Flask
#from webassets.loaders import PythonLoader
#from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

#assets = Environment(app)
#bundles = PythonLoader('assetbundle').load_bundles()
#for name, bundle in bundles.iteritems():
#    assets.register(name, bundle)

from polliste import views, models, api
