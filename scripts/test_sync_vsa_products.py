"""Tests voor sync_vsa_products (collect + playback syllabify)."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from score_filenames import is_bibliotheek_vsa_source
from sync_vsa_products import collect_vsa, playback_vsa_for_export


class TestBibliotheekVsaSource(unittest.TestCase):
    def test_sidecar_not_canonical(self) -> None:
        self.assertTrue(is_bibliotheek_vsa_source(Path("a.vsa")))
        self.assertFalse(is_bibliotheek_vsa_source(Path("a.syl.vsa")))


class TestCollectVsa(unittest.TestCase):
    def test_skips_syl_sidecar(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="vsa-collect-test-"))
        try:
            leaf = root / "leaf"
            leaf.mkdir(parents=True)
            (leaf / "index.md").write_text("---\n---\n", encoding="utf-8")
            (leaf / "stem.vsa").write_text("---\ndo: C4\n---\nwoord\n", encoding="utf-8")
            (leaf / "stem.syl.vsa").write_text("---\ndo: C4\n---\nwo-ord\n", encoding="utf-8")
            found = collect_vsa(root)
            names = {p.name for p in found}
            self.assertEqual(names, {"stem.vsa"})
        finally:
            shutil.rmtree(root, ignore_errors=True)


class TestPlaybackVsaForExport(unittest.TestCase):
    def test_unchanged_uses_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vsa = Path(tmp) / "x.vsa"
            # Al volledig gesyllabificeerd, inclusief brugstreepje voor de
            # scope; Pyphen mag hier niets meer wijzigen.
            vsa.write_text(
                "---\ndo: C4\nmode: major\n---\nmar-te-{la_}\n", encoding="utf-8"
            )
            playback = playback_vsa_for_export(vsa)
            self.assertEqual(playback.path, vsa)
            self.assertIsNone(playback._temp)
            playback.cleanup()

    def test_hyphenates_to_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vsa = Path(tmp) / "x.vsa"
            vsa.write_text("---\ndo: C4\nmode: major\n---\nlijden\n", encoding="utf-8")
            playback = playback_vsa_for_export(vsa)
            try:
                self.assertNotEqual(playback.path, vsa)
                text = playback.path.read_text(encoding="utf-8")
                self.assertIn("lij-den", text)
            finally:
                playback.cleanup()
            self.assertFalse(playback.path.is_file())


if __name__ == "__main__":
    unittest.main()
