"""build.py — shared helpers for NordicWebFlow static site"""

NAV_LINKS = [
    ('Forside', '/'),
    ('Ydelser', None, [
        ('Premium Hjemmesider', '/ydelser/lynhurtige-hjemmesider-framer'),
        ('Lokal SEO Optimering', '/ydelser/lokal-seo-koebenhavn'),
        ('Google & Meta Ads', '/ydelser/google-meta-ads-koebenhavn'),
        ('Drift & Sikkerhed', '/ydelser/drift-og-sikkerhed'),
    ]),
    ('Brancher', None, [
        ('Tømrer', '/toemrer'),
        ('Tandlæge', '/tandlaege'),
        ('Advokat', '/advokat'),
        ('Murer', '/murer'),
        ('Elektriker', '/elektriker'),
        ('Maler', '/maler'),
        ('VVS', '/vvs'),
        ('Fysioterapeut', '/fysioterapeut'),
        ('Revisor', '/revisor'),
        ('Ejendomsmægler', '/ejendomsmaegler'),
        ('Arkitekt', '/arkitekt'),
    ]),
    ('Priser', '/priser'),
    ('Cases', '/cases'),
    ('Kontakt', '/kontakt'),
]

def head(title, desc, canonical, og_img="/images/og-default.jpg", extra=""):
    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://nordicwebflow.com{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://nordicwebflow.com{canonical}">
<meta property="og:image" content="https://nordicwebflow.com{og_img}">
<meta property="og:locale" content="da_DK">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/style.css">
{extra}
</head>"""

def nav():
    return """<nav>
  <div class="nav-inner">
    <a href="/" class="nav-logo" aria-label="NordicWebFlow — Webbureau København">
      <div class="nav-logo-icon">N</div>
      <span class="nav-logo-text">Nordic<span>WebFlow</span></span>
    </a>
    <div class="nav-links">
      <a href="/">Forside</a>
      <div class="dropdown">
        <a href="/ydelser">Ydelser ▾</a>
        <div class="dropdown-menu">
          <a href="/ydelser/lynhurtige-hjemmesider-framer">Premium Hjemmesider</a>
          <a href="/ydelser/lokal-seo-koebenhavn">Lokal SEO Optimering</a>
          <a href="/ydelser/google-meta-ads-koebenhavn">Google &amp; Meta Ads</a>
          <a href="/ydelser/drift-og-sikkerhed">Drift &amp; Sikkerhed</a>
        </div>
      </div>
      <div class="dropdown">
        <a href="#">Brancher ▾</a>
        <div class="dropdown-menu">
          <a href="/toemrer">Tømrer</a>
          <a href="/tandlaege">Tandlæge</a>
          <a href="/advokat">Advokat</a>
          <a href="/murer">Murer</a>
          <a href="/elektriker">Elektriker</a>
          <a href="/maler">Maler</a>
          <a href="/vvs">VVS</a>
          <a href="/fysioterapeut">Fysioterapeut</a>
          <a href="/revisor">Revisor</a>
          <a href="/ejendomsmaegler">Ejendomsmægler</a>
          <a href="/arkitekt">Arkitekt</a>
        </div>
      </div>
      <a href="/priser">Priser</a>
      <a href="/cases">Cases</a>
      <a href="https://seotjek.dk/" target="_blank" rel="noopener noreferrer">Gratis SEO-tjek</a>
      <a href="/faa-et-tilbud" class="nav-cta">Få et tilbud</a>
    </div>
    <button class="hamburger" id="hamburger-btn" aria-label="Åbn menu" aria-expanded="false" aria-controls="mobile-menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="mobile-menu" id="mobile-menu" role="navigation" aria-label="Mobilmenu">
    <a href="/">Forside</a>
    <a href="/ydelser/lynhurtige-hjemmesider-framer">Premium Hjemmesider</a>
    <a href="/ydelser/lokal-seo-koebenhavn">Lokal SEO Optimering</a>
    <a href="/ydelser/google-meta-ads-koebenhavn">Google &amp; Meta Ads</a>
    <a href="/toemrer">Tømrer</a><a href="/tandlaege">Tandlæge</a>
    <a href="/advokat">Advokat</a><a href="/murer">Murer</a>
    <a href="/elektriker">Elektriker</a><a href="/maler">Maler</a>
    <a href="/vvs">VVS</a><a href="/fysioterapeut">Fysioterapeut</a>
    <a href="/revisor">Revisor</a><a href="/ejendomsmaegler">Ejendomsmægler</a>
    <a href="/arkitekt">Arkitekt</a>
    <a href="/priser">Priser</a><a href="/cases">Cases</a>
    <a href="/kontakt">Kontakt</a>
    <a href="https://seotjek.dk/" target="_blank" rel="noopener noreferrer">Gratis SEO-tjek ↗</a>
    <a href="/faa-et-tilbud">Få et tilbud →</a>
  </div>
