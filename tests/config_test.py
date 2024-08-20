import os
import unittest

from jfw.Config import Config


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.dirname(__file__)
        self.config = Config(self.base_path)

    def test_base_path(self):
        self.assertEqual(self.base_path, str(self.config.base_path()))

    def test_app_path(self):
        self.assertEqual(f'{self.base_path}/app', str(self.config.app_path()))

    def test_logs_path(self):
        self.assertEqual(f'{self.base_path}/logs', str(self.config.log_path()))

    def test_set_and_get(self):
        self.config.set('test', 123)
        self.assertEqual(123, self.config.get('test'))
