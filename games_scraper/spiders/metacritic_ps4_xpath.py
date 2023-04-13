# Main question: What is the most popular game across PC, PlayStation, X-box, and Nintendo based on the games released in the past 5 years?

# Sub question: Where is the game most affordable?
# Sub question: Which genre is the most popular?

import scrapy
from ..items import GameItem


class MetacriticSpiderPS4(scrapy.Spider):
    name = "metacritic_ps4"
    allowed_domains = ["metacritic.com"]
    start_urls = [
        "https://www.metacritic.com/browse/games/release-date/available/ps4/date?view=condensed&page=0"
    ]

    # start request
    def start_requests(self):
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(
                url,
                dont_filter=True,
                meta={
                    "index": index + 1,
                },
            )

    # defining a function
    def parse_details(self, response):
        product_genre = response.css(".product_genre")
        product_genre_data = product_genre.xpath(
            ".//span[contains(@class, 'data')]/text()"
        ).getall()
        # creating a game item object
        game = GameItem()
        game["title"] = response.meta["title"]
        game["meta_score"] = response.meta["meta_score"]
        game["user_score"] = response.meta["user_score"]
        game["platform"] = response.meta["platform"]
        game["release_date"] = response.meta["release_date"]
        game["summary"] = response.meta["summary"]
        game["page"] = response.meta["page"]
        game["product_genre"] = product_genre_data
        yield game

    def parse(self, response):
        for table in response.xpath(
            './/div[contains(concat(" ",normalize-space(@class)," ")," browse_list_wrapper ")]//table'
        ):
            for item in table.xpath(".//tr"):
                title = item.xpath(".//h3/text()").get()
                release_date = item.xpath(
                    './/td[contains(concat(" ",normalize-space(@class)," ")," details ")]/span/text()'
                ).get()
                meta_score = item.xpath(
                    './/div[contains(concat(" ",normalize-space(@class)," ")," metascore_w ")]/text()'
                ).get()
                user_score = item.xpath(
                    './/*[contains(concat(" ",normalize-space(@class)," ")," metascore_w ")][contains(concat(" ",normalize-space(@class)," ")," user ")]/text()'
                ).get()
                # platform = item.xpath(
                #     './/div[contains(concat(" ",normalize-space(@class)," ")," platform ")]/span[contains(concat(" ",normalize-space(@class)," ")," data ")]/text()'
                # ).get()
                summary = item.xpath(
                    './/div[contains(concat(" ",normalize-space(@class)," ")," summary ")]/p/text()'
                ).get()
                # getting link to the detail page
                detail_page = item.css("a.title::attr(href)").get()
                detail_page_url = f"https://www.metacritic.com{detail_page}"

                yield scrapy.Request(
                    detail_page_url,
                    callback=self.parse_details,
                    meta={
                        "title": title,
                        "meta_score": meta_score,
                        "user_score": user_score,
                        "platform": "PlayStation4",
                        "release_date": release_date,
                        "summary": summary,
                        "page": response.meta["index"],
                    },
                )
        # getting the next page href
        next_page = response.css(".page_nav .next .action::attr(href)").get()
        next_page_url = f"https://www.metacritic.com{next_page}"
        if next_page:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                meta={"index": response.meta["index"] + 1},
            )
