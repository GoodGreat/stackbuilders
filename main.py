# MAIN FILE

from bs4 import BeautifulSoup
import requests
from entry import Entry
from urllib.parse import urlparse


class Main:

    def retrieve_data_from_url(url):
        """
        retrieve_data_from_url is a Webscraping function to retrieve relevant data from the given url

        :param url: References the url where data is gonna be retrieved from
        :return: Dictionary with the entries retrieved from the url where the title words are the key and the associated list of entries are the value
        """
        # This variable is just a defensive measure in case the website is in some way protected against scraping (it does not work everytime, but it's something)
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        if (urlparse.urlparse(url)):
            url_ = url
        else:
            return None
        req = requests.get(url_, headers)

        # Creating the HTML DOM in the variable soup
        soup = BeautifulSoup(req.content, 'html.parser')

        # Dictionary to store the entries retrieved
        entries = {}

        links = soup.find_all('tr', class_="athing")
        for link in links:

            # Every title row is followed by the Subtext row. As it does not have its own class, I found this as a valid solution to get it.
            next_tr = link.find_next_sibling('tr')
            subtext = next_tr.find('td', class_="subtext")

            # I get the points by looking for the span inside each subtext row with the "score" class and trimming the points string at the end
            # This try/except block prevents the cases where find() returns None. It is repeated for the comments.
            try:
                points_ = int(subtext.find(
                    'span', class_="score").get_text().split(" points")[0])
            except AttributeError:
                points_ = 0

            # I get the number of comments by looking for the last link at every subtext row and trimming the comments string at the end
            try:
                last_subtext_a_tag = subtext.find_all('a')[-1].get_text()

                # Sometimes the last link is something not related to the comments, thats why I check if it contains the comments string
                if("\xa0comments" in last_subtext_a_tag):
                    comments_ = int(
                        last_subtext_a_tag.split("\xa0comments")[0])
                else:
                    comments_ = 0
            except AttributeError:
                comments_ = 0

            # I get the number of the order by looking for the span inside each row with the "rank" class and trimming the dot at the end
            num_order_ = int(
                link.find('span', class_="rank").get_text().split(".")[0])

            # I get the title by looking for the a tag with the "storylink" class
            title_ = link.find('a', class_="storylink").get_text()

            title_length = len(title_.split())

            # Instantiate the Entry class with the values retrieved
            entry = Entry(title=title_, num_order=num_order_,
                          comments=comments_, points=points_)

            # I store the entries in a dictionary where the keys are the length of the title and the values are the Entries
            # The reason for doing it this way is that the filtering will be optimized if the keys are directly the length of the titles

            # Inserting the Entries into the Dictionary.
            # If the length of the title has not already been seen before, we create the new list. Otherwise, we append the new Entry
            if (title_length in entries):
                entries[title_length].append(entry)
            else:
                entries[title_length] = [entry]

            return entries

    # PROCEED WITH FIRST FILTER
    # "Filter all previous entries with more than five words in the title ordered by the amount of comments first"
    def sort_entries_by_gt_title_words_and_comments(self, list_, title_words):
        """
        sort_entries_by_gt_title_words_and_comments filters a given list of entries with a
        number of words in the title greater than the given title_words and sorts them
        by the number of comments.

        :param self: References the Main class
        :param list_: References the list of entries to filter
        :param title_words: References the number of words in the title
        :return: Sorted list of entries that pass the filter 
        """
        sorted_by_comments = []

        for key in list_:
            if key > title_words:
                sorted_by_comments += list_[key]

        sorted_by_comments = sorted(
            sorted_by_comments, key=self.sort_by_comments)

        return sorted_by_comments

    # PROCEED WITH SECOND FILTER
    # "Filter all previous entries with less than or equal to five words in the title ordered by points."
    def sort_entries_by_le_title_words_and_points(self, list_, title_words):
        """
        sort_entries_by_le_title_words_and_points filters a given list of entries with a
        number of words in the title less than or equal to the given title_words and sorts them
        by the number of points.

        :param self: References the Main class
        :param list_: References the list of entries to filter
        :param title_words: References the number of words in the title
        :return: Sorted list of entries that pass the filter 
        """
        sorted_by_points = []

        for key in list_:
            if key <= title_words:
                sorted_by_points += list_[key]

        sorted_by_points = sorted(sorted_by_points, key=self.sort_by_points)

        return sorted_by_points

    def sort_by_comments(item):
        """
        sort_by_comments defines the "comments" field of Entry class as the sorting key

        :param item: References object of Entry class
        :return: The "comments" field of the Entry class
        """
        return item.comments

    def sort_by_points(item):
        """
        sort_by_comments defines the "points" field of Entry class as the sorting key

        :param item: References object of Entry class
        :return: The "points" field of the Entry class
        """
        return item.points
