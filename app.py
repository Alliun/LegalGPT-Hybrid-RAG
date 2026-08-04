from conversation.context import conversation_context
from conversation.conversation_manager import handle_message
from flask import Flask, request, jsonify
from flask_cors import CORS

import json

from retrieval.hybrid_pipeline import run_pipeline

from metadata.document_lookup import get_document_by_citation
from query_processor.relevance import explain_relevance
from query_processor.explain import explain_judgment
from query_processor.compare import compare_judgments


# Legacy memory (temporary)
from memory.conversation_memory import save_search

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

        decision = handle_message(query)

        print("\n")
        print("=" * 80)
        print("CONVERSATION DECISION")
        print("=" * 80)
        print(decision)

        # =====================================================
        # Direct Conversation Response
        # =====================================================

        if decision["action"] == "respond":

            return jsonify({

        "type": "text",

        "content": decision["response"]

    })


        # =====================================================
        # Clarification Response
        # =====================================================

        if decision["action"] == "clarify":

                return jsonify({

        "type": "clarification",

        "content": decision["question"]

    })

         

        # =====================================================
        # Explain Previous Judgment
        # =====================================================

        if decision["action"] == "explain":

            results = conversation_context.get_last_results()

            if len(results) == 0:

                return jsonify({

                    "error":
                    "No previous search found. Search for a legal issue first."

                }), 400

            number = decision["judgment_number"]

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

        merged_results, llm_output = run_pipeline(decision["query"])

        cleaned = (

            llm_output
            .replace("```json", "")
            .replace("```", "")
            .strip()

        )

        print("\n")
        print("=" * 80)
        print("RAW LLM OUTPUT")
        print("=" * 80)
        print(llm_output)

        print("\n")
        print("=" * 80)
        print("PARSED RESPONSE")
        print("=" * 80)
        print(cleaned)

        response = json.loads(cleaned)

        

        # ========================================
        # Normalize Search Response
        # ========================================

        response["type"] = "judgment-list"

        save_search(query, merged_results)


        conversation_context.save_search(
            query,
            merged_results
        )

        conversation_context.save_search
        (
            query,
            merged_results
        )

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

        print("\n")
        print("=" * 80)
        print("FINAL RESPONSE")
        print("=" * 80)
        print(response)

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
# Explain API
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
# Relevance API
# =====================================================

@app.route("/api/relevance", methods=["POST"])
def relevance():

    try:

        data = request.get_json()

        citation = data.get("citation", "").strip()

        if citation == "":

            return jsonify({

                "error": "Citation required."

            }), 400

        # Get the user's most recent search query
        user_query = conversation_context.get_last_query()

        if not user_query:

            return jsonify({

                "error": "No previous search query found."

            }), 400

        # Retrieve the judgment
        document = get_document_by_citation(citation)

        if document is None:

            return jsonify({

                "error": "Judgment not found."

            }), 404

        # Generate AI relevance analysis
        analysis = explain_relevance(

            user_query,
            document

        )

     

        return jsonify({

            "type": "relevance",

            "citation": document.get("citation", ""),

            "case_number": document.get("case_number", ""),

            "court": document.get("court", ""),

            "judges": document.get("judges", ""),

            "decided_date": document.get("decided_date", ""),

            "source_file": document.get("source_file", ""),

            "query": user_query,

            "content": analysis

        })

    except Exception as e:

        print(e)

        return jsonify({

            "error": str(e)

        }), 500


# =====================================================
# Compare API
# =====================================================

@app.route("/api/compare", methods=["POST"])
def compare():

    try:

        data = request.get_json()

        citation1 = data.get("citation1", "").strip()
        citation2 = data.get("citation2", "").strip()

        if citation1 == "" or citation2 == "":

            return jsonify({

                "error": "Two citations are required."

            }), 400

        document1 = get_document_by_citation(citation1)
        document2 = get_document_by_citation(citation2)

        if document1 is None:

            return jsonify({

                "error": "First judgment not found."

            }), 404

        if document2 is None:

            return jsonify({

                "error": "Second judgment not found."

            }), 404

        comparison = compare_judgments(

            document1,
            document2

        )

        return jsonify({

            "type": "comparison",

            "citation1": document1.get("citation", ""),

            "citation2": document2.get("citation", ""),

            "content": comparison

        })

    except Exception as e:

        print(e)

        return jsonify({

            "error": str(e)

        }), 500

# =====================================================
# Open Full Judgment API
# =====================================================

@app.route("/api/open", methods=["POST"])
def open_judgment():

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

        

        return jsonify({

            "type": "judgment",

            "citation": document.get("citation", ""),

            "case_number": document.get("case_number", ""),

            "court": document.get("court", ""),

            "judges": document.get("judges", ""),

            "decided_date": document.get("decided_date", ""),

            "source_file": document.get("source_file", ""),

            "judgment_text": document.get("judgment_text", "")

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