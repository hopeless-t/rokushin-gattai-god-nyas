import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from godnyas import assets


def make_bundle() -> bytes:
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w") as z:
        z.writestr("ASSET_LICENSE.txt", "test")
        z.writestr("godnyas_default_0b/__init__.py", "def load_default_0b(memory_path=None): return {'ok': True}\n")
    return data.getvalue()


class AssetsTest(unittest.TestCase):
    def test_pinned_hash_is_sha256(self):
        self.assertEqual(len(assets.ASSET_SHA256), 64)
        int(assets.ASSET_SHA256, 16)

    def test_verify_accepts_digest_patch(self):
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

    def test_bundle_install_and_load(self):
        payload = make_bundle()
        old_hash = assets.ASSET_SHA256
        old_version = assets.ASSET_VERSION
        try:
            assets.ASSET_SHA256 = hashlib.sha256(payload).hexdigest()
            assets.ASSET_VERSION = "test"
            with tempfile.TemporaryDirectory() as td, patch.object(assets, "_download", return_value=payload):
                model = assets.load_default_0b(asset_dir=Path(td) / "asset")
                self.assertEqual(model, {"ok": True})
        finally:
            assets.ASSET_SHA256 = old_hash
            assets.ASSET_VERSION = old_version


if __name__ == "__main__":
    unittest.main()
