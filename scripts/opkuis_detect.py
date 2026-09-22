"""Herkomstdetectie voor scripts/opkuisen.py (hoek + confidence).

Geen transforms — alleen fingerprints lezen.
"""
from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from cleanup_capella_mxl import findall, is_pitched, load_mxl
from score_filenames import is_print_mscz

HOEK_CAPELLA = "capella"
HOEK_MUSICXML_GENERIC = "musicxml-generic"
HOEK_MUSESCORE = "musescore"
HOEK_VSA = "vsa"
HOEK_MVSA = "mvsa"
HOEK_UNKNOWN = "unknown"

KNOWN_HOEKEN = frozenset(
    {
        HOEK_CAPELLA,
        HOEK_MUSICXML_GENERIC,
        HOEK_MUSESCORE,
        HOEK_VSA,
        HOEK_MVSA,
    }
)

MUSICXML_SUFFIXES = frozenset({".mxl", ".musicxml", ".xml"})
MUSESCORE_SUFFIXES = frozenset({".mscz", ".mscx"})
VSA_SUFFIXES = frozenset({".vsa", ".mvsa"})
SUPPORTED_SUFFIXES = MUSICXML_SUFFIXES | MUSESCORE_SUFFIXES | VSA_SUFFIXES
REFUSED_SUFFIXES = frozenset({".cap", ".capx"})

_CAPELLA_SOFT = re.compile(
    r"capto\s*music|capella", re.IGNORECASE
)
_HIDDEN_PITCHED_RATIO_CAPELLA = 0.02  # >= 2% of pitched notes hidden -> Capella-ish
_MIN_HIDDEN_FOR_CAPELLA = 3
_LOW_CONFIDENCE = 0.5


@dataclass
class DetectResult:
    path: Path
    hoek: str
    confidence: float
    signals: list[str] = field(default_factory=list)
    suggested_passes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str | None = None

    @property
    def low_confidence(self) -> bool:
        return self.confidence < _LOW_CONFIDENCE

    @property
    def ok(self) -> bool:
        return self.error is None


def _software_and_comments(root: ET.Element, raw_prefix: str = "") -> list[str]:
    texts: list[str] = []
    if raw_prefix:
        texts.append(raw_prefix[:4000])
    for el in findall(root, "software"):
        if el.text:
            texts.append(el.text)
    for el in findall(root, "encoding-description"):
        if el.text:
            texts.append(el.text)
    return texts


def _hidden_pitched_stats(root: ET.Element) -> tuple[int, int]:
    pitched = 0
    hidden = 0
    for note in findall(root, "note"):
        if not is_pitched(note):
            continue
        pitched += 1
        if note.get("print-object") == "no":
            hidden += 1
    return hidden, pitched


def _passes_for(hoek: str) -> list[str]:
    if hoek == HOEK_CAPELLA:
        return ["capella-musicxml"]
    if hoek == HOEK_MUSICXML_GENERIC:
        return ["generic-musicxml"]
    if hoek == HOEK_MUSESCORE:
        return ["musescore-content"]
    if hoek == HOEK_VSA:
        return ["vsa-analyze-only"]
    if hoek == HOEK_MVSA:
        return ["mvsa-reserved"]
    return []


