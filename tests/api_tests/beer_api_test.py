from flask import Flask
import unittest
import json

from polliste.models import Beer, Brewery, User
from test_config import setup_app, remove_app

class BeerApiTest(unittest.TestCase):
    def setUp(self):
        self.app, self.client = setup_app()

        brewery1 = Brewery("Brewery 1")

        beer1 = Beer("Beer 1", brewery1)
        beer2 = Beer("test ", brewery1)
        beer3 = Beer("Beer 2", brewery1)

        self.app.db_session.add(brewery1)
        self.app.db_session.add(beer1)
        self.app.db_session.add(beer2)
        self.app.db_session.add(beer3)
        self.app.db_session.commit()

    def tearDown(self):
        remove_app(self.app)

    def test_user_can_create_beer(self):

        u = User(username='a', email='a@b.c', name='a', role=0)
        self.app.db_session.add(u)
        self.app.db_session.commit()
        # login user
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = int(u.get_id())
                sess['_fresh'] = True

            data = { "name": "Beer 1", "brewery": 1, "style": "lager", "abv": 4.5, "size": 33}
            rv = c.post(
                "/api/v1/beers/",
                data = json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data["id"], 4)
        self.assertEqual(data["name"], "Beer 1")
        self.assertEqual(data["abv"], 4.5)
        self.assertEqual(data["size"], 33)
        self.assertEqual(data["style"], "lager")
        self.assertEqual(data["brewery"]["id"], 1)
        self.assertEqual(data["brewery"]["name"], "Brewery 1")

    def test_user_can_create_beer_with_just_name_and_brewery(self):

        u = User(username='a', email='a@b.c', name='a', role=0)
        self.app.db_session.add(u)
        self.app.db_session.commit()
        # login user
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = int(u.get_id())
                sess['_fresh'] = True

            data = { "name": "Beer 1", "brewery": 1}
            rv = c.post(
                "/api/v1/beers/",
                data = json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data["id"], 4)
        self.assertEqual(data["name"], "Beer 1")
        self.assertEqual(data["abv"], None)
        self.assertEqual(data["size"], None)
        self.assertEqual(data["style"], None)
        self.assertEqual(data["brewery"]["id"], 1)
        self.assertEqual(data["brewery"]["name"], "Brewery 1")

    def test_anonymous_create_beer(self):
        data = { "name": "Beer 1", "brewery": 1, "style": "lager", "abv": 4.5, "size": 33}
        rv = self.client.post(
            "/api/v1/beers/",
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(rv.status_code, 401)

    def test_can_search_for_beer(self):
        rv = self.client.get("/api/v1/beers/?query=beer")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 2)

        rv = self.client.get("/api/v1/beers/?query=beer 1")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)

    def xtest_can_search_for_beer_and_brewery(self):
        rv = self.client.get("/api/v1/beers/?query=brewery 1 test")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)