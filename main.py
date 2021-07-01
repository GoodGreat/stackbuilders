# MAIN FILE

from bs4 import BeautifulSoup
import requests
from entry import Entry

# This variable is just a defensive measure in case the website is in some way protected against scraping (it does not work everytime, but it's something)
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

url = "https://news.ycombinator.com/"
req = requests.get(url, headers)

# Creating the HTML DOM in the variable soup
soup = BeautifulSoup(req.content, 'html.parser')

# print(soup.prettify())

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
            comments_ = int(last_subtext_a_tag.split("\xa0comments")[0])
    except AttributeError:
        comments_ = 0

    # I get the number of the order by looking for the span inside each row with the "rank" class and trimming the dot at the end
    num_order_ = int(link.find('span', class_="rank").get_text().split(".")[0])

    # I get the title by looking for the a tag with the "storylink" class
    title_ = link.find('a', class_="storylink").get_text()

    # Instantiate the Entry class with the values retrieved
    entry = Entry(title=title_, num_order=num_order_,
                  comments=comments_, points=points_)

    print(entry)
