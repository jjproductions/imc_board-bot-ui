from pathlib import Path
import os
from pydantic import Field
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# ---- Project paths ----------------------------------------------------------
# Adjust parents[...] if your nesting differs.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Determine which environment to load (default: development)
# OS env has highest precedence. If not set, we use "development".
ENV = os.getenv("ENVIRONMENT", "development").strip().lower()

# Select the appropriate .env file
# e.g., .env.development, .env.staging, .env.production
ENV_FILE = PROJECT_ROOT / f".env.{ENV}"
# Fallback: if the env-specific file is missing, try .env
if not ENV_FILE.exists():
    ENV_FILE = PROJECT_ROOT / ".env"

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Core
    APP_NAME: str = "Board Policy Bot API"
    APP_VERSION: str = "0.5.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = ENV  # bound to ENV
    DEBUG: bool = ENV == "development"
    

    # Qdrant
    QDRANT_URL: str = Field("http://localhost:6333", env="QDRANT_URL")
    QDRANT_API_KEY: str | None = Field(None, env="QDRANT_API_KEY")
    QDRANT_COLLECTION: str = Field("board-policies", env="QDRANT_COLLECTION")
    EMBEDDING_MODEL: str = Field("BAAI/bge-m3", env="EMBEDDING_MODEL")
    EMBEDDING_DIM: int = Field(1024, env="EMBEDDING_DIM")
    TEXT_PAYLOAD_KEY: str = Field("text", env="TEXT_PAYLOAD_KEY")
    # LLM
    LLM_PROVIDER: str = Field("ollama", env="LLM_PROVIDER")
    LLM_MODEL: str = Field(default="mixtral:8x7b-instruct-v0.1-q4_K_M", env="LLM_MODEL")
    LLM_SYS_PROMPT: str = Field(
        """You are an assistant that MUST answer ONLY using the provided context.
        If the answer is not explicitly contained in the context, reply:
        "I do not know based on the provided IMC board policies context."

        Rules:
        - Cite the specific section titles or IDs when possible.
        - Never invent facts beyond the context.
        - If the user asks for content not found, say you do not know based on the context.
        """, 
        env="LLM_PROMPT")
    LLM_USER_PROMPT: str = Field(
        """Answer the user question using ONLY the context below.

        [CONTEXT]
        {context}

        [QUESTION]
        {question}

        If the answer is not in the context, say:
        "I do not know based on the provided IMC board policies context."
        """,
        env="LLM_USER_PROMPT"
    )
    BOARD_POLICIES_IDK_RESPONSE: str = Field("I do not know based on the provided IMC board policies.", env="BOARD_POLICIES_IDK_RESPONSE")

    PORT: int = Field(8002, env="PORT")
    
    TOP_K_DEFAULT: int = Field(5, env="TOP_K")
    MAX_CONTEXT_CHARS: int = Field(12000, env="MAX_CONTEXT_CHARS")

settings = AppSettings()