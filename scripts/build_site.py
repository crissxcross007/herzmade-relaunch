#!/usr/bin/env python3
"""Build the static Herzmade website. Run: python scripts/build_site.py

Requires Pillow for image optimization. Navigation and footer are defined once
here; content remains editable in content/*.json. No browser-side build/runtime.
"""
from pathlib import Path
from PIL import Image, ImageOps
import hashlib, html, json, re, io

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'img'
ASSETS.mkdir(parents=True, exist_ok=True)
E = lambda value: html.escape(str(value), quote=True)
MATERIALS = {'holz': 'Holz', 'glas': 'Glas', 'schiefer': 'Schiefer', 'edelstahl': 'Edelstahl', 'keramik': 'Keramik', 'leder': 'Leder'}
OCCASIONS = {'geburtstag': 'Geburtstag', 'freundschaft': 'Freundschaft & Danke', 'paare': 'Hochzeit & Paare', 'ehrung': 'Jubiläum & Ehrung', 'weihnachten': 'Weihnachten', 'andenken': 'Andenken & Gedenken'}
DATA = {key: json.loads((ROOT/'content'/f'{key}.json').read_text()) for key in MATERIALS}
PRODUCTS = json.loads((ROOT/'content/gifts.json').read_text())
IMAGES = {}

