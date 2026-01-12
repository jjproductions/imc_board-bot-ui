
import ollama
from ..core.config import settings

MODEL_NAME = settings.LLM_MODEL
SYSTEM_PROMPT = settings.LLM_USER_PROMPT

def answer(question: str, context: str) -> ollama.ChatResponse:
    #user_prompt = f"{settings.LLM_USER_PROMPT}"
    user_prompt = f"""Answer the user question using ONLY the context below.

[CONTEXT]
{context}

[QUESTION]
{question}

If the answer is not in the context, say:
"I do not know based on the provided IMC board policies context."
"""
    resp = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp
