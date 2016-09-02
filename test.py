import api
import unittest
# import doctest


class ApiUnitTests(unittest.TestCase):
    """Examples of unit tests: discrete code testing."""

    def test_move_the(self):
        assert api.move_the('The Smiths') == 'Smiths, The'

    # def test_adder_2(self):
    #     self.assertEqual(arithmetic.adder(2, 2), 4)

    # def test_things(self):
    #     self.assertEqual(len(arithmetic.things_from_db()), 3)


# def load_tests(loader, tests, ignore):
#     """Also run our doctests and file-based doctests.
#
#     This function name, ``load_tests``, is required.
#     """
#
#     tests.addTests(doctest.DocTestSuite(arithmetic))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests


if __name__ == '__main__':
    # If called like a script, run the tests
    unittest.main()