"""Provider implementations for cost‑aware model serving.

This module defines a base provider class and two simple example
providers.  Each provider implements a `generate` method returning
text.  In a real system these classes would invoke external APIs
such as OpenAI, Anthropic, or local models.
"""

from __future__ import annotations

from typing import Any, Dict


class BaseProvider:
    """Abstract base class for model providers."""

    # Cost per thousand tokens in USD
    cost_per_1k: float = 0.0
    # Average latency in seconds
    avg_latency: float = 0.0

    def generate(self, prompt: str, max_tokens: int = 128) -> str:
        raise NotImplementedError


class EchoProvider(BaseProvider):
    """A trivial provider that echoes the prompt."""

    cost_per_1k = 0.0
    avg_latency = 0.1

    def generate(self, prompt: str, max_tokens: int = 128) -> str:
        return prompt[:max_tokens]


class CheapProvider(BaseProvider):
    """Simulates a low‑cost, high‑latency provider."""

    cost_per_1k = 0.5
    avg_latency = 1.5

    def generate(self, prompt: str, max_tokens: int = 128) -> str:
        # Return reversed prompt to differentiate output
        return prompt[::-1][:max_tokens]


class FastProvider(BaseProvider):
    """Simulates a high‑cost, low‑latency provider."""

    cost_per_1k = 2.0
    avg_latency = 0.2

    def generate(self, prompt: str, max_tokens: int = 128) -> str:
        # Return uppercase prompt as dummy output
        return prompt.upper()[:max_tokens]