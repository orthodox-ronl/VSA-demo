"""Ask Coria whether it can retrieve our MusicXML (play_from_url).

Coria haalt het bestand server-side op. github.io is onbetrouwbaar
(failed to retrieve file); Oefenen gebruikt raw.githubusercontent.com
op branch gh-pages. Deze check:

1. wacht tot de MusicXML-URL HTTP 200 + XML geeft (Pages/raw-vertraging);
2. opent daarna play_from_url en faalt op 'failed to retrieve file'.

Niet in lokale check: unpublished hashes staan nog niet op gh-pages.
CI: na Pages-deploy (pages.yml). Tests: test_check_coria_retrieve.py.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, unquote, urlparse
from urllib.request import Request, urlopen

from check_hugo_links_and_assets import (
    LinkParser,
    coria_target_path,
    is_coria_play_url,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "generated" / "site"
RETRIEVE_ERROR = "failed to retrieve file"
USER_AGENT = "VSA-demo-coria-retrieve-check/1.0"


def file_url_from_play(href: str) -> str:
    parsed = urlparse(href.strip())
    targets = parse_qs(parsed.query).get("url") or []
    if not targets:
        return ""
    return unquote(targets[0].strip())


def play_urls_from_site(site_dir: Path) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for html in sorted(site_dir.rglob("*.html")):
        parser = LinkParser(html)
        parser.feed(html.read_text(encoding="utf-8", errors="ignore"))
        for ref in parser.refs:
            if not is_coria_play_url(ref.value):
                continue
            if ref.value in seen:
                continue
            seen.add(ref.value)
            out.append(ref.value)
    return out


def sample_urls(urls: list[str], max_n: int) -> list[str]:
    if max_n <= 0 or len(urls) <= max_n:
        return urls
    if max_n == 1:
        return [urls[0]]
    last = len(urls) - 1
    picks: list[int] = []
    for i in range(max_n):
        idx = 0 if max_n == 1 else round(i * last / (max_n - 1))
        if idx not in picks:
            picks.append(idx)
    return [urls[i] for i in picks]


def fetch_bytes(url: str, timeout: float) -> tuple[int, bytes]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return int(resp.status), resp.read()
    except HTTPError as exc:
        body = exc.read() if exc.fp else b""
        return int(exc.code), body


def looks_like_musicxml(body: bytes) -> bool:
    head = body.lstrip()[:200].lower()
    return b"<?xml" in head or b"<score" in head


def wait_for_musicxml(
    url: str,
    *,
    retries: int,
    retry_wait: float,
    timeout: float,
) -> str | None:
    last = "geen antwoord"
    attempts = max(1, retries)
    for attempt in range(attempts):
        try:
            status, body = fetch_bytes(url, timeout)
            if status == 200 and looks_like_musicxml(body):
                return None
            last = f"HTTP {status}, geen MusicXML"
        except URLError as exc:
            last = str(exc.reason or exc)
        except TimeoutError as exc:
            last = str(exc)
        if attempt + 1 < attempts:
            time.sleep(retry_wait)
    return last


def coria_retrieve_error(body: bytes) -> str | None:
    text = body.decode("utf-8", errors="replace")
    lowered = text.lower()
    if RETRIEVE_ERROR in lowered:
        return RETRIEVE_ERROR
    return None


def check_play_url(
    href: str,
    *,
    retries: int,
    retry_wait: float,
    timeout: float,
) -> str | None:
    path, err = coria_target_path(href, "")
    if err:
        return err
    if path is None:
        return "geen fingerprint-pad"
    file_url = file_url_from_play(href)
    if not file_url:
        return "play_from_url zonder url="
    wait_err = wait_for_musicxml(
        file_url, retries=retries, retry_wait=retry_wait, timeout=timeout
    )
    if wait_err:
        return f"MusicXML nog niet ophaalbaar ({file_url}): {wait_err}"
    try:
        status, body = fetch_bytes(href, timeout)
    except (URLError, TimeoutError) as exc:
        return f"Coria niet bereikbaar: {exc}"
    if status != 200:
        return f"Coria HTTP {status} voor {file_url}"
    retrieve = coria_retrieve_error(body)
    if retrieve:
        return f"Coria {retrieve} voor {file_url}"
    return None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Controleer of Coria play_from_url onze MusicXML ophaalt."
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=DEFAULT_SITE_DIR,
        help="Gebouwde Hugo-site (HTML met Oefenen-links)",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=5,
        metavar="N",
        help="Aantal unieke Coria-links om te proberen (default 5)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=8,
        help="Pogingen tot de MusicXML-URL HTTP 200 geeft",
    )
    parser.add_argument(
        "--retry-wait",
        type=float,
        default=15.0,
        help="Seconden tussen MusicXML-pogingen",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        help="HTTP-timeout in seconden",
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Extra play_from_url om te controleren (herhaalbaar)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    urls: list[str] = list(args.url)
    if args.site_dir.is_dir():
        urls.extend(play_urls_from_site(args.site_dir))
    elif not urls:
        print(f"Niet gevonden: {args.site_dir}", file=sys.stderr)
        print(
            "Oplossing: draai scripts\\build.cmd, of geef --url.",
            file=sys.stderr,
        )
        return 2

    # Uniek, volgorde behouden.
    seen: set[str] = set()
    unique: list[str] = []
    for href in urls:
        if href in seen:
            continue
        seen.add(href)
        unique.append(href)
    sample = sample_urls(unique, args.max)
    if not sample:
        print("Geen Coria play_from_url-links gevonden.", file=sys.stderr)
        print(
            "Oplossing: controleer of de Hugo-site Oefenen-knoppen heeft.",
            file=sys.stderr,
        )
        return 1

    errors: list[str] = []
    for href in sample:
        err = check_play_url(
            href,
            retries=args.retries,
            retry_wait=args.retry_wait,
            timeout=args.timeout,
        )
        if err:
            errors.append(err)

    if errors:
        print("Coria retrieve-check: fouten gevonden.")
        for err in errors:
            print(f"- {err}")
            print(
                "  Oplossing: Oefenen moet raw.githubusercontent.com/"
                "orthodox-ronl/VSA-demo/gh-pages/... gebruiken, niet github.io."
            )
        return 1

    print(
        f"Coria retrieve-check: OK ({len(sample)} play_from_url-link(s)).",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
