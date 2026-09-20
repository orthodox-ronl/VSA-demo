"""Tests for GitHub Pages public-base mapping used in Coria URLs."""

from __future__ import annotations

import unittest

from fingerprint_coria_mxl import github_pages_base_url


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


if __name__ == "__main__":
    unittest.main()