def detect_musicxml_tree(
    root: ET.Element,
    path: Path,
    *,
    raw_head: str = "",
) -> DetectResult:
    signals: list[str] = []
    warnings: list[str] = []
    texts = _software_and_comments(root, raw_head)
    joined = "\n".join(texts)
    hidden, pitched = _hidden_pitched_stats(root)

    path_hint_capella = "capella" in [p.lower() for p in path.parts]

    if _CAPELLA_SOFT.search(joined):
        signals.append("encoding/software of comment noemt Capella/CapToMusic")
        conf = 0.95
        if path_hint_capella:
            signals.append("pad bevat mapnaam capella (zwakke prior)")
        return DetectResult(
            path=path,
            hoek=HOEK_CAPELLA,
            confidence=conf,
            signals=signals,
            suggested_passes=_passes_for(HOEK_CAPELLA),
            warnings=warnings,
        )

    if pitched > 0 and hidden >= _MIN_HIDDEN_FOR_CAPELLA:
        ratio = hidden / pitched
        if ratio >= _HIDDEN_PITCHED_RATIO_CAPELLA:
            signals.append(
                f"verborgen klinkende noten (print-object=no): {hidden}/{pitched}"
            )
            conf = 0.8 if ratio >= 0.05 else 0.65
            if path_hint_capella:
                signals.append("pad bevat mapnaam capella (zwakke prior)")
                conf = min(0.9, conf + 0.1)
            return DetectResult(
                path=path,
                hoek=HOEK_CAPELLA,
                confidence=conf,
                signals=signals,
                suggested_passes=_passes_for(HOEK_CAPELLA),
                warnings=warnings,
            )

    if path_hint_capella:
        signals.append("pad bevat mapnaam capella maar geen sterke Capella-signalen")
        warnings.append(
            "lage confidence: gebruik --assume capella of --assume musicxml-generic"
        )
        return DetectResult(
            path=path,
            hoek=HOEK_UNKNOWN,
            confidence=0.35,
            signals=signals,
            suggested_passes=[],
            warnings=warnings,
        )

    signals.append("MusicXML zonder Capella/CapToMusic-signalen")
    return DetectResult(
        path=path,
        hoek=HOEK_MUSICXML_GENERIC,
        confidence=0.6,
        signals=signals,
        suggested_passes=_passes_for(HOEK_MUSICXML_GENERIC),
        warnings=warnings,
    )


def _load_musicxml_root(path: Path) -> tuple[ET.Element, str]:
    suf = path.suffix.lower()
    if suf == ".mxl":
        root, _name, _extras = load_mxl(path)
        return root, ""
    text = path.read_text(encoding="utf-8", errors="replace")
    root = ET.fromstring(text)
    return root, text[:2000]


def detect_mscz(path: Path) -> DetectResult:
    signals: list[str] = ["extensie .mscz (MuseScore-archief)"]
    try:
        with zipfile.ZipFile(path, "r") as z:
            names = z.namelist()
            mscx = [n for n in names if n.lower().endswith(".mscx")]
            if not mscx:
                return DetectResult(
                    path=path,
                    hoek=HOEK_UNKNOWN,
                    confidence=0.0,
                    signals=signals,
                    error=f"geen .mscx in archief: {path}",
                )
            head = z.read(mscx[0])[:800].decode("utf-8", errors="replace")
            if "museScore" in head or "MuseScore" in head:
                signals.append("MSCX bevat museScore-root")
    except zipfile.BadZipFile as e:
        return DetectResult(
            path=path,
            hoek=HOEK_UNKNOWN,
            confidence=0.0,
            signals=signals,
            error=f"ongeldige .mscz (geen zip): {path}: {e}",
        )
    return DetectResult(
        path=path,
        hoek=HOEK_MUSESCORE,
        confidence=0.95,
        signals=signals,
        suggested_passes=_passes_for(HOEK_MUSESCORE),
    )


def detect_mscx(path: Path) -> DetectResult:
    signals = ["extensie .mscx (MuseScore XML)"]
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:800]
    except OSError as e:
        return DetectResult(
            path=path,
            hoek=HOEK_UNKNOWN,
            confidence=0.0,
            error=f"kan .mscx niet lezen: {path}: {e}",
        )
    if "museScore" not in head and "MuseScore" not in head:
        signals.append("geen museScore-root in kop (toch als MuseScore behandeld)")
        return DetectResult(
            path=path,
            hoek=HOEK_MUSESCORE,
            confidence=0.55,
            signals=signals,
            suggested_passes=_passes_for(HOEK_MUSESCORE),
            warnings=["twijfelachtige .mscx; gebruik --assume musescore indien bedoeld"],
        )
    signals.append("MSCX bevat museScore-root")
    return DetectResult(
        path=path,
        hoek=HOEK_MUSESCORE,
        confidence=0.95,
        signals=signals,
        suggested_passes=_passes_for(HOEK_MUSESCORE),
    )


