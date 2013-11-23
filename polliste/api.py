from flask import current_app, request
from flask.ext import restful
from flask.ext.restful import abort, fields, marshal, marshal_with
from models import Pol, Brewery, Beer

pol_fields = {
    'id': fields.Integer,
    'name': fields.String
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
    def post(self):
        data = request.get_json()
        name = data.get('name')
        if name is None:
            abort(400)
        pol = Pol(name)
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

def create_api(app, api_version):
    api = restful.Api(app)
    api.add_resource(PolResource, '/api/%s/pol/' % api_version)
    api.add_resource(SinglePolResource, '/api/%s/pol/<int:pol_id>' % api_version)
    api.add_resource(BreweryResource, '/api/%s/breweries/' % api_version)
    api.add_resource(BeerResource, '/api/%s/beers/' % api_version)
    return app