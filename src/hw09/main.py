from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


json_dest = Path(__file__).parent.joinpath("database").joinpath("json")


class QuoteItem(Item):
    keywords = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": str(json_dest.joinpath(f"{name}.json")),
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            keywords = list(map(lambda x: x.strip(), quote.xpath("div[@class='tags']/a/text()").getall()))
            author = quote.xpath("span/small/text()").get().strip()
            quote = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(keywords=keywords, author=author, quote=quote)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response):
        ...
 

# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
