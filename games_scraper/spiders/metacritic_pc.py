# scrapy crawl metacritic_pc -o test.csv

import scrapy
from ..items import GameItem


class MetacriticSpiderPC(scrapy.Spider):
    name = "metacritic_pc"
    allowed_domains = ["metacritic.com"]
    start_urls = [
        "https://www.metacritic.com/browse/games/release-date/available/pc/date?view=condensed&page=0"
    ]

    def start_requests(self):
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(
                url,
                dont_filter=True,
                meta={
                    "index": index + 1,
                },
            )

    def parse_details(self, response):
        product_genre = response.css(".product_genre")
        product_genre_data = product_genre.xpath(
            ".//span[contains(@class, 'data')]/text()"
        ).getall()
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
        # First find the link to the next page from pagination.
        next_page = response.css(".page_nav .next .action::attr(href)").get()
        next_page_url = f"https://www.metacritic.com{next_page}"
        if next_page:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                meta={"index": response.meta["index"] + 1},
            )

        # Then from each row in the table extract the data items.
        for table in response.xpath(
            './/div[contains(concat(" ",normalize-space(@class)," ")," browse_list_wrapper ")]//table'
        ):
            for item in table.css("tr"):
                title = item.css("h3::text").get()
                release_date = item.css("td.details > span::text").get()
                meta_score = item.css("div.metascore_w::text").get()
                user_score = item.css(".metascore_w.user::text").get()
                # platform = item.css("div.platform > span.data::text").get()
                summary = item.css("div.summary > p::text").get()

                detail_page = item.css("a.title::attr(href)").get()
                detail_page_url = f"https://www.metacritic.com{detail_page}"

                yield scrapy.Request(
                    detail_page_url,
                    callback=self.parse_details,
                    meta={
                        "title": title,
                        "meta_score": meta_score,
                        "user_score": user_score,
                        "platform": "PC",
                        "release_date": release_date,
                        "summary": summary,
                        "page": response.meta["index"],
                    },
                )