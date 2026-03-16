"""HTTP server that routes requests to model providers based on cost and latency.

This module exposes a FastAPI app with a single `/generate` endpoint.  The
router selects the cheapest provider that meets the caller’s latency
requirement.  Providers are defined in `providers.py`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from providers import BaseProvider, CheapProvider, EchoProvider, FastProvider


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to send to the model.")
    max_tokens: int = Field(128, ge=1, le=2048, description="Maximum number of tokens to generate.")
    desired_latency: Optional[float] = Field(
        None, ge=0.0, description="Maximum acceptable latency in seconds.  If not provided, the cheapest provider is selected."
    )


class GenerateResponse(BaseModel):
    provider: str
    output: str


class Router:
    """Selects among providers based on cost and latency."""

    def __init__(self, providers: Optional[List[BaseProvider]] = None):
        # Register default providers if none specified
        self.providers: List[BaseProvider] = providers or [EchoProvider(), CheapProvider(), FastProvider()]

    def select_provider(self, desired_latency: Optional[float] = None) -> BaseProvider:
        # Filter providers by latency if desired
        candidates = self.providers
        if desired_latency is not None:
            candidates = [p for p in candidates if p.avg_latency <= desired_latency]
            if not candidates:
                raise ValueError("No provider meets the desired latency requirement.")
        # Choose the candidate with the lowest cost
        return min(candidates, key=lambda p: p.cost_per_1k)

    def generate(self, prompt: str, max_tokens: int, desired_latency: Optional[float] = None) -> Dict[str, Any]:
        provider = self.select_provider(desired_latency)
        output = provider.generate(prompt, max_tokens)
        return {"provider": provider.__class__.__name__, "output": output}


app = FastAPI(title="Cost‑Aware Model Router", version="0.1.0")
router = Router()


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        result = router.generate(request.prompt, request.max_tokens, request.desired_latency)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return GenerateResponse(**result)


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)