from typing import List, Dict


def generate_answer(messages: List[Dict], context: str | None = None) -> str:
    """Minimal placeholder LLM call.

    Replace with integration to Ollama, OpenAI, or other provider.
    """
    user_msgs = [m for m in messages if m.get("role") == "user"]
    last = user_msgs[-1]["content"] if user_msgs else ""
    ctx = f"\nContext:\n{context}" if context else ""
    return f"(placeholder answer) Response to: '{last}'{ctx}"
