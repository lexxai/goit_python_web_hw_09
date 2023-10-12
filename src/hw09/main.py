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
            keywords = [
                k.strip() for k in quote.xpath("div[@class='tags']/a/text()").getall()
            ]
            author = quote.xpath("span/small/text()").get().strip()
            author_link = quote.xpath("span/a/@href").get()
            quote = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(keywords=keywords, author=author, quote=quote)
            yield response.follow(
                url=self.start_urls[0] + author_link, callback=self.nested_parse_author
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response):
        author = response.xpath("/html//div[@class='author-details']")
        fullname = author.xpath('h3[@class="author-title"]/text()').get().strip()
        born_date = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = (
            author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        )
        description = author.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )


# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
