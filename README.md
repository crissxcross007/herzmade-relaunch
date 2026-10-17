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


## Bilder selbst mit Pages CMS pflegen

Backend: https://app.pagescms.org

1. Mit deinem GitHub-Konto anmelden.
2. Repository `crissxcross007/herzmade-relaunch`, Branch `main` auswählen.
3. Die passende Materialseite öffnen (z. B. Glas oder Holz).
4. Unter Galerie einen Eintrag hinzufügen, ein Bild hochladen/auswählen und optional Titel und Bildbeschreibung eintragen.
5. Speichern. GitHub Actions optimiert die Bilder, erstellt die Seiten und stößt die Veröffentlichung an.

Nur eine Datei unter Medien hochzuladen fügt noch keinen Galerieeintrag hinzu. Das Bild muss in der gewünschten Galerie ausgewählt und gespeichert werden.
Ist das neue Repository im Backend nicht sichtbar, muss die bestehende Pages-CMS-GitHub-App auch Zugriff auf dieses Repository erhalten.

Der Workflow `.github/workflows/pages-cms.yml` reagiert auf Änderungen an Bildern, Inhaltsdateien und dem Seitengenerator. Er verändert ausschließlich dieses Repository. GitHub Pages bleibt auf `main` und `/ (root)` eingestellt. Es werden keine persönlichen Tokens benötigt.

Falls eine Bilddatei noch von einer Geschenkidee verwendet wird, sollte sie nicht aus Medien gelöscht werden, bevor dort ein anderes Bild ausgewählt wurde. Das Entfernen eines Galerieeintrags ist davon unabhängig.
