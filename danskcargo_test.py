import unittest
import danskcargo_gui as dcg
import danskcargo_data as dcd
import danskcargo_sql as dcsql

class TestStringMethods(unittest.TestCase):  # basic example from https://docs.python.org/3/library/unittest.html

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


class TestEmptyEntries(unittest.TestCase):

    def test_empty_container_entries(self):
        # arrange
        # act
        # assert
        dcg.clear_container_entries()
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()