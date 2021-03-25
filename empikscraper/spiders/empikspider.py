from scrapy.spiders import Rule, CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from empikscraper.items import Book
import unicodedata

class BookLoader(ItemLoader):
    def _normalize(text):
        text = text.replace('\n', '')
        return unicodedata.normalize('NFKC', text)

    def _clean_stars(selector):
        def rate(selector):
            return self.__css_text(selector)

        def amount(selector):
            return self.__css_text(selector, 'span')

        return {rate(row) : amount(row) for row in selector }


    default_input_processor = MapCompose(remove_tags, str.strip, _normalize)
    default_output_processor = TakeFirst()

    description_in = MapCompose(remove_tags, str.strip)
    description_out = Join()

    data_out = Compose(lambda v: {v[i-1][:-1]:v[i] for i in range(1, len(v), 2)})
    tags_out = Compose(lambda v: v[2::])

    stars_in = MapCompose(remove_tags, str.strip, _normalize)
    stars_out = Compose(reversed, list)


class EmpikSpider(CrawlSpider):
    name = "empik"
    allowed_domains = ['empik.com']
    start_urls = ["https://www.empik.com/ksiazki,31,s?hideUnavailable=true&sort=scoreDesc&resultsPP=60"]

    rules = (
        Rule(LinkExtractor(restrict_css='.seoTitle'), callback='parse_book'),
        Rule(LinkExtractor(restrict_css='.ta-next-page'))
    )
    def parse(self, response):
        pass

    def parse_book(self, response):
        book_loader = BookLoader(item=Book(), response=response)

        tags_loader = book_loader.nested_css('.empikBreadcrumb')
        tags_loader.add_css('tags', 'ul > li')
        
        price_loader = book_loader.nested_css('.productPriceInfo__wrapper')
        price_loader.add_css('original_price', '.productPriceInfo__originalPrice')
        price_loader.add_css('price', '.productPriceInfo__price')

        data_loader = book_loader.nested_xpath('//div[@data-structure-preset="productTabs"]')
        data_loader.add_css('description', '.productDescription')
        data_loader.add_css('stars', '.productComments__ratingNum')

        table_loader = data_loader.nested_css('.productDataTable')
        table_loader.add_css('data', 'td')

        yield book_loader.load_item()


