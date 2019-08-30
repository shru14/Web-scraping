import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class QuotesSpider(scrapy.Spider):
	name = "programs"
	start_urls = ['https://www.futurelearn.com/programs',]
	def parse(self, response):
		for quote in response.css('div.o-signpost__content'):
			item= {
			'Title':quote.css('div.o-signpost__title::text').extract_first().encode('ascii',errors="ignore").strip("\n"),
			'Description': quote.css('div.o-signpost__intro::text').extract_first().encode('ascii',errors="ignore").strip("\n"),
			'Number': quote.css('div.o-signpost__info>span.a-text-with-icon::text').extract_first().encode('ascii',errors="ignore").strip("\n"),
		   	}
			yield item

		

