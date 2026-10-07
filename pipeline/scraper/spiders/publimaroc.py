import scrapy
from scraper.items import InternshipItem

KNOWN_SKILLS = [
    "Python",
    "SQL",
    "Pandas",
    "Power BI",
    "Excel",
    "Java",
    "C++",
    "JavaScript",
    "React",
    "Docker",
    "Git",
    "Machine Learning",
    "Data Analysis",
    "Data Engineering",
]

def extract_skills(description):

    if not description:
        return []

    found_skills = []

    description_lower = description.lower()

    for skill in KNOWN_SKILLS:

        if skill.lower() in description_lower:

            found_skills.append(skill)

    return found_skills

class PublimarocSpider(scrapy.Spider):

    name = "publimaroc"

    allowed_domains = ["publimaroc.com"]

    start_urls = [
        "https://www.publimaroc.com/stages-maroc"
    ]

    # =========================================================
    # LISTING PAGE
    # =========================================================

    def parse(self, response):

        self.logger.info("=" * 70)
        self.logger.info("LISTING PAGE")
        self.logger.info("STATUS: %s", response.status)
        self.logger.info("URL: %s", response.url)
        self.logger.info("=" * 70)

        # Get all announcement links
        links = response.css('a[href*="/annonce/"]')

        seen = set()

        for link in links:

            href = link.css("::attr(href)").get()

            if href and href not in seen:

                seen.add(href)

                yield response.follow(
                    href,
                    callback=self.parse_offer
                )

        self.logger.info(
            "NUMBER OF UNIQUE OFFERS FOUND: %s",
            len(seen)
        )

    # =========================================================
    # DETAIL PAGE
    # =========================================================

    def parse_offer(self, response):

        # =====================================================
        # TITLE
        # =====================================================

        title = response.css(
            "h1.detail-title::text"
        ).get()

        if title:
            title = " ".join(title.split())

        # =====================================================
        # LOCATION
        # =====================================================

        location = response.css(
            "a.detail-badge.city::text"
        ).get()

        if location:
            location = " ".join(location.split())

        # =====================================================
        # PUBLISHED DATE
        # =====================================================

        published_at = response.css(
            "span.detail-badge.date::text"
        ).get()

        if published_at:
            published_at = " ".join(
                published_at.split()
            )

        # =====================================================
        # CATEGORY
        # =====================================================

        category = response.css(
            "a.detail-badge.cat::text"
        ).get()

        if category:
            category = " ".join(
                category.split()
            )

        # =====================================================
        # SPEC CARDS
        # =====================================================

        specs = {}

        for card in response.css("div.spec-card"):

            label = card.css(
                "span.spec-card-label::text"
            ).get()

            value = card.css(
                "span.spec-card-value ::text"
            ).get()

            if not value:

                value = card.css(
                    "span.spec-card-value::text"
                ).get()

            if label and value:

                label = " ".join(
                    label.split()
                )

                value = " ".join(
                    value.split()
                )

                specs[label] = value

        # =====================================================
        # EXTRACT SPECIFIC FIELDS
        # =====================================================

        company = specs.get("Entreprise")

        internship_type = specs.get("Stage")

        work_mode = specs.get("Temps de travail")

        sector = specs.get("Secteur")

        function = specs.get("Fonction")

        education_level = specs.get(
            "Niveau d'études"
        )

        # =====================================================
        # FILTER
        # =====================================================

        # Ignore internship requests
        if category == "Demandes stage":

            self.logger.info(
                "SKIPPED: Internship request | %s",
                title
            )

            return

        # Ignore normal job offers
        if internship_type != "Stage":

            self.logger.info(
                "SKIPPED: Not an internship | %s",
                title
            )

            return

        # =====================================================
        # DESCRIPTION
        # =====================================================

        description = response.css(
            "div#desc-content"
        ).xpath(
            "string(.)"
        ).get()

        if description:

            description = " ".join(
                description.split()
            )

        skills = extract_skills(description)

        stipend = None

        if description:
            description_lower = description.lower()

            if "non rémunéré" in description_lower:
                stipend = "Non rémunéré"

            elif "rémunéré" in description_lower:
                stipend = "Rémunéré"
        
        # =====================================================
        # APPLICATION DEADLINE
        # =====================================================

        application_deadline = None

        deadline_text = response.xpath(
            '//*[contains(normalize-space(), "Expire le")]//text()'
        ).getall()

        for text in deadline_text:

            text = " ".join(
                text.split()
            )

            if "Expire le" in text:

                application_deadline = (
                    text
                    .replace("Expire le", "")
                    .strip()
                )

                break

        # =====================================================
        # URL
        # =====================================================

        url = response.url
        self.logger.info("RAW URL: %r", url)
        # =====================================================
        # SOURCE
        # =====================================================

        source = "Publimaroc"

        # =====================================================
        # SCRAPED AT
        # =====================================================
        # We will add the exact scraping timestamp later
        # in the pipeline.

        # =====================================================
        # CREATE ITEM
        # =====================================================

        internship = InternshipItem(

           title=title,
           company=company,
           location=location,
           work_mode=work_mode,
           stipend=stipend,
           internship_type=internship_type,
           description=description,
           skills=skills,
           published_at=published_at,
           application_deadline=application_deadline,
           url=url,
           source=source,

)

        # =====================================================
        # LOG RESULT
        # =====================================================

        self.logger.info("=" * 70)
        self.logger.info("INTERNSHIP FOUND")
        self.logger.info("=" * 70)

        self.logger.info("TITLE: %s", title)
        self.logger.info("COMPANY: %s", company)
        self.logger.info("LOCATION: %s", location)
        self.logger.info("WORK MODE: %s", work_mode)
        self.logger.info("STIPEND: %s", stipend)
        self.logger.info(
            "INTERNSHIP TYPE: %s",
            internship_type
        )
        self.logger.info("SECTOR: %s", sector)
        self.logger.info("FUNCTION: %s", function)
        self.logger.info(
            "EDUCATION: %s",
            education_level
        )
        self.logger.info(
            "PUBLISHED AT: %s",
            published_at
        )
        self.logger.info(
            "APPLICATION DEADLINE: %s",
            application_deadline
        )
        self.logger.info(
            "URL: %s",
            url
        )

        self.logger.info("=" * 70)

        # =====================================================
        # RETURN ITEM
        # =====================================================

        yield internship

