"""Optional asset bootstrap for 六親合体ゴッドにゃ〜ず.

The God Nyāzu runtime is Apache-2.0. The official default 0B asset is separate,
optional, and distributed under its own license.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ASSET_VERSION = "0.2.0"
ASSET_URL = (
    "https://raw.githubusercontent.com/hopeless-t/god-nyas-default-0b/"
    "main/dist/god-nyas-default-0b-v0.2.0.zip"
)
ASSET_SHA256 = "fb31b201415ffef756e97420226fa1d85ed7a58f91067e2d8e37229dff872531"


class AssetUnavailable(RuntimeError):
    """Official optional asset cannot currently be acquired."""


def default_asset_dir() -> Path:
    root = os.environ.get("GODNYAS_ASSET_DIR")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".local" / "share" / "godnyas" / "assets" / "default-0b"


def _download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "rokushin-gattai-god-nyas/0.2"})
    try:
        with urlopen(req, timeout=20) as response:
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


def _safe_extract(payload: bytes, target: Path) -> None:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for member in archive.infolist():
            out = (target / member.filename).resolve()
            if target.resolve() not in out.parents and out != target.resolve():
                raise AssetUnavailable("Default 0B asset contains an unsafe archive path.")
        archive.extractall(target)


def install_default_0b(destination: str | Path | None = None) -> Path:
    """Fetch and install the optional official 0B starter bundle."""
    dest = Path(destination).expanduser() if destination else default_asset_dir()
    payload = _download(ASSET_URL)
    _verify(payload)

    dest.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="godnyas-0b-", dir=dest.parent))
    try:
        _safe_extract(payload, stage)
        package_init = stage / "godnyas_default_0b" / "__init__.py"
        license_file = stage / "ASSET_LICENSE.txt"
        if not package_init.is_file() or not license_file.is_file():
            raise AssetUnavailable("Default 0B bundle is missing required files.")
        (stage / ".bundle.sha256").write_text(ASSET_SHA256 + "\n")
        (stage / ".bundle.version").write_text(ASSET_VERSION + "\n")
        if dest.exists():
            shutil.rmtree(dest)
        stage.replace(dest)
    except Exception:
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)
        raise
    return dest / "godnyas_default_0b" / "__init__.py"


def load_default_0b(
    memory_path: str | Path | None = None,
    *,
    auto_install: bool = True,
    asset_dir: str | Path | None = None,
) -> Any:
    """Load the optional official 0B asset, fetching/upgrading it when needed."""
    dest = Path(asset_dir).expanduser() if asset_dir else default_asset_dir()
    package_init = dest / "godnyas_default_0b" / "__init__.py"
    version_file = dest / ".bundle.version"
    installed_version = version_file.read_text().strip() if version_file.exists() else None
    if not package_init.exists() or installed_version != ASSET_VERSION:
        if not auto_install:
            raise AssetUnavailable(f"Default 0B asset v{ASSET_VERSION} is not installed.")
        package_init = install_default_0b(dest)

    package_name = "godnyas_optional_default_0b"
    for name in list(sys.modules):
        if name == package_name or name.startswith(package_name + "."):
            sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(
        package_name,
        package_init,
        submodule_search_locations=[str(package_init.parent)],
    )
    if spec is None or spec.loader is None:
        raise AssetUnavailable("Unable to load installed default 0B asset.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        for name in list(sys.modules):
            if name == package_name or name.startswith(package_name + "."):
                sys.modules.pop(name, None)
        raise
    return module.load_default_0b(memory_path=memory_path)
