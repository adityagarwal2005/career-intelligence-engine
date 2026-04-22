from __future__ import annotations

import json
from typing import Any

from openai import OpenAI


class LLMService:
    def __init__(self, api_key: str, model: str, max_retries: int = 2) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_retries = max_retries

    def generate_text(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                )
                output_text = response.choices[0].message.content.strip() if response.choices else ""
                if output_text:
                    return output_text
                raise ValueError("Empty model output")
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries:
                    continue
        raise RuntimeError(f"Text generation failed after retries: {last_error}")

    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float) -> dict[str, Any]:
        raw = self.generate_text(system_prompt, user_prompt, temperature)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            repaired = self.generate_text(
                system_prompt="You repair malformed JSON. Return only valid JSON.",
                user_prompt=f"Malformed JSON:\n{raw}",
                temperature=0.0,
            )
            try:
                return json.loads(repaired)
            except json.JSONDecodeError as second_exc:
                raise RuntimeError(
                    f"Unable to parse analysis JSON. First error: {exc}; second error: {second_exc}"
                ) from second_exc