</nav>"""

def ticker():
    items = ['Tømrermestre','Tandlæger','Advokater','Klinikker','Entreprenører','Murere','Elektrikere','Malere','VVS-firmaer','Fysioterapeuter','Revisorer','Ejendomsmæglere']
    html = '<div class="ticker-wrap"><div class="ticker-track">'
    for _ in range(2):
        for item in items:
            html += f'<div class="ticker-item"><span class="ticker-dot"></span>{item}</div>'
    html += '</div></div>'
    return html

def footer():
    return """<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-logo">
          <div class="footer-logo-icon">N</div>
          <span class="footer-logo-text">Nordic<span>WebFlow</span></span>
        </div>
        <p>Vi bygger lynhurtige digitale salgsmaskiner for ambitiøse lokale virksomheder. Fra premium webdesign til lokal dominans på Google.</p>
      </div>
      <div class="footer-col">
        <h5>Brancher</h5>
        <a href="/toemrer">Tømrer</a>
        <a href="/tandlaege">Tandlæge</a>
        <a href="/advokat">Advokat</a>
        <a href="/murer">Murer</a>
        <a href="/elektriker">Elektriker</a>
        <a href="/maler">Maler</a>
        <a href="/vvs">VVS</a>
        <a href="/fysioterapeut">Fysioterapeut</a>
        <a href="/revisor">Revisor</a>
        <a href="/ejendomsmaegler">Ejendomsmægler</a>
        <a href="/arkitekt">Arkitekt</a>
      </div>
      <div class="footer-col">
        <h5>Ydelser</h5>
        <a href="/ydelser/lynhurtige-hjemmesider-framer">Premium Hjemmesider</a>
        <a href="/ydelser/lokal-seo-koebenhavn">Lokal SEO Optimering</a>
        <a href="/ydelser/google-meta-ads-koebenhavn">Google &amp; Meta Ads</a>
        <a href="/ydelser/drift-og-sikkerhed">Drift &amp; Sikkerhed</a>
        <h5 style="margin-top:20px">Sider</h5>
        <a href="https://seotjek.dk/" target="_blank" rel="noopener noreferrer">Gratis SEO Tjek</a>
        <a href="/">Forside</a>
        <a href="/priser">Priser</a>
        <a href="/cases">Cases</a>
        <a href="/legal">Privatlivspolitik</a>
      </div>
      <div class="footer-col">
        <h5>Kontakt os</h5>
        <a href="/kontakt">Kontaktformular</a>
        <a href="mailto:hej@nordicwebflow.com">hej@nordicwebflow.com</a>
        <a href="/faa-et-tilbud">Få et tilbud</a>
        <p style="font-size:.8rem;color:var(--muted2);margin-top:12px">København, Danmark<br>CVR: 46305639</p>
        <div style="display:flex;gap:8px;margin-top:16px">
          <a href="https://www.trustpilot.com/review/nordicwebflow.com" target="_blank" rel="noopener noreferrer" style="font-size:.78rem;color:var(--orange);border:1px solid var(--border-orange);padding:4px 10px;border-radius:999px">★ Trustpilot</a>
          <a href="https://www.linkedin.com/company/nordicwebflow/" target="_blank" rel="noopener noreferrer" style="font-size:.78rem;color:rgba(255,255,255,.5);border:1px solid rgba(255,255,255,.15);padding:4px 10px;border-radius:999px">LinkedIn</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 NordicWebFlow. Alle rettigheder forbeholdes.</span>
      <div style="display:flex;gap:16px">
        <a href="/legal" style="color:rgba(255,255,255,.3)">Privatlivspolitik</a>
        <a href="/legal" style="color:rgba(255,255,255,.3)">Cookiepolitik</a>
        <a href="https://seotjek.dk" target="_blank" rel="noopener noreferrer" style="color:rgba(255,255,255,.3)">Gratis SEO-analyseværktøj</a>
      </div>
    </div>
  </div>
