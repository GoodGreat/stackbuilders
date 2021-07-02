from main import *
import unittest
from entry import Entry


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

    def test_sort_entries_by_gt_title_words_and_comments_one(self):
        myDict = {}
        entry1 = Entry("Title with more than four words", 1, 32, 20)
        entry2 = Entry("Title with more than four words too", 2, 25, 36)
        entry3 = Entry("Less than four words", 3, 156, 48)

        myDict[6] = [entry1]
        myDict[7] = [entry2]
        myDict[4] = [entry3]

        sorted_entries = self.main.sort_entries_by_gt_title_words_and_comments(
            myDict, 4)

        # The first on the list should be the one with ID = 2 and the second one the one with ID = 1
        self.assertEqual(sorted_entries[0].num_order, 2)
        self.assertEqual(sorted_entries[1].num_order, 1)
        self.assertEqual(len(sorted_entries), 2)

    def test_sort_entries_by_gt_title_words_and_comments_two(self):
        myDict = {}
        sorted_entries = self.main.sort_entries_by_gt_title_words_and_comments(
            myDict, 4)

        # If the dict is empty, the sorted_entries should be none
        self.assertEqual(len(sorted_entries), 0)

    def test_sort_entries_by_gt_title_words_and_comments_three(self):
        myDict = {}
        sorted_entries = self.main.sort_entries_by_gt_title_words_and_comments(
            myDict, -1)

        # If the dict is empty, the sorted_entries should be none
        self.assertEqual(sorted_entries, [])

    def test_sort_entries_by_le_title_words_and_points_one(self):
        myDict = {}
        entry1 = Entry("Title with more than three words", 1, 32, 20)
        entry2 = Entry("Exactly three words", 2, 25, 36)
        entry3 = Entry("Two words", 3, 156, 48)

        myDict[6] = [entry1]
        myDict[3] = [entry2]
        myDict[2] = [entry3]

        sorted_entries = self.main.sort_entries_by_le_title_words_and_points(
            myDict, 3)

        # The first on the list should be the one with ID = 2 and the second one the one with ID = 1
        self.assertEqual(sorted_entries[0].num_order, 2)
        self.assertEqual(sorted_entries[1].num_order, 3)
        self.assertEqual(len(sorted_entries), 2)

    def test_sort_entries_by_le_title_words_and_points_two(self):
        myDict = {}
        sorted_entries = self.main.sort_entries_by_le_title_words_and_points(
            myDict, 3)

        # If the dict is empty, the sorted_entries should be none
        self.assertEqual(len(sorted_entries), 0)

    def test_sort_entries_by_le_title_words_and_points_three(self):
        myDict = {}
        sorted_entries = self.main.sort_entries_by_le_title_words_and_points(
            myDict, 0)

        # If the dict is empty, the sorted_entries should be none
        self.assertEqual(sorted_entries, [])


if __name__ == '__main__':
    unittest.main()
