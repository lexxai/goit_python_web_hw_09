from pathlib import Path
from pprint import pprint
import requests
from bs4 import BeautifulSoup

from database.models import Quotes, Authors


json_dest = Path(__file__).parent.joinpath("database").joinpath("json")


def parse_data():
    url = "https://quotes.toscrape.com/"
    css_selector_quote = "div.quote  span.text"
    css_selector_author_link = "div.quote:nth-child(1) > span:nth-child(2) > a"
    css_selector_author_name = "div.quote  small.author"
    css_selector_tags = "div.quote div.tags > a.tag"
    css_selector_next = "nav .next > a"

    store_ = []
    html_doc = requests.get(url)

    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, "html.parser")
        quotes = soup.find_all("span", attrs={"class": "text"})
        authors = soup.find_all("small", attrs={"class": "author"})
        tags = soup("div", attrs={"class": "tags"})

        for quote, author, tag in zip(quotes, authors, tags):

            q_text = quote.text.strip()
            q_author = author.text.strip()
            q_tags = [t.text.strip() for t in tag.find_all("a", attrs={"class": "tag"})]
            store_.append(
                {
                    "tags": q_tags,
                    "author": q_author,
                    "quote": q_text
                }
            )
    pprint(store_)
            
            


if __name__ == "__main__":
    parse_data()
