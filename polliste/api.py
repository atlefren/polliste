from flask import current_app, request, g
from flask.ext import restful
from flask.ext.restful import abort, fields, marshal, marshal_with
from functools import wraps

from models import Pol, Brewery, Beer, Observation


def ensure_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.is_authenticated():
            return func(*args, **kwargs)
        restful.abort(401)
    return wrapper

def ensure_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.is_authenticated() and g.user.is_admin:
            return func(*args, **kwargs)
        restful.abort(401)
    return wrapper

pol_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
}

class SinglePolResource(restful.Resource):
    @marshal_with(pol_fields)
    def get(self, pol_id):
        if pol_id is None:
            abort(405)
        pol = current_app.db_session.query(Pol).get(pol_id)
        if pol is None:
            abort(404)
        return pol

class PolResource(restful.Resource):

    @marshal_with(pol_fields)
    def get(self):
        pol = current_app.db_session.query(Pol)
        return pol.all()

    @marshal_with(pol_fields)
    @ensure_user
    @ensure_admin
    def post(self):
        data = request.get_json()
        name = data.pop('name')
        if name is None:
            abort(400)
        pol = Pol(name, **data)
        current_app.db_session.add(pol)
        current_app.db_session.commit()

        current_app.db_session.refresh(pol)
        return pol, 201

brewery_fields = {
    'id': fields.Integer,
    'name': fields.String
}

class BreweryResource(restful.Resource):

    @marshal_with(brewery_fields)
    def get(self):

        breweries = current_app.db_session.query(Brewery)

        if request.args.get("query"):
            name_filter = Brewery.name.ilike('%%%s%%' % request.args['query'])
            breweries = breweries.filter(name_filter)
        return breweries.all()


    @marshal_with(brewery_fields)
    @ensure_user
    def post(self):
        data = request.get_json()
        name = data.get('name')
        if name is None:
            abort(400)
        brewery = Brewery(name)
        current_app.db_session.add(brewery)
        current_app.db_session.commit()

        current_app.db_session.refresh(brewery)
        return brewery, 201

beer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'style': fields.String,
    'size': fields.Raw,
    'abv': fields.Raw,
    'brewery': fields.Nested(brewery_fields)
}

class BeerResource(restful.Resource):

    @marshal_with(beer_fields)
    def get(self):
        beers = current_app.db_session.query(Beer)

        if request.args.get("query"):
            name_filter = Beer.name.ilike('%%%s%%' % request.args['query'])
            beers = beers.filter(name_filter)
        return beers.all()


    @marshal_with(beer_fields)
    @ensure_user
    def post(self):
        data = request.get_json()
        name = data.pop('name')
        brewery_id = data.pop("brewery")
        if name is None or brewery_id is None:
            abort(400)

        brewery = current_app.db_session.query(Brewery).get(brewery_id)
        beer = Beer(name, brewery, **data)
        current_app.db_session.add(beer)
        current_app.db_session.commit()
        current_app.db_session.refresh(beer)

        return beer, 201

class DateTime(fields.Raw):
    def format(self, value):
        return value.isoformat()

observation_fields = {
    'id': fields.Integer,
    'pol': fields.Nested(pol_fields),
    'time': DateTime,
    'beer': fields.Nested(beer_fields),
    'comment': fields.String
}

class ObservationResource(restful.Resource):
    @marshal_with(observation_fields)
    @ensure_user
    def post(self, pol_id):
        data = request.get_json()
        beer_id = data.pop('beer')

        pol = current_app.db_session.query(Pol).get(pol_id)
        beer = current_app.db_session.query(Beer).get(beer_id)

        if beer is None or pol is None:
            abort(400)

        comment = data.pop("comment", None)
        observation = Observation(beer, g.user, pol, comment)

        current_app.db_session.add(observation)
        current_app.db_session.commit()
        current_app.db_session.refresh(observation)

        return observation, 201

def create_api(app, api_version):
    api = restful.Api(app)
    api.add_resource(PolResource, '/api/%s/pol/' % api_version)
    api.add_resource(SinglePolResource, '/api/%s/pol/<int:pol_id>' % api_version)
    api.add_resource(BreweryResource, '/api/%s/breweries/' % api_version)
    api.add_resource(BeerResource, '/api/%s/beers/' % api_version)
    api.add_resource(ObservationResource, '/api/%s/pol/<int:pol_id>/observations/' % api_version)
    return app