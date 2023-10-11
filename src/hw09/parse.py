from pathlib import Path
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import concurrent.futures

from database.models import Quotes, Authors


json_dest = Path(__file__).parent.joinpath("database").joinpath("json")


def parse_url_author(url: str, base_author_name: str) -> dict:
    result = {}
    next = None
    if not url:
        return result, next
    css_author = "h3.author-title"
    css_born = "div.author-details > p > strong"
    css_born = "div.author-details span.author-born-date"
    css_born_location = "div.author-details span.author-born-location"
    css_desc = "div.author-description"
    # print(url)
    html_doc = requests.get(url)
    if html_doc.status_code != 200:
        return result, next
    soup = BeautifulSoup(html_doc.content, "html.parser")
    author_name = soup.select_one(css_author).text.strip()
    author_born = soup.select_one(css_born).text.strip()
    author_born_location = soup.select_one(css_born_location).text.strip()
    author_desc = soup.select_one(css_desc).text.strip()
    result = {
        base_author_name: {
            "fullname": author_name,
            "born_date": author_born,
            "born_location": author_born_location,
            "description": author_desc,
        }
    }
    return result


def parse_url_quotes(url: str) -> tuple[list[dict], next]:
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
    quotes_block = soup.select("div.quote")
    next = soup.select_one(css_selector_next)

    for quote in quotes_block:
        quote_text = quote.select_one("span.text")
        tag = quote.select_one("div.tags")
        author_block = quote.select_one("span:nth-child(2)")
        author_name = author_block.select_one("small.author")
        author_link = author_block.select_one("a")
        q_text = quote_text.text.strip()
        q_author = {
            "author_name": author_name.text.strip(),
            "author_link": author_link.get("href"),
        }
        q_tags = [t.text.strip() for t in tag.find_all("a", attrs={"class": "tag"})]
        result.append({"tags": q_tags, "author": q_author, "quote": q_text})
    if next:
        next = next.get("href")
    return result, next


def parse_data_quotes(
    base_url: str = "https://quotes.toscrape.com", max_records: int = 1000
) -> list[dict]:
    store_ = []
    url = base_url
    while True:
        if not url:
            break
        result, next_url = parse_url_quotes(url)
        store_.extend(result)
        if max_records:
            max_records -= 1
            if max_records <= 0:
                print("Limit on the number of accepted records, stop.")
                break
        if not next:
            break
        if next_url:
            url = base_url + next_url
        else:
            break
    return store_


def parse_data_authors(
    data: list[dict], base_url: str = "https://quotes.toscrape.com"
) -> dict:
    store_ = {}
    url = base_url
    urls = []
    authors = []
    for record in data:
        author = record.get("author")
        if author:
            author_name = author.get("author_name")
            if author_name in authors:
                break
            else:
                authors.append(author_name)
            author_link = author.get("author_link")
            print(author_name, author_link)
            url = base_url + author_link
            urls.append(url)
            # author_info = parse_url_author(url)
            # store_.append(author_info)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(parse_url_author, urls, [author_name])

    for result in results:
        store_.update(result)

    return store_


def correction_quotes_author_name(
    data_quotes: list[dict], data_authors: dict
) -> list[dict]:
    result = []
    for record in data_quotes:
        author = record.get("author")
        if author:
            author_name = author.get("author_name")
            data_author = data_authors.get(author_name)
            if data_author:
                record["author"] = data_author.get("fullname")
        result.append(record)
    return result


if __name__ == "__main__":
    data_quotes = parse_data_quotes(max_records=1)
    # pprint(data_quotes)
    print("-" * 120)
    data_authors = parse_data_authors(data_quotes)
    pprint(data_authors)
    data_quotes = correction_quotes_author_name(data_quotes, data_authors)
    pprint(data_quotes)
    ##pprint(data_authors)
    # print(len(data_quotes), len(data_authors))
    # pprint(data)
    # auth = parse_url_author("http://quotes.toscrape.com/author/Eleanor-Roosevelt/")
    # pprint(auth)
