from flask import Flask, request, jsonify
from flask_cors import CORS

import json

from retrieval.hybrid_pipeline import run_pipeline

from metadata.document_lookup import get_document_by_citation

from query_processor.explain import explain_judgment
from query_processor.intent import detect_intent

from memory.conversation_memory import (
    save_search,
    get_last_results
)

app = Flask(__name__)

CORS(app)


# =====================================================
# Health Check
# =====================================================

@app.route("/")
def home():
    return "LegalGPT Backend Running"


# =====================================================
# Debug Routes
# =====================================================

@app.route("/routes")
def routes():

    return {
        "routes": sorted(
            [str(rule) for rule in app.url_map.iter_rules()]
        )
    }


# =====================================================
# Main Chat API
# =====================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        query = data.get("query", "").strip()

        if not query:

            return jsonify({
                "error": "Query cannot be empty."
            }), 400

        print("\n")
        print("=" * 80)
        print("USER QUERY")
        print("=" * 80)
        print(query)

        # =====================================================
        # Detect Intent
        # =====================================================

        intent = detect_intent(query)

        print("\n")
        print("=" * 80)
        print("INTENT")
        print("=" * 80)
        print(intent)

        # =====================================================
        # Explain Previous Judgment
        # =====================================================

        if intent["intent"] == "explain":

            results = get_last_results()

            if len(results) == 0:

                return jsonify({

                    "error":
                    "No previous search found. Search for a legal issue first."

                }), 400

            number = intent["judgment_number"]

            if number < 1 or number > len(results):

                return jsonify({

                    "error":
                    f"Judgment {number} not found."

                }), 400

            document = results[number - 1]["document"]["_source"]

            explanation = explain_judgment(document)

            return jsonify({

                "type": "explanation",

                "judgment": number,

                "citation": document.get("citation", ""),

                "case_number": document.get("case_number", ""),

                "court": document.get("court", ""),

                "judges": document.get("judges", ""),

                "decided_date": document.get("decided_date", ""),

                "source_file": document.get("source_file", ""),

                "content": explanation

            })

        # =====================================================
        # Search Intent
        # =====================================================

        merged_results, llm_output = run_pipeline(query)

        cleaned = (

            llm_output
            .replace("```json", "")
            .replace("```", "")
            .strip()

        )

        response = json.loads(cleaned)

        save_search(query, merged_results)

        print("\n")
        print("=" * 80)
        print("SEARCH SAVED")
        print("=" * 80)
        print(query)

        print("\n")
        print("=" * 80)
        print("RESULTS STORED")
        print("=" * 80)
        print(len(merged_results))

        return jsonify(response)

    except Exception as e:

        print("\n")
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print(str(e))

        return jsonify({

            "error": str(e)

        }), 500


# =====================================================
# Direct Explain API
# =====================================================

@app.route("/api/explain", methods=["POST"])
def explain():

    try:

        data = request.get_json()

        citation = data.get("citation", "").strip()

        if citation == "":

            return jsonify({

                "error": "Citation required."

            }), 400

        document = get_document_by_citation(citation)

        if document is None:

            return jsonify({

                "error": "Judgment not found."

            }), 404

        explanation = explain_judgment(document)

        return jsonify({

            "type": "explanation",

            "citation": document.get("citation", ""),

            "case_number": document.get("case_number", ""),

            "court": document.get("court", ""),

            "judges": document.get("judges", ""),

            "decided_date": document.get("decided_date", ""),

            "source_file": document.get("source_file", ""),

            "content": explanation

        })

    except Exception as e:

        print(e)

        return jsonify({

            "error": str(e)

        }), 500


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    print("\nREGISTERED ROUTES\n")

    for rule in app.url_map.iter_rules():

        print(rule)

    print()

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )