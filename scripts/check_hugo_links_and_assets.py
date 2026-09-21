"""Controleer interne href/src in de gebouwde Hugo-site.

Spiegel van VSA-tooling/scripts/check-hugo-links-and-assets.py,
met configureerbare site-root en optionele URL-prefix (GitHub Pages).

Coria play_from_url-links: controleer dat de url=-parameter een absolute
http(s)-URL is (geen localhost, geen github.io, geen pad-only) naar een
bestaand /mxl/c/*.musicxml op de site (geen dubbele baseURL-path).
github.io is de site voor mensen; Coria haalt MusicXML op vanaf
raw.githubusercontent.com (gh-pages).
"""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import NamedTuple
from urllib.parse import parse_qs, unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "generated" / "site"


class LinkRef(NamedTuple):
    html: Path
    attr: str
    value: str
    tag: str


class LinkParser(HTMLParser):
    def __init__(self, html: Path):
        super().__init__(convert_charrefs=True)
        self.html = html
        self.refs: list[LinkRef] = []

    def handle_starttag(self, tag: str, attrs):
        data = dict(attrs)
        for attr in ("href", "src"):
            value = data.get(attr)
            if value:
                self.refs.append(LinkRef(self.html, attr, value, tag))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Controleer interne links en assets in Hugo-output.",
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=DEFAULT_SITE_DIR,
        help="Gebouwde site-root (default: generated/site).",
    )
    parser.add_argument(
        "--url-prefix",
        default="",
        help="Strip deze prefix van absolute paden (bijv. /VSA-demo of /VSA-demo/preview).",
    )
    parser.add_argument(
        "--forbidden-prefix",
        action="append",
        default=[],
        metavar="PATH",
        help="Pad-prefix die als fout telt (herhaalbaar). Standaard: geen.",
    )
    return parser.parse_args()


def normalize_url_prefix(prefix: str) -> str:
    prefix = prefix.strip()
    if not prefix:
        return ""
    parsed = urlparse(prefix)
    if parsed.scheme:
        prefix = parsed.path or "/"
    if not prefix.startswith("/"):
        prefix = "/" + prefix
    return prefix.rstrip("/")


def strip_fragment_query(value: str) -> str:
    return value.split("#", 1)[0].split("?", 1)[0]


def should_skip(value: str) -> bool:
    value = value.strip()
    clean = strip_fragment_query(value)
    return (
        not value
        or value.startswith("#")
        or value.startswith("http://")
        or value.startswith("https://")
        or value.startswith("mailto:")
        or value.startswith("tel:")
        or value.startswith("data:")
        or value.startswith("javascript:")
        or clean == "/livereload.js"
    )


def is_coria_play_url(value: str) -> bool:
    try:
        parsed = urlparse(value.strip())
    except ValueError:
        return False
    host = (parsed.netloc or "").lower()
    return host.endswith("coria.nl") and "play_from_url" in (parsed.path or "")


def _is_localhost_host(host: str) -> bool:
    host = host.lower()
    return (
        host in {"localhost", "127.0.0.1"}
        or host.startswith("localhost:")
        or host.startswith("127.0.0.1:")
    )


def _doubled_path_prefix(prefix: str) -> bool:
    """True if /a/b/a/b (even number of segments, first half == second half)."""
    parts = [p for p in prefix.split("/") if p]
    n = len(parts)
    if n < 2 or n % 2:
        return False
    half = n // 2
    return parts[:half] == parts[half:]


def coria_target_path(value: str, url_prefix: str) -> tuple[str | None, str | None]:
    """Return (site-relative /mxl/c/… path, error). Path starts with /."""
    parsed = urlparse(value.strip())
    qs = parse_qs(parsed.query)
    targets = qs.get("url") or []
    if not targets:
        return None, "play_from_url zonder url="
    raw = unquote(targets[0].strip())
    if not raw:
        return None, "play_from_url met lege url="
    target = urlparse(raw)
    if target.scheme not in {"http", "https"} or not target.netloc:
        return None, f"Coria-url is geen absolute http(s)-URL: {raw}"
    if _is_localhost_host(target.netloc):
        return None, f"Coria kan localhost niet ophalen: {raw}"
    host = (target.netloc or "").lower()
    if host.endswith("github.io"):
        return None, (
            "Coria haalt MusicXML niet betrouwbaar op vanaf github.io "
            "(failed to retrieve file). Oplossing: fingerprint_coria_mxl.py "
            "moet data/coria-public-base.json op "
            "raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages/ zetten."
        )
    path = target.path or ""
    if not path.startswith("/"):
        path = "/" + path
    lower = path.lower()
    if not lower.endswith((".musicxml", ".mxl", ".xml")):
        return None, f"Coria-url eindigt niet op .musicxml/.mxl/.xml: {path}"
    if url_prefix:
        doubled = f"{url_prefix}{url_prefix}/"
        if path == f"{url_prefix}{url_prefix}" or path.startswith(doubled):
            return None, f"dubbele URL-prefix in Coria-url: {path}"
    marker = "/mxl/c/"
    idx = path.find(marker)
    if idx < 0:
        return None, f"Coria-url is geen fingerprint-pad /mxl/c/…: {path}"
    prefix = path[:idx]
    if _doubled_path_prefix(prefix):
        return None, f"dubbele URL-prefix in Coria-url: {path}"
    fingerprint = path[idx:]
    rest = path[idx + len(marker) :]
    if not rest or "/" in rest:
        return None, f"Coria-url is geen fingerprint-pad /mxl/c/…: {path}"
    return fingerprint, None


