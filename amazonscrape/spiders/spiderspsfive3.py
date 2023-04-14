import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'amazon_games_ps5'
    allowed_domains = ['amazon.nl']
    start_urls = [f'https://www.amazon.nl/s?rh=n%3A20904746031&language=nl_NL&brr=1&pf_rd_p=4c4a5340-6aeb-417e-9c89-2187866224f9&pf_rd_r=J3935EY8RYHFX4AV0QYH&pf_rd_s=nl_subnav_flyout_games_vtwo-content-2&pf_rd_t=SubnavFlyout&rd=1&ref=sn_gfs_co_games_20904746031_1']

    def parse(self, response):
        title_css = 'span.a-size-medium.a-color-base.a-text-normal::text'
        title_xpath = ('normalize-space(.//span[@class="a-size-medium a-color-base a-text-normal"]/text())')
        
        price_css = 'span.a-price-whole::text'
        price_xpath = ('normalize-space(.//span[@class="a-price-whole"]/text())')
        
        pegi_rating_css = 'span.a-size-base.a-color-secondary::text'
        pegi_rating_xpath = ('normalize-space(.//span[@class="a-size-base a-color-secondary"]/text())')
        
        platform_css = 'a.a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-bold::text'
        platform_xpath = ('normalize-space(.//a[@class="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold"]/text())')
        
        
        for game in response.css('div.sg-col-inner'):
            yield {
                'title': game.css(title_css).get() or game.xpath(title_xpath).get(),
                'price': game.css(price_css).get() or game.xpath(price_xpath).get(),
                'pegi_rating': game.css(pegi_rating_css).get() or game.xpath(pegi_rating_xpath).get(),
                'platform': game.css(platform_css).get() or game.xpath(platform_xpath).get()
            }
            
        next_page_url = response.css('span.s-pagination-strip > a::attr(href)').extract()[-1]
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)