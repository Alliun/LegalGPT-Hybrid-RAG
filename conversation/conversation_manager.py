from conversation.intent_classifier import detect_intent
from conversation.clarification import needs_clarification
from conversation.context import conversation_context
from conversation.guardrails import run_guardrails
from conversation.followup import resolve_followup

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

    # =====================================================
    # Store User Message
    # =====================================================

    conversation_context.add_user_message(query)

    # =====================================================
    # Guardrails
    # =====================================================

    guardrail = run_guardrails(
        query,
        conversation_context
    )

    if guardrail:

        conversation_context.add_ai_message(
            guardrail["response"]
        )

        conversation_context.set_last_action("guardrail")
        conversation_context.set_last_intent("guardrail")

        return {

            "action": "respond",

            "response": guardrail["response"]

        }

    # =====================================================
    # Detect Intent
    # =====================================================

    intent = detect_intent(query)

    conversation_context.set_last_intent(
        intent["intent"]
    )

    # =====================================================
    # Resolve Follow-up References
    # =====================================================

    followup_index = resolve_followup(
        query,
        conversation_context
    )

    if followup_index is not None:

        conversation_context.set_active_judgment(
            followup_index
        )

    # =====================================================
    # Greeting
    # =====================================================

    if intent["intent"] == "greeting":

        conversation_context.add_ai_message(
            GREETING_RESPONSE
        )

        conversation_context.set_last_action("greeting")

        return {

            "action": "respond",

            "response": GREETING_RESPONSE

        }

    # =====================================================
    # Goodbye
    # =====================================================

    if intent["intent"] == "goodbye":

        conversation_context.add_ai_message(
            GOODBYE_RESPONSE
        )

        conversation_context.set_last_action("goodbye")

        return {

            "action": "respond",

            "response": GOODBYE_RESPONSE

        }

    # =====================================================
    # Thanks
    # =====================================================

    if intent["intent"] == "thanks":

        conversation_context.add_ai_message(
            THANKS_RESPONSE
        )

        conversation_context.set_last_action("thanks")

        return {

            "action": "respond",

            "response": THANKS_RESPONSE

        }

    # =====================================================
    # Help
    # =====================================================

    if intent["intent"] == "help":

        conversation_context.add_ai_message(
            HELP_RESPONSE
        )

        conversation_context.set_last_action("help")

        return {

            "action": "respond",

            "response": HELP_RESPONSE

        }

    # =====================================================
    # Follow-up Commands
    # =====================================================

    if intent["intent"] == "follow_up":

        conversation_context.set_last_action(
            intent["action"]
        )

        return {

            "action": intent["action"],

            **intent

        }

    # =====================================================
    # Clarification
    # =====================================================

    clarification = needs_clarification(query)

    if clarification["needs_clarification"]:

        conversation_context.add_ai_message(
            clarification["question"]
        )

        conversation_context.set_last_action(
            "clarify"
        )

        conversation_context.set_pending_clarification(
            clarification["keyword"]
        )

        return {

            "action": "clarify",

            "question": clarification["question"],

            "keyword": clarification["keyword"]

        }

    # =====================================================
    # Default Search
    # =====================================================

    conversation_context.set_last_action("search")
    conversation_context.set_current_topic(query)
    conversation_context.clear_pending_clarification()

    return {

        "action": "search",

        "query": query

    }