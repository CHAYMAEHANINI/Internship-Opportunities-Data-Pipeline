import json
from pathlib import Path
from datetime import datetime


def transform_data(data):
    transformed_data = []

    for record in data:
        record = clean_record(record)

        if not validate_record(record):
            continue

        record = normalize_dates(record)

        transformed_data.append(record)

    return transformed_data

def save_processed_data(data):
    processed_file = Path("data/processed/internships.json")

    with open(processed_file, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def normalize_dates(record):
    if record.get("published_at"):
        record["published_at"] = datetime.fromisoformat(
            record["published_at"]
        ).isoformat(sep=" ")

    if record.get("application_deadline"):
        record["application_deadline"] = datetime.strptime(
            record["application_deadline"],
            "%Y-%m-%d"
        ).date().isoformat()

    return record

def load_raw_data():
    raw_file = Path("data/raw/publimaroc.json")

    with open(raw_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data



def clean_text(value):
    if value is None:
        return None

    return " ".join(str(value).split())

TEXT_FIELDS = [
    "title",
    "company",
    "location",
    "work_mode",
    "stipend",
    "internship_type",
    "description",
    "source",
]
REQUIRED_FIELDS = [
    "title",
    "published_at",
    "url",
    "source",
]
def validate_record(record):
    for field in REQUIRED_FIELDS:
        if not record.get(field):
            return False

    return True

def clean_record(record):
    for field in TEXT_FIELDS:
        record[field] = clean_text(record.get(field))

    return record

def filter_valid_records(data):
    valid_records = []

    for record in data:
        if validate_record(record):
            valid_records.append(record)

    return valid_records

if __name__ == "__main__":
    data = load_raw_data()

    transformed_data = transform_data(data)

    save_processed_data(transformed_data)

    print(f"Raw records: {len(data)}")
    print(f"Transformed records: {len(transformed_data)}")
    print("Processed data saved successfully.")