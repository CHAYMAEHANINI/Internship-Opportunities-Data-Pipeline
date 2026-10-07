import scrapy


class StagiairesSpider(scrapy.Spider):
    name = "stagiaires"
    allowed_domains = ["stagiaires.ma"]

    start_urls = [
        "https://www.stagiaires.ma/"
    ]

    def parse(self, response):
        print("STATUS:", response.status)
        print("TITLE:", response.css("title::text").get())