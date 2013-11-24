from flask import Flask
import unittest
import json

from polliste.models import Brewery, User
from test_config import setup_app, remove_app

class BreweryApiTest(unittest.TestCase):

    def setUp(self):
        self.app, self.client = setup_app()
        brewery1 = Brewery("Noe")
        brewery2 = Brewery("Noe mer")
        brewery3 = Brewery("Noe mer 2")
        self.app.db_session.add(brewery1)
        self.app.db_session.add(brewery2)
        self.app.db_session.add(brewery3)
        self.app.db_session.commit()

    def tearDown(self):
        remove_app(self.app)

    def test_user_can_create_brewery(self):
        u = User(username='a', email='a@b.c', name='a', role=0)
        self.app.db_session.add(u)
        self.app.db_session.commit()
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = int(u.get_id())
                sess['_fresh'] = True

            data = { "name": "Brewery1"}
            rv = c.post(
                "/api/v1/breweries/",
                data = json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "Brewery1")
        self.assertEqual(data["id"], 4)

    def test_anonymous_cannot_create_brewery(self):
        data = { "name": "Brewery1"}
        rv = self.client.post(
            "/api/v1/breweries/",
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(rv.status_code, 401)

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