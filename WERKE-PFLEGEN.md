# Werke und Anlässe pflegen

Im Pages CMS das Repository **herzmade-relaunch** auswählen.

## Normale Werke

Unter **Content → Werke & Anlässe** jedes Werk einmal pflegen:

1. Titel, Foto und Beschreibung eintragen.
2. Materialgalerie und Produktart auswählen. Das Werk erscheint automatisch in dieser Materialgalerie.
3. Nur die Anlässe auswählen, zu denen der konkrete Auftrag tatsächlich passt. Mehrfachauswahl ist möglich.
4. „Bei den Ideen beziehungsweise beim Gedenken anzeigen“ einschalten, wenn das Werk zusätzlich als Anlass-Beispiel erscheinen soll. Ohne ausgewählten Anlass erscheint es dort nicht.
5. Optional den Ab-Preis als `14,90` eintragen. Ohne Preis erscheint „Preis auf Anfrage“. Im Preishinweis genau angeben, ob etwa nur die Gravur, eine einzelne Tasse oder eine Verpackung ohne Inhalt gemeint ist.

„Erinnern & Gedenken“ ist eine eigene Anlass-Kategorie in der Ideen-Auswahl. Beim Auswählen wechseln Einleitung und Kontaktaufruf zur passenden ruhigen Ansprache. Die eigene Erinnerungsseite bleibt zusätzlich verfügbar. Tierporträts und Fotobücher bitte nicht automatisch als Trauerarbeit einordnen.

Die Schalter für die Ideen-Auswahl beeinflussen die Materialgalerie nicht. Ein Bild muss nicht doppelt hochgeladen werden.

## Weihnachtsbaumkugeln

Die bestehende Pflege unter **Content → Weihnachtsbaumkugeln → Galerie** bleibt erhalten. Mit „Auch in der Ideen-Auswahl Weihnachten anzeigen“ lässt sich ein Beispiel zusätzlich im Anlassfilter zeigen. Die übrigen Kugeln bleiben in der vollständigen Weihnachtsgalerie sichtbar.

## Seitentexte und bestehende Daten

Die Einträge **Holz – Seitentext**, **Glas – Seitentext** usw. bearbeiten die jeweiligen Einleitungen. Die Bilder werden jetzt aus `content/werke/*.json` zusammengestellt. Die alten Galerie-Listen in `content/holz.json` usw. bleiben als Migrationsbestand erhalten, werden aber nicht mehr für die Materialgalerien verwendet und sind im CMS nicht mehr als zweite Bildpflege sichtbar.

Die separate Weihnachtsgalerie bleibt in `content/weihnachtsbaumkugeln.json`.

## Zuordnung prüfen

`zuordnung-pruefen.html` zeigt sechs gezielte Rückfragen mit Bildern. Die Seite ist nicht im öffentlichen Menü verlinkt. Die Auswahl der Fragen liegt in `content/zuordnung.json`. Sobald einem Werk ein Anlass zugeordnet wurde, entfällt seine Rückfrage dort automatisch.

Nach Speichern baut der bestehende GitHub-Workflow die Website samt Bildgrößen automatisch neu. Das Live-Repository `herzmade` wird nicht geändert.
