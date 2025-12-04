import os
from typing import Dict, Any

from google import genai

_client: genai.Client | None = None
_MODEL_NAME = os.getenv("GEMINI_HINT_MODEL", "gemini-2.5-flash")


class HintGenerationError(Exception):
    """Raised when the hint generation pipeline fails."""


def _get_client() -> genai.Client:
    """Lazy-init the Gemini client so tests without a key do not break imports."""
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HintGenerationError("GEMINI_API_KEY is not configured.")

    _client = genai.Client(api_key=api_key)
    return _client


def _build_prompt(word_context: Dict[str, Any]) -> str:
    """Craft an instruction prompt for the LLM using available context."""
    spelling = word_context.get("spelling", "")
    summary = word_context.get("summary_meaning", "")
    definition = word_context.get("full_definition", "")
    example_sentence = word_context.get("example_sentence", "")
    example_translation = word_context.get("example_translation", "")
    mnemonic_tip = word_context.get("mnemonic_tip", "")

    return f"""
You are a helpful bilingual vocabulary tutor. The student only saw the Korean meaning
and wants an English hint to recall the word. Provide ONE short, encouraging hint
in Korean that nudges them toward the answer without revealing the spelling.

Word data (do not reveal directly):
- English spelling: {spelling}
- Summary meaning: {summary}
- Full definition: {definition}
- Example sentence: {example_sentence}
- Example translation: {example_translation}
- Mnemonic tip: {mnemonic_tip}

Constraints:
- Output must be under 50 Korean characters if possible.
- Do not mention the exact English spelling.
- Focus on imagery, situations, or root meanings to jog memory.
"""


def generate_hint(word_context: Dict[str, Any]) -> str:
    """Create an AI-generated hint using Gemini + the supplied RAG context."""
    if not word_context:
        raise HintGenerationError("word_context is required for hint generation.")

    prompt = _build_prompt(word_context)

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
        )
    except Exception as exc:  # pragma: no cover - upstream client errors
        raise HintGenerationError(f"Gemini API error: {exc}") from exc

    text = getattr(response, "text", None)
    if not text:
        raise HintGenerationError("Gemini API returned an empty response.")

    return text.strip()