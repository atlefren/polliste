from flask import Flask
import unittest
import json

from polliste.models import Pol, User
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

    def test_logged_in_admin_can_create_pol(self):
        u = User(username='a', email='a@b.c', name='a', role=1)
        self.app.db_session.add(u)
        self.app.db_session.commit()
        # login user
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = int(u.get_id())
                sess['_fresh'] = True

            data = { "name": "Pol 4", "address": "address bla bla"}
            rv = c.post(
                "/api/v1/pol/",
                data = json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "Pol 4")
        self.assertEqual(data["address"], "address bla bla")
        self.assertEqual(data["id"], 4)
        self.assertEqual(len(self.app.db_session.query(Pol).all()), 4)

    def test_logged_in_user_cannot_create_pol(self):
        u = User(username='a', email='a@b.c', name='a', role=0)
        self.app.db_session.add(u)
        self.app.db_session.commit()
        # login user
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = int(u.get_id())
                sess['_fresh'] = True

            data = { "name": "Pol 4"}
            rv = c.post(
                "/api/v1/pol/",
                data = json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(rv.status_code, 401)

    def test_anonymous_cannot_create_pol(self):
        u = User(username='a', email='a@b.c', name='a', role=0)
        self.app.db_session.add(u)
        self.app.db_session.commit()

        data = { "name": "Pol 4"}
        rv = self.client.post(
            "/api/v1/pol/",
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(rv.status_code, 401)