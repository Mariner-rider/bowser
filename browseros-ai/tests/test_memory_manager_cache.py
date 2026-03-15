import unittest

from memory.core.memory_manager import MemoryManager


class _CountingEmbeddingService:
    def __init__(self) -> None:
        self.calls = 0

    def embed(self, text: str):
        self.calls += 1
        return [float(len(text))]


class MemoryManagerCacheTest(unittest.TestCase):
    def test_embedding_cache_reuses_same_query_embedding(self) -> None:
        manager = MemoryManager()
        manager.embedding_service = _CountingEmbeddingService()  # type: ignore[assignment]

        manager.store_memory("ns", "k1", "hello world")
        manager.search_memory("ns", "hello world")
        manager.search_memory("ns", "hello world")

        self.assertEqual(manager.embedding_service.calls, 1)


if __name__ == "__main__":
    unittest.main()
