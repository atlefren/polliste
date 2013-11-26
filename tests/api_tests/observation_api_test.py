from flask import Flask
import unittest
import json

from polliste.models import Brewery, Beer, User, Pol
from test_config import setup_app, remove_app

class ObservationApiTest(unittest.TestCase):

    def setUp(self):
        self.app, self.client = setup_app()

        pol1 = Pol("pol 1")
        brewery1 = Brewery("Brewery 1")

        beer1 = Beer("Beer 1", brewery1)
        beer2 = Beer("test ", brewery1)
        beer3 = Beer("Beer 2", brewery1)

        self.app.db_session.add(pol1)
        self.app.db_session.add(brewery1)
        self.app.db_session.add(beer1)
        self.app.db_session.add(beer2)
        self.app.db_session.add(beer3)
        self.app.db_session.commit()



    def tearDown(self):
        remove_app(self.app)

    def test_user_can_add_observation(self):

        u = User(username='a', email='a@b.c', name='a', role=0)
        self.app.db_session.add(u)
        self.app.db_session.commit()
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = int(u.get_id())
                sess['_fresh'] = True

            data = { "beer": 1, "comment": "haha"}
            rv = c.post(
                "/api/v1/pol/1/observations/",
                data = json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data["beer"]["id"], 1)
        self.assertEqual(data["comment"], "haha")
