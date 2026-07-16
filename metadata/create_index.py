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
# Delete Existing Index
# ----------------------------------------

if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)
    print(f"Deleted existing index: {INDEX_NAME}")

# ----------------------------------------
# Create Index Mapping
# ----------------------------------------

mapping = {
    "mappings": {
        "properties": {

            "citation": {
                "type": "keyword"
            },

            "case_number": {
                "type": "text"
            },

            "court": {
                "type": "text"
            },

            "judges": {
                "type": "text"
            },

            "judges_raw": {
                "type": "text"
            },

            "appellants": {
                "type": "text"
            },

            "respondents": {
                "type": "text"
            },

            "decided_date": {
                "type": "text"
            },

            "headnotes": {
                "type": "text"
            },

            "cases_referred": {
                "type": "text"
            },

            "citations_referred": {
                "type": "text"
            },

            "sections_referred": {
                "type": "text"
            },

            "advocates": {
                "type": "text"
            },

            "outcome": {
                "type": "text"
            },

            "prayer": {
                "type": "text"
            },

            "judgment_text": {
                "type": "text"
            },

            "source_file": {
                "type": "keyword"
            }

        }
    }
}

# ----------------------------------------
# Create Index
# ----------------------------------------

es.indices.create(
    index=INDEX_NAME,
    body=mapping
)

print(f"\nIndex '{INDEX_NAME}' created successfully.")