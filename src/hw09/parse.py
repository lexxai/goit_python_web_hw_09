from pathlib import Path
from pprint import pprint
import requests
from bs4 import BeautifulSoup

from database.models import Quotes, Authors


json_dest = Path(__file__).parent.joinpath("database").joinpath("json")


def parse_url(url: str) -> tuple[list[dict], next]:
    result = []
    next = None
    if not url:
        return result, next
    css_selector_next = "nav .next > a"
    # print(url)
    html_doc = requests.get(url)
    if html_doc.status_code != 200:
        return result, next
    soup = BeautifulSoup(html_doc.content, "html.parser")
    quotes = soup.find_all("span", attrs={"class": "text"})
    authors = soup.find_all("small", attrs={"class": "author"})
    tags = soup("div", attrs={"class": "tags"})
    next = soup.select_one(css_selector_next)

    for quote, author, tag in zip(quotes, authors, tags):
        q_text = quote.text.strip()
        q_author = author.text.strip()
        q_tags = [t.text.strip() for t in tag.find_all("a", attrs={"class": "tag"})]
        result.append({"tags": q_tags, "author": q_author, "quote": q_text})

    if next:
        next = next.get("href")
    return result, next


def parse_data(base_url: str = "https://quotes.toscrape.com") -> list[dict]:
    store_ = []
    url = base_url
    while True:
        if not url:
            break
        result, next_url = parse_url(url)
        store_.extend(result)
        if not next:
            break
        if next_url:
            url = base_url + next_url
        else:
            break
    return store_


if __name__ == "__main__":
    data = parse_data()
    print(len(data))
    # pprint(data)
