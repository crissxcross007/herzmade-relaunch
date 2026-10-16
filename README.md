# Herzmade Relaunch

Statische Testseite für Herzmade. Die Live-Seite in crissxcross007/herzmade bleibt getrennt.
Keine CNAME-Datei hinzufügen und keine Hauptdomain in diesem Repository setzen.

## Aufbau

- content/gifts.json: neun Geschenkideen, Preise, Anlässe und Bilder.
- content/holz.json, glas.json, schiefer.json, edelstahl.json, keramik.json, leder.json: vorhandene Texte und Galerien.
- scripts/build_site.py: zentraler Seitengenerator mit Menü und Footer. Diese werden beim Erstellen in jede Seite geschrieben; im Browser gibt es keine Includes und keine Inhalts-Fetches.
- assets/site.css, assets/site.js: Gestaltung, mobile Navigation, Anlassfilter und Galerie-Dialog.
- assets/img/: lokal optimierte WebP-Dateien in zwei Größen.
- images/: Originalbilder als Grundlage für spätere Bearbeitung; Besucher laden nur die optimierten Assets.

## Änderungen erstellen

Mit Python und Pillow (requirements-build.txt) im Projektordner ausführen:

    python scripts/build_site.py

Anschließend die generierten HTML-Seiten, aktualisierten Assets und Quelldateien gemeinsam committen. GitHub Pages veröffentlicht main aus dem Stammordner.
Nicht nur menu.html oder footer.html ändern: Diese Dateien werden aus den zentralen Funktionen navigation() und footer() erzeugt.

## Prüfung

Die Seiten bleiben während der Testphase auf noindex,nofollow. Keine externen Schriften, kein Bootstrap, kein jQuery. Formularziel bleibt der vorhandene Formspree-Endpunkt. Es wurden keine Testnachrichten versendet.
