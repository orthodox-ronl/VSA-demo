"""Tests voor twee-balks G/F-sleutelbeleid."""
from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from staff_clefs import (
    ensure_two_staff_clefs_musicxml,
    ensure_two_staff_header_clefs_mscx,
    count_nonempty_score_staves_mscx,
)


def _musicxml_two_staff(*, lower_sign: str = "G", lower_line: str = "2") -> ET.Element:
    root = ET.Element("score-partwise", version="3.1")
    part = ET.SubElement(root, "part", id="P1")
    measure = ET.SubElement(part, "measure", number="1")
    attrs = ET.SubElement(measure, "attributes")
    ET.SubElement(attrs, "staves").text = "2"
    c1 = ET.SubElement(attrs, "clef", number="1")
    ET.SubElement(c1, "sign").text = "G"
    ET.SubElement(c1, "line").text = "2"
    c2 = ET.SubElement(attrs, "clef", number="2")
    ET.SubElement(c2, "sign").text = lower_sign
    ET.SubElement(c2, "line").text = lower_line
    # Mid-score C2 on staff 1
    m2 = ET.SubElement(part, "measure", number="2")
    a2 = ET.SubElement(m2, "attributes")
    c_mid = ET.SubElement(a2, "clef", number="1")
    ET.SubElement(c_mid, "sign").text = "C"
    ET.SubElement(c_mid, "line").text = "2"
    return root


def _mscx_two_staff(*, staff2_clef: str | None = None) -> str:
    def clef(t: str) -> str:
        return (
            f"<Clef><concertClefType>{t}</concertClefType>"
            f"<transposingClefType>{t}</transposingClefType>"
            f"<isHeader>1</isHeader><eid>x</eid></Clef>"
        )

    s2_inner = ""
    if staff2_clef is not None:
        s2_inner = clef(staff2_clef)
    return (
        '<?xml version="1.0"?><museScore version="4.70"><Score>'
        '<Part id="1"><Staff/><Staff/></Part>'
        '<Staff id="1"><Measure><voice>'
        f"{clef('G')}"
        "<Chord><durationType>quarter</durationType>"
        "<Note><pitch>60</pitch><tpc>14</tpc></Note></Chord>"
        "</voice></Measure></Staff>"
        f'<Staff id="2"><Measure><voice>{s2_inner}'
        "<Chord><durationType>quarter</durationType>"
        "<Note><pitch>48</pitch><tpc>14</tpc></Note></Chord>"
        "</voice></Measure></Staff>"
        "</Score></museScore>"
    )


class MusicXmlClefTests(unittest.TestCase):
    def test_adds_f_and_rewrites_mid_score_c(self) -> None:
        root = _musicxml_two_staff(lower_sign="G", lower_line="2")
        notes = ensure_two_staff_clefs_musicxml(root)
        self.assertTrue(notes)
        part = root.find("part")
        assert part is not None
        measures = list(part.findall("measure"))
        attrs0 = measures[0].find("attributes")
        assert attrs0 is not None
        clefs = attrs0.findall("clef")
        by_num = {c.get("number"): c for c in clefs}
        self.assertEqual(by_num["1"].findtext("sign"), "G")
        self.assertEqual(by_num["2"].findtext("sign"), "F")
        self.assertEqual(by_num["2"].findtext("line"), "4")
        mid = measures[1].find("attributes").find("clef")
        self.assertEqual(mid.findtext("sign"), "G")
        self.assertEqual(mid.findtext("line"), "2")

    def test_two_parts_g8vb_to_f(self) -> None:
        root = ET.Element("score-partwise")
        for i, (sign, line, octv) in enumerate(
            (("G", "2", None), ("G", "2", "-1")), start=1
        ):
            part = ET.SubElement(root, "part", id=f"P{i}")
            meas = ET.SubElement(part, "measure", number="1")
            attrs = ET.SubElement(meas, "attributes")
            cl = ET.SubElement(attrs, "clef")
            ET.SubElement(cl, "sign").text = sign
            ET.SubElement(cl, "line").text = line
            if octv is not None:
                ET.SubElement(cl, "clef-octave-change").text = octv
        notes = ensure_two_staff_clefs_musicxml(root)
        self.assertTrue(notes)
        p2 = root.findall("part")[1]
        cl = p2.find("measure").find("attributes").find("clef")
        self.assertEqual(cl.findtext("sign"), "F")
        self.assertEqual(cl.findtext("line"), "4")
        self.assertIsNone(cl.find("clef-octave-change"))