def optimize(path):
    path = path.removeprefix('/').removeprefix('./')
    if path in IMAGES:
        return IMAGES[path]
    original = ROOT/path
    digest = hashlib.sha256(original.read_bytes()).hexdigest()[:12]
    with Image.open(original) as opened:
        img = ImageOps.exif_transpose(opened).convert('RGB')
        result = {}
        for size in (600, 1200):
            target = ASSETS/f'{digest}-{size}.webp'
            if not target.exists() or not target.stat().st_size:
                copy = img.copy()
                copy.thumbnail((size, size), Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                copy.save(buffer, 'WEBP', quality=78, method=6)
                target.write_bytes(buffer.getvalue())
            result[str(size)] = target.relative_to(ROOT).as_posix()
            with Image.open(target) as saved:
                result['w'+str(size)] = saved.width
        result['width'], result['height'] = img.size
    IMAGES[path] = result
    return result

def picture(path, alt, eager=False, cls='', sizes=None):
    data = optimize(path)
    loading = 'eager' if eager else 'lazy'
    priority = ' fetchpriority="high"' if eager else ''
    if sizes is None:
        sizes = '(max-width: 600px) 94vw, 46vw' if eager else '(max-width: 360px) 94vw, (max-width: 850px) 46vw, 32vw'
    candidates = {data['w600']: data['600'], data['w1200']: data['1200']}
    srcset = ', '.join(f'{url} {width}w' for width, url in candidates.items())
    return f'<img class="{E(cls)}" src="{data["600"]}" srcset="{srcset}" sizes="{sizes}" width="{data["width"]}" height="{data["height"]}" alt="{E(alt)}" loading="{loading}" decoding="async"{priority}>'

def navigation(active):
    gift_links = ''.join(f'<a href="geschenkideen.html#{key}">{E(label)}</a>' for key,label in OCCASIONS.items())
    material_links = ''.join(f'<a href="{key}.html">{label}</a>' for key,label in MATERIALS.items())
    def link(url, label, key):
        return f'<a href="{url}"'+(' aria-current="page"' if active == key else '')+f'>{label}</a>'
    return f'''<header class="site-header"><div class="header-inner">
      <a class="brand" href="index.html" aria-label="Herzmade Startseite"><img src="assets/logo.png" width="240" height="93" alt="Herzmade – mit Herz gemacht statt Barcode"></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav"><span>Menü</span><svg width="22" height="18" viewBox="0 0 22 18" aria-hidden="true"><path d="M1 2H21M1 9H21M1 16H21" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
      <nav id="main-nav" aria-label="Hauptnavigation">
        {link('index.html', 'Startseite', 'home')}
        <div class="nav-group"><div class="nav-group-title">{link('geschenkideen.html', 'Geschenkideen', 'gifts')}<button type="button" class="submenu-toggle" aria-label="Anlässe anzeigen" aria-expanded="false">⌄</button></div><div class="nav-submenu"><a href="geschenkideen.html">Alle Geschenkideen</a>{gift_links}</div></div>
        <div class="nav-group"><div class="nav-group-title">{link('index.html#materialien', 'Materialien', 'materials')}<button type="button" class="submenu-toggle" aria-label="Materialien anzeigen" aria-expanded="false">⌄</button></div><div class="nav-submenu">{material_links}</div></div>
        {link('about.html','Über uns','about')}{link('contact.html','Deine Idee anfragen <span aria-hidden="true">↗</span>','contact')}
      </nav>
    </div></header>'''

def footer():
    return '''<footer class="site-footer"><div class="wrap footer-top"><div><a class="footer-name" href="index.html">HERZMADE<span>Mit Herz gemacht statt Barcode.</span></a><p>Persönliche Gravuren und Geschenkideen<br>aus Döbern in der Lausitz.</p></div><div><p class="footer-label">Entdecken</p><a href="geschenkideen.html">Geschenkideen & Preise</a><a href="about.html">Chris & Levi</a><a href="contact.html">Kontakt</a></div><div><p class="footer-label">Lass uns etwas Persönliches machen.</p><a class="footer-mail" href="mailto:kontakt@herzmade.de">kontakt@herzmade.de</a><a href="tel:+4917650830805">+49 176 50830805</a><a href="https://instagram.com/crissXcross.creations" rel="noopener noreferrer" target="_blank">Instagram ↗</a></div></div><div class="wrap footer-bottom"><span>© 2026 Herzmade</span><span>03159 Döbern · Lausitz</span></div></footer>'''

def cta():
    return '''<section class="process wrap" aria-labelledby="process-title"><div class="section-intro"><p class="eyebrow">Von deiner Idee zum Einzelstück</p><h2 id="process-title">Persönlich schenken<br>geht ganz einfach.</h2></div><ol class="steps"><li><span class="step-number">01</span><h3>Lieblingsstück entdecken</h3><p>Wähle ein Produkt und lass dich von unseren Arbeiten inspirieren.</p></li><li><span class="step-number">02</span><h3>Deinen Wunsch erzählen</h3><p>Erzähl uns vom Anlass, deinem Wunschmotiv und dem Menschen, dem du eine Freude machen möchtest.</p></li><li><span class="step-number">03</span><h3>Gemeinsam gestalten</h3><p>Gestaltung, Ausführung und Preis stimmen wir persönlich mit dir ab.</p></li></ol><div class="center"><a class="button" href="contact.html">Deine Geschenkidee anfragen <span aria-hidden="true">↗</span></a></div></section>'''

def page(filename, title, desc, content, active, lightbox=False):
    dialog = '''<dialog class="lightbox" aria-label="Bild in Großansicht"><button class="lightbox-close" aria-label="Großansicht schließen">×</button><button class="lightbox-prev" aria-label="Vorheriges Bild">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lightbox-next" aria-label="Nächstes Bild">›</button></dialog>''' if lightbox else ''
    url = 'https://herzmade.de/'+('' if filename == 'index.html' else filename)
    out = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#eeeeeb"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="https://herzmade.de/images/herzmade-social.jpg"><link rel="stylesheet" href="assets/site.css?v=20261016"><script src="assets/site.js?v=20261016" defer></script></head><body><a class="skip-link" href="#inhalt">Zum Inhalt</a>{navigation(active)}<main id="inhalt">{content}</main>{footer()}{dialog}</body></html>'''
    (ROOT/filename).write_text(out)

def product_card(p):
    return f'''<article class="product" data-occasions="{E(' '.join(p['occasions']))}"><a class="product-photo" href="{p['material']}.html#gallery">{picture(p['image'],p['alt'])}<span class="photo-arrow" aria-hidden="true">↗</span></a><div class="product-top"><h3>{E(p['title'])}</h3><p class="price">ab {E(p['price'])} €</p></div><p>{E(p['description'])}</p><p class="product-detail">{E(p['detail'])}</p><a class="text-link" href="{p['material']}.html#gallery">Beispiele ansehen <span aria-hidden="true">↗</span></a></article>'''

def gallery_example(material, preferred):
    """Keep featured examples stable when editors reorder or empty a gallery."""
    gallery = DATA[material].get('galerie') or []
    candidates = sorted(gallery, key=lambda item: item.get('bild', '').lstrip('/') != preferred)
    for item in candidates:
        path = (item.get('bild') or '').lstrip('/').removeprefix('./')
        if path and (ROOT/path).is_file():
            return {'bild': path, 'alt': item.get('alt') or item.get('titel') or f'Gravur auf {MATERIALS[material]}'}
    return {'bild': 'images/herzmade-social.jpg', 'alt': f'Herzmade – Gravuren auf {MATERIALS[material]}'}

def build_home():
    featured = {
        'holz': 'images/holz/brett-lieblingsfussballer.jpg',
        'glas': 'images/glas/weinglas-hochzeit.jpg',
        'schiefer': 'images/schiefer/schiefertafel-goldene-hochzeit.jpg',
        'edelstahl': 'images/edelstahl/tasse-geschenkbox.jpg',
        'keramik': 'images/keramik/img5124.jpeg',
        'leder': 'images/leder/dd52daca-2171-4a2e-866a-46794246d3cd2025-12-1922-35-57764.jpeg',
    }
    material_images = {key: gallery_example(key, path) for key, path in featured.items()}
    hero_item = gallery_example('glas', 'images/glas/laterne-lebensbaum.jpg')
    hero = picture(hero_item['bild'],hero_item['alt'],True)
    small_item = gallery_example('holz', 'images/holz/hochzeitsbox-holz.jpg')
    small = picture(small_item['bild'],small_item['alt'])
    cards = ''.join(f'<a class="material-card" href="{key}.html"><div>{picture(material_images[key]["bild"],material_images[key]["alt"])}</div><h3>{label}<span aria-hidden="true">↗</span></h3></a>' for key,label in MATERIALS.items())
    content = f'''<section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><p class="eyebrow">Gravuren & Geschenkideen aus Döbern</p><h1>Kein Geschenk<br>wie jedes.<br><em>Deins.</em></h1><p class="hero-lead">Ein Name. Ein besonderer Moment. Eine Erinnerung, die bleibt. Wir machen aus deiner Idee ein persönliches Einzelstück.</p><div class="hero-actions"><a class="button" href="geschenkideen.html">Geschenkideen entdecken <span aria-hidden="true">↗</span></a><a class="text-link" href="about.html">Das ist Herzmade</a></div><p class="hero-signoff">Mit Herz gemacht statt Barcode.</p></div><div class="hero-visual"><div class="hero-main">{hero}<span class="image-label">Ein Licht.<br>Deine persönliche Botschaft.</span></div><div class="hero-small">{small}<span>Für deine Lieblingsmenschen.</span></div></div></div></section>
    <div class="values-strip"><div class="wrap"><span>Individuell graviert</span><span>Material & Gravur inklusive</span><span>Persönlich aus der Lausitz</span></div></div>
    <section class="occasion-section wrap"><div class="section-heading"><div><p class="eyebrow">Weil jeder Moment anders ist</p><h2>Was möchtest du<br>in Erinnerung behalten?</h2></div><p>Zum Geburtstag, als Dankeschön oder für einen ganz besonderen Menschen: Hier beginnt deine Geschenkidee.</p></div><div class="occasion-links">{''.join(f'<a href="geschenkideen.html#{key}"><span>{E(label)}</span><span aria-hidden="true">↗</span></a>' for key,label in OCCASIONS.items())}</div></section>
    <section class="materials-section wrap" id="materialien"><div class="section-heading"><div><p class="eyebrow">Echte Materialien. Deine Geschichte.</p><h2>Mit Charakter gemacht.</h2></div><p>Natürliches Holz, kontrastreicher Schiefer oder edles Glas. Entdecke unsere Materialien und echten Arbeiten.</p></div><div class="materials-grid">{cards}</div></section>
    <section class="about-band"><div class="wrap about-grid"><p class="eyebrow">Zwei Köpfe. Viele Ideen.</p><div><h2>Vater, Sohn<br>und ein Herzensprojekt.</h2><p>Wir sind Chris und Levi aus Döbern. Bei Herzmade verbinden wir Technik, Kreativität und unsere Freude an persönlichen Geschenken.</p><a class="text-link" href="about.html">Lerne uns kennen <span aria-hidden="true">↗</span></a></div></div></section>{cta()}'''
    page('index.html','Herzmade – persönliche Geschenke & Gravuren aus Döbern','Individuelle Geschenkideen aus Holz, Glas, Schiefer und Edelstahl. Persönlich graviert von Chris und Levi aus Döbern in der Lausitz.',content,'home')

def build_gifts():
    filters = '<button type="button" data-filter="alle" aria-pressed="true">Alle Geschenkideen</button>'+''.join(f'<button type="button" data-filter="{key}" aria-pressed="false">{E(label)}</button>' for key,label in OCCASIONS.items())
    content = f'''<section class="page-intro wrap"><p class="eyebrow">Kleine Aufmerksamkeiten. Große Erinnerungen.</p><h1>Für deinen Anlass.<br><em>Für deinen Lieblingsmenschen.</em></h1><p>Entdecke persönliche Geschenke mit deinem Namen, Wunschtext oder Motiv. Jedes Stück beginnt mit deiner Idee.</p></section><section class="gift-collection wrap" aria-label="Geschenkideen mit Preisen"><div class="filters" role="group" aria-label="Nach Anlass filtern">{filters}</div><div class="collection-meta"><p id="gift-count" role="status" aria-live="polite">{len(PRODUCTS)} Geschenkideen</p><p>Alle Preise pro Stück inklusive Material und Gravur.<br>Je nach Größe und Ausführung kann der Preis variieren.</p></div><div class="product-grid">{''.join(product_card(p) for p in PRODUCTS)}</div><noscript><p>Alle Geschenkideen sind sichtbar. Die Auswahl nach Anlass ist mit JavaScript verfügbar.</p></noscript></section>{cta()}'''
    page('geschenkideen.html','Geschenkideen mit Gravur – Anlässe & Preise | Herzmade','Persönliche Geschenke für Geburtstag, Hochzeit, Jubiläum und Weihnachten. Entdecke Gravuren aus Döbern mit Preisen ab 7 Euro inklusive Material.',content,'gifts')

def clean(text):
    return re.sub('[\U0001F000-\U0001FAFF\u2600-\u27ff\ufe0f]', '', text).strip()

def build_materials():
    subtitles={'holz':'Natürlich. Persönlich. Ein Stück für jeden Tag.', 'glas':'Ein besonderer Moment, für immer festgehalten.', 'schiefer':'Dunkler Stein. Helle Erinnerungen.', 'edelstahl':'Dein Lieblingsstück. Immer dabei.', 'keramik':'Eine kleine Auszeit mit persönlicher Note.', 'leder':'Charakter, den man sehen und fühlen kann.'}
    for key,label in MATERIALS.items():
        data=DATA[key]
        gallery=''
        for item in data.get('galerie') or []:
            if not item.get('bild'):
                continue
            item_title = clean(item.get('titel') or f'Gravur auf {label}')
            item_alt = clean(item.get('alt') or item_title)
            optimized=optimize(item['bild'])
            gallery+=f'<article class="gallery-item"><a class="gallery-photo" href="{optimized["1200"]}" data-lightbox data-caption="{E(item_title)}" aria-label="{E(item_title)} vergrößern">{picture(item["bild"],item_alt)}<span class="photo-arrow" aria-hidden="true">+</span></a><h3>{E(item_title)}</h3><p>{E(item_alt)}</p></article>'
        related=[p for p in PRODUCTS if p['material']==key]
        prices=''.join(f'<div><span>{E(p["title"])}</span><strong>ab {E(p["price"])} €</strong></div>' for p in related)
        priceblock=f'<aside class="material-prices"><p class="eyebrow">Deine Preisorientierung</p>{prices}<p>Inklusive Material und Gravur. Details zu Größen und Ausführungen findest du bei den Geschenkideen.</p><a class="text-link" href="geschenkideen.html">Geschenkideen & Preise ↗</a></aside>' if related else ''
        content=f'''<section class="page-intro wrap"><p class="eyebrow">Materialien / {label}</p><h1>{label} mit Gravur.<br><em>{subtitles[key]}</em></h1><p>Individuelle Arbeiten von Herzmade aus Döbern. Lass dich inspirieren und bring deine eigene Idee mit.</p></section><section class="material-overview wrap"><div class="material-story">{clean(data.get('einleitung') or '')}</div>{priceblock}</section><section class="gallery-section wrap" id="gallery"><div class="section-heading"><div><p class="eyebrow">So persönlich kann {label} sein</p><h2>Einblicke in unsere Arbeiten.</h2></div><p>Echte Einzelstücke aus unserer Werkstatt.<br>Tippe auf ein Bild für die Großansicht.</p></div><div class="gallery-grid">{gallery}</div></section>{cta()}'''
        page(key+'.html',f'{label} gravieren lassen in Döbern | Herzmade',f'Individuelle Gravuren auf {label} aus Döbern. Entdecke echte Arbeiten, persönliche Geschenkideen und Gestaltungsmöglichkeiten von Herzmade.',content,'materials',True)

def build_about():
    drawing=gallery_example('schiefer', 'images/schiefer/2025-11-0216-28-30563.jpg')
    content=f'''<section class="page-intro wrap"><p class="eyebrow">Hallo, wir sind Herzmade</p><h1>Chris & Levi.<br><em>Technik trifft Fantasie.</em></h1><p>Vater und Sohn aus Döbern. Ein gemeinsames Hobby. Und die Freude daran, aus einer Idee etwas Persönliches zu machen.</p></section><section class="story-grid wrap"><div class="story-photo">{picture(drawing['bild'],drawing['alt'],sizes='(max-width: 600px) 94vw, 46vw')}<p>Aus einer Zeichnung wird eine Erinnerung.</p></div><div class="story-copy"><p class="eyebrow">Unsere Geschichte</p><h2>Mit Herz gemacht.<br>Ganz wörtlich.</h2><p>Herzmade ist unser gemeinsames Herzensprojekt. Chris bringt als gelernter IT-Systemelektroniker den technischen Hintergrund mit. Levi zeichnet gerne, entwickelt Motive und probiert neue Ideen aus.</p><p>In unserer Freizeit verbinden wir beides: Kreativität und präzise Technik. So entstehen Gravuren auf Holz, Glas, Keramik, Schiefer, Edelstahl und Leder – und manchmal auf einer Weihnachtskugel.</p><p>Uns geht es um Dinge mit persönlicher Bedeutung. Einen Namen. Eine Zeichnung. Einen Moment, den du festhalten möchtest.</p><p>Wir sind in 03159 Döbern zu Hause und gestalten für Menschen aus Döbern, Forst (Lausitz), Spree-Neiße, Cottbus und Umgebung.</p><a class="text-link" href="geschenkideen.html">Unsere Geschenkideen entdecken ↗</a></div></section><section class="about-band"><div class="wrap about-grid"><p class="eyebrow">Was uns ausmacht</p><div><h2>Persönlich statt von der Stange.</h2><p>Gezeichnete Motive, kleine Botschaften oder eine ganz eigene Idee: Wir nehmen uns Zeit, gemeinsam mit dir das passende Material und die Gestaltung zu finden.</p></div></div></section>{cta()}'''
    page('about.html','Chris & Levi – das ist Herzmade aus Döbern','Lerne Chris und Levi kennen: Vater und Sohn aus Döbern, die Kreativität und Technik zu persönlichen Gravuren und Geschenkideen verbinden.',content,'about')

def build_contact():
    content='''<section class="page-intro wrap"><p class="eyebrow">Aus deiner Idee wird etwas Persönliches</p><h1>Was möchtest du<br><em>verschenken?</em></h1><p>Eine erste Idee reicht. Erzähl uns vom Anlass und deinem Wunsch – den Rest besprechen wir gemeinsam.</p></section><section class="contact-layout wrap"><div class="contact-details"><h2>Lass uns reden.</h2><a class="contact-big" href="mailto:kontakt@herzmade.de">kontakt@herzmade.de</a><a href="tel:+4917650830805">+49 176 50830805</a><div class="contact-address"><p class="eyebrow">Hier entstehen deine Geschenke</p><p>Herzmade · Chris & Levi<br>Jerischker Weg 8<br>03159 Döbern · Lausitz</p></div><a class="text-link" href="https://instagram.com/crissXcross.creations" target="_blank" rel="noopener noreferrer">Weitere Einblicke auf Instagram ↗</a></div><form class="contact-form" action="https://formspree.io/f/xeeropko" method="POST"><input type="text" name="_gotcha" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="hidden" name="_subject" value="Neue Geschenkidee über Herzmade"><div class="form-row"><div><label for="name">Dein Name</label><input id="name" name="name" autocomplete="name" required></div><div><label for="email">Deine E-Mail-Adresse</label><input id="email" name="email" type="email" autocomplete="email" required></div></div><label for="product">Wofür interessierst du dich? <span>(optional)</span></label><select id="product" name="produkt"><option value="">Ich bin noch offen für Ideen</option>'''+''.join(f'<option>{E(p["title"])}</option>' for p in PRODUCTS)+'''<option>Eine ganz eigene Idee</option></select><label for="message">Deine Idee</label><textarea id="message" name="message" rows="6" placeholder="Für wen ist das Geschenk? Zu welchem Anlass? Gibt es schon ein Wunschmotiv oder einen Text?" required></textarea><p class="form-note">Deine Nachricht wird über Formspree übermittelt.</p><button class="button" type="submit">Geschenkidee senden <span aria-hidden="true">↗</span></button><p class="form-note">Du kannst uns auch direkt per E-Mail schreiben.</p></form></section>'''
    page('contact.html','Deine Geschenkidee anfragen | Herzmade Döbern','Erzähl uns von deiner Geschenkidee. Persönliche Gravuren aus Döbern – Kontakt per Formular, E-Mail oder Telefon.',content,'contact')

def main():
    # Keep the exact logo artwork; only resize its transparent image for the web.
    with Image.open(ROOT/'images/1Herzmade-transparent.png') as original:
        logo=ImageOps.exif_transpose(original).convert('RGBA');logo.thumbnail((480,208),Image.Resampling.LANCZOS);logo.save(ROOT/'assets/logo.png',optimize=True)
    build_home();build_gifts();build_materials();build_about();build_contact()
    page('work.html','Geschenkideen | Herzmade','Persönliche Geschenkideen mit Gravur.', '<section class="page-intro wrap"><h1>Unsere Geschenkideen.</h1><p>Du findest unsere Arbeiten jetzt nach Anlässen sortiert.</p><a class="button" href="geschenkideen.html">Zu den Geschenkideen ↗</a></section>','gifts')
    page('danke.html','Danke für deine Nachricht | Herzmade','Wir freuen uns auf deine Geschenkidee.','<section class="page-intro wrap"><p class="eyebrow">Mit Herz gelesen</p><h1>Danke für deine Nachricht.</h1><p>Wir freuen uns auf deine Idee und melden uns bei dir.</p><a class="button" href="index.html">Zur Startseite</a></section>','contact')
    # Central snippets remain available; published pages already contain them.
    (ROOT/'menu.html').write_text(navigation(''))
    (ROOT/'footer.html').write_text(footer())
    (ROOT/'assets/image-manifest.json').write_text(json.dumps(IMAGES,ensure_ascii=False,indent=2))
    (ROOT/'.nojekyll').touch()
    assert not (ROOT/'CNAME').exists(), 'Test repository must not claim the live domain'
    print(f'Built 12 pages, {len(PRODUCTS)} products and {len(IMAGES)} optimized image pairs.')

if __name__=='__main__':main()
