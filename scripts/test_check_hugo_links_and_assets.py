"""Tests for Coria play_from_url checks in check_hugo_links_and_assets."""

from __future__ import annotations

import unittest
from urllib.parse import quote

from check_hugo_links_and_assets import coria_target_path


def _play(file_url: str) -> str:
    return f"https://coria.nl/play_from_url?back=coria.nl&url={quote(file_url, safe='')}"


RAW_PREVIEW = (
    "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/"
    "gh-pages/preview"
)
RAW_ROOT = "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages"


class CoriaTargetPathTests(unittest.TestCase):
    def test_raw_fingerprint_ok(self) -> None:
        href = _play(f"{RAW_PREVIEW}/mxl/c/04affef0fef2.musicxml")
        path, err = coria_target_path(href, "/VSA-demo/feat-oefenhoek-mxl-opkuis")
        self.assertIsNone(err)
        self.assertEqual(path, "/mxl/c/04affef0fef2.musicxml")

    def test_production_fingerprint_ok_without_url_prefix(self) -> None:
        href = _play(f"{RAW_ROOT}/mxl/c/5fde29f59d4e.musicxml")
        path, err = coria_target_path(href, "")
        self.assertIsNone(err)
        self.assertEqual(path, "/mxl/c/5fde29f59d4e.musicxml")

    def test_github_io_rejected(self) -> None:
        href = _play(
            "https://orthodox-ronl.github.io/VSA-demo/preview/"
            "mxl/c/357b138434ae.musicxml"
        )
        path, err = coria_target_path(href, "/VSA-demo/preview")
        self.assertIsNone(path)
        self.assertIsNotNone(err)
        self.assertIn("github.io", err or "")

    def test_relative_path_rejected(self) -> None:
        href = _play("/mxl/c/04affef0fef2.musicxml")
        path, err = coria_target_path(href, "")
        self.assertIsNone(path)
        self.assertIsNotNone(err)
        self.assertIn("geen absolute http(s)-URL", err or "")

    def test_localhost_rejected(self) -> None:
        href = _play("http://127.0.0.1:18731/mxl/c/04affef0fef2.musicxml")
        path, err = coria_target_path(href, "")
        self.assertIsNone(path)
        self.assertIsNotNone(err)
        self.assertIn("localhost", err or "")

    def test_doubled_prefix_rejected(self) -> None:
        href = _play(
            "https://example.test/VSA-demo/preview/"
            "VSA-demo/preview/mxl/c/5fde29f59d4e.musicxml"
        )
        path, err = coria_target_path(href, "/VSA-demo/preview")
        self.assertIsNone(path)
        self.assertIsNotNone(err)
        self.assertIn("dubbele URL-prefix", err or "")

    def test_doubled_prefix_without_url_prefix_arg(self) -> None:
        href = _play(
            "https://example.test/VSA-demo/preview/"
            "VSA-demo/preview/mxl/c/5fde29f59d4e.musicxml"
        )
        path, err = coria_target_path(href, "")
        self.assertIsNone(path)
        self.assertIsNotNone(err)
        self.assertIn("dubbele URL-prefix", err or "")

    def test_page_bundle_mxl_rejected(self) -> None:
        href = _play(f"{RAW_PREVIEW}/praktijk/oefenhoek/bibliotheek/x.mxl")
        path, err = coria_target_path(href, "/VSA-demo/preview")
        self.assertIsNone(path)
        self.assertIsNotNone(err)
        self.assertIn("geen fingerprint-pad", err or "")

    def test_missing_url_param(self) -> None:
        path, err = coria_target_path("https://coria.nl/play_from_url", "")
        self.assertIsNone(path)
        self.assertEqual(err, "play_from_url zonder url=")


if __name__ == "__main__":
    unittest.main()
