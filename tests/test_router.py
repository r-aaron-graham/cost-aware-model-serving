import pytest

from router import Router


def test_select_provider_no_latency():
    router = Router()
    provider = router.select_provider()
    # Without latency constraint the cheapest provider should be selected
    assert provider.cost_per_1k == min(p.cost_per_1k for p in router.providers)


def test_select_provider_with_latency():
    router = Router()
    provider = router.select_provider(desired_latency=0.5)
    # Only providers with latency <= 0.5 should be considered
    assert provider.avg_latency <= 0.5


def test_generate_returns_provider_name():
    router = Router()
    result = router.generate("hello", 5, desired_latency=None)
    assert "provider" in result
    assert "output" in result
