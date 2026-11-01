"""Optional asset bootstrap for 六親合体ゴッドにゃ〜ず.

The God Nyāzu runtime is Apache-2.0. The official default 0B asset is separate,
optional, and distributed under its own license.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ASSET_URL = (
    "https://raw.githubusercontent.com/hopeless-t/god-nyas-default-0b/"
    "main/godnyas_default_0b/model.py"
)
ASSET_LICENSE_URL = (
    "https://raw.githubusercontent.com/hopeless-t/god-nyas-default-0b/"
    "main/ASSET_LICENSE.txt"
)
ASSET_SHA256 = "985f13236606d0985a361d608017833ea1dd74b5495a3604024016783c8b1a00"


class AssetUnavailable(RuntimeError):
    """Official optional asset cannot currently be acquired."""


def default_asset_dir() -> Path:
    root = os.environ.get("GODNYAS_ASSET_DIR")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".local" / "share" / "godnyas" / "assets" / "default-0b"


def _download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "rokushin-gattai-god-nyas/0.1"})
    try:
        with urlopen(req, timeout=15) as response:
            return response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        raise AssetUnavailable(
            "Official default 0B asset is not currently available. "
            "God Nyāzu itself still works: provide your own model/part instead."
        ) from exc


def _verify(payload: bytes) -> None:
    actual = hashlib.sha256(payload).hexdigest()
    if actual != ASSET_SHA256:
        raise AssetUnavailable(
            f"Default 0B asset hash mismatch: expected {ASSET_SHA256}, got {actual}"
        )


def install_default_0b(destination: str | Path | None = None) -> Path:
    """Fetch the optional official starter asset and its separate license."""
    dest = Path(destination).expanduser() if destination else default_asset_dir()
    dest.mkdir(parents=True, exist_ok=True)

    payload = _download(ASSET_URL)
    _verify(payload)
    license_payload = _download(ASSET_LICENSE_URL)

    with tempfile.NamedTemporaryFile(dir=dest, delete=False) as tmp:
        tmp.write(payload)
        tmp_path = Path(tmp.name)
    tmp_path.replace(dest / "model.py")
    (dest / "ASSET_LICENSE.txt").write_bytes(license_payload)
    return dest / "model.py"


def load_default_0b(
    memory_path: str | Path | None = None,
    *,
    auto_install: bool = True,
    asset_dir: str | Path | None = None,
) -> Any:
    """Load the optional official 0B asset, fetching it once when requested."""
    dest = Path(asset_dir).expanduser() if asset_dir else default_asset_dir()
    model_path = dest / "model.py"
    if not model_path.exists():
        if not auto_install:
            raise AssetUnavailable("Default 0B asset is not installed.")
        model_path = install_default_0b(dest)

    payload = model_path.read_bytes()
    _verify(payload)
    spec = importlib.util.spec_from_file_location("godnyas_optional_default_0b", model_path)
    if spec is None or spec.loader is None:
        raise AssetUnavailable("Unable to load installed default 0B asset.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return module.load_default_0b(memory_path=memory_path)
