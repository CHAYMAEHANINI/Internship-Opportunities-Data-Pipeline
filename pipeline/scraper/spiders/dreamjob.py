import scrapy


class DreamjobSpider(scrapy.Spider):
    name = "dreamjob"
    allowed_domains = ["dreamjob.ma"]

    start_urls = [
        "https://www.dreamjob.ma/"
    ]

    def parse(self, response):

        print("STATUS:", response.status)
        print("TITLE:", response.css("title::text").get())

        offer_links = response.css('a[href*="/stage/"]')

        print("NUMBER OF STAGE LINKS:", len(offer_links))

        seen = set()

        for link in offer_links:

            href = link.css("::attr(href)").get()

            if href and href not in seen:
               seen.add(href)

               print("OFFER URL:", href)

               yield response.follow(
                     href,
                     callback=self.parse_offer
               )


    def parse_offer(self, response):

        print("OFFER STATUS:", response.status)
        print("OFFER URL:", response.url)
        print("OFFER TITLE:", response.css("title::text").get())