import scrapy


class Book(scrapy.Item):
    description = scrapy.Field()
    stars = scrapy.Field()
    data = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    pass