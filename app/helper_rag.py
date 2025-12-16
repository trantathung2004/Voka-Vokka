import os
from typing import Dict, Any

import ollama

_MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")


class HintGenerationError(Exception):
    """Raised when the hint generation pipeline fails."""


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
in Korean that nudges them toward the answer WITHOUT REVEALING THE SPELLING.

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
    """Create an AI-generated hint using Ollama + the supplied RAG context."""
    if not word_context:
        raise HintGenerationError("word_context is required for hint generation.")

    prompt = _build_prompt(word_context)

    try:
        response = ollama.chat(
            model=_MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
    except Exception as exc:
        raise HintGenerationError(f"Ollama API error: {exc}") from exc

    # Ollama response structure: {'model': '...', 'created_at': '...', 'message': {'role': 'assistant', 'content': '...'}, ...}
    message = response.get("message", {})
    text = message.get("content", "")

    if not text:
        raise HintGenerationError("Ollama API returned an empty response.")

    return text.strip()
