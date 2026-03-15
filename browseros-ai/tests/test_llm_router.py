import unittest

from llm.base_provider import BaseProvider
from llm.llm_router import LLMRouter, RoutePolicy, SupportedTask


class DummyProvider(BaseProvider):
    def __init__(self, name: str, should_fail: bool = False) -> None:
        self.name = name
        self.should_fail = should_fail

    def generate(self, prompt: str, **kwargs):
        if self.should_fail:
            raise RuntimeError("provider failure")
        return f"{self.name}:{prompt}"

    def stream(self, prompt: str, **kwargs):
        if self.should_fail:
            raise RuntimeError("provider failure")
        yield f"{self.name}:{prompt}"

    def embed(self, text: str, **kwargs):
        return [1.0, 2.0]


class LLMRouterTest(unittest.TestCase):
    def test_router_fallback_and_deduplicated_chain(self) -> None:
        router = LLMRouter(
            providers={
                "p1": DummyProvider("p1", should_fail=True),
                "p2": DummyProvider("p2"),
            },
            task_routes={
                SupportedTask.RESEARCH: RoutePolicy(primary_provider="p1", fallback_providers=["p1", "p2"])
            },
            default_route=RoutePolicy(primary_provider="p2"),
        )
        output = router.generate(SupportedTask.RESEARCH, "hello")
        self.assertEqual(output, "p2:hello")


if __name__ == "__main__":
    unittest.main()
