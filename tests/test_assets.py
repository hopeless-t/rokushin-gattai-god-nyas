import hashlib
import unittest

from godnyas import assets


class AssetsTest(unittest.TestCase):
    def test_pinned_hash_is_sha256(self):
        self.assertEqual(len(assets.ASSET_SHA256), 64)
        int(assets.ASSET_SHA256, 16)

    def test_verify_accepts_pinned_payload_shape_via_digest_patch(self):
        original = assets.ASSET_SHA256
        try:
            payload = b"nya"
            assets.ASSET_SHA256 = hashlib.sha256(payload).hexdigest()
            assets._verify(payload)
        finally:
            assets.ASSET_SHA256 = original

    def test_verify_rejects_wrong_payload(self):
        with self.assertRaises(assets.AssetUnavailable):
            assets._verify(b"not-the-official-asset")


if __name__ == "__main__":
    unittest.main()
