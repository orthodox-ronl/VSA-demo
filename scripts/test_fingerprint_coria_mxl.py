"""Tests for GitHub Pages site URL and Coria fetch-base mapping."""

from __future__ import annotations

import unittest

from fingerprint_coria_mxl import coria_fetch_base_url, github_pages_base_url


class GithubPagesBaseUrlTests(unittest.TestCase):
    def test_main(self) -> None:
        self.assertEqual(
            github_pages_base_url("main"),
            "https://orthodox-ronl.github.io/VSA-demo/",
        )

    def test_development(self) -> None:
        self.assertEqual(
            github_pages_base_url("development"),
            "https://orthodox-ronl.github.io/VSA-demo/preview/",
        )

    def test_feature_branch_slug(self) -> None:
        self.assertEqual(
            github_pages_base_url("feat/oefenhoek-mxl-opkuis"),
            "https://orthodox-ronl.github.io/VSA-demo/feat-oefenhoek-mxl-opkuis/",
        )

    def test_reserved_slug(self) -> None:
        self.assertEqual(
            github_pages_base_url("mxl"),
            "https://orthodox-ronl.github.io/VSA-demo/b-mxl/",
        )

    def test_empty_rejected(self) -> None:
        with self.assertRaises(ValueError):
            github_pages_base_url("")


class CoriaFetchBaseUrlTests(unittest.TestCase):
    def test_main(self) -> None:
        self.assertEqual(
            coria_fetch_base_url("main"),
            "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages/",
        )

    def test_development(self) -> None:
        self.assertEqual(
            coria_fetch_base_url("development"),
            "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages/preview/",
        )

    def test_feature_branch_slug(self) -> None:
        self.assertEqual(
            coria_fetch_base_url("feat/oefenhoek-mxl-opkuis"),
            "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/"
            "gh-pages/feat-oefenhoek-mxl-opkuis/",
        )

    def test_reserved_slug(self) -> None:
        self.assertEqual(
            coria_fetch_base_url("mxl"),
            "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages/b-mxl/",
        )


if __name__ == "__main__":
    unittest.main()
