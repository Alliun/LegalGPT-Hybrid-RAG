from conversation.intent_classifier import detect_intent

from conversation.clarification import needs_clarification

from conversation.responses import (
    GREETING_RESPONSE,
    GOODBYE_RESPONSE,
    THANKS_RESPONSE,
    HELP_RESPONSE
)


# =====================================================
# Conversation Manager
# =====================================================

def handle_message(query):

    intent = detect_intent(query)

    # ==========================================
    # Greeting
    # ==========================================

    if intent["intent"] == "greeting":

        return {

            "action": "respond",

            "response": GREETING_RESPONSE

        }

    # ==========================================
    # Goodbye
    # ==========================================

    if intent["intent"] == "goodbye":

        return {

            "action": "respond",

            "response": GOODBYE_RESPONSE

        }

    # ==========================================
    # Thanks
    # ==========================================

    if intent["intent"] == "thanks":

        return {

            "action": "respond",

            "response": THANKS_RESPONSE

        }

    # ==========================================
    # Help
    # ==========================================

    if intent["intent"] == "help":

        return {

            "action": "respond",

            "response": HELP_RESPONSE

        }

    # ==========================================
    # Follow-up Commands
    # ==========================================

    if intent["intent"] == "follow_up":

        return {

            "action": intent["action"],

            **intent

        }

    # ==========================================
    # Clarification Guardrail
    # ==========================================

    clarification = needs_clarification(query)

    if clarification["needs_clarification"]:

        return {

            "action": "clarify",

            "question": clarification["question"],

            "keyword": clarification["keyword"]

        }

    # ==========================================
    # Default Legal Search
    # ==========================================

    return {

        "action": "search",

        "query": query

    }