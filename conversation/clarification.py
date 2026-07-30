# =====================================================
# Ambiguous Legal Topics
# =====================================================

CLARIFICATION_RULES = {

    "harassment": {
        "question": (
            "Could you clarify what type of harassment you mean?\n\n"
            "• Workplace harassment\n"
            "• Sexual harassment\n"
            "• Criminal harassment\n"
            "• Cyber harassment"
        ),
        "options": [
            "workplace harassment",
            "sexual harassment",
            "criminal harassment",
            "cyber harassment"
        ]
    },

    "fraud": {
        "question": (
            "Could you clarify what type of fraud you are referring to?\n\n"
            "• Banking fraud\n"
            "• Property fraud\n"
            "• Online fraud\n"
            "• Corporate fraud"
        ),
        "options": [
            "banking fraud",
            "property fraud",
            "online fraud",
            "corporate fraud"
        ]
    },

    "assault": {
        "question": (
            "Could you clarify what type of assault you mean?\n\n"
            "• Physical assault\n"
            "• Sexual assault\n"
            "• Domestic violence"
        ),
        "options": [
            "physical assault",
            "sexual assault",
            "domestic violence"
        ]
    }

}


# =====================================================
# Check Clarification
# =====================================================

def needs_clarification(query):

    query = query.lower().strip()

    for keyword in CLARIFICATION_RULES:

        if query == keyword:

            return {

                "needs_clarification": True,

                "keyword": keyword,

                "question": CLARIFICATION_RULES[keyword]["question"]

            }

    return {

        "needs_clarification": False

    }