import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'amazon_games_pc1'
    allowed_domains = ['amazon.nl']
    start_urls = [f'https://www.amazon.nl/s?i=videogames&bbn=16480683031&rh=n%3A16480683031%2Cp_n_theme_browse-bin%3A16480575031%7C16480576031%7C16480578031%7C16480582031%7C16480585031%7C16480589031%7C16480590031&dc&fs=true&qid=1681288845&rnid=16480569031&ref=sr_nr_p_n_theme_browse-bin_7&ds=v1%3AVrZjGTCza9tlj2HHs4iKF4X1em8h2Um1BgyL8jHCaY4']

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