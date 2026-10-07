from datetime import datetime
import hashlib
import json
from pathlib import Path


class InternshipPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    # ==========================================
    # LOAD SEEN OFFERS
    # ==========================================

    def load_seen_offers(self):

        seen_file = Path(
            "../../data/processed/seen_offers.json"
        )

        if not seen_file.exists():
            return set()

        with open(
            seen_file,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return set(data)

    # ==========================================
    # SAVE SEEN OFFERS
    # ==========================================

    def save_seen_offers(self, seen_offers):

        seen_file = Path(
            "../../data/processed/seen_offers.json"
        )

        with open(
            seen_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                list(seen_offers),
                file,
                indent=4
            )

    # ==========================================
    # NORMALIZE DATES
    # ==========================================

    def normalize_dates(self, item):

        # Publication date
        if item.get("published_at"):

            item["published_at"] = datetime.strptime(
                item["published_at"],
                "%d %b %Y %H:%M"
            ).isoformat(sep=" ")

        # Application deadline
        if item.get("application_deadline"):

            item["application_deadline"] = datetime.strptime(
                item["application_deadline"],
                "%d/%m/%Y"
            ).date().isoformat()

        return item

    # ==========================================
    # PROCESS ITEM
    # ==========================================

    def process_item(self, item):

        # ==========================================
        # 1. VALIDATION
        # ==========================================

        required_fields = [
            "title",
            "published_at",
            "url",
            "source",
        ]

        for field in required_fields:

            if not item.get(field):

                raise ValueError(
                    f"Missing required field: {field}"
                )

        # ==========================================
        # 2. CLEANING
        # ==========================================

        text_fields = [
            "title",
            "company",
            "location",
            "work_mode",
            "stipend",
            "internship_type",
            "description",
            "published_at",
            "application_deadline",
            "url",
            "source",
        ]

        for field in text_fields:

            if item.get(field):

                item[field] = " ".join(
                    str(item[field]).split()
                )

        # ==========================================
        # 3. NORMALIZE DATES
        # ==========================================

        item = self.normalize_dates(item)

        # ==========================================
        # 4. GENERATE UNIQUE ID
        # ==========================================

        item["id"] = hashlib.md5(
            item["url"].encode()
        ).hexdigest()

        # ==========================================
        # 5. ADD SCRAPING TIMESTAMP
        # ==========================================

        item["scraped_at"] = datetime.now().isoformat()

        # ==========================================
        # 6. NEW OFFER DETECTION
        # ==========================================

        seen_offers = self.load_seen_offers()

        if item["id"] in seen_offers:

            print(
                "ALREADY SEEN ❌:",
                item["title"]
            )

        else:

            print(
                "NEW OFFER ✅:",
                item["title"]
            )

            seen_offers.add(item["id"])

            self.save_seen_offers(
                seen_offers
            )

        # ==========================================
        # 7. RETURN PROCESSED ITEM
        # ==========================================

        return item