def detect_path(path: Path, *, assume: str | None = None) -> DetectResult:
    """Detecteer hoek voor een bestaand bestand. assume overschrijft detectie."""
    if not path.is_file():
        return DetectResult(
            path=path,
            hoek=HOEK_UNKNOWN,
            confidence=0.0,
            error=f"geen bestand: {path}",
        )
    if is_print_mscz(path):
        return DetectResult(
            path=path,
            hoek=HOEK_UNKNOWN,
            confidence=0.0,
            error=(
                f"print-.mscz hoort niet bij opkuisen: {path.name}. "
                r"Zie handleiding partituur/7-print-mscz."
            ),
        )

    suf = path.suffix.lower()
    if suf in REFUSED_SUFFIXES:
        return DetectResult(
            path=path,
            hoek=HOEK_UNKNOWN,
            confidence=0.0,
            error=(
                f"geweigerd formaat {suf}: {path.name}. "
                "Eerst CapToMusic naar .mxl exporteren, daarna opkuisen."
            ),
        )

    if assume:
        assume_l = assume.strip().lower()
        if assume_l not in KNOWN_HOEKEN:
            return DetectResult(
                path=path,
                hoek=HOEK_UNKNOWN,
                confidence=0.0,
                error=(
                    f"onbekende --assume {assume!r}; "
                    f"kies een van: {', '.join(sorted(KNOWN_HOEKEN))}"
                ),
            )
        base = _detect_by_suffix(path)
        if base.error and (
            "ongeldig" in (base.error or "").lower()
            or "geen musicxml" in (base.error or "").lower()
            or "geen .mscx" in (base.error or "").lower()
        ):
            return base
        return DetectResult(
            path=path,
            hoek=assume_l,
            confidence=1.0,
            signals=[f"--assume {assume_l}"],
            suggested_passes=_passes_for(assume_l),
            warnings=[],
            error=None,
        )

    return _detect_by_suffix(path)


def _detect_by_suffix(path: Path) -> DetectResult:
    suf = path.suffix.lower()
    if suf == ".vsa":
        return DetectResult(
            path=path,
            hoek=HOEK_VSA,
            confidence=1.0,
            signals=["extensie .vsa"],
            suggested_passes=_passes_for(HOEK_VSA),
        )
    if suf == ".mvsa":
        return DetectResult(
            path=path,
            hoek=HOEK_MVSA,
            confidence=1.0,
            signals=["extensie .mvsa (voorzien)"],
            suggested_passes=_passes_for(HOEK_MVSA),
            warnings=["mvsa-spoor is nog niet actief; geen automatische opkuis"],
        )
    if suf == ".mscz":
        return detect_mscz(path)
    if suf == ".mscx":
        return detect_mscx(path)
    if suf in MUSICXML_SUFFIXES:
        try:
            root, head = _load_musicxml_root(path)
        except zipfile.BadZipFile as e:
            return DetectResult(
                path=path,
                hoek=HOEK_UNKNOWN,
                confidence=0.0,
                error=f"ongeldige .mxl (geen zip): {path}: {e}",
            )
        except (ET.ParseError, ValueError, OSError) as e:
            return DetectResult(
                path=path,
                hoek=HOEK_UNKNOWN,
                confidence=0.0,
                error=f"ongeldige MusicXML: {path}: {e}",
            )
        return detect_musicxml_tree(root, path, raw_head=head)
    return DetectResult(
        path=path,
        hoek=HOEK_UNKNOWN,
        confidence=0.0,
        error=(
            f"onbekende extensie {suf or '(geen)'}: {path.name}. "
            f"Verwacht: {', '.join(sorted(SUPPORTED_SUFFIXES))}"
        ),
    )
