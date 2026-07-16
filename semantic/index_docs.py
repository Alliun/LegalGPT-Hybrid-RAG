import os
import json

from elasticsearch import Elasticsearch

from config import *
from semantic.embeddings import embed_text


# ======================================================
# Elasticsearch Connection
# ======================================================

es = Elasticsearch(
    ELASTIC_URL,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
    verify_certs=False
)


# ======================================================
# Helper Function
# ======================================================

def list_to_text(items):
    """
    Converts any list (strings/dicts/mixed) into plain text.
    """

    if items is None:
        return ""

    if not isinstance(items, list):
        return str(items)

    output = []

    for item in items:

        if isinstance(item, str):
            output.append(item)

        elif isinstance(item, dict):

            values = []

            for value in item.values():

                if isinstance(value, list):
                    values.extend([str(v) for v in value])

                else:
                    values.append(str(value))

            output.append(" ".join(values))

        else:
            output.append(str(item))

    return " ".join(output)


# ======================================================
# Build Semantic Document
# ======================================================

def build_semantic_document(data):

    sections = list_to_text(data.get("sections_referred"))

    judges = list_to_text(data.get("judges"))

    appellants = list_to_text(data.get("appellants"))

    respondents = list_to_text(data.get("respondents"))

    headnotes = list_to_text(data.get("headnotes"))

    cases_referred = list_to_text(data.get("cases_referred"))

    citations_referred = list_to_text(data.get("citations_referred"))

    advocates = list_to_text(data.get("advocates"))

    document = f"""
Citation:
{data.get("citation","")}

Court:
{data.get("court","")}

Case Number:
{data.get("case_number","")}

Judges:
{judges}

Appellants:
{appellants}

Respondents:
{respondents}

Sections Referred:
{sections}

Cases Referred:
{cases_referred}

Citations Referred:
{citations_referred}

Headnotes:
{headnotes}

Advocates:
{advocates}

Outcome:
{data.get("outcome","")}

Prayer:
{data.get("prayer","")}

Judgment Text:

{data.get("judgment_text","")}
"""

    return document


# ======================================================
# Index Documents
# ======================================================

count = 0

for filename in os.listdir(DATA_FOLDER):

    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(DATA_FOLDER, filename)

    try:

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        semantic_document = build_semantic_document(data)

        embedding = embed_text(semantic_document)

        document = {
            "citation": data.get("citation", ""),
            "court": data.get("court", ""),
            "case_number": data.get("case_number", ""),
            "source_file": data.get("source_file", ""),
            "judgment_text": semantic_document,
            "embedding": embedding
        }

        es.index(
            index=SEMANTIC_INDEX,
            id=filename,
            document=document
        )

        count += 1

        if count % 100 == 0:
            print(f"Indexed {count} documents...")

    except Exception as e:

        print(f"\nError indexing {filename}")
        print(e)


print("\n======================================")
print(f"Finished indexing {count} judgments.")
print("======================================")