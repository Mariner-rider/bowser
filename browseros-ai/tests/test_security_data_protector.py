import unittest

from core.security.data_protector import SecureDataProtector


class SecureDataProtectorTest(unittest.TestCase):
    def test_seal_and_unseal_roundtrip(self) -> None:
        protector = SecureDataProtector(master_key="unit-test-key")
        payload = {"user": "alice", "token": "abcd1234", "nested": {"password": "secret-pass"}}
        sealed = protector.seal(payload)
        unsealed = protector.unseal(sealed)
        self.assertEqual(unsealed, payload)

    def test_mask_payload_masks_sensitive_values(self) -> None:
        protector = SecureDataProtector(master_key="unit-test-key")
        masked = protector.mask_payload({"token": "abcd1234", "safe": "ok", "nested": {"password": "secret"}})
        self.assertNotEqual(masked["token"], "abcd1234")
        self.assertEqual(masked["safe"], "ok")
        self.assertNotEqual(masked["nested"]["password"], "secret")


if __name__ == "__main__":
    unittest.main()
