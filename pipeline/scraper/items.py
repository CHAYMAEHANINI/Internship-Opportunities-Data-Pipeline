import scrapy


class InternshipItem(scrapy.Item):

    id = scrapy.Field()

    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    work_mode = scrapy.Field()
    stipend = scrapy.Field()
    internship_type = scrapy.Field()

    description = scrapy.Field()
    skills = scrapy.Field()

    published_at = scrapy.Field()
    application_deadline = scrapy.Field()

    url = scrapy.Field()
    source = scrapy.Field()

    scraped_at = scrapy.Field()