

USELESS_ANSWERS = [
    "Well, that's a difficult request...",
    "I'm not sure I can help with that.",
    "That's an interesting question, but I don't have a good answer.",
    "Let me think about that... Hmm, I've got nothing.",
    "Have you tried turning it off and on again?",
    "42 is probably the answer you're looking for.",
    "I'm just a dummy agent, I can't really help.",
    "Ask me again later, I might have a better answer then."
]


class DummyAgent:
    """A dummy agent that does nothing."""
    SUPPORTED_CONTENT_TYPES = ["text"]
    
    def invoke(self, query, sessionId) -> str:
        # return random.choice(USELESS_ANSWERS)
        return {
            "is_task_complete": True,
            "require_user_input": False,
            "content": "We are unable to process your request at the moment. Please try again.",
        }

