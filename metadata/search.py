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


# ==========================================================
# Build Explicit Metadata Query
# ==========================================================

def build_explicit_query(explicit):

    should = []

    # ---------------- Sections ----------------

    for section in explicit.get("sections_referred", []):

        should.append({
            "match": {
                "sections_referred": {
                    "query": section,
                    "boost": 15
                }
            }
        })

    # ---------------- Constitutional Articles ----------------

    for article in explicit.get("constitutional_articles", []):

        should.append({
            "match": {
                "sections_referred": {
                    "query": article,
                    "boost": 14
                }
            }
        })

    # ---------------- Acts ----------------

    for act in explicit.get("acts", []):

        should.append({
            "match": {
                "judgment_text": {
                    "query": act,
                    "boost": 12
                }
            }
        })

    # ---------------- Cases Referred ----------------

    for case in explicit.get("cases_referred", []):

        should.append({
            "match": {
                "cases_referred": {
                    "query": case,
                    "boost": 13
                }
            }
        })

    # ---------------- Citations ----------------

    for citation in explicit.get("citations_referred", []):

        should.append({
            "match": {
                "citations_referred": {
                    "query": citation,
                    "boost": 13
                }
            }
        })

    # ---------------- Court ----------------

    if explicit.get("court"):

        should.append({
            "match": {
                "court": {
                    "query": explicit["court"],
                    "boost": 10
                }
            }
        })

    # ---------------- Judges ----------------

    for judge in explicit.get("judges", []):

        should.append({
            "match": {
                "judges": {
                    "query": judge,
                    "boost": 10
                }
            }
        })

    # ---------------- Appellants ----------------

    for appellant in explicit.get("appellants", []):

        should.append({
            "match": {
                "appellants": {
                    "query": appellant,
                    "boost": 8
                }
            }
        })

    # ---------------- Respondents ----------------

    for respondent in explicit.get("respondents", []):

        should.append({
            "match": {
                "respondents": {
                    "query": respondent,
                    "boost": 8
                }
            }
        })

    return should


# ==========================================================
# Build Inferred Metadata Query
# ==========================================================

def build_inferred_query(inferred):

    should = []

    # ---------------- Legal Domain ----------------

    if inferred.get("legal_domain"):

        should.append({
            "multi_match": {
                "query": inferred["legal_domain"],
                "fields": [
                    "headnotes^4",
                    "judgment_text^3",
                    "prayer^2"
                ],
                "boost": 5
            }
        })

    # ---------------- Acts ----------------

    for act in inferred.get("acts", []):

        should.append({
            "multi_match": {
                "query": act,
                "fields": [
                    "judgment_text^4",
                    "headnotes^3",
                    "prayer^2"
                ],
                "boost": 5
            }
        })

    # ---------------- Legal Principles ----------------

    for principle in inferred.get("legal_principles", []):

        should.append({
            "multi_match": {
                "query": principle,
                "fields": [
                    "judgment_text^4",
                    "headnotes^4",
                    "prayer^2"
                ],
                "boost": 4
            }
        })

    # ---------------- Keywords ----------------

    for keyword in inferred.get("keywords", []):

        should.append({
            "multi_match": {
                "query": keyword,
                "fields": [
                    "headnotes^5",
                    "judgment_text^4",
                    "prayer^3",
                    "sections_referred^2",
                    "cases_referred^2"
                ],
                "boost": 3
            }
        })

    return should


# ==========================================================
# Build Final Query
# ==========================================================

def build_query(metadata):

    explicit = metadata.get("explicit", {})
    inferred = metadata.get("inferred", {})

    should = []

    should.extend(build_explicit_query(explicit))
    should.extend(build_inferred_query(inferred))

    return {
        "bool": {
            "should": should,
            "minimum_should_match": 1
        }
    }


# ==========================================================
# Metadata Search
# ==========================================================

def metadata_search(metadata, top_k=10):

    query = build_query(metadata)

    response = es.search(
        index=INDEX_NAME,
        size=top_k,
        query=query
    )

    return response["hits"]["hits"]


# ==========================================================
# Standalone Test
# ==========================================================

if __name__ == "__main__":

    sample_metadata = {
        "explicit": {},
        "inferred": {
            "legal_domain": "Labour Law",
            "acts": [
                "Industrial Disputes Act"
            ],
            "legal_principles": [
                "Natural Justice"
            ],
            "keywords": [
                "wrongful termination",
                "employment",
                "domestic enquiry"
            ]
        }
    }

    results = metadata_search(sample_metadata)

    print("\nTop Results\n")

    for i, hit in enumerate(results, start=1):

        source = hit["_source"]

        print("=" * 100)
        print(f"Rank: {i}")
        print(f"Elastic Score: {hit['_score']:.2f}")
        print(f"Citation: {source.get('citation')}")
        print(f"Case Number: {source.get('case_number')}")
        print(f"Court: {source.get('court')}")
        print(f"Outcome: {source.get('outcome')}")
        print(f"Source File: {source.get('source_file')}")

        print("\nJudgment Preview:\n")
        print(source.get("judgment_text", "")[:500])
        print()