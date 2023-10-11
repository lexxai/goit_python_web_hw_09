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
    css_author  = "h3.author-title"
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
        "base_author_name": base_author_name,
        "fullname": author_name,
        "born_date": author_born, 
        "born_location": author_born_location,
        "description": author_desc
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
    quotes = soup.find_all("span", attrs={"class": "text"})
    authors = soup.find_all("small", attrs={"class": "author"})
    authors_link = soup.select_one("div.quote:nth-child(1) > span:nth-child(2) > a:nth-child(2)")
    tags = soup("div", attrs={"class": "tags"})
    next = soup.select_one(css_selector_next)

    for quote, author, tag in zip(quotes, authors, tags):
        q_text = quote.text.strip()
        q_author = {
            "author_name": author.text.strip(),
            "author_link": authors_link.get('href')
        }
        q_tags = [t.text.strip() for t in tag.find_all("a", attrs={"class": "tag"})]
        result.append({"tags": q_tags, "author": q_author, "quote": q_text})  
    if next:
        next = next.get("href")
    return result, next


def parse_data_quotes(base_url: str = "https://quotes.toscrape.com") -> list[dict]:
    store_ = []
    url = base_url
    while True:
        if not url:
            break
        result, next_url = parse_url_quotes(url)
        store_.extend(result)
        break  # TEST !!! #TODO
        if not next:
            break
        if next_url:
            url = base_url + next_url
        else:
            break
    return store_


def parse_data_authors(data: list[dict], base_url: str = "https://quotes.toscrape.com") -> list[dict]:
    store_ = []
    url = base_url
    urls = []
    for record in data:
        author = record.get("author")
        if author:
            author_name = author.get("author_name")
            author_link = author.get("author_link")
            print(author_name, author_link)
            url = base_url + author_link
            urls.append(url)
            # author_info = parse_url_author(url)
            # store_.append(author_info)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        store_ = list(executor.map(parse_url_author, urls, author_name))

    return store_




if __name__ == "__main__":
    data_quotes = parse_data_quotes()
    pprint(data_quotes)
    print("-"*120)
    data_authors = parse_data_authors(data_quotes)
    pprint(data_authors)
    # print(len(data_quotes), len(data_authors))
    # pprint(data)
    # auth = parse_url_author("http://quotes.toscrape.com/author/Eleanor-Roosevelt/")
    # pprint(auth) 
