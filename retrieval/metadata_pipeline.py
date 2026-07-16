from query_processor.metadata_extractor import extract_metadata
from metadata.search import metadata_search
import json


# ==========================================================
# Complete Metadata Retrieval Pipeline
# ==========================================================

def retrieve_similar_judgments(user_query, top_k=10):

    print("\nExtracting legal metadata...\n")

    metadata = extract_metadata(user_query)

    print("=" * 100)
    print("EXTRACTED METADATA")
    print("=" * 100)

    print(json.dumps(metadata, indent=4))

    print("\nSearching Elasticsearch...\n")

    results = metadata_search(metadata, top_k)

    return metadata, results


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    query = input("\nEnter Legal Query:\n\n")

    metadata, results = retrieve_similar_judgments(query)

    print("\n")
    print("=" * 100)
    print("TOP SIMILAR JUDGMENTS")
    print("=" * 100)

    if len(results) == 0:

        print("\nNo matching judgments found.")

    else:

        for rank, hit in enumerate(results, start=1):

            source = hit["_source"]

            print("\n")
            print("=" * 100)
            print(f"Rank : {rank}")
            print(f"Elastic Score : {hit['_score']:.2f}")

            print(f"Citation : {source.get('citation')}")

            print(f"Case Number : {source.get('case_number')}")

            print(f"Court : {source.get('court')}")

            print(f"Judges : {source.get('judges')}")

            print(f"Outcome : {source.get('outcome')}")

            print(f"Source File : {source.get('source_file')}")

            print("\nSections Referred")

            print(source.get("sections_referred"))

            print("\nCases Referred")

            print(source.get("cases_referred"))

            print("\nJudgment Preview\n")

            print(source.get("judgment_text", "")[:700])

            print("\n")