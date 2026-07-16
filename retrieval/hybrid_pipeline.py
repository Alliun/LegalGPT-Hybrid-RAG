import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from query_processor.metadata_extractor import extract_metadata
from metadata.search import metadata_search
from semantic.search import semantic_search
from retrieval.merge import reciprocal_rank_fusion
from query_processor.reranker import rerank


# =====================================================
# Hybrid Search
# =====================================================

def hybrid_search(query):

    print("\nExtracting Metadata...\n")

    metadata = extract_metadata(query)

    print("\nSearching Metadata Index...\n")

    metadata_results = metadata_search(metadata)

    print("\nSearching Semantic Index...\n")

    semantic_results = semantic_search(query)

    print("\nMerging Results...\n")

    merged = reciprocal_rank_fusion(
        metadata_results,
        semantic_results
    )

    return merged
# =====================================================
# Complete Pipeline
# =====================================================

def run_pipeline(query):

    # -------------------------------
    # Run Hybrid Search
    # -------------------------------

    merged_results = hybrid_search(query)

    # -------------------------------
    # Debug - First Retrieved Document
    # -------------------------------

    import pprint

    print("\nFIRST DOCUMENT:\n")

    pprint.pprint(
        merged_results[0]["document"]["_source"]
    )

    # -------------------------------
    # LLM Re-ranking
    # -------------------------------

    llm_response = rerank(
        query,
        merged_results
    )

    # -------------------------------
    # Return BOTH
    # -------------------------------

    return merged_results, llm_response
# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    query = input("\nEnter Legal Query:\n\n")

    results = hybrid_search(query)

    print("\n")
    print("=" * 120)
    print("HYBRID RESULTS")
    print("=" * 120)

    for rank, item in enumerate(results[:10], start=1):

        hit = item["document"]
        source = hit["_source"]

        print("\n")
        print("=" * 120)

        print(f"Rank : {rank}")

        print(f"Hybrid Score : {item['score']:.5f}")

        print(f"Metadata Contribution : {item['metadata_score']:.5f}")

        print(f"Semantic Contribution : {item['semantic_score']:.5f}")

        print()

        print("Retrieved By:")

        if item["metadata_score"] > 0:
            print("✓ Metadata Search")

        if item["semantic_score"] > 0:
            print("✓ Semantic Search")

        print()

        print(f"Citation : {source.get('citation','')}")

        print(f"Court : {source.get('court','')}")

        print(f"Case Number : {source.get('case_number','')}")

        print(f"Judges : {source.get('judges','')}")

        print(f"Outcome : {source.get('outcome','')}")

        print(f"Sections : {source.get('sections_referred','')}")

        print(f"Respondents : {source.get('respondents','')}")

        print(f"Source File : {source.get('source_file','')}")

        print("\nPreview:\n")

        print(source.get("judgment_text","")[:700])

    print("\n")
    print("=" * 120)
    print("Total Unique Results :", len(results))
    print("=" * 120)

    # =====================================================
    # LLM Re-ranking
    # =====================================================

    print("\n")
    print("=" * 120)
    print("LLM RE-RANKING")
    print("=" * 120)

    llm_output = rerank(query, results)

    print(llm_output)

    