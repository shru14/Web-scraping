import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class QuotesSpider(scrapy.Spider):
	name = "courses"
	start_urls = ['https://www.futurelearn.com/courses',]
	def parse(self, response):
		urls=response.css('div.m-course-run__main>header>h2>a::attr("href")').extract()
		for url in urls:
			url=response.urljoin(url)
			yield scrapy.Request(url=url,callback=self.parse_details)
	def parse_details(self,response):
		tit=response.css('div.m-course-run__main>header>h2>a>span::text').extract_first().encode('ascii', errors='ignore')
		course=response.selector.xpath('//*[@id="course-requirements"]/div/p[1]/text()').extract()
		Syllabus=response.css("div.a-text-context>ul>li::text").extract()
		name=response.selector.xpath('//*[@id="section-educators"]/div/div/div/div/div[2]/div/header/h3/a/text()').extract()
		pro=response.selector.xpath('//*[@id="main-content"]/section[12]/div[2]/div[2]/p/text()').extract()
		avail=response.selector.xpath('//*[@id="section-dates"]/div/ul/li[1]/div[2]/div[1]/text()').extract()
		date=response.selector.xpath('//*[@id="section-dates"]/div/ul/li[2]/div[2]/div[1]/text()').extract()
		achieve=response.css('div.m-list-with-icon__text::text').extract()
		soft=response.selector.xpath('//*[@id="technical-requirements"]/div/p/text()').extract()
		disc=response.css('p.m-dual-billboard__message::text').extract_first().encode('ascii', errors='ignore')

		

		items={		
		'Title':tit,
		'Description':disc,
		'Recommended course length':response.css('span.m-metadata__title::text').extract_first().encode('ascii',errors='ignore').strip("\n"),
		'Commitment':response.css('span.m-metadata__title::text').extract()[1].encode('ascii',errors='ignore').strip("\n"),
		'Price':response.css('span.m-metadata__title::text').extract()[2].encode('ascii',errors='ignore').strip("\n"),
		'Providers':"".join([p.encode('ascii',errors='ignore').strip("\n") for p in pro]),
		'Name of the instructors':"".join([n.encode('ascii',errors='ignore').strip("\n") for n in name]),
		'Course Syllabus':"".join([s.encode('ascii',errors='ignore').strip("\n") for s in Syllabus]),
		'What will you achieve':"".join([av.encode('ascii',errors='ignore').strip("\n") for av in achieve]),
		'Available status':"".join([a.encode('ascii',errors="ignore").strip("\n") for a in avail]),
		'Date of joining':"".join([d.encode('ascii',errors="ignore").strip("\n") for d in date]),
		'Who is this course for':"".join([c.encode('ascii',errors="ignore").strip("\n") for c in course]),
		'Software tools requirements':"".join([so.encode('ascii',errors="ignore").strip("\n") for so in soft]),
		'Upgrade':response.css('span.m-metadata__title::text').extract()[3].encode('ascii',errors='ignore').strip("\n"),
		'Upgrade info':response.css('div.m-accordion>div::text').extract_first().encode('ascii',errors="ignore").strip("\n").replace("\n"," "),
}
		yield items
		
