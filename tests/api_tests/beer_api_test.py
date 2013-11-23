from flask import Flask
import unittest
import json

from polliste.models import Beer
from test_config import setup_app, remove_app

class BreweryApiTest(unittest.TestCase):
    def setUp(self):
        self.app, self.client = setup_app()

    def tearDown(self):
        remove_app(self.app)