import unittest
from main import *


class MainTest(unittest.TestCase):

    def setUp(self):
        self.main = Main()

    def test_retrieve_data_from_url_one(self):

        url = "https://news.ycombinator.com/"
        entries = self.main.retrieve_data_from_url(url)
        entries_count = 0
        ideal_total_count = 30

        # Assert in the ideal case that the dict has some entries
        self.assertTrue(entries)

        for key in entries:
            for a in entries[key]:
                entries_count += 1

        # Assert that the dict has exactly 30 entries
        self.assertEqual(entries_count, ideal_total_count)

    def test_retrieve_data_from_url_two(self):
        url = "123"
        entries = self.main.retrieve_data_from_url(url)

        # Assert that the dict has no entries as the url has invalid format
        self.assertFalse(entries)


if __name__ == '__main__':
    unittest.main()
