from flask import current_app
from flask_testing import TestCase

from thundersnow import app


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('thundersnow.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestProductionConfig(TestCase):

    def create_app(self):
        app.config.from_object('thundersnow.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)
