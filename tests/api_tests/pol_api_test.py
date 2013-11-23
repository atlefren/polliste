from flask import Flask
import unittest
import json

from polliste.models import Pol
from test_config import setup_app, remove_app

class PolApiTest(unittest.TestCase):
    def setUp(self):
        self.app, self.client = setup_app()

        pol1 = Pol("pol 1")
        pol2 = Pol("pol 2")
        pol3 = Pol("pol 3")

        self.app.db_session.add(pol1)
        self.app.db_session.add(pol2)
        self.app.db_session.add(pol3)

        self.app.db_session.commit()


    def tearDown(self):
        remove_app(self.app)

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