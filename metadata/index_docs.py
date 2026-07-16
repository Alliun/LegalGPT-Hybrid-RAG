import os
import json
from elasticsearch import Elasticsearch

# ----------------------------------------
# Elasticsearch Connection
# ----------------------------------------

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "mRdWR4YB9yC4PsAE2zlx"),
    verify_certs=False
)

INDEX_NAME = "legal_metadata"

# ----------------------------------------
# Folder containing JSON judgments
# ----------------------------------------

DATA_FOLDER = "data/corpus"

# ----------------------------------------
# Index Documents
# ----------------------------------------

count = 0

for filename in os.listdir(DATA_FOLDER):

    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(DATA_FOLDER, filename)

    try:

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        document = {

            "citation": data.get("citation", ""),

            "court": data.get("court", ""),

            "judges": " ".join(data.get("judges", [])),

            "judges_raw": data.get("judges_raw", ""),

            "appellants": " ".join(data.get("appellants", [])),

            "respondents": " ".join(data.get("respondents", [])),

            "case_number": data.get("case_number", ""),

            "decided_date": data.get("decided_date", ""),

            "headnotes": " ".join(data.get("headnotes", [])),

            "cases_referred": " ".join(data.get("cases_referred", [])),

            "citations_referred": " ".join(data.get("citations_referred", [])),

            "sections_referred": " ".join(data.get("sections_referred", [])),

            "advocates": " ".join(data.get("advocates", [])),

            "outcome": data.get("outcome", ""),

            "prayer": data.get("prayer", ""),

            "judgment_text": data.get("judgment_text", ""),

            "source_file": data.get("source_file", filename)
        }

        es.index(
            index=INDEX_NAME,
            document=document
        )

        count += 1

        if count % 100 == 0:
            print(f"{count} judgments indexed...")

    except Exception as e:

        print(f"Failed to index {filename}")
        print(e)

print("\n------------------------------------")
print(f"Successfully indexed {count} judgments")
print("------------------------------------")