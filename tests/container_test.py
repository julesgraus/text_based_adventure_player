import unittest

from jfw.Container import Container


class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        self.container = Container()

    def test_simple_binding(self):
        self.container.bind('key', 'value')
        self.assertEqual('value', self.container.resolve('key'))

