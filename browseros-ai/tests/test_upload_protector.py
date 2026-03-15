import unittest

from core.security.upload_protector import UploadProtector
from core.security.data_protector import SecureDataProtector


class UploadProtectorTest(unittest.TestCase):
    def test_seal_unseal_upload_roundtrip(self) -> None:
        protector = UploadProtector(data_protector=SecureDataProtector(master_key="upload-test-key"))
        content = b"hello secure upload"
        sealed = protector.seal_upload(filename="secret.pdf", content=content, content_type="application/pdf")
        recovered = protector.unseal_upload(sealed)
        self.assertEqual(recovered["filename"], "secret.pdf")
        self.assertEqual(recovered["content"], content)
        self.assertEqual(recovered["content_type"], "application/pdf")

    def test_mask_upload_metadata(self) -> None:
        protector = UploadProtector(data_protector=SecureDataProtector(master_key="upload-test-key"))
        masked = protector.mask_upload_metadata(filename="private-seed.txt", content_type="text/plain", size=22)
        self.assertIn("filename", masked)
        self.assertNotEqual(masked["filename"], "private-seed.txt")
        self.assertEqual(masked["content_type"], "text/plain")


if __name__ == "__main__":
    unittest.main()
