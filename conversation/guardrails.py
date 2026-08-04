# =====================================================
# Guardrails for Conversation
# =====================================================

LEGAL_KEYWORDS = [

    "law",
    "legal",
    "court",
    "judge",
    "judgment",
    "case",
    "petition",
    "section",
    "article",
    "ipc",
    "bns",
    "crpc",
    "harassment",
    "divorce",
    "property",
    "consumer",
    "cheque",
    "labour",
    "criminal",
    "civil",
    "contract",
    "appeal",
    "bail",
    "evidence",
    "murder",
    "rape",
    "posco",
    "pocso"

]


def run_guardrails(query, conversation_context):

    query = query.strip()

    # ==========================================
    # Empty Query
    # ==========================================

    if not query:

        return {

            "blocked": True,

            "response": "Please enter a legal question."

        }

    # ==========================================
    # Domain Check
    # ==========================================

    text = query.lower()

    if not any(keyword in text for keyword in LEGAL_KEYWORDS):

        greetings = [

            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "bye"

        ]

        if not any(word in text for word in greetings):

            return {

                "blocked": True,

                "response":
                "I can only assist with legal research, legal judgments, and legal questions."

            }

    # ==========================================
    # Passed
    # ==========================================

    return None