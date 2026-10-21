import re
from email.utils import parsedate_to_datetime

import scrapy
from scrapy import Selector

from scraper.items import InternshipItem
from scraper.spiders.publimaroc import extract_skills


class DreamjobSpider(scrapy.Spider):

    name = "dreamjob"

    allowed_domains = ["dreamjob.ma"]

    # Official RSS feed (the HTML page /stage/ is behind a Cloudflare challenge)
    start_urls = ["https://www.dreamjob.ma/stage/feed/"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "FEEDS": {
            "../data/raw/dreamjob.json": {
                "format": "json",
                "overwrite": True,
            }
        },
    }

    def parse(self, response):

        entries = response.xpath("//item")
        self.logger.info("STATUS: %s | ENTRIES: %s", response.status, len(entries))

        for entry in entries:

            title = entry.xpath("title/text()").get()
            url = (entry.xpath("link/text()").get() or "").strip()
            pub_date = entry.xpath("pubDate/text()").get()
            categories = entry.xpath("category/text()").getall()
            description_html = entry.xpath("description/text()").get() or ""

            if not title or not url or not pub_date:
                self.logger.warning("SKIPPED: incomplete entry | %s", title)
                continue

            # published_at: RFC822 -> ISO (naive, UTC)
            published_at = (
                parsedate_to_datetime(pub_date)
                .replace(tzinfo=None)
                .isoformat(sep=" ")
            )

            # location / company come from the WordPress categories
            location = None
            company = None

            for category in categories:

                if location is None:
                    match = re.match(r"^Offres d.Emploi à (.+)$", category)
                    if match:
                        location = match.group(1).strip()

                if company is None:
                    match = re.match(r"^(.+?) Emploi et Recrutement$", category)
                    if match:
                        company = match.group(1).strip()

            # description: clean HTML summary
            selector = Selector(text=description_html)
            paragraphs = [
                " ".join(p.xpath("string(.)").get().split())
                for p in selector.xpath("//p")
            ]
            paragraphs = [
                p for p in paragraphs
                if p and "est apparu en premier sur" not in p
            ]
            description = " ".join(paragraphs)

             # keep only internship-related posts
            text = f"{title} {description}".lower()

            is_internship = "/stage/" in url or any(
                keyword in text for keyword in ("stage", "stagi", "pfe", "intern")
            )

            if not is_internship:
                self.logger.info("SKIPPED: not an internship | %s", title)
                continue
            
            yield InternshipItem(
                title=title,
                company=company,
                location=location,
                work_mode=None,
                stipend=None,
                internship_type="Stage",
                description=description,
                skills=extract_skills(description),
                published_at=published_at,
                application_deadline=None,
                url=url,
                source="Dreamjob",
            )