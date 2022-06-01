from gc import callbacks
import scrapy
from scrapy.crawler import CrawlerProcess

class ArticleSpider(scrapy.Spider):
    name = "articles"
    
    # def start_requests(self):
    #     urls = [
    #         'https://english.elpais.com/economy-and-business/'
    #         ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
       
    # def parse(self,response):
    #     for article in response.xpath("//header/h2/a/@href"): 
    #         yield{
    #             "link" : "https://english.elpais.com/" + article.get()
    #              }

    #     next_page = "https://english.elpais.com/" + response.xpath("/html/body/div/main/div/div/a/@href").get()
    #     if next_page is not None:
    #         yield response.follow(next_page,callback=self.parse)

    #         response.xpath("/html/body/div/main/div/div[3]/a/@href").get()
    start_urls = ['https://english.elpais.com/economy-and-business/' ]

    def parse(self, response):
        author_page_links = response.xpath("//header/h2/a/@href")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = "https://english.elpais.com/" + response.xpath("/html/body/div/main/div/div/a/@href").get()
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.xpath(query).get(default='').strip()
        def extract_all(query):
            return response.xpath(query).getall()

        yield {
            'url': response.url,
            'date': extract_with_css('//*[@id="article_date_p"]/text()'),
            'tittle': extract_with_css('//header/div/h1/text()'),
            'author': extract_with_css('/html/body/div/article/div/div/div/a/text()'),
            'text_art': extract_all('/html/body/div/article/div/p/text()'),
        }