</footer>"""

def scripts():
    return """<script>
// FAQ accordion
document.querySelectorAll('.faq-q').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const item=btn.closest('.faq-item');
    const isOpen=item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i=>i.classList.remove('open'));
    if(!isOpen)item.classList.add('open');
  });
});
// Hamburger
const btn=document.getElementById('hamburger-btn');
const mob=document.getElementById('mobile-menu');
if(btn&&mob){
  btn.addEventListener('click',()=>{
    const open=mob.classList.toggle('open');
    btn.setAttribute('aria-expanded',open);
    btn.setAttribute('aria-label',open?'Luk menu':'Åbn menu');
  });
}
</script>"""

def schema_localbusiness():
    return """<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"LocalBusiness",
  "name":"NordicWebFlow",
  "description":"Webbureau i København der leverer professionelt webdesign, lokal SEO og Google Ads til lokale virksomheder.",
  "url":"https://nordicwebflow.com",
  "logo":"https://nordicwebflow.com/images/logo.svg",
  "email":"hej@nordicwebflow.com",
  "address":{"@type":"PostalAddress","addressLocality":"København","addressCountry":"DK"},
  "geo":{"@type":"GeoCoordinates","latitude":55.6761,"longitude":12.5683},
  "areaServed":{"@type":"City","name":"København"},
  "priceRange":"2999-8999 DKK",
  "openingHours":"Mo-Fr 09:00-18:00",
  "sameAs":["https://www.linkedin.com/company/nordicwebflow/","https://www.trustpilot.com/review/nordicwebflow.com"]
}
</script>"""

def review_schema():
    return """<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Review",
  "reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},
  "author":{"@type":"Person","name":"Benjamin Wenneke"},
  "reviewBody":"Jeg kan klart anbefale Nordicwebflow. De har lavet min hjemmeside, og resultatet er virkelig imponerende. Designet er flot, stilrent og professionelt.",
  "itemReviewed":{"@type":"LocalBusiness","name":"NordicWebFlow"}
}
</script>"""

def faq_schema(faqs):
    items = ','.join([f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}' for q,a in faqs])
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}</script>'

FAQS_HOME = [
    ("Hvad koster en hjemmeside hos NordicWebFlow?", "Vores priser starter fra 2.999 kr. for Starter-pakken op til 8.999 kr. for Premium+. Du betaler én gang og ejer siden 100%."),
    ("Hvor lang tid tager det at bygge en hjemmeside?", "Vi leverer din færdige hjemmeside på under 14 dage fra bestilling til lancering."),
    ("Hvilke brancher arbejder I med?", "Vi specialiserer os i lokale virksomheder som tømrere, tandlæger, advokater, murere, elektrikere, malere, VVS-firmaer, fysioterapeuter, revisorer og ejendomsmæglere i København."),
    ("Er hjemmesiden SEO-optimeret?", "Ja, alle vores hjemmesider er 100% teknisk SEO-optimerede fra dag ét — inkl. meta-titler, schema markup, sitemap og Core Web Vitals."),
    ("Ejer jeg min hjemmeside?", "Ja, 100%. Du ejer siden, koden og domænet fra dag ét. Ingen bindende abonnementer eller lock-in."),
    ("Hvad er inkluderet i Lokal SEO-pakken?", "Lokal SEO-pakken til 1.999 kr./md. inkluderer optimering af Google Business Profile, månedlig keyword-tracking, on-page SEO-opdateringer og en simpel månedlig rapport."),
    ("Bruger I Framer til alle hjemmesider?", "Ja. Vi bygger udelukkende i Framer fordi det producerer lynhurtige hjemmesider med sub-1-sekunds loadtid og 97+ PageSpeed-score."),
]

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {path}")

if __name__ == '__main__':
    print("Build helpers loaded OK")
