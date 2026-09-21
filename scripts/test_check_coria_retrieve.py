"""Tests for Coria retrieve-check helpers (geen live netwerk)."""

from __future__ import annotations

import unittest
from unittest.mock import patch
from urllib.parse import quote

from check_coria_retrieve import (
    check_play_url,
    coria_retrieve_error,
    looks_like_musicxml,
    play_urls_from_site,
    sample_urls,
)


def _play(file_url: str) -> str:
    return f"https://coria.nl/play_from_url?back=coria.nl&url={quote(file_url, safe='')}"


RAW = (
    "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/"
    "gh-pages/preview/mxl/c/357b138434ae.musicxml"
)


class LooksLikeMusicxmlTests(unittest.TestCase):
    def test_xml_declaration(self) -> None:
        self.assertTrue(looks_like_musicxml(b'  <?xml version="1.0"?><score-partwise'))

    def test_html_rejected(self) -> None:
        self.assertFalse(looks_like_musicxml(b"<!DOCTYPE html><html>"))


class CoriaRetrieveErrorTests(unittest.TestCase):
    def test_detects_message(self) -> None:
        html = b"<p>Fout: failed to retrieve file</p>"
        self.assertEqual(coria_retrieve_error(html), "failed to retrieve file")

    def test_ok_page(self) -> None:
        self.assertIsNone(coria_retrieve_error(b"<p>Kies een partij</p>"))


class SampleUrlsTests(unittest.TestCase):
    def test_spread(self) -> None:
        urls = [f"u{i}" for i in range(5)]
        self.assertEqual(sample_urls(urls, 3), ["u0", "u2", "u4"])

    def test_cap(self) -> None:
        self.assertEqual(sample_urls(["a", "b"], 5), ["a", "b"])


class CheckPlayUrlTests(unittest.TestCase):
    def test_github_io_rejected_without_fetch(self) -> None:
        href = _play(
            "https://orthodox-ronl.github.io/VSA-demo/preview/"
            "mxl/c/357b138434ae.musicxml"
        )
        err = check_play_url(href, retries=1, retry_wait=0, timeout=1)
        self.assertIsNotNone(err)
        self.assertIn("github.io", err or "")

    def test_retrieve_failure_after_file_ok(self) -> None:
        href = _play(RAW)

        def fake_fetch(url: str, timeout: float) -> tuple[int, bytes]:
            if url == RAW:
                return 200, b'<?xml version="1.0"?><score-partwise/>'
            return 200, b"<p>Fout: failed to retrieve file</p>"

        with patch("check_coria_retrieve.fetch_bytes", side_effect=fake_fetch):
            err = check_play_url(href, retries=1, retry_wait=0, timeout=1)
        self.assertIsNotNone(err)
        self.assertIn("failed to retrieve file", err or "")

    def test_ok(self) -> None:
        href = _play(RAW)

        def fake_fetch(url: str, timeout: float) -> tuple[int, bytes]:
            if url == RAW:
                return 200, b'<?xml version="1.0"?><score-partwise/>'
            return 200, b"<p>Kies een partij</p>"

        with patch("check_coria_retrieve.fetch_bytes", side_effect=fake_fetch):
            err = check_play_url(href, retries=1, retry_wait=0, timeout=1)
        self.assertIsNone(err)


class PlayUrlsFromSiteTests(unittest.TestCase):
    def test_extracts_unique(self) -> None:
        import tempfile
        from pathlib import Path

        href = _play(RAW)
        html = (
            f'<a href="{href}">Oefenen</a>'
            f'<a href="{href}">Oefenen</a>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text(html, encoding="utf-8")
            found = play_urls_from_site(Path(tmp))
        self.assertEqual(found, [href])


if __name__ == "__main__":
    unittest.main()
