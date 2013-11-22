from flask import Flask
import app
import unittest
import json
from polliste.models import Pol, Brewery
import os



class PolApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app(os.environ.get("TEST_DATABASE_URL", 'sqlite:///test_db.db'))
        self.app.config['TESTING'] = True
        self.app.debug = True

        pol1 = Pol("pol 1")
        pol2 = Pol("pol 2")
        pol3 = Pol("pol 3")

        self.app.db_session.add(pol1)
        self.app.db_session.add(pol2)
        self.app.db_session.add(pol3)

        self.app.db_session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        self.app.db_session.remove()
        self.app.db_metadata.drop_all(self.app.db_engine)

    def test_api_can_list_pol(self):
        rv = self.client.get("/api/v1/pol/")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 3)

    def test_can_get_pol_by_id(self):
        rv = self.client.get("/api/v1/pol/1")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "pol 1")

    def test_can_create_pol(self):

        data = { "name": "Pol 4"}
        rv = self.client.post(
            "/api/v1/pol/",
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(201, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "Pol 4")
        self.assertEqual(data["id"], 4)
        self.assertEqual(len(self.app.db_session.query(Pol).all()), 4)

class BreweryApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app(os.environ.get("TEST_DATABASE_URL", 'sqlite:///test_db.db'))
        self.app.config['TESTING'] = True
        self.app.debug = True

        brewery1 = Brewery("Noe")
        brewery2 = Brewery("Noe mer")
        brewery3 = Brewery("Noe mer 2")

        self.app.db_session.add(brewery1)
        self.app.db_session.add(brewery2)
        self.app.db_session.add(brewery3)

        self.app.db_session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        self.app.db_session.remove()
        self.app.db_metadata.drop_all(self.app.db_engine)

    def test_can_create_brewery(self):
        data = { "name": "Brewery1"}
        rv = self.client.post(
            "/api/v1/breweries/",
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(201, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "Brewery1")
        self.assertEqual(data["id"], 4)

    def test_can_search_for_brewery(self):
        rv = self.client.get("/api/v1/breweries/?query=noe")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 3)

        rv = self.client.get("/api/v1/breweries/?query=noe%20mer")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 2)

        rv = self.client.get("/api/v1/breweries/?query=noe%20mer%202")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)