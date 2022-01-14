import unittest

class TestSomething(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_stuff(self):
        self.assertEqual('T','T')

if __name__ == '__main__':
    unittest.main()