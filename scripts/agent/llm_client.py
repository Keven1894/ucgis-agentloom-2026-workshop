"""Provider-portable LLM client.

Uses the OpenAI Python SDK's OpenAI-compatible chat completions interface.
Configurable via:
  - api_key   (defaults to OPENAI_API_KEY)
  - base_url  (defaults to None = openai.com; set to OpenRouter / Azure /
               local vLLM endpoint to swap providers without code change)
  - model     (any string the chosen endpoint accepts)

Deliberately no provider-locked features: no response_format=json_schema,
no Assistants API, no function calling. Output discipline lives entirely
in the prompt + tolerant parser. This is what allows us to compare frontier
models (gpt-5.2 / opus-4.7) against smaller models (gpt-4o / llama-3-70b)
on identical inputs for the SoftwareX comparison table.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class LLMResponse:
    model: str
    base_url: str
    elapsed_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    raw_text: str
    finish_reason: str | None


class LLMClient:
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,
        env_path: Path | None = None,
    ) -> None:
        if env_path is not None:
            _load_env_file(env_path)
        self.model = model
        resolved_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not resolved_key:
            raise RuntimeError(
                "No API key. Pass api_key= or set OPENAI_API_KEY in env / .env"
            )
        self._key = resolved_key
        self._base_url = base_url
        try:
            from openai import OpenAI  # noqa: PLC0415  - lazy import keeps tests fast
        except ImportError as e:
            raise RuntimeError(
                "openai package not installed; run `pip install openai`"
            ) from e
        kwargs: dict[str, Any] = {"api_key": self._key}
        if base_url:
            kwargs["base_url"] = base_url
        self._client = OpenAI(**kwargs)

    @property
    def base_url(self) -> str:
        return self._base_url or "https://api.openai.com/v1"

    def complete(self, system: str, user: str, *, temperature: float = 0.2,
                 max_tokens: int | None = None) -> LLMResponse:
        t0 = time.monotonic()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        # Note: we deliberately do NOT pass response_format=json_schema here.
        # That's an OpenAI-specific feature; using it would lock us out of
        # OpenRouter / vLLM / Azure. JSON discipline is enforced in proposal_io
        # via tolerant parsing.
        resp = self._client.chat.completions.create(**kwargs)
        elapsed = time.monotonic() - t0

        choice = resp.choices[0] if resp.choices else None
        text = (choice.message.content if choice and choice.message else "") or ""
        finish = choice.finish_reason if choice else None
        usage = getattr(resp, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
        completion_tokens = getattr(usage, "completion_tokens", None) if usage else None

        return LLMResponse(
            model=self.model,
            base_url=self.base_url,
            elapsed_seconds=elapsed,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            raw_text=text,
            finish_reason=finish,
        )


def _load_env_file(env_path: Path) -> None:
    """Tiny .env loader (no python-dotenv dep). Only sets keys that aren't
    already set in os.environ — never overrides explicit env."""
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
