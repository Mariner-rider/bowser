import importlib.util
import pathlib
import sys
import unittest


class ModuleApiProtocolsTest(unittest.TestCase):
    def test_protocol_module_loads_and_defines_expected_interfaces(self) -> None:
        path = pathlib.Path(__file__).resolve().parents[1] / "core" / "module_api_protocols.py"
        spec = importlib.util.spec_from_file_location("module_api_protocols", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        expected_names = [
            "RequestContext",
            "AgentKernelAPI",
            "LLMRouterAPI",
            "MemoryEngineAPI",
            "AutomationEngineAPI",
            "LearningEngineAPI",
            "LocalAIEngineAPI",
            "DashboardAPI",
            "Web3LayerAPI",
            "CapacitorRuntimeAPI",
        ]

        for name in expected_names:
            self.assertTrue(hasattr(module, name), f"missing protocol: {name}")


if __name__ == "__main__":
    unittest.main()