class MscxClefTests(unittest.TestCase):
    def test_count_nonempty(self) -> None:
        self.assertEqual(count_nonempty_score_staves_mscx(_mscx_two_staff(staff2_clef="G")), 2)

    def test_insert_missing_f(self) -> None:
        mscx = _mscx_two_staff(staff2_clef=None)
        out, notes = ensure_two_staff_header_clefs_mscx(mscx)
        self.assertTrue(any("ontbrekende F" in n for n in notes))
        # Staff 2 first clef should be F
        staff2 = out.split('<Staff id="2">', 1)[1]
        self.assertIn("<concertClefType>F</concertClefType>", staff2.split("</Staff>", 1)[0])

    def test_rewrite_g8vb_and_c2(self) -> None:
        mscx = _mscx_two_staff(staff2_clef="G8vb")
        # Inject mid-score C2 on staff 1
        mscx = mscx.replace(
            "</voice></Measure></Staff>",
            '<Clef><concertClefType>C2</concertClefType>'
            "<transposingClefType>C2</transposingClefType>"
            "<eid>y</eid></Clef></voice></Measure></Staff>",
            1,
        )
        out, notes = ensure_two_staff_header_clefs_mscx(mscx)
        self.assertTrue(notes)
        staff1 = out.split('<Staff id="1">', 1)[1].split("</Staff>", 1)[0]
        staff2 = out.split('<Staff id="2">', 1)[1].split("</Staff>", 1)[0]
        self.assertNotIn("C2", staff1)
        self.assertNotIn("G8vb", staff2)
        self.assertEqual(staff1.count("<concertClefType>G</concertClefType>"), 2)
        self.assertIn("<concertClefType>F</concertClefType>", staff2)

    def test_skips_one_staff(self) -> None:
        mscx = (
            '<Staff id="1"><Measure><voice><Chord><Note><pitch>60</pitch>'
            "</Note></Chord></voice></Measure></Staff>"
        )
        out, notes = ensure_two_staff_header_clefs_mscx(mscx)
        self.assertEqual(out, mscx)
        self.assertEqual(notes, [])


class HemelumIntegrationTests(unittest.TestCase):
    """Echte bibliotheek-hub: twee balken met G/F na normalisatie."""

    HUB = (
        Path(__file__).resolve().parents[1]
        / "content-source/praktijk/oefenhoek/bibliotheek"
        / "4-tweede-antifoon/zondag/hemelum"
        / "4-tweede-antifoon-zondag-hemelum.mscz"
    )

    def test_hemelum_has_f_on_staff2(self) -> None:
        if not self.HUB.is_file():
            self.skipTest("hub ontbreekt")
        with zipfile.ZipFile(self.HUB) as z:
            name = next(n for n in z.namelist() if n.endswith(".mscx"))
            mscx = z.read(name).decode("utf-8")
        staff2 = mscx.split('<Staff id="2">', 1)[1].split("</Staff>", 1)[0]
        self.assertIn("<concertClefType>F</concertClefType>", staff2)
        # Idempotent: opnieuw aanroepen verandert niets wezenlijks
        out, notes = ensure_two_staff_header_clefs_mscx(mscx)
        self.assertIn("<concertClefType>F</concertClefType>", out)
        staff2_out = out.split('<Staff id="2">', 1)[1].split("</Staff>", 1)[0]
        self.assertIn("<concertClefType>F</concertClefType>", staff2_out)


if __name__ == "__main__":
    unittest.main()
