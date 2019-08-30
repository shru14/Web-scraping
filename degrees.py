import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class QuotesSpider(scrapy.Spider):
	name = "degrees"
	start_urls = ['https://www.futurelearn.com/degrees',]
	def parse(self, response):
		urls=response.css('div.m-grid-of-cards>a::attr("href")').extract()
		for url in urls:
			url=response.urljoin(url)
			yield scrapy.Request(url=url,callback=self.parse_details)
	def parse_details(self,response):
		tit=response.css('h2.m-dual-billboard__heading::text').extract_first().encode('ascii', errors='ignore').replace("\n","")
		disc=response.css('p.m-dual-billboard__message::text').extract_first().encode('ascii', errors='ignore')
		why=response.css('div.a-text-context>p::text').extract()[0:3]
		what=response.css('ul.m-list-grid>li>div.m-list-with-icon__text::text').extract()
		expi=response.selector.xpath('//*[@id="main-content"]/section[8]/div/div/p').extract()
		grad=response.selector.xpath('//*[@id="main-content"]/section[5]/div[2]/div/div[1]/a/div/span/text()').extract()
		items={		
		'Title':tit,
		'Description':disc,
		'Why join this degree':"".join([w.encode('ascii',errors='ignore').strip("\n").replace("\n","") for w in why]),
		'What are the benefits':"".join([wh.encode('ascii',errors='ignore').strip("\n").replace("\n","") for wh in what]),
		'What experience is required':"".join([e.encode('ascii',errors='ignore').strip("\n").replace("\n","").replace("<p>","").replace("</p>","").replace("<a href=","").replace(">The Guide</a>.","") for e in expi]),
		'Graduate Certificate Programs':"".join([g.encode('ascii',errors='ignore').strip("\n").replace("\n","") for g in grad]),
		
}
		yield items
		
