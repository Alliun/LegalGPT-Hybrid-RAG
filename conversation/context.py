from langchain_classic.memory import ConversationBufferWindowMemory


class ConversationContext:

    def __init__(self):

        # =====================================================
        # Conversation Memory (Last 5 Exchanges)
        # =====================================================

        self.memory = ConversationBufferWindowMemory(
            k=5,
            return_messages=True
        )

        # =====================================================
        # Search Context
        # =====================================================

        self.last_query = None
        self.last_results = []

        # =====================================================
        # Active Judgment
        # =====================================================

        self.active_judgment = None
        self.active_index = None

        # =====================================================
        # Conversation State
        # =====================================================

        self.last_action = None
        self.last_intent = None
        self.current_topic = None
        self.pending_clarification = None

    # -------------------------------------------------
    # Conversation Memory
    # -------------------------------------------------

    def add_user_message(self, message):

        self.memory.chat_memory.add_user_message(message)

    def add_ai_message(self, message):

        self.memory.chat_memory.add_ai_message(message)

    def get_history(self):

        return self.memory.chat_memory.messages

    def clear_history(self):

        self.memory.clear()

    # -------------------------------------------------
    # Search Context
    # -------------------------------------------------

    def save_search(self, query, results):

        self.last_query = query
        self.last_results = results

        self.active_judgment = None
        self.active_index = None

    def get_last_results(self):

        return self.last_results

    def get_last_query(self):

        return self.last_query

    # -------------------------------------------------
    # Active Judgment
    # -------------------------------------------------

    def set_active_judgment(self, index):

        if 0 <= index < len(self.last_results):

            self.active_index = index
            self.active_judgment = self.last_results[index]

    def get_active_judgment(self):

        return self.active_judgment

    def get_active_index(self):

        return self.active_index

    # -------------------------------------------------
    # Conversation State
    # -------------------------------------------------

    def set_last_action(self, action):

        self.last_action = action

    def get_last_action(self):

        return self.last_action

    def set_last_intent(self, intent):

        self.last_intent = intent

    def get_last_intent(self):

        return self.last_intent

    def set_current_topic(self, topic):

        self.current_topic = topic

    def get_current_topic(self):

        return self.current_topic

    def set_pending_clarification(self, keyword):

        self.pending_clarification = keyword

    def get_pending_clarification(self):

        return self.pending_clarification

    def clear_pending_clarification(self):

        self.pending_clarification = None

    # -------------------------------------------------
    # Reset Everything
    # -------------------------------------------------

    def clear(self):

        self.clear_history()

        self.last_query = None
        self.last_results = []

        self.active_judgment = None
        self.active_index = None

        self.last_action = None
        self.last_intent = None
        self.current_topic = None
        self.pending_clarification = None


conversation_context = ConversationContext()