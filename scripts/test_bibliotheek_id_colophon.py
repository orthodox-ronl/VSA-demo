"""Tests voor bibliotheek-id in colofontekst."""
from __future__ import annotations

import unittest

from apply_mscz_layout import (
    _BIB_ID_LABEL,
    format_copyright_notices,
    strip_bibliotheek_id_line,
    with_bibliotheek_id_line,
)


class BibliotheekIdColophonTests(unittest.TestCase):
    def test_with_bibliotheek_id_appends_line(self) -> None:
        _short, full = format_copyright_notices("")
        out = with_bibliotheek_id_line(full, "5-eniggeboren-zoon/default/hemelum")
        self.assertIn(
            f"{_BIB_ID_LABEL} 5-eniggeboren-zoon/default/hemelum", out
        )
        self.assertTrue("eredienst" in out.lower() or "CC BY-SA" in out)

    def test_with_bibliotheek_id_idempotent(self) -> None:
        text = "Notice\nBibliotheek-id: old/id/here"
        once = with_bibliotheek_id_line(text, "a/b/c")
        twice = with_bibliotheek_id_line(once, "a/b/c")
        self.assertEqual(once, twice)
        self.assertEqual(once.count("Bibliotheek-id:"), 1)
        self.assertIn("a/b/c", once)
        self.assertNotIn("old/id/here", once)

    def test_strip_removes_line(self) -> None:
        text = "A\nBibliotheek-id: x/y/z\nB"
        cleaned = strip_bibliotheek_id_line(text)
        self.assertNotIn("Bibliotheek-id", cleaned)
        self.assertIn("A", cleaned)
        self.assertIn("B", cleaned)

    def test_empty_id_strips_only(self) -> None:
        text = "Notice\nBibliotheek-id: x/y/z"
        self.assertEqual(with_bibliotheek_id_line(text, ""), "Notice")


if __name__ == "__main__":
    unittest.main()
