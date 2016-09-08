import api
import unittest



class ApiUnitTests(unittest.TestCase):
    """Tests the helper function(s) in the api module."""

    def test_move_the(self):
        assert api.move_the('The Smiths') == 'Smiths, The'

    def special_char(self):
        assert api.special_char(u'\u2013') == '&2013'


if __name__ == '__main__':
    # If called like a script, run the tests
    unittest.main()