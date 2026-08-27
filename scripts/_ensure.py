"""Install/check repo deps after scripts/_ensure.cmd has verified Python 3.14."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = ROOT / ".ensure-stamp"
HUGO_VERSION = "0.160.1"
NODE_MAJOR = 22


def fail(message: str, *hints: str) -> None:
    print("ERROR: " + message)
    for hint in hints:
        print(hint)
    raise SystemExit(1)


def run(args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=False, text=True, **kwargs)


def check_hugo() -> None:
    hugo = shutil.which("hugo")
    if not hugo:
        fail(
            "hugo not found on PATH",
            "Install Hugo Extended 0.160.1 and add it to PATH.",
            "Reference folder: C:\\Git\\tools\\hugo",
        )
    proc = run([hugo, "version"], capture_output=True)
    text = (proc.stdout or "") + (proc.stderr or "")
    if HUGO_VERSION not in text:
        fail(
            f"hugo version is not {HUGO_VERSION}",
            text.strip() or "(no hugo version output)",
            f"Replace the binary with Hugo Extended {HUGO_VERSION}.",
            "Reference folder: C:\\Git\\tools\\hugo",
        )
    if "extended" not in text.lower():
        fail(
            "hugo is not the Extended build",
            text.strip(),
            f"Install Hugo Extended {HUGO_VERSION}.",
        )


def check_vsa() -> None:
    vsa = shutil.which("vsa")
    if not vsa:
        fail(
            "vsa not found on PATH",
            "Add the VSA-tooling venv Scripts folder to PATH after installing vsa-tool there.",
            "Reference: C:\\Git\\orthodox-ronl\\VSA-tooling\\.venv\\Scripts",
        )


def check_node() -> None:
    node = shutil.which("node")
    if not node:
        fail(
            "node not found on PATH",
            "Install Node.js 22 and add C:\\Program Files\\nodejs\\ to PATH.",
        )
    proc = run([node, "--version"], capture_output=True)
    text = (proc.stdout or proc.stderr or "").strip()
    if not text.startswith("v") or not text[1:].split(".", 1)[0].isdigit():
        fail("could not parse node --version", text)
    major = int(text[1:].split(".", 1)[0])
    if major != NODE_MAJOR:
        fail(
            f"node is not version {NODE_MAJOR}.x",
            text,
            "Install Node.js 22 (CI uses node-version: \"22\").",
        )


def pip_install(args: list[str]) -> None:
    cmd = [sys.executable, "-m", "pip", "install", *args]
    proc = run(cmd)
    if proc.returncode != 0:
        fail("pip install failed: " + " ".join(args))


def module_ok(name: str) -> bool:
    proc = run(
        [sys.executable, "-c", f"import {name}"],
        capture_output=True,
    )
    return proc.returncode == 0


def stamp_payload(files: list[Path], extras: list[str]) -> str:
    h = hashlib.sha256()
    for path in files:
        h.update(path.read_bytes())
    for extra in extras:
        h.update(extra.encode("utf-8"))
    h.update(f"py{sys.version_info[:2]}".encode())
    return h.hexdigest()


def sibling_or_vendor(*relatives: str) -> Path | None:
    for rel in relatives:
        candidate = (ROOT / rel).resolve()
        if (candidate / "pyproject.toml").is_file():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--hugo", action="store_true")
    parser.add_argument("--vsa", action="store_true")
    parser.add_argument("--node", action="store_true")
    parser.add_argument("--pip-r", action="append", default=[])
    parser.add_argument("--pip-e", action="append", default=[])
    parser.add_argument("--import", dest="imports", action="append", default=[])
    parser.add_argument("--catalogus", action="store_true")
    parser.add_argument("--vsa-tool", action="store_true")
    parser.add_argument("--npm-install", action="store_true")
    args, _unknown = parser.parse_known_args()

    if args.hugo:
        check_hugo()
    if args.vsa:
        check_vsa()
    if args.node:
        check_node()
    if args.npm_install:
        if shutil.which("npm") is None:
            fail(
                "npm not found on PATH",
                "Install Node.js 22 so npm is available.",
            )
        if not (ROOT / "node_modules").is_dir():
            proc = run(["npm", "install"], cwd=ROOT)
            if proc.returncode != 0:
                fail("npm install failed")

    req_files = [ROOT / rel for rel in args.pip_r]
    for path in req_files:
        if not path.is_file():
            fail(f"requirements file not found: {path}")

    extras = list(args.pip_e)
    if args.catalogus:
        extras.append("catalogus:sibling")
    if args.vsa_tool:
        extras.append("vsa-tool:sibling")

    payload = stamp_payload(req_files, extras + args.imports)
    if STAMP.is_file() and STAMP.read_text(encoding="utf-8").strip() == payload:
        missing = [name for name in args.imports if not module_ok(name)]
        if not missing:
            return 0

    for rel in args.pip_r:
        pip_install(["-r", str(ROOT / rel)])

    for spec in args.pip_e:
        pip_install(["-e", spec])

    if args.catalogus and not module_ok("catalogus"):
        bron = sibling_or_vendor(os.path.join("..", "bron"), os.path.join("vendor", "bron"))
        if bron is None:
            fail(
                "catalogus is not installed and bron was not found",
                "Expected ..\\bron or vendor\\bron with pyproject.toml",
                "Clone https://github.com/orthodox-ronl/bron next to this repo.",
            )
        pip_install(["-e", str(bron)])

    if args.vsa_tool and not module_ok("vsa"):
        tooling = sibling_or_vendor(
            os.path.join("..", "VSA-tooling"),
            os.path.join("vendor", "VSA-tooling"),
        )
        if tooling is None:
            pip_install(["vsa-tool[rendering] @ git+https://github.com/orthodox-ronl/VSA-tooling.git@main"])
        else:
            pip_install(["-e", f"{tooling}[rendering]"])

    missing = [name for name in args.imports if not module_ok(name)]
    if missing:
        fail(
            "python imports still missing: " + ", ".join(missing),
            "pip install did not provide them in this Python 3.14 interpreter.",
        )

    STAMP.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
