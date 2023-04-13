import scrapy


# creating a class GameItem
class GameItem(scrapy.Item):
    title = scrapy.Field()
    meta_score = scrapy.Field()
    user_score = scrapy.Field()
    platform = scrapy.Field()
    release_date = scrapy.Field()
    summary = scrapy.Field()
    page = scrapy.Field()
    product_genre = scrapy.Field()
