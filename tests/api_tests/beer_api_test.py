from flask import Flask
import unittest
import json

from polliste.models import Beer, Brewery
from test_config import setup_app, remove_app

class BeerApiTest(unittest.TestCase):
    def setUp(self):
        self.app, self.client = setup_app()

        brewery1 = Brewery("Brewery 1")
        self.app.db_session.add(brewery1)
        self.app.db_session.commit()

    def tearDown(self):
        remove_app(self.app)

    def test_can_create_beer(self):
        data = { "name": "Beer 1", "brewery": 1, "style": "lager", "abv": 4.5, "size": 33}
        rv = self.client.post(
            "/api/v1/beers/",
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(201, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Beer 1")
        self.assertEqual(data["abv"], 4.5)
        self.assertEqual(data["size"], 33)
        self.assertEqual(data["style"], "lager")
        self.assertEqual(data["brewery"]["id"], 1)
        self.assertEqual(data["brewery"]["name"], "Brewery 1")