def site_path_from_ref(ref: LinkRef, site_dir: Path, url_prefix: str) -> Path | None:
    clean = strip_fragment_query(ref.value.strip())
    if not clean:
        return None

    if clean.startswith("/"):
        path = clean
        if url_prefix and (path == url_prefix or path.startswith(url_prefix + "/")):
            path = path[len(url_prefix) :] or "/"
        return site_dir / path.lstrip("/")

    return (ref.html.parent / clean).resolve()


def resolves(ref: LinkRef, site_dir: Path, url_prefix: str) -> bool:
    candidate = site_path_from_ref(ref, site_dir, url_prefix)
    if candidate is None:
        return False

    site_resolved = site_dir.resolve()
    try:
        candidate.resolve().relative_to(site_resolved)
    except ValueError:
        return False

    if candidate.exists():
        return True

    clean = strip_fragment_query(ref.value)
    if clean.endswith("/") or candidate.suffix == "":
        return (candidate / "index.html").exists()

    return False


def is_forbidden(value: str, forbidden: list[str], url_prefix: str) -> bool:
    clean = strip_fragment_query(value.strip())
    if clean.startswith("/") and url_prefix:
        if clean == url_prefix or clean.startswith(url_prefix + "/"):
            clean = clean[len(url_prefix) :] or "/"
    for route in forbidden:
        route = route if route.startswith("/") else "/" + route
        route = route.rstrip("/") + "/"
        normalized = clean if clean.endswith("/") else clean + "/"
        if normalized == route or normalized.startswith(route):
            return True
    return False


def format_ref(ref: LinkRef, site_dir: Path) -> str:
    try:
        html = ref.html.relative_to(site_dir.resolve())
    except ValueError:
        html = ref.html
    return f'- {html}: <{ref.tag} {ref.attr}="{ref.value}">'


def suggest(value: str, site_dir: Path, url_prefix: str) -> str | None:
    clean = Path(strip_fragment_query(value)).name
    if not clean:
        return None
    matches = list(site_dir.rglob(clean))
    if not matches:
        return None
    rel = matches[0].relative_to(site_dir).as_posix()
    prefix = url_prefix.rstrip("/") if url_prefix else ""
    return f"{prefix}/{rel}"


def main() -> int:
    args = parse_args()
    site_dir = args.site_dir.resolve()
    url_prefix = normalize_url_prefix(args.url_prefix)
    forbidden = list(args.forbidden_prefix)

    if not site_dir.is_dir():
        print(f"Niet gevonden: {site_dir}", file=sys.stderr)
        print("Draai eerst scripts\\build-hugo.cmd", file=sys.stderr)
        return 2

    refs: list[LinkRef] = []
    for html in sorted(site_dir.rglob("*.html")):
        parser = LinkParser(html)
        parser.feed(html.read_text(encoding="utf-8", errors="ignore"))
        refs.extend(parser.refs)

    broken: list[LinkRef] = []
    forbidden_hits: list[LinkRef] = []
    coria_broken: list[tuple[LinkRef, str]] = []
    coria_checked = 0

    for ref in refs:
        if is_coria_play_url(ref.value):
            coria_checked += 1
            path, err = coria_target_path(ref.value, url_prefix)
            if err:
                coria_broken.append((ref, err))
                continue
            assert path is not None
            candidate = site_dir / path.lstrip("/")
            if not candidate.is_file():
                coria_broken.append((ref, f"bestand ontbreekt op site: {path}"))
            continue
        if should_skip(ref.value):
            continue
        if forbidden and is_forbidden(ref.value, forbidden, url_prefix):
            forbidden_hits.append(ref)
        elif not resolves(ref, site_dir, url_prefix):
            broken.append(ref)

    if broken or forbidden_hits or coria_broken:
        print("Hugo link/asset checker: fouten gevonden.")
        if forbidden_hits:
            print()
            print("Verboden/oude routes:")
            for ref in forbidden_hits:
                print(format_ref(ref, site_dir))
        if broken:
            print()
            print("Kapotte links/assets:")
            for ref in broken:
                print(format_ref(ref, site_dir))
                hint = suggest(ref.value, site_dir, url_prefix)
                if hint:
                    print(f"  mogelijk bedoeld: {hint}")
        if coria_broken:
            print()
            print("Coria play_from_url:")
            for ref, err in coria_broken:
                print(format_ref(ref, site_dir))
                print(f"  {err}")
        return 1

    print(
        f"Hugo link/asset checker: OK "
        f"({len(refs)} verwijzingen gecontroleerd in {site_dir}"
        f", {coria_checked} Coria-link(s))."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
