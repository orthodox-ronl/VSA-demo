---
title: "Ruw materiaal binnenhalen"
linkTitle: "Binnenhalen"
weight: 10
---

# Ruw materiaal binnenhalen

{{< cue >}}
1. Zet het bestand in `content-source\praktijk\oefenhoek\input\<herkomst>\` (of eerst `_inbox\`).
2. Laat de originele bestandsnaam staan.
3. Draai `scripts\check.cmd` of `python scripts\update_werkvoorraad.py`.
4. Vul in `input\werkvoorraad.md` het **doel-id** in als die kolom leeg is — niet raden, vragen.
{{< /cue >}}

**Wat je nu doet:** het ruwe bestand bewaren op de afgesproken plek en in
de werkvoorraad zetten, nog zonder te converteren.

**Wanneer:** bij elk nieuw Capella-, VOW-, MuseScore-, MusicXML- of
PDF-bestand. Sla deze pagina over als het bestand al in `input\` staat en
de tabel al een doel-id heeft.

Het **doel-id** is de toekomstige mapnaam van de bladermap (alleen
`a-z`, `0-9`, `-`, `_`).

## Stap voor stap

1. Bepaal de herkomst-map (zie [Waar ligt wat](../../start/waar-ligt-wat/)).
2. Kopieer het bestand naar die herkomst-map. Twijfel je nog of je het
   wilt bewaren? Zet het eerst in `_inbox\` (die map gaat niet naar git).
3. Open het Windows-opdrachtvenster in `VSA-demo`
   ([hoe](../../start/wat-heb-je-nodig/)).
4. Ververs de werkvoorraad:

```cmd
python scripts\update_werkvoorraad.py
```

Of draai `scripts\check.cmd` — dat doet dezelfde update plus de rest van
de keten.

5. Open `content-source\praktijk\oefenhoek\input\werkvoorraad.md`. Zoek
   de nieuwe rij.
6. Kolom **Doel-id**:
   - Ken je de bladermap al (bijvoorbeeld `8a-trisagion`)? Vul dat id in.
   - Weet je het niet? Laat de cel leeg en vraag het na. **Niet verzinnen.**
7. Kolom **Notitie** mag alles zijn dat je over een maand nog wilt weten
   (bijvoorbeeld “zelfde bladermap als 7b”, “tweede bron, niet publiceren”).

De kolommen *Stap* en *Volgende* vult het script. Zet die niet met de hand
recht.

Op de Oefenhoek-pagina van de site staat dezelfde tabel uitklapbaar
onderaan — handig als geheugen, niet als plek om te bewerken. Bewerken
doe je in het markdown-bestand `werkvoorraad.md`.

## Klaar als

Er staat een rij voor het nieuwe bestand, het origineel zit in
`input\<herkomst>\`, en het doel-id is ingevuld **of** bewust leeg met een
vraag in de notitie.

{{< navbuttons "Volgende: opkuisen|/praktijk/handleiding/partituur/2-opkuisen/" >}}
