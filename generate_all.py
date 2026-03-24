#!/usr/bin/env python3
"""generate_all.py — builds all 30 NordicWebFlow pages"""
import os, sys
sys.path.insert(0, '/home/claude/nordicwebflow')
from build import head, nav, footer, scripts, ticker, schema_localbusiness, review_schema, faq_schema, FAQS_HOME, write

BASE = '/home/claude/nordicwebflow'

# ─────────────────────────────────────────────
# SHARED COMPONENTS
# ─────────────────────────────────────────────

def NAV(): return nav()
def FOOT(): return footer()
def SCR(): return scripts()

def TESTIMONIAL(extra_class=""):
    return f"""<section style="padding:60px 0">
  <div class="container">
    <div class="testimonial-card {extra_class}">
      <div class="t-stars">★★★★★</div>
      <p class="t-text">Jeg kan klart anbefale Nordicwebflow. De har lavet min hjemmeside, og resultatet er virkelig imponerende. Designet er flot, stilrent og professionelt — og vigtigst af alt, så spiller det hele bare.<br><br>Siden er 100% SEO-optimeret, så jeg står stærkt på Google, og der er virkelig tænkt over detaljerne hele vejen igennem. Derudover har de også hjulpet mig med optimering af mine sociale medier, så min virksomhed fremstår professionel og skarp på alle platforme.<br><br>Hele processen har været professionel fra start til slut med god dialog, hurtig respons og styr på tingene. Jeg kan varmt anbefale dem til alle, der vil tage deres online tilstedeværelse til næste niveau.</p>
      <div class="t-author">
        <img src="/images/Colorful_Graffiti_Circle_Framed_Instagram_Profile_Picture__1_.png" alt="Benjamin Wenneke — Ejer, Wenneke Tømrer &amp; Snedker ApS" class="t-avatar" width="52" height="52" loading="lazy">
        <div>
          <div class="t-name">Benjamin Wenneke</div>
          <div class="t-role">Ejer, Wenneke Tømrer &amp; Snedker ApS</div>
          <a href="https://wtsbyg.dk" class="t-link" target="_blank" rel="noopener noreferrer">wtsbyg.dk</a>
        </div>
      </div>
    </div>
  </div>
</section>"""

def CTA(h="Klar til en hjemmeside, der rent faktisk skaffer kunder?", p="Et gratis SEO-tjek fortæller dig, hvad der er galt. Vi bygger løsningen. Har du brug for en professionel hjemmeside, der indlæses på under ét sekund og rangerer lokalt på Google?"):
    return f"""<section>
  <div class="container">
    <div class="cta-section">
      <h2>{h}</h2>
      <p>{p}</p>
      <div class="cta-actions">
        <a href="/faa-et-tilbud" class="btn btn-primary btn-lg">Få et gratis tilbud →</a>
        <a href="/performancechecker" class="btn btn-ghost btn-lg">Gratis SEO-tjek</a>
      </div>
    </div>
  </div>
</section>"""

def FAQ_SECTION(faqs, badge="FAQ", title="Ofte stillede spørgsmål"):
    items = ''.join([f'<div class="faq-item"><button class="faq-q">{q}<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>' for q,a in faqs])
    return f"""<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">{badge}</span>
      <h2>{title}</h2>
    </div>
    <div class="faq-list">{items}</div>
  </div>
</section>"""

def PARTNER_SECTION():
    return """<section style="padding:60px 0">
  <div class="container">
    <div class="grid-2" style="gap:48px">
      <div>
        <span class="badge badge-orange" style="margin-bottom:16px">Din Partner</span>
        <h2 style="margin-bottom:14px">Din faste digitale partner i <span style="color:var(--orange)">København</span></h2>
        <p style="margin-bottom:20px">Vi gemmer os ikke bag forvirrende bureau-sprog eller lange ventetider. Hos NordicWebFlow får du direkte kontakt til specialisterne, der bygger din nye hjemmeside og skalerer din forretning.</p>
        <div style="display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:20px;">
          <img src="/images/1771542850470.jpg" alt="Diego Maldonado — Stifter af NordicWebFlow" style="width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid var(--border-orange);flex-shrink:0" width="64" height="64" loading="lazy">
          <div>
            <div style="font-family:var(--font-display);font-weight:700;color:var(--white);font-size:1rem">Diego Maldonado</div>
            <div style="font-size:.82rem;color:var(--muted)">Stifter &amp; Digital Strateg</div>
            <a href="mailto:hej@nordicwebflow.com" style="font-size:.8rem;color:var(--orange)">hej@nordicwebflow.com</a>
          </div>
        </div>
        <a href="/faa-et-tilbud" class="btn btn-primary" style="margin-top:20px">Se lanceringspriser →</a>
      </div>
      <div class="stats-row" style="align-self:center">
        <div style="text-align:center"><div class="s-val o">97</div><div class="s-lbl">PageSpeed</div></div>
        <div style="text-align:center"><div class="s-val g">&lt;1s</div><div class="s-lbl">Loadtid</div></div>
        <div style="text-align:center"><div class="s-val b">100%</div><div class="s-lbl">SEO Score</div></div>
        <div style="text-align:center"><div class="s-val p">14d</div><div class="s-lbl">Lancering</div></div>
      </div>
    </div>
  </div>
</section>"""

def SEO_BLOCK(text, links):
    link_html = ' · '.join([f'<a href="{u}">{l}</a>' for l,u in links])
    return f"""<div class="seo-block">
  <h3>Relaterede sider &amp; ydelser</h3>
  <p>{text}</p>
  <div class="internal-links">{link_html}</div>
</div>"""

def PRICING_CARDS():
    return """<div class="pricing-grid">
    <!-- STARTER -->
    <div class="pricing-card">
      <div class="pricing-label">Starter Pakke</div>
      <div class="pricing-name">Starter</div>
      <div class="pricing-price-row">
        <span class="pricing-old">25.000 kr.</span>
        <span class="pricing-price">14.999</span>
        <span class="pricing-currency">kr.</span>
      </div>
      <p class="pricing-desc">Engangsbeløb — ingen abonnement</p>
      <div>
        <div class="pricing-feature"><span class="check">✓</span>1-3 Undersider (Forside, Ydelser, Kontakt)</div>
        <div class="pricing-feature"><span class="check">✓</span>Lynhurtig indlæsningstid &amp; 100% mobiloptimeret</div>
        <div class="pricing-feature"><span class="check">✓</span>Brugervenlig kontaktformular &amp; CTA-knapper</div>
        <div class="pricing-feature"><span class="check">✓</span>Basal SEO-opsætning til Google</div>
        <div class="pricing-feature"><span class="check">✓</span>100% ejerskab — ingen skjulte abonnementer</div>
        <div class="pricing-feature"><span class="check">✓</span>Gratis hosting via Framer Free</div>
        <div class="pricing-feature"><span class="check">✓</span>Gratis .framer.website domæne</div>
      </div>
      <a href="/faa-et-tilbud" class="btn btn-ghost" style="width:100%;justify-content:center;margin-top:24px">Vælg Starter →</a>
      <p class="pricing-note">* Engangsbeløb. Sikker kortbetaling.</p>
    </div>
    <!-- PROFESSIONEL -->
    <div class="pricing-card featured">
      <div class="pricing-popular">Mest Populære</div>
      <div class="pricing-label">Professionel Pakke</div>
      <div class="pricing-name">Professionel</div>
      <div class="pricing-price-row">
        <span class="pricing-old">40.000 kr.</span>
        <span class="pricing-price">19.999</span>
        <span class="pricing-currency">kr.</span>
      </div>
      <p class="pricing-desc">Engangsbeløb — inkl. 1 års gratis hosting</p>
      <div>
        <div class="pricing-feature"><span class="check">✓</span>Alt fra Starter-pakken</div>
        <div class="pricing-feature"><span class="check">✓</span>Op til 8 undersider — vis dine specifikke ydelser</div>
        <div class="pricing-feature"><span class="check">✓</span>Sektion til cases, portefølje eller referencer</div>
        <div class="pricing-feature"><span class="check">✓</span>Lokal SEO-optimering til dit nærområde</div>
        <div class="pricing-feature"><span class="check">✓</span>Opsætning af kundeanmeldelser (Trustpilot/Google)</div>
        <div class="pricing-feature"><span class="check">✓</span>Hjælp til tekstforfatning</div>
        <div class="pricing-feature"><span class="check">✓</span>Nyt domæne (gratis 1 år) ELLER tilkobling af dit nuværende</div>
      </div>
      <a href="/faa-et-tilbud" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:24px">Vælg Professionel →</a>
      <p class="pricing-note">* Engangsbeløb. Sikker kortbetaling.</p>
    </div>
    <!-- PREMIUM+ -->
    <div class="pricing-card">
      <div class="pricing-label">Premium+ Pakke</div>
      <div class="pricing-name">Premium+</div>
      <div class="pricing-price-row">
        <span class="pricing-old">60.000 kr.</span>
        <span class="pricing-price">30.000</span>
        <span class="pricing-currency">kr.</span>
      </div>
      <p class="pricing-desc">Engangsbeløb — inkl. 1 år SEO management</p>
      <div>
        <div class="pricing-feature"><span class="check">✓</span>Alt fra Professionel-pakken</div>
        <div class="pricing-feature"><span class="check">✓</span>Op til 15 undersider</div>
        <div class="pricing-feature"><span class="check">✓</span>Dybdegående SEO &amp; Konverteringsoptimering (CRO)</div>
        <div class="pricing-feature"><span class="check">✓</span>Professionel tekstskrivning — vi skriver det hele</div>
        <div class="pricing-feature"><span class="check">✓</span>Skræddersyede landingssider til kampagner eller byer</div>
        <div class="pricing-feature"><span class="check">✓</span>Avanceret analyse &amp; tracking (Google Analytics/Meta Pixel)</div>
        <div class="pricing-feature"><span class="check">✓</span>Nyt domæne (gratis 1 år) ELLER tilkobling</div>
      </div>
      <a href="/faa-et-tilbud" class="btn btn-ghost" style="width:100%;justify-content:center;margin-top:24px">Vælg Premium+ →</a>
      <p class="pricing-note">* Engangsbeløb. Sikker kortbetaling.</p>
    </div>
  </div>"""

def PROCESS_STEPS():
    return """<div class="process-grid">
    <div class="process-step"><div class="process-num">01</div><h4>Bestilling &amp; Onboarding</h4><p>Vælg din pakke og betal sikkert online. Du modtager et kort skema til upload af logo, billeder og ønsker.</p></div>
    <div class="process-step"><div class="process-num">02</div><h4>Design &amp; Udvikling</h4><p>Vi går straks i gang. Din hjemmeside bygges i Framer med fokus på lynhurtig loadtid, moderne æstetik og høj konvertering.</p></div>
    <div class="process-step"><div class="process-num">03</div><h4>Gennemgang &amp; Tilpasning</h4><p>Inden for få hverdage sender vi dig det første udkast. Vi tilpasser til du er 100% tilfreds.</p></div>
    <div class="process-step"><div class="process-num">04</div><h4>Lancering &amp; Overdragelse</h4><p>Vi tilkobler dit domæne, opsætter Google Analytics og Search Console — og overdrager fuld ejerskab til dig.</p></div>
  </div>"""

# ─────────────────────────────────────────────
# PAGE: INDEX
# ─────────────────────────────────────────────
def page_index():
    schema = schema_localbusiness() + review_schema() + faq_schema(FAQS_HOME) + """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"NordicWebFlow","url":"https://nordicwebflow.com","potentialAction":{"@type":"SearchAction","target":"https://nordicwebflow.com/performancechecker?url={search_term_string}","query-input":"required name=search_term_string"}}
</script>"""
    return head(
        "Webbureau København — Professionelt Webdesign & Lokal SEO | NordicWebFlow",
        "Webbureau i København. Vi bygger lynhurtige hjemmesider i Framer med 97+ PageSpeed og 100% lokal SEO. Fra 2.999 kr. — du ejer siden 100%. Gratis SEO-tjek.",
        "/",
        extra=schema
    ) + f"""
<body>
{NAV()}
<!-- HERO -->
<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div class="fade-up">
        <div class="hero-label">
          <span class="badge badge-orange">⚡ Tidsbegrænset Lanceringstilbud — Kun 2 pladser tilbage</span>
        </div>
        <h1>Ny hjemmeside der <span>skaffer kunder</span>: Professionelt webdesign</h1>
        <p class="lead">Glem alt om langsomme skabeloner. Som dit lokale webbureau i København leverer vi professionelt webdesign og SEO optimering til ambitiøse virksomheder. Få en ny hjemmeside, du ejer 100% fra dag ét.</p>
        <div class="hero-actions">
          <a href="/priser" class="btn btn-primary btn-lg">Se priser &amp; bestil →</a>
          <a href="/performancechecker" class="btn btn-ghost btn-lg">Gratis hjemmeside test</a>
        </div>
        <div class="hero-stats">
          <div><div class="stat-val o">97</div><div class="stat-lbl">PageSpeed Score</div></div>
          <div><div class="stat-val g">&lt;1s</div><div class="stat-lbl">Loadtid</div></div>
          <div><div class="stat-val b">100%</div><div class="stat-lbl">SEO Optimeret</div></div>
          <div><div class="stat-val p">14d</div><div class="stat-lbl">Lancering</div></div>
        </div>
      </div>
      <div class="hero-visual fade-up d2">
        <img src="/images/azwedo-l-lc-6uR0dkm3ya0-unsplash.jpg" alt="Professionelt webdesign og SEO optimering til danske virksomheder vist på en bærbar computer" class="hero-img" width="600" height="450" loading="eager">
        <div class="hero-float hero-float-br">
          <div class="float-score">97</div>
          <div class="float-lbl">PageSpeed Score</div>
        </div>
        <div class="hero-float hero-float-tl">
          <div class="float-stars">★★★★★</div>
          <div class="float-review">"Resultatet er virkelig imponerende" — Benjamin W.</div>
        </div>
      </div>
    </div>
  </div>
</section>

{ticker()}

<!-- WHY US -->
<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Hvorfor NordicWebFlow</span>
      <h2>Dit Webbureau i København: Vi bygger mere end bare <span>pæne hjemmesider</span></h2>
      <p>De fleste virksomheder har hjemmesider der er langsomme, forældede og usynlige på Google. Det koster kunder hver eneste dag. Vi kombinerer premium design i Framer med benhård Lokal SEO.</p>
    </div>
    <div class="features-grid">
      <div class="card">
        <div class="card-icon">⚡</div>
        <h4>Lynhurtige Hjemmesider i Framer</h4>
        <p>Sub-1-sekunds loadtid og 97+ PageSpeed-score. Vi bygger udelukkende i Framer — platformen der slår WordPress og Wix på alle hastighedsmålinger.</p>
        <a href="/ydelser/lynhurtige-hjemmesider-framer" style="color:var(--orange);font-size:.87rem;margin-top:12px;display:inline-block">Fra 2.999 kr. — Læs mere →</a>
      </div>
      <div class="card">
        <div class="card-icon">📍</div>
        <h4>Lokal SEO Optimering i København</h4>
        <p>Dominér Google lokalt. Vi optimerer din Google Business Profile, bygger lokale citationer og sikrer, at din virksomhed dukker op når kunderne søger.</p>
        <a href="/ydelser/lokal-seo-koebenhavn" style="color:var(--orange);font-size:.87rem;margin-top:12px;display:inline-block">Fra 1.999 kr./md. — Læs mere →</a>
      </div>
      <div class="card">
        <div class="card-icon">📊</div>
        <h4>Google &amp; Meta Annoncering i København</h4>
        <p>Få kunder i morgen. Vi opsætter og styrer Google Ads og Meta Ads kampagner med fokus på lokal ROI — ikke vanity metrics.</p>
        <a href="/ydelser/google-meta-ads-koebenhavn" style="color:var(--orange);font-size:.87rem;margin-top:12px;display:inline-block">Læs mere om Ads →</a>
      </div>
    </div>
  </div>
</section>

<!-- SEO CHECKER CTA -->
<section style="padding:40px 0">
  <div class="container">
    <div style="background:var(--card2);border:1px solid var(--border-orange);border-radius:var(--radius-xl);padding:48px;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center">
      <div>
        <span class="badge badge-orange" style="margin-bottom:14px">Taber du kunder på Google lige nu?</span>
        <h2 style="font-size:clamp(1.5rem,3vw,2.2rem);margin-bottom:14px">Find ud af det på <span style="color:var(--orange)">60 sekunder</span> — helt gratis</h2>
        <p>De fleste lokale virksomheder ved ikke, at deres hjemmeside er usynlig på Google og mister dem kunder hver dag. Test din hjemmeside nu.</p>
        <a href="/performancechecker" class="btn btn-primary btn-lg" style="margin-top:24px">Få dit gratis SEO-tjek nu →</a>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px">
        <div style="display:flex;justify-content:space-between;margin-bottom:16px">
          <span style="font-size:.8rem;color:var(--muted)">Live SEO Analyse</span>
          <span style="font-size:.75rem;color:var(--green)">● Live analyse</span>
        </div>
        <div style="display:flex;align-items:center;gap:20px;margin-bottom:20px">
          <div style="width:80px;height:80px;border-radius:50%;border:4px solid var(--orange);display:flex;align-items:center;justify-content:center;flex-shrink:0">
            <span style="font-family:var(--font-display);font-weight:800;font-size:1.6rem;color:var(--orange)">97</span>
          </div>
          <div style="flex:1">
            <div style="display:flex;justify-content:space-between;font-size:.8rem;color:var(--muted);margin-bottom:6px"><span>Loadtid</span><span style="color:var(--green)">0.8s</span></div>
            <div style="height:4px;background:var(--border);border-radius:2px;margin-bottom:8px"><div style="width:95%;height:100%;background:var(--green);border-radius:2px"></div></div>
            <div style="display:flex;justify-content:space-between;font-size:.8rem;color:var(--muted);margin-bottom:6px"><span>SEO Score</span><span style="color:var(--orange)">100</span></div>
            <div style="height:4px;background:var(--border);border-radius:2px"><div style="width:100%;height:100%;background:var(--orange);border-radius:2px"></div></div>
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;text-align:center;padding-top:16px;border-top:1px solid var(--border)">
          <div><div style="font-family:var(--font-display);font-weight:800;color:var(--muted)">42</div><div style="font-size:.68rem;color:var(--muted2);text-transform:uppercase">Konkurrent gns.</div></div>
          <div><div style="font-family:var(--font-display);font-weight:800;color:var(--orange)">97</div><div style="font-size:.68rem;color:var(--muted2);text-transform:uppercase">NordicWebFlow</div></div>
          <div><div style="font-family:var(--font-display);font-weight:800;color:var(--green)">+131%</div><div style="font-size:.68rem;color:var(--muted2);text-transform:uppercase">Forbedring</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- TRUST PILLARS -->
<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Din sikkerhed</span>
      <h2>Gennemsigtige priser: <span>Ingen overraskelser</span></h2>
      <p>Vi ved, at du har travlt med at drive din forretning. Derfor gør vi den digitale del utrolig nem, gennemskuelig og 100% til at regne med.</p>
    </div>
    <div class="features-grid">
      <div class="card">
        <div class="card-icon">💰</div>
        <h4>Fast Projektpris</h4>
        <p>Du betaler en fast, lav pris for din hjemmeside. Ingen uforudsete regninger eller dyre bureau-abonnementer. Du ejer siden 100% fra dag ét.</p>
        <a href="/priser" style="color:var(--orange);font-size:.87rem;margin-top:12px;display:inline-block">Se vores priser →</a>
      </div>
      <div class="card">
        <div class="card-icon">🔑</div>
        <h4>100% Ejerskab</h4>
        <p>Du bliver ikke fanget i et dyrt leje-abonnement. Når siden er betalt, er den din — for altid. Koden, domænet, alt.</p>
        <a href="/cases" style="color:var(--orange);font-size:.87rem;margin-top:12px;display:inline-block">Se vores cases →</a>
      </div>
      <div class="card">
        <div class="card-icon">📞</div>
        <h4>Hurtig Support</h4>
        <p>Vi sidder i København og er altid til at få fat på, når du har brug for ændringer. Ingen lange ventetider eller anonyme supportsystemer.</p>
        <a href="/kontakt" style="color:var(--orange);font-size:.87rem;margin-top:12px;display:inline-block">Kontakt os →</a>
      </div>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section style="background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Vores Proces</span>
      <h2>Sådan laver vi din nye hjemmeside: <span>Fra idé til lancering</span></h2>
      <p>Fra første møde til færdig salgsmaskine på under 14 dage.</p>
    </div>
    {PROCESS_STEPS()}
    <div style="text-align:center;margin-top:36px">
      <a href="/priser" class="btn btn-primary">Se priser &amp; kom i gang →</a>
    </div>
  </div>
</section>

{TESTIMONIAL()}

{FAQ_SECTION(FAQS_HOME, "FAQ", "Alt du vil vide om NordicWebFlow")}

{PARTNER_SECTION()}

<!-- INDUSTRIES -->
<section style="background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Brancher vi betjener</span>
      <h2>Vi kender din branche — <span>og dine kunder</span></h2>
      <p>Vi har dybdegående erfaring med at bygge hjemmesider og SEO til specifikke håndværks- og servicebrancher i København.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
      {"".join([f'<a href="/{slug}" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px;display:flex;align-items:center;gap:10px;font-size:.9rem;font-weight:600;color:var(--text);transition:all var(--t)" onmouseover="this.style.borderColor=\'var(--border-orange)\'" onmouseout="this.style.borderColor=\'var(--border)\'">{icon} {name}</a>' for name,slug,icon in [
        ("Tømrer","toemrer","🔨"),("Tandlæge","tandlaege","🦷"),("Advokat","advokat","⚖️"),
        ("Murer","murer","🧱"),("Elektriker","elektriker","⚡"),("Maler","maler","🎨"),
        ("VVS","vvs","🔧"),("Fysioterapeut","fysioterapeut","💪"),("Revisor","revisor","📊"),
        ("Ejendomsmægler","ejendomsmaegler","🏠"),("Arkitekt","arkitekt","📐"),("Se alle","ydelser","→"),
      ]])}
    </div>
  </div>
</section>

{CTA()}

{SEO_BLOCK(
  "NordicWebFlow er et webbureau i København der specialiserer sig i lynhurtige hjemmesider i Framer og lokal SEO til håndværkere og servicefirmaer. Vi tilbyder professionelt webdesign fra 2.999 kr. med 100% ejerskab og sub-1-sekunds loadtid. Brug vores gratis SEO-analyseværktøj på seotjek.dk til at teste din nuværende hjemmeside.",
  [("Webdesign til tømrere","/toemrer"),("Lokal SEO København","/ydelser/lokal-seo-koebenhavn"),
   ("Gratis SEO-tjek","https://seotjek.dk"),("Priser & pakker","/priser"),
   ("Cases & resultater","/cases"),("Kontakt os","/kontakt")]
)}

{FOOT()}
{SCR()}
</body>
</html>"""

# ─────────────────────────────────────────────
# PAGE: PRISER
# ─────────────────────────────────────────────
def page_priser():
    faqs = [
        ("Hvad er forskellen på Starter og Professionel?","Starter er til 1-3 sider — perfekt til simple visitkortsider. Professionel giver op til 8 sider, lokal SEO og 1 år gratis hosting."),
        ("Er der skjulte gebyrer?","Nej. Du betaler den viste pris én gang og ejer siden 100%. Den eneste løbende udgift er Framer-hosting (ca. 800 kr./år) efter 1 år — og det betaler du direkte."),
        ("Kan jeg opgradere min pakke senere?","Ja, du kan altid tilkøbe flere sider eller SEO-ydelser efterfølgende."),
        ("Hvornår og hvordan betaler jeg?","Du betaler sikkert online med kort. Hele beløbet ved bestilling — ingen rater."),
        ("Hvad sker der efter mine 14 dage?","Vi leverer som regel inden 14 dage. Herefter fortsætter vi med rettelser indtil du er 100% tilfreds."),
        ("Er Lokal SEO en separat ydelse?","Ja, Lokal SEO-abonnementet er en tillægsydelse til 1.999 kr./md. uden bindingsperiode."),
    ]
    schema = faq_schema(faqs) + """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList","name":"NordicWebFlow Webdesign Pakker","itemListElement":[
{"@type":"Offer","position":1,"name":"Starter","price":"14999","priceCurrency":"DKK","description":"1-3 undersider, lynhurtig loadtid, basal SEO"},
{"@type":"Offer","position":2,"name":"Professionel","price":"19999","priceCurrency":"DKK","description":"Op til 8 sider, lokal SEO, 1 år hosting"},
{"@type":"Offer","position":3,"name":"Premium+","price":"30000","priceCurrency":"DKK","description":"Op til 15 sider, fuld SEO, tekstskrivning, 1 år SEO management"}
]}</script>"""
    return head(
        "Priser på Hjemmeside til din Virksomhed — Fra 14.999 kr. | NordicWebFlow",
        "Se vores priser på professionelt webdesign i Framer. Starter fra 14.999 kr., Professionel fra 19.999 kr. og Premium+ fra 30.000 kr. Ingen skjulte gebyrer — du ejer siden 100%.",
        "/priser", extra=schema
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">⚡ Tidsbegrænset Lanceringstilbud</span>
    <h1>Hvad koster en ny hjemmeside? <span>Se vores priser</span></h1>
    <p class="lead">Få en premium hjemmeside, der skaffer kunder, til en brøkdel af bureauprisen. Du betaler kun én gang, og du ejer siden 100%.</p>
  </div>
</div>

<section>
  <div class="container">
    {PRICING_CARDS()}
    <p style="text-align:center;font-size:.82rem;color:var(--muted2);margin-top:20px">For Professionel og Premium+ er 1 års lynhurtig hosting og evt. nyt domæne fuldt inkluderet. Herefter betaler du direkte til Framer (ca. 800-1.000 kr./år).</p>
  </div>
</section>

<!-- LOKAL SEO -->
<section style="background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-header">
      <span class="badge badge-green">Mest efterspurgte tillæg</span>
      <h2>Lokal SEO <span>Vækst-abonnement</span></h2>
    </div>
    <div style="max-width:560px;margin:0 auto;background:var(--card2);border:1px solid var(--green);border-radius:var(--radius-xl);padding:36px;position:relative">
      <div style="position:absolute;top:-13px;left:50%;transform:translateX(-50%);background:var(--green);color:#fff;padding:4px 16px;border-radius:999px;font-size:.73rem;font-weight:700;white-space:nowrap;font-family:var(--font-display)">Mest Efterspurgte</div>
      <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:4px">
        <span style="font-size:.95rem;color:var(--muted2);text-decoration:line-through">4.000 kr./md.</span>
        <span style="font-family:var(--font-display);font-weight:800;font-size:2.4rem;color:var(--white)">1.999</span>
        <span style="color:var(--muted)">kr./md.</span>
      </div>
      <p style="font-size:.85rem;color:var(--muted);margin-bottom:24px">Månedligt abonnement — ingen bindingsperiode. Opsig med 30 dages varsel.</p>
      <div class="pricing-feature"><span class="check">✓</span>Optimering af Google Business Profile</div>
      <div class="pricing-feature"><span class="check">✓</span>Månedlig lokal keyword-tracking</div>
      <div class="pricing-feature"><span class="check">✓</span>On-page SEO-opdateringer (metatitler, tekst, struktur)</div>
      <div class="pricing-feature"><span class="check">✓</span>Simpel månedlig rapport — ingen 40-siders konsulentrapport</div>
      <div class="pricing-feature"><span class="check">✓</span>Prioriteret support via telefon og e-mail</div>
      <div class="pricing-feature"><span class="check">✓</span>Tilpasses din branche og dit lokalområde i København</div>
      <a href="/faa-et-tilbud" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:24px">Start Lokal SEO →</a>
      <p style="font-size:.73rem;color:var(--muted2);margin-top:12px;text-align:center">Lokal SEO er en tillægsydelse. For bedste resultat anbefaler vi en aktiv NordicWebFlow hjemmeside.</p>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Vores Proces</span>
      <h2>Fra bestilling til <span>køreklar hjemmeside</span> på rekordtid</h2>
    </div>
    {PROCESS_STEPS()}
  </div>
</section>

{FAQ_SECTION(faqs, "FAQ", "Spørgsmål om vores priser")}

{CTA("Klar til at starte?","Vælg din pakke og få en professionel hjemmeside der skaffer kunder — på under 14 dage.")}

{SEO_BLOCK(
  "NordicWebFlow tilbyder professionelt webdesign til faste priser. Vores Starter-pakke koster 14.999 kr., Professionel 19.999 kr. og Premium+ 30.000 kr. Alle priser er engangsbeløb uden skjulte abonnementer. Vi tilbyder også lokal SEO-abonnement fra 1.999 kr./md. uden bindingsperiode.",
  [("Webdesign til tømrere","/toemrer"),("Lokal SEO København","/ydelser/lokal-seo-koebenhavn"),
   ("Se vores cases","/cases"),("Kontakt os","/kontakt"),("Gratis SEO-tjek","https://seotjek.dk")]
)}
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# PAGE: CASES
# ─────────────────────────────────────────────
def page_cases():
    return head(
        "Cases & Resultater — Webdesign der Skaber Vækst | NordicWebFlow",
        "Se vores webdesign cases. Vi har hjulpet lokale virksomheder i København med professionelle hjemmesider, lokal SEO og Google Ads. Læs om resultaterne.",
        "/cases"
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Dokumenterede resultater</span>
    <h1>Webdesign Cases: Resultater der <span>skaber vækst</span></h1>
    <p class="lead">Vi bygger ikke bare hjemmesider — vi bygger forretninger. Udforsk vores seneste projekter og se, hvordan vi har forvandlet lokale virksomheder til digitale markedsledere.</p>
  </div>
</div>
<section>
  <div class="container">
    <!-- WENNEKE CASE -->
    <div style="background:var(--card2);border:1px solid var(--border-orange);border-radius:var(--radius-xl);overflow:hidden;margin-bottom:32px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0">
        <div style="padding:40px">
          <span class="badge badge-orange" style="margin-bottom:16px">Tømrer &amp; Snedker</span>
          <h2 style="font-size:1.7rem;margin-bottom:8px">Wenneke Tømrer &amp; Snedker ApS</h2>
          <a href="https://wtsbyg.dk" target="_blank" rel="noopener noreferrer" style="color:var(--orange);font-size:.85rem;text-decoration:underline;display:block;margin-bottom:20px">wtsbyg.dk</a>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px">
            <div style="text-align:center;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:12px">
              <div style="font-family:var(--font-display);font-weight:800;font-size:1.5rem;color:var(--orange)">97</div>
              <div style="font-size:.68rem;color:var(--muted);text-transform:uppercase">PageSpeed</div>
            </div>
            <div style="text-align:center;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:12px">
              <div style="font-family:var(--font-display);font-weight:800;font-size:1.5rem;color:var(--green)">&lt;1s</div>
              <div style="font-size:.68rem;color:var(--muted);text-transform:uppercase">Loadtid</div>
            </div>
            <div style="text-align:center;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:12px">
              <div style="font-family:var(--font-display);font-weight:800;font-size:1.5rem;color:var(--blue)">100%</div>
              <div style="font-size:.68rem;color:var(--muted);text-transform:uppercase">SEO Score</div>
            </div>
          </div>
          <div class="t-stars">★★★★★</div>
          <p style="color:var(--text);font-size:.93rem;line-height:1.8;margin-bottom:16px">"Jeg kan klart anbefale Nordicwebflow. De har lavet min hjemmeside, og resultatet er virkelig imponerende. Designet er flot, stilrent og professionelt — og vigtigst af alt, så spiller det hele bare."</p>
          <div style="font-family:var(--font-display);font-weight:700;color:var(--white);font-size:.9rem">Benjamin Wenneke</div>
          <div style="font-size:.8rem;color:var(--muted)">Ejer, Wenneke Tømrer &amp; Snedker ApS</div>
        </div>
        <div style="background:var(--bg3);display:flex;align-items:center;justify-content:center;padding:32px">
          <img src="/images/Image.png" alt="Wenneke Tømrer hjemmeside bygget af NordicWebFlow — professionelt webdesign til tømrere" style="border-radius:var(--radius-lg);border:1px solid var(--border);max-width:100%" width="500" height="350" loading="lazy">
        </div>
      </div>
    </div>

    <!-- COMING SOON -->
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px">
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius-xl);padding:40px;text-align:center;opacity:.6">
        <div style="font-size:2rem;margin-bottom:16px">🔜</div>
        <h3 style="margin-bottom:8px">Kommende case</h3>
        <p style="font-size:.87rem">Vi arbejder på vores næste projekt. Resultaterne deles her snart.</p>
      </div>
      <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius-xl);padding:40px;text-align:center;opacity:.6">
        <div style="font-size:2rem;margin-bottom:16px">🔜</div>
        <h3 style="margin-bottom:8px">Kommende case</h3>
        <p style="font-size:.87rem">Bliv den næste succes-case. Kontakt os i dag.</p>
        <a href="/faa-et-tilbud" class="btn btn-primary btn-sm" style="margin-top:16px;opacity:1">Bliv vores næste case →</a>
      </div>
    </div>
  </div>
</section>

{FAQ_SECTION([
  ("Hvad kan jeg forvente af et samarbejde?","Du kan forvente en professionel, lynhurtig hjemmeside leveret på under 14 dage med 100% ejerskab."),
  ("Kan I vise resultater for min branche?","Vi arbejder med håndværkere, klinikker og servicefirmaer i København. Kontakt os for at se relevante cases."),
  ("Giver I garanti for resultater?","Vi garanterer teknisk kvalitet — sub-1-sekunds loadtid og 97+ PageSpeed. SEO-resultater afhænger af konkurrencen i din branche."),
], "FAQ", "Spørgsmål om vores cases")}

{CTA("Bliv vores næste succes-case","Kontakt os i dag og find ud af, hvad vi kan gøre for din virksomhed.")}

{SEO_BLOCK(
  "Se NordicWebFlows webdesign cases og resultater. Vi specialiserer os i hjemmesider til håndværkere og lokale servicefirmaer i København. Brug vores gratis SEO-analyseværktøj på seotjek.dk til at analysere din nuværende hjemmeside.",
  [("Webdesign til tømrere","/toemrer"),("Priser","/priser"),("Gratis SEO-tjek","https://seotjek.dk")]
)}
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# PAGE: PERFORMANCE CHECKER
# ─────────────────────────────────────────────
def page_checker():
    return head(
        "Gratis SEO-tjek af Din Hjemmeside — Test på 60 sekunder | NordicWebFlow",
        "Få et gratis SEO-tjek af din hjemmeside. Test loadtid, mobiloptimering og Google-synlighed på 60 sekunder. Powered by Google PageSpeed Insights.",
        "/performancechecker"
    ) + f"""
<body>
{NAV()}
<div class="page-hero" style="text-align:center">
  <div class="container">
    <span class="badge badge-orange">Gratis SEO-tjek</span>
    <h1>Test din hjemmeside på <span>60 sekunder</span></h1>
    <p class="lead" style="margin:14px auto 0;max-width:520px">Find ud af hvad der koster dig kunder på Google. Vores gratis SEO-analyseværktøj giver dig en øjeblikkelig rapport om din hjemmesides performance.</p>
  </div>
</div>
<section>
  <div class="container" style="max-width:720px">
    <div style="background:var(--card2);border:1px solid var(--border-orange);border-radius:var(--radius-xl);padding:40px">
      <h2 style="font-size:1.4rem;margin-bottom:8px">Analysér din hjemmeside nu</h2>
      <p style="margin-bottom:24px;font-size:.9rem">Skriv din hjemmesideadresse og få en øjeblikkelig SEO-analyse. Powered by <a href="https://seotjek.dk" target="_blank" rel="noopener noreferrer" style="color:var(--orange);text-decoration:underline">seotjek.dk</a> — Danmarks gratis SEO-analyseværktøj.</p>
      <div style="display:flex;gap:10px;margin-bottom:12px">
        <input type="url" id="url-input" class="form-input" placeholder="https://dinhjemmeside.dk" style="flex:1">
        <button onclick="runCheck()" class="btn btn-primary">Analysér →</button>
      </div>
      <p style="font-size:.75rem;color:var(--muted2)">Vi gemmer ikke din URL. Analysen er 100% gratis og uden forpligtelse.</p>
      <div id="checker-loading" style="display:none;text-align:center;padding:32px 0">
        <div style="font-size:2rem;margin-bottom:12px">🔍</div>
        <p>Analyserer din hjemmeside...</p>
      </div>
      <div id="checker-result" style="display:none;margin-top:28px">
        <div style="display:flex;align-items:center;gap:20px;margin-bottom:24px">
          <div style="width:90px;height:90px;border-radius:50%;border:5px solid var(--orange);display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0">
            <div id="score-num" style="font-family:var(--font-display);font-weight:800;font-size:1.8rem;color:var(--orange)">—</div>
            <div style="font-size:.6rem;color:var(--muted);text-transform:uppercase">Score</div>
          </div>
          <div style="flex:1">
            <h3 style="font-size:1.1rem;margin-bottom:4px" id="score-verdict">Din hjemmeside er analyseret</h3>
            <p style="font-size:.87rem" id="score-desc">Se detaljerne nedenfor.</p>
          </div>
        </div>
        <div id="score-details"></div>
        <div style="margin-top:24px;padding:20px;background:var(--card);border:1px solid var(--border-orange);border-radius:var(--radius);text-align:center">
          <p style="font-size:.9rem;color:var(--text);margin-bottom:12px">Vil du have en professionel hjemmeside med 97+ PageSpeed og 100% SEO?</p>
          <a href="/faa-et-tilbud" class="btn btn-primary">Få et gratis tilbud →</a>
        </div>
      </div>
    </div>

    <!-- WHAT WE CHECK -->
    <div style="margin-top:32px">
      <h2 style="font-size:1.4rem;margin-bottom:20px">Hvad tjekker vores gratis SEO-analyse?</h2>
      <div class="grid-3">
        <div class="card"><div class="card-icon">⚡</div><h4>PageSpeed Score</h4><p style="font-size:.87rem">Vi måler din hjemmesides loadtid og PageSpeed-score via Google PageSpeed Insights.</p></div>
        <div class="card"><div class="card-icon">📱</div><h4>Mobiloptimering</h4><p style="font-size:.87rem">Vi tjekker om din hjemmeside er mobilvenlig — afgørende da 60%+ af søgningerne sker på mobil.</p></div>
        <div class="card"><div class="card-icon">🔍</div><h4>SEO Score</h4><p style="font-size:.87rem">Vi analyserer teknisk SEO inkl. meta-tags, SSL-certifikat og grundlæggende on-page faktorer.</p></div>
      </div>
    </div>

    <div style="margin-top:28px;padding:24px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);text-align:center">
      <p style="font-size:.9rem;color:var(--text);margin-bottom:8px">For en endnu mere dybdegående gratis SEO-analyse — prøv Danmarks bedste gratis SEO-tjek:</p>
      <a href="https://seotjek.dk" target="_blank" rel="noopener noreferrer" class="btn btn-ghost btn-sm">Besøg seotjek.dk — Danmarks gratis SEO-analyseværktøj →</a>
    </div>
  </div>
</section>

{CTA()}
{FOOT()}
<script>
async function runCheck(){{
  const url=document.getElementById('url-input').value.trim();
  if(!url){{alert('Indtast venligst en URL');return;}}
  document.getElementById('checker-loading').style.display='block';
  document.getElementById('checker-result').style.display='none';
  try{{
    const key='AIzaSyExample_replace_with_real_key';
    const apiUrl=`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${{encodeURIComponent(url)}}&strategy=mobile`;
    const r=await fetch(apiUrl);
    const d=await r.json();
    const score=Math.round((d.lighthouseResult?.categories?.performance?.score||0)*100);
    document.getElementById('score-num').textContent=score;
    const verdict=score>=90?'Din hjemmeside er hurtig! 🎉':score>=50?'Din hjemmeside har forbedringspotentiale ⚠️':'Din hjemmeside er langsom — det koster kunder ❌';
    const desc=score>=90?'God performance. Vi kan hjælpe dig med at optimere SEO og konvertering yderligere.':score<50?'En langsom hjemmeside mister kunder. NordicWebFlow kan hjælpe med en lynhurtig ny hjemmeside.':'Der er plads til forbedringer. Kontakt os for at se hvad vi kan gøre.';
    document.getElementById('score-verdict').textContent=verdict;
    document.getElementById('score-desc').textContent=desc;
    document.getElementById('score-details').innerHTML=`<div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px"><p style="font-size:.85rem;color:var(--muted)">Score ${{score}}/100 — <a href="https://seotjek.dk" target="_blank" style="color:var(--orange);text-decoration:underline">Få en fuld gratis SEO-analyse på seotjek.dk</a></p></div>`;
  }}catch(e){{
    document.getElementById('score-verdict').textContent='Analysen mislykkedes';
    document.getElementById('score-desc').textContent='Tjek URL og prøv igen, eller besøg seotjek.dk for en manuel analyse.';
    document.getElementById('score-details').innerHTML='';
  }}
  document.getElementById('checker-loading').style.display='none';
  document.getElementById('checker-result').style.display='block';
}}
document.getElementById('url-input').addEventListener('keydown',e=>{{if(e.key==='Enter')runCheck();}});
{SCR().replace('<script>','').replace('</script>','')}
</script>
</body></html>"""

# ─────────────────────────────────────────────
# PAGE: CONTACT
# ─────────────────────────────────────────────
def page_kontakt():
    return head(
        "Kontakt NordicWebFlow — Webbureau København | hej@nordicwebflow.com",
        "Kontakt NordicWebFlow. Vi er et webbureau i København der bygger professionelle hjemmesider og lokal SEO. Skriv til hej@nordicwebflow.com eller udfyld formularen.",
        "/kontakt"
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Kontakt os</span>
    <h1>Lad os tale om <span>din næste hjemmeside</span></h1>
    <p class="lead">Vi sidder i København og svarer normalt inden for én hverdag. Ingen forpligtelse — bare en ærlig snak om, hvad vi kan gøre for din virksomhed.</p>
  </div>
</div>
<section>
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start">
      <div>
        <h2 style="font-size:1.6rem;margin-bottom:24px">Send os en besked</h2>
        <form name="kontakt" method="POST" action="/tak">
          <div class="form-group">
            <label class="form-label">Dit navn *</label>
            <input type="text" name="navn" class="form-input" placeholder="Jens Jensen" required>
          </div>
          <div class="form-group">
            <label class="form-label">Din e-mail *</label>
            <input type="email" name="email" class="form-input" placeholder="jens@dinvirksomhed.dk" required>
          </div>
          <div class="form-group">
            <label class="form-label">Telefonnummer</label>
            <input type="tel" name="telefon" class="form-input" placeholder="+45 12 34 56 78">
          </div>
          <div class="form-group">
            <label class="form-label">Virksomhedsnavn</label>
            <input type="text" name="virksomhed" class="form-input" placeholder="Din Virksomhed ApS">
          </div>
          <div class="form-group">
            <label class="form-label">Hvad kan vi hjælpe med?</label>
            <select name="ydelse" class="form-select">
              <option value="">Vælg ydelse...</option>
              <option>Ny hjemmeside — Starter pakke</option>
              <option>Ny hjemmeside — Professionel pakke</option>
              <option>Ny hjemmeside — Premium+ pakke</option>
              <option>Lokal SEO abonnement</option>
              <option>Google &amp; Meta Ads</option>
              <option>Andet</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Din besked</label>
            <textarea name="besked" class="form-textarea" placeholder="Fortæl os kort om din virksomhed og hvad du ønsker hjælp til..."></textarea>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center">Send besked →</button>
        </form>
      </div>
      <div>
        <div class="card" style="margin-bottom:20px">
          <h4 style="margin-bottom:12px">Direkte kontakt</h4>
          <div style="display:flex;flex-direction:column;gap:12px">
            <a href="mailto:hej@nordicwebflow.com" style="display:flex;align-items:center;gap:10px;color:var(--text);font-size:.9rem"><span style="color:var(--orange)">✉</span> hej@nordicwebflow.com</a>
            <span style="display:flex;align-items:center;gap:10px;color:var(--text);font-size:.9rem"><span style="color:var(--orange)">📍</span> København, Danmark</span>
            <span style="display:flex;align-items:center;gap:10px;color:var(--text);font-size:.9rem"><span style="color:var(--orange)">🕐</span> Man-fre: 09:00 — 18:00</span>
            <span style="display:flex;align-items:center;gap:10px;color:var(--text);font-size:.9rem"><span style="color:var(--orange)">📋</span> CVR: 46305639</span>
          </div>
        </div>
        <div style="background:var(--card2);border:1px solid var(--border-orange);border-radius:var(--radius-lg);padding:24px">
          <div class="t-stars" style="margin-bottom:10px">★★★★★</div>
          <p style="font-size:.87rem;color:var(--text);line-height:1.7;margin-bottom:14px">"Hele processen har været professionel fra start til slut med god dialog, hurtig respons og styr på tingene."</p>
          <div style="font-size:.82rem;font-weight:700;color:var(--white)">Benjamin Wenneke</div>
          <div style="font-size:.75rem;color:var(--muted)">Ejer, Wenneke Tømrer &amp; Snedker ApS</div>
        </div>
        <div class="card" style="margin-top:20px">
          <h4 style="margin-bottom:8px">Foretrækker du et hurtigt tilbud?</h4>
          <p style="font-size:.87rem;margin-bottom:14px">Udfyld vores tilbudsformular og få svar inden for 24 timer.</p>
          <a href="/faa-et-tilbud" class="btn btn-primary btn-sm">Få et tilbud →</a>
        </div>
      </div>
    </div>
  </div>
</section>
{SEO_BLOCK(
  "NordicWebFlow er et webbureau i København med direkte kontakt til specialisterne. Vi besvarer alle henvendelser inden for én hverdag. Brug vores gratis SEO-analyseværktøj på seotjek.dk til at analysere din nuværende hjemmeside inden du kontakter os.",
  [("Priser","/priser"),("Cases","/cases"),("Gratis SEO-tjek","https://seotjek.dk"),("Få et tilbud","/faa-et-tilbud")]
)}
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# PAGE: FAA ET TILBUD
# ─────────────────────────────────────────────
def page_tilbud():
    return head(
        "Få et Gratis Tilbud på Din Hjemmeside | NordicWebFlow — Webbureau København",
        "Få et gratis, uforpligtende tilbud på din nye hjemmeside fra NordicWebFlow. Vi svarer inden for 24 timer. Fra 2.999 kr. — 100% ejerskab, ingen skjulte gebyrer.",
        "/faa-et-tilbud"
    ) + f"""
<body>
{NAV()}
<div class="page-hero" style="text-align:center">
  <div class="container">
    <span class="badge badge-green">Gratis &amp; uforpligtende</span>
    <h1>Få et tilbud på din <span>nye hjemmeside</span></h1>
    <p class="lead" style="margin:14px auto 0;max-width:520px">Udfyld formularen og modtag et personligt tilbud inden for 24 timer. Ingen forpligtelse — bare en ærlig pris.</p>
  </div>
</div>
<section>
  <div class="container" style="max-width:680px">
    <div style="background:var(--card2);border:1px solid var(--border-orange);border-radius:var(--radius-xl);padding:40px">
      <form name="tilbud" method="POST" action="/tak">
        <div class="form-group">
          <label class="form-label">Dit navn *</label>
          <input type="text" name="navn" class="form-input" placeholder="Jens Jensen" required>
        </div>
        <div class="form-group">
          <label class="form-label">E-mail *</label>
          <input type="email" name="email" class="form-input" placeholder="jens@dinvirksomhed.dk" required>
        </div>
        <div class="form-group">
          <label class="form-label">Telefon</label>
          <input type="tel" name="telefon" class="form-input" placeholder="+45 12 34 56 78">
        </div>
        <div class="form-group">
          <label class="form-label">Virksomhedsnavn &amp; branche *</label>
          <input type="text" name="virksomhed" class="form-input" placeholder="Jensen Tømrer ApS — tømrer" required>
        </div>
        <div class="form-group">
          <label class="form-label">Hvilken pakke interesserer dig? *</label>
          <select name="pakke" class="form-select" required>
            <option value="">Vælg pakke...</option>
            <option>Starter — 14.999 kr.</option>
            <option>Professionel — 19.999 kr. (Mest populær)</option>
            <option>Premium+ — 30.000 kr.</option>
            <option>Lokal SEO abonnement — 1.999 kr./md.</option>
            <option>Jeg er ikke sikker — rådgiv mig</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Har du en eksisterende hjemmeside?</label>
          <input type="url" name="eksisterende" class="form-input" placeholder="https://dineksisterende.dk (valgfrit)">
        </div>
        <div class="form-group">
          <label class="form-label">Beskriv kort din virksomhed og dine mål</label>
          <textarea name="besked" class="form-textarea" placeholder="Vi er en tømrervirksomhed i København med 3 ansatte. Vi ønsker at tiltrække flere kunder via Google og have en professionel hjemmeside..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-lg" style="width:100%;justify-content:center">Send tilbudsforespørgsel →</button>
        <p style="font-size:.75rem;color:var(--muted2);text-align:center;margin-top:12px">Du hører fra os inden for 24 timer på hverdage. Ingen forpligtelse.</p>
      </form>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:24px">
      <div style="text-align:center;padding:16px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius)"><div style="color:var(--green);font-size:1.3rem;margin-bottom:6px">✓</div><div style="font-size:.82rem;color:var(--text);font-weight:600">100% gratis</div></div>
      <div style="text-align:center;padding:16px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius)"><div style="color:var(--green);font-size:1.3rem;margin-bottom:6px">✓</div><div style="font-size:.82rem;color:var(--text);font-weight:600">Svar inden 24t</div></div>
      <div style="text-align:center;padding:16px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius)"><div style="color:var(--green);font-size:1.3rem;margin-bottom:6px">✓</div><div style="font-size:.82rem;color:var(--text);font-weight:600">Ingen forpligtelse</div></div>
    </div>
  </div>
</section>
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# PAGE: TAK
# ─────────────────────────────────────────────
def page_tak():
    return head("Tak for din henvendelse! | NordicWebFlow","Din besked er modtaget. Vi vender tilbage inden for 24 timer.","/tak") + f"""
<body>
{NAV()}
<div class="tak-page">
  <div class="container">
    <div class="tak-icon">🎉</div>
    <h1 style="margin-bottom:14px">Tak for din henvendelse!</h1>
    <p class="lead" style="max-width:480px;margin:0 auto 28px">Vi har modtaget din besked og vender tilbage inden for én hverdag. Glæder os til at høre mere om dit projekt.</p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      <a href="/" class="btn btn-ghost">Tilbage til forsiden</a>
      <a href="/performancechecker" class="btn btn-primary">Få et gratis SEO-tjek →</a>
    </div>
    <div style="margin-top:48px;max-width:480px;margin-left:auto;margin-right:auto">
      <div class="card" style="text-align:center">
        <p style="font-size:.87rem;margin-bottom:12px">Mens du venter — test din nuværende hjemmeside gratis på:</p>
        <a href="https://seotjek.dk" target="_blank" rel="noopener noreferrer" class="btn btn-ghost btn-sm">seotjek.dk — Gratis SEO-analyseværktøj →</a>
      </div>
    </div>
  </div>
</div>
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# PAGE: 404
# ─────────────────────────────────────────────
def page_404():
    return head("Side ikke fundet — 404 | NordicWebFlow","Siden du leder efter findes ikke. Gå tilbage til forsiden eller kontakt os.","/404") + f"""
<body>
{NAV()}
<div class="notfound">
  <div class="container">
    <div class="big-num">404</div>
    <h2>Siden findes ikke</h2>
    <p style="margin-bottom:28px">Siden du leder efter er enten flyttet eller findes ikke. Brug menuerne ovenfor eller gå tilbage til forsiden.</p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      <a href="/" class="btn btn-primary">Gå til forsiden →</a>
      <a href="/kontakt" class="btn btn-ghost">Kontakt os</a>
    </div>
  </div>
</div>
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# PAGE: LEGAL
# ─────────────────────────────────────────────
def page_legal():
    return head("Privatlivspolitik & Cookiepolitik | NordicWebFlow","Læs NordicWebFlows privatlivspolitik og cookiepolitik. GDPR-compliant. Sidst opdateret 4. marts 2026.","/legal") + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-white">Juridisk</span>
    <h1>Privatlivspolitik &amp; Cookiepolitik</h1>
    <p class="lead">Sidst opdateret: 4. marts 2026</p>
  </div>
</div>
<section>
  <div class="container" style="max-width:760px">
    <div class="prose">
      <h2>Afsnit 1: Dataansvarlig</h2>
      <p>Den dataansvarlige for behandlingen af dine personoplysninger på nordicwebflow.com er:<br><strong>NordicWebFlow</strong> · CVR: 46305639 · <a href="mailto:hej@nordicwebflow.com">hej@nordicwebflow.com</a> · nordicwebflow.com · København, Danmark</p>
      <h2>Afsnit 2: Hvilke personoplysninger indsamler vi?</h2>
      <p>Vi indsamler kun de personoplysninger du selv afgiver via kontaktformular (navn, e-mail, telefon, besked) eller direkte e-mailhenvendelse. Tekniske data (anonymiseret IP, browsertype, besøgstidspunkt) indsamles via cookies.</p>
      <h2>Afsnit 3: Formål med behandlingen</h2>
      <p>Vi behandler dine oplysninger til: besvarelse af henvendelser (GDPR art. 6(1)(f)), opfyldelse af aftaler (art. 6(1)(b)) og anonymiseret statistik med samtykke (art. 6(1)(a)).</p>
      <h2>Afsnit 4: Videregivelse</h2>
      <p>Vi sælger aldrig dine data. Vi anvender Framer B.V. (hosting), Google LLC (Analytics, Search Console), Cloudflare Inc. (sikkerhed/CDN) og Google Workspace (e-mail) som databehandlere. Alle er forpligtet af GDPR artikel 28.</p>
      <h2>Afsnit 5: Overførsler til tredjelande</h2>
      <p>Overførsler til USA-baserede databehandlere sker på grundlag af EU-US Data Privacy Framework (GDPR art. 45) eller EU's standardkontraktbestemmelser (art. 46).</p>
      <h2>Afsnit 6: Cookiepolitik</h2>
      <p><strong>Nødvendige cookies:</strong> Kræver ikke samtykke. Slettes ved lukning af browser.</p>
      <p><strong>Statistik-cookies (Google Analytics):</strong> Kræver samtykke. Anonymiseret. Kan afvises via cookie-banner.</p>
      <h2>Afsnit 7: Dine rettigheder</h2>
      <p>Du har ret til indsigt, berigtigelse, sletning, begrænsning, dataportabilitet og indsigelse (GDPR kap. III). Kontakt os på <a href="mailto:hej@nordicwebflow.com">hej@nordicwebflow.com</a>.</p>
      <h2>Afsnit 8: Klage til Datatilsynet</h2>
      <p>Datatilsynet · Carl Jacobsens Vej 35, 2500 Valby · <a href="mailto:dt@datatilsynet.dk">dt@datatilsynet.dk</a> · <a href="https://www.datatilsynet.dk" target="_blank" rel="noopener">datatilsynet.dk</a></p>
      <h2>Afsnit 9: Datasikkerhed</h2>
      <p>Vores hjemmeside er sikret med SSL/TLS-kryptering (HTTPS). Vi har implementeret passende tekniske og organisatoriske sikkerhedsforanstaltninger.</p>
    </div>
  </div>
</section>
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# YDELSER PAGES
# ─────────────────────────────────────────────
def page_ydelser_hub():
    ydelser = [
        ("⚡","Premium Hjemmesider i Framer","/ydelser/lynhurtige-hjemmesider-framer","Sub-1-sekunds loadtid og 97+ PageSpeed. Fra 2.999 kr. — du ejer siden 100%."),
        ("📍","Lokal SEO Optimering København","/ydelser/lokal-seo-koebenhavn","Dominér Google lokalt. Fra 1.999 kr./md. uden bindingsperiode."),
        ("📊","Google &amp; Meta Ads København","/ydelser/google-meta-ads-koebenhavn","Få kunder i morgen. Vi opsætter og styrer dine annoncekampagner."),
        ("🛡️","Drift &amp; Sikkerhed","/ydelser/drift-og-sikkerhed","Vi holder din hjemmeside hurtig, sikker og opdateret."),
    ]
    cards = ''.join([f'<div class="card"><div class="card-icon">{icon}</div><h3><a href="{url}" style="color:var(--white)">{name}</a></h3><p style="margin:8px 0 14px;font-size:.9rem">{desc}</p><a href="{url}" style="color:var(--orange);font-size:.87rem">Læs mere →</a></div>' for icon,name,url,desc in ydelser])
    return head("Ydelser — Webdesign, Lokal SEO & Google Ads | NordicWebFlow","Se alle NordicWebFlows ydelser: premium hjemmesider i Framer, lokal SEO i København, Google & Meta Ads og drift. Fra 2.999 kr.","/ydelser") + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Vores Ydelser</span>
    <h1>Alt hvad din virksomhed behøver for at <span>dominere digitalt</span></h1>
    <p class="lead">Fra lynhurtigt webdesign til lokal SEO-dominans og betalt annoncering — vi leverer det komplette digitale arsenal til ambitiøse lokale virksomheder.</p>
  </div>
</div>
<section>
  <div class="container">
    <div class="features-grid">{cards}</div>
  </div>
</section>
{CTA()}
{SEO_BLOCK("NordicWebFlow tilbyder professionelt webdesign i Framer, lokal SEO i København og Google & Meta Ads til lokale virksomheder. Brug vores gratis SEO-analyseværktøj på seotjek.dk.",
  [("Priser","/priser"),("Cases","/cases"),("Gratis SEO-tjek","https://seotjek.dk"),("Kontakt","/kontakt")])}
{FOOT()}{SCR()}</body></html>"""

def page_framer():
    faqs_framer = [
        ("Kan jeg selv opdatere min Framer-hjemmeside?","Ja. Framer er designet til at være nemt for ikke-tekniske brugere. Vi viser dig præcis hvordan ved overdragelsen."),
        ("Hvad koster hosting af en Framer-hjemmeside?","Hosting via Framer koster ca. 800-1.000 kr. om året. Professionel og Premium+ inkluderer 1 år gratis."),
        ("Er Framer-hjemmesider virkelig hurtigere end WordPress?","Konsekvent ja. Framer producerer ren kode uden plugins og serverer via Vercels globale CDN. Vi scorer typisk 90-97 mod 40-65 for WordPress."),
        ("Hvad sker der hvis Framer lukker?","Du kan til enhver tid eksportere den komplette kildekode og hoste den på en hvilken som helst server. Du er aldrig låst fast."),
    ]
    return head(
        "Lynhurtige Hjemmesider i Framer — Fra 14.999 kr. | NordicWebFlow",
        "Få en lynhurtig hjemmeside i Framer med sub-1-sekunds loadtid og 97+ PageSpeed. Fra 14.999 kr. — 100% ejerskab, ingen skjulte gebyrer. Webbureau København.",
        "/ydelser/lynhurtige-hjemmesider-framer",
        extra=faq_schema(faqs_framer)
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Premium Webdesign i Framer</span>
    <h1>Lynhurtige Hjemmesider i Framer — <span>Fra 14.999 kr.</span></h1>
    <p class="lead">Få en lynhurtig hjemmeside der forvandler klik til bookede opgaver. Sub-1-sekunds loadtid garanteret. 97+ PageSpeed-score på desktop. 100% ejerskab fra dag ét.</p>
    <div class="page-hero-actions">
      <a href="/faa-et-tilbud" class="btn btn-primary btn-lg">Få et gratis tilbud →</a>
      <a href="/priser" class="btn btn-ghost">Se priser</a>
    </div>
  </div>
</div>
<section>
  <div class="container">
    <div class="stats-row">
      <div style="text-align:center"><div class="s-val o">97+</div><div class="s-lbl">PageSpeed Desktop</div></div>
      <div style="text-align:center"><div class="s-val g">&lt;1s</div><div class="s-lbl">Loadtid</div></div>
      <div style="text-align:center"><div class="s-val b">100%</div><div class="s-lbl">SEO Optimeret</div></div>
      <div style="text-align:center"><div class="s-val p">14d</div><div class="s-lbl">Lancering</div></div>
    </div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Framer vs WordPress vs Wix</span>
      <h2>Hvorfor Framer slår <span>alle alternativer</span></h2>
    </div>
    <table class="comparison-table">
      <thead><tr><th>Funktion</th><th class="hl">Framer (NordicWebFlow)</th><th>WordPress</th><th>Wix</th></tr></thead>
      <tbody>
        <tr><td>PageSpeed score</td><td class="hl yes">90-97 / 100</td><td class="no">40-65 / 100</td><td class="no">51-65 / 100</td></tr>
        <tr><td>Loadtid</td><td class="hl yes">&lt;1 sekund</td><td class="no">3-8 sekunder</td><td class="no">2-5 sekunder</td></tr>
        <tr><td>100% ejerskab af kode</td><td class="hl yes">✓</td><td class="yes">✓</td><td class="no">✗</td></tr>
        <tr><td>Kræver plugins til hastighed</td><td class="hl yes">Nej</td><td class="no">Ja — dyrt &amp; komplekst</td><td class="no">Nej</td></tr>
        <tr><td>Sikkerhedsopdateringer</td><td class="hl yes">Automatisk</td><td class="no">Manuel — tidskrævende</td><td class="yes">Automatisk</td></tr>
        <tr><td>Lock-in</td><td class="hl yes">Ingen — eksportér kode</td><td class="yes">Ingen</td><td class="no">Ja — platform-afhængig</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section style="background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-header">
      <h2>Hvad er inkluderet i en <span>NordicWebFlow</span> hjemmeside?</h2>
    </div>
    <div class="features-grid">
      <div class="card"><div class="card-icon">🎨</div><h4>Fuldt custom design</h4><p>Ingen skabeloner, ingen generiske layouts. Hvert design er bygget fra bunden til din virksomhed.</p></div>
      <div class="card"><div class="card-icon">⚡</div><h4>Sub-1-sekunds loadtid</h4><p>97+ PageSpeed-score på desktop. Vi optimerer hvert element — billeder, fonts, scripts.</p></div>
      <div class="card"><div class="card-icon">🔍</div><h4>100% teknisk SEO</h4><p>Meta-titler, schema markup, sitemap.xml, robots.txt — alt korrekt fra dag ét.</p></div>
      <div class="card"><div class="card-icon">📱</div><h4>Mobiloptimering</h4><p>Perfekt på alle skærmstørrelser fra iPhone til 4K desktop. 100% responsivt.</p></div>
      <div class="card"><div class="card-icon">📊</div><h4>Google Analytics & Search Console</h4><p>Komplet tracking opsætning. Du kan følge din trafik fra dag ét.</p></div>
      <div class="card"><div class="card-icon">🔑</div><h4>100% ejerskab</h4><p>Du ejer siden, koden og domænet. Ingen bindende abonnementer.</p></div>
    </div>
  </div>
</section>
{TESTIMONIAL()}
{FAQ_SECTION(faqs_framer,"FAQ","Spørgsmål om hjemmesider i Framer")}
{CTA()}
{SEO_BLOCK("NordicWebFlow bygger lynhurtige hjemmesider i Framer til lokale virksomheder i København. Alle sider leveres med sub-1-sekunds loadtid, 97+ PageSpeed og 100% teknisk SEO. Brug vores gratis SEO-analyseværktøj på seotjek.dk.",
  [("Priser","/priser"),("Lokal SEO","/ydelser/lokal-seo-koebenhavn"),("Cases","/cases"),("Gratis SEO-tjek","https://seotjek.dk")])}
{FOOT()}{SCR()}</body></html>"""

def page_lokal_seo():
    faqs_seo = [
        ("Hvad er lokal SEO?","Lokal SEO er optimering af din synlighed i lokale Google-søgninger. Når nogen søger 'tømrer København', er lokal SEO det der afgør om du dukker op øverst."),
        ("Hvor lang tid tager det at se resultater?","De fleste kunder ser de første forbedringer inden for 4-8 uger. Fuld effekt typisk inden for 3-6 måneder."),
        ("Er der bindingsperiode?","Nej. Vores Lokal SEO-abonnement kan opsiges med 30 dages varsel. Ingen kontrakter."),
        ("Hvad er Google Business Profile?","Google Business Profile er din gratis virksomhedsprofil på Google Maps og i lokale søgeresultater. Korrekt optimering er afgørende for lokal synlighed."),
        ("Kan I garantere top 1 på Google?","Ingen kan garantere specifikke placeringer. Vi kan garantere professionel, datadrevet SEO-arbejde der konsekvent forbedrer din synlighed."),
    ]
    return head(
        "Lokal SEO Optimering i København — Fra 1.999 kr./md. | NordicWebFlow",
        "Professionel lokal SEO i København. Vi optimerer din Google Business Profile og sikrer at din virksomhed dukker op øverst lokalt. Fra 1.999 kr./md. — ingen bindingsperiode.",
        "/ydelser/lokal-seo-koebenhavn",
        extra=faq_schema(faqs_seo)
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Lokal SEO Optimering</span>
    <h1>Lokal SEO i København — <span>Bliv fundet først</span></h1>
    <p class="lead">Folk ringer til den virksomhed de finder først på Google. Vi opsætter målrettet Lokal SEO så din virksomhed dukker op præcis når kunderne søger i København og omegn.</p>
    <div class="page-hero-actions">
      <a href="/faa-et-tilbud" class="btn btn-primary btn-lg">Start Lokal SEO →</a>
      <a href="/performancechecker" class="btn btn-ghost">Test din synlighed gratis</a>
    </div>
  </div>
</div>
<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Hvad er inkluderet</span>
      <h2>Lokal SEO-abonnement — <span>1.999 kr./md.</span></h2>
      <p>Ingen bindingsperiode. Opsig med 30 dages varsel. Vi arbejder månedligt på at forbedre din lokale Google-synlighed.</p>
    </div>
    <div class="features-grid">
      <div class="card"><div class="card-icon">📍</div><h4>Google Business Profile Optimering</h4><p>Vi optimerer din GBP komplet — kategori, beskrivelse, billeder, attributter og ugentlige opslag.</p></div>
      <div class="card"><div class="card-icon">🔑</div><h4>Månedlig Keyword-tracking</h4><p>Vi overvåger dine placeringer for lokale søgetermer og rapporterer fremgang hver måned.</p></div>
      <div class="card"><div class="card-icon">📝</div><h4>On-page SEO-opdateringer</h4><p>Metatitler, beskrivelser, interne links og sidestruktur justeres løbende efter data.</p></div>
      <div class="card"><div class="card-icon">📊</div><h4>Simpel månedlig rapport</h4><p>Ingen 40-siders konsulentrapport. En klar, enkel oversigt over dine resultater.</p></div>
      <div class="card"><div class="card-icon">📞</div><h4>Prioriteret support</h4><p>Direkte adgang til specialisten. Telefon og e-mail på alle hverdage.</p></div>
      <div class="card"><div class="card-icon">🏙️</div><h4>Branche- og lokaltilpasning</h4><p>Vi tilpasser SEO-strategien specifikt til din branche og dit lokalområde i København.</p></div>
    </div>
  </div>
</section>
<section style="background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-header">
      <h2>Hvad er <span>Core Web Vitals</span> — og hvorfor det betyder noget</h2>
    </div>
    <div class="grid-3">
      <div class="card"><div style="font-family:var(--font-display);font-weight:800;font-size:1.1rem;color:var(--orange);margin-bottom:8px">LCP</div><h4>Largest Contentful Paint</h4><p style="font-size:.87rem">Måler hvor hurtigt det største element loader. Google anbefaler under 2,5 sek. Vores sider: under 1,2 sek.</p></div>
      <div class="card"><div style="font-family:var(--font-display);font-weight:800;font-size:1.1rem;color:var(--green);margin-bottom:8px">CLS</div><h4>Cumulative Layout Shift</h4><p style="font-size:.87rem">Måler om elementer rykker sig under indlæsning. Framer producerer pixel-perfekt rendering der eliminerer layout shift.</p></div>
      <div class="card"><div style="font-family:var(--font-display);font-weight:800;font-size:1.1rem;color:var(--blue);margin-bottom:8px">INP</div><h4>Interaction to Next Paint</h4><p style="font-size:.87rem">Måler sidens responstid på brugerinteraktioner. Hurtig respons signalerer teknisk kvalitet til Google.</p></div>
    </div>
  </div>
</section>
{TESTIMONIAL()}
{FAQ_SECTION(faqs_seo,"FAQ","Spørgsmål om lokal SEO")}
{CTA("Klar til at dominere Google lokalt?","Kontakt os i dag og få en gratis vurdering af din nuværende lokale SEO-situation.")}
{SEO_BLOCK("NordicWebFlow tilbyder professionel lokal SEO optimering i København fra 1.999 kr./md. uden bindingsperiode. Vi optimerer Google Business Profile, sporer lokale søgeplaceringer og opdaterer on-page SEO månedligt. Brug vores gratis SEO-analyseværktøj på seotjek.dk.",
  [("Premium Hjemmesider","/ydelser/lynhurtige-hjemmesider-framer"),("Google & Meta Ads","/ydelser/google-meta-ads-koebenhavn"),("Gratis SEO-tjek","https://seotjek.dk"),("Kontakt","/kontakt")])}
{FOOT()}{SCR()}</body></html>"""

def page_ads():
    return head(
        "Google & Meta Ads i København — Betalt Annoncering for Lokale Virksomheder | NordicWebFlow",
        "Professionel Google Ads og Meta Ads opsætning for lokale virksomheder i København. Vi styrer dine kampagner med fokus på lokal ROI og kvalitetsleads. Kontakt os i dag.",
        "/ydelser/google-meta-ads-koebenhavn"
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Betalt Annoncering</span>
    <h1>Google &amp; Meta Ads — <span>Få kunder i morgen</span></h1>
    <p class="lead">Mens SEO er en langsigtet investering, kan betalt annoncering bringe dig kunder allerede i morgen. Vi opsætter og styrer dine Google Ads og Meta Ads kampagner med fokus på lokal ROI.</p>
    <div class="page-hero-actions">
      <a href="/faa-et-tilbud" class="btn btn-primary btn-lg">Få et tilbud →</a>
      <a href="/kontakt" class="btn btn-ghost">Kontakt os</a>
    </div>
  </div>
</div>
<section>
  <div class="container">
    <div class="features-grid">
      <div class="card"><div class="card-icon">🔍</div><h4>Google Search Ads</h4><p>Vis annoncer til folk der aktivt søger dine ydelser på Google. Perfekt til at fange kunder med høj købeintention.</p></div>
      <div class="card"><div class="card-icon">📱</div><h4>Meta (Facebook/Instagram) Ads</h4><p>Nå potentielle kunder baseret på demografi og interesser. Idéelt til at bygge kendskab og generere leads.</p></div>
      <div class="card"><div class="card-icon">📍</div><h4>Lokal Annoncering</h4><p>Vi målretter udelukkende til relevante postnumre og lokalområder i København — ingen spildte annoncebudgetter.</p></div>
      <div class="card"><div class="card-icon">📊</div><h4>Konverteringssporing</h4><p>Vi opsætter korrekt sporing så du ved præcis hvilke annoncer der skaffer kunder — ikke bare klik.</p></div>
      <div class="card"><div class="card-icon">🔄</div><h4>Løbende optimering</h4><p>Vi overvåger og optimerer dine kampagner løbende. Budgetter flyttes til det der virker.</p></div>
      <div class="card"><div class="card-icon">📋</div><h4>Månedlig rapport</h4><p>Klar og forståelig rapport over spend, kliks, leads og ROI — uden bureau-jargon.</p></div>
    </div>
  </div>
</section>
{TESTIMONIAL()}
{CTA("Klar til at få kunder med det samme?","Kontakt os for en gratis gennemgang af dine annonceringsmuligheder.")}
{SEO_BLOCK("NordicWebFlow tilbyder professionel Google Ads og Meta Ads opsætning for lokale virksomheder i København. Vi kombinerer betalt annoncering med lokal SEO og lynhurtige hjemmesider for maksimal effekt.",
  [("Lokal SEO","/ydelser/lokal-seo-koebenhavn"),("Premium Hjemmesider","/ydelser/lynhurtige-hjemmesider-framer"),("Priser","/priser"),("Kontakt","/kontakt")])}
{FOOT()}{SCR()}</body></html>"""

def page_drift():
    return head(
        "Drift & Sikkerhed — Din Hjemmeside Holdes Hurtig & Sikker | NordicWebFlow",
        "NordicWebFlow tilbyder drift og vedligeholdelse af hjemmesider i Framer. Vi holder din hjemmeside sikker, hurtig og opdateret. Kontakt os for en pris.",
        "/ydelser/drift-og-sikkerhed"
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container">
    <span class="badge badge-orange">Drift &amp; Sikkerhed</span>
    <h1>Vi holder din hjemmeside <span>hurtig og sikker</span></h1>
    <p class="lead">En hjemmeside er ikke et engangsprojekt. Den kræver løbende opmærksomhed for at forblive hurtig, sikker og synlig på Google. Vi tager os af det, så du kan fokusere på din forretning.</p>
    <div class="page-hero-actions">
      <a href="/kontakt" class="btn btn-primary btn-lg">Kontakt os →</a>
    </div>
  </div>
</div>
<section>
  <div class="container">
    <div class="features-grid">
      <div class="card"><div class="card-icon">🛡️</div><h4>Sikkerhedsovervågning</h4><p>Vi overvåger din hjemmeside for sikkerhedstrusler og sikrer at SSL-certifikater altid er aktive.</p></div>
      <div class="card"><div class="card-icon">⚡</div><h4>Hastighedsoptimering</h4><p>Vi sikrer at din hjemmeside forbliver hurtig over tid. Billeder, scripts og cache optimeres løbende.</p></div>
      <div class="card"><div class="card-icon">✏️</div><h4>Indholdsopdateringer</h4><p>Har du brug for at ændre tekster, tilføje billeder eller opdatere priser? Vi klarer det hurtigt.</p></div>
      <div class="card"><div class="card-icon">📊</div><h4>Performance-rapportering</h4><p>Månedlig rapport over din hjemmesides performance, trafikudvikling og PageSpeed-score.</p></div>
    </div>
  </div>
</section>
{CTA()}
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# TRADE PAGES — generic template
# ─────────────────────────────────────────────
def trade_page(name, slug, emoji, title_da, desc_da, industry_faq, img1, img2, cross_links):
    faqs = industry_faq
    return head(
        f"Hjemmeside til {name}e i København — Fra 14.999 kr. | NordicWebFlow",
        f"Professionelt webdesign til {name.lower()}e i København. Lynhurtig hjemmeside med 97+ PageSpeed og 100% lokal SEO. Fra 14.999 kr. — 100% ejerskab.",
        f"/{slug}",
        extra=faq_schema(faqs)
    ) + f"""
<body>
{NAV()}
<div class="page-hero">
  <div class="container" style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center">
    <div>
      <span class="badge badge-orange" style="margin-bottom:16px">{emoji} Webdesign til {name}e</span>
      <h1>{title_da}</h1>
      <p class="lead" style="margin:14px 0 26px">{desc_da}</p>
      <div class="page-hero-actions">
        <a href="/faa-et-tilbud" class="btn btn-primary btn-lg">Ny hjemmeside fra 14.999 kr. →</a>
        <a href="/performancechecker" class="btn btn-ghost">Gratis SEO-tjek</a>
      </div>
      <p style="font-size:.78rem;color:var(--muted2);margin-top:12px">Betalt én gang. Ejet for altid. Ingen skjulte abonnementer.</p>
    </div>
    <div style="position:relative">
      <img src="/images/{img1}" alt="{name} i København — professionelt webdesign til {name.lower()}e" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius-xl);border:1px solid var(--border)" width="580" height="435" loading="eager">
    </div>
  </div>
</div>

<section>
  <div class="container">
    <div class="section-header">
      <span class="badge badge-white">Dit lokale webbureau</span>
      <h2>Vi bygger hjemmesider der <span>skaffer {name.lower()}-kunder</span></h2>
      <p>Kunderne finder dig på Google — ikke kun via anbefalinger. Vi bygger lynhurtige, professionelle hjemmesider der viser dine ydelser frem og forvandler besøgende til bookede opgaver.</p>
    </div>
    <div class="features-grid">
      <div class="card"><div class="card-icon">📍</div><h4>Lokal SEO: Bliv fundet i nærheden</h4><p>Når folk søger "{name.lower()} København" skal din hjemmeside ligge øverst. Vi opsætter målrettet Lokal SEO der sikrer, at du dukker op præcis der.</p></div>
      <div class="card"><div class="card-icon">⚡</div><h4>Sub-1-sekunds loadtid</h4><p>En langsom hjemmeside mister kunder. Vi leverer konsekvent sub-1-sekunds loadtid og 97+ PageSpeed — bedre end 95% af konkurrenterne.</p></div>
      <div class="card"><div class="card-icon">💰</div><h4>Fast pris — ingen overraskelser</h4><p>Du betaler én fast pris og ejer din hjemmeside 100% fra dag ét. Ingen dyre bureau-abonnementer eller skjulte gebyrer.</p></div>
    </div>
  </div>
</section>

<section style="background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="grid-2">
      <div>
        <img src="/images/{img2}" alt="Professionel {name.lower()} udfører arbejde — webdesign til {name.lower()}e" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius-lg);border:1px solid var(--border)" width="560" height="420" loading="lazy">
      </div>
      <div>
        <span class="badge badge-orange" style="margin-bottom:16px">Vis dine projekter professionelt</span>
        <h2 style="font-size:1.7rem;margin-bottom:14px">Et projekt-galleri der <span style="color:var(--orange)">sælger for dig</span></h2>
        <p style="margin-bottom:16px">Et billede siger mere end tusind ord. Vi bygger et professionelt projekt-galleri ind i din hjemmeside, så potentielle kunder kan se kvaliteten af dit arbejde, inden de ringer.</p>
        <ul style="margin:0;padding:0">
          {"".join([f'<li style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);font-size:.9rem;color:var(--text)"><span style="color:var(--green);flex-shrink:0">✓</span>{item}</li>' for item in [
            "Professionelle billeder af dine projekter og referencer",
            "Anmeldelser fra Trustpilot eller Google integreret direkte",
            "Kontaktformular der sender leads direkte til din e-mail",
            "Mobiloptimeret — 60%+ af dine kunder søger på mobil",
            "100% teknisk SEO fra lancering — synlig på Google fra dag ét",
          ]])}
        </ul>
        <a href="/faa-et-tilbud" class="btn btn-primary" style="margin-top:20px">Få et gratis tilbud →</a>
      </div>
    </div>
  </div>
</section>

{TESTIMONIAL()}

{FAQ_SECTION(faqs, "FAQ", f"Spørgsmål om hjemmesider til {name.lower()}e")}

{PARTNER_SECTION()}

{CTA(f"Klar til en hjemmeside der skaffer dig flere {name.lower()}-kunder?","Vi leverer en lynhurtig, professionel hjemmeside på under 14 dage — med lokal SEO der sikrer synlighed på Google.")}

{SEO_BLOCK(
  f"NordicWebFlow er et webbureau i København der specialiserer sig i hjemmesider til {name.lower()}e og andre håndværkere. Vi leverer lynhurtige hjemmesider i Framer med 100% lokal SEO fra 14.999 kr. Brug vores gratis SEO-analyseværktøj på seotjek.dk til at teste din nuværende hjemmeside.",
  [("Se vores priser","/priser"),("Lokal SEO København","/ydelser/lokal-seo-koebenhavn"),
   ("Gratis SEO-tjek","https://seotjek.dk"),("Cases & resultater","/cases")] + cross_links
)}
{FOOT()}{SCR()}</body></html>"""

# ─────────────────────────────────────────────
# BUILD ALL PAGES
# ─────────────────────────────────────────────
def build():
    os.makedirs(f'{BASE}/ydelser', exist_ok=True)

    write(f'{BASE}/index.html', page_index())
    write(f'{BASE}/priser.html', page_priser())
    write(f'{BASE}/cases.html', page_cases())
    write(f'{BASE}/kontakt.html', page_kontakt())
    write(f'{BASE}/faa-et-tilbud.html', page_tilbud())
    write(f'{BASE}/tak.html', page_tak())
    write(f'{BASE}/404.html', page_404())
    write(f'{BASE}/legal.html', page_legal())
    write(f'{BASE}/performancechecker.html', page_checker())
    write(f'{BASE}/ydelser.html', page_ydelser_hub())
    write(f'{BASE}/ydelser/lynhurtige-hjemmesider-framer.html', page_framer())
    write(f'{BASE}/ydelser/lokal-seo-koebenhavn.html', page_lokal_seo())
    write(f'{BASE}/ydelser/google-meta-ads-koebenhavn.html', page_ads())
    write(f'{BASE}/ydelser/drift-og-sikkerhed.html', page_drift())

    # Trade pages
    trades = [
        ("Tømrer","toemrer","🔨",
         "Hjemmesider til Tømrere — Få nye byggeprojekter fra Google",
         "Få nye byggeprojekter fra Google uden at bruge tid på marketing du ikke forstår. Vi bygger lynhurtige, professionelle hjemmesider til tømrere i København.",
         [("Har du brug for en tømrer-hjemmeside?","Ja — som tømrer er Google din vigtigste salgskanal. En professionel hjemmeside med lokal SEO sikrer at nye kunder finder dig, ikke konkurrenten."),
          ("Hvad koster en hjemmeside til tømrere?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting. Du ejer siden 100% — betalt én gang."),
          ("Kan jeg vise mine projekter på hjemmesiden?","Ja, vi bygger altid et projekt-galleri ind der viser dine bedste arbejder frem."),
          ("Vil en hjemmeside hjælpe mig med at få flere kunder?","Ja. En professionel hjemmeside med lokal SEO er den mest effektive investering du kan gøre for at tiltrække nye kunder i lokalområdet.")],
         "gabriel-alenius-cPDTVCsbxcg-unsplash.jpg","austin-ramsey-rbi4q0-b-8g-unsplash.jpg",
         [("Webdesign til murere","/murer"),("Webdesign til elektrikere","/elektriker")]),

        ("Tandlæge","tandlaege","🦷",
         "Hjemmesider til Tandlæger — Fyld din bookingkalender fra Google",
         "Nye patienter søger tandlæge på Google. Vi bygger en professionel hjemmeside der tiltrækker patienter og viser din klinik som det selvfølgelige valg i lokalområdet.",
         [("Hvad skal en tandlæge-hjemmeside indeholde?","Dine ydelser (tandrensning, tandregulering, blegning mv.), priser, bookingmulighed, personale-profiler og patientanmeldelser."),
          ("Kan hjemmesiden integreres med mit bookingsystem?","Vi kan integrere med de fleste online bookingsystemer eller sætte en simpel kontaktformular op."),
          ("Rangerer tandlæge-hjemmesider godt på Google?","Med korrekt lokal SEO — ja. Vi optimerer for søgetermer som 'tandlæge København' og dit specifikke postnummer."),
          ("Hvad koster en hjemmeside til tandlæger?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting.")],
         "katarzyna-zygnerska-44jaETSVX2I-unsplash.jpg","jonathan-borba-v_2FRXEba94-unsplash.jpg",
         [("Webdesign til fysioterapeuter","/fysioterapeut"),("Lokal SEO","/ydelser/lokal-seo-koebenhavn")]),

        ("Advokat","advokat","⚖️",
         "Hjemmesider til Advokater — Tiltræk kvalitets-klienter fra Google",
         "Kvalitets-klienter søger advokat på Google. Vi bygger en professionel, troværdig hjemmeside der præsenterer dit kontor som det naturlige valg — og forvandler besøgende til klienter.",
         [("Hvad er vigtigt på en advokat-hjemmeside?","Klar præsentation af specialer, advokat-profiler med billeder og baggrund, klientanmeldelser og en nem kontaktformular."),
          ("Kan hjemmesiden hjælpe med at tiltrække erhvervsklienter?","Ja. Med korrekt lokal SEO og B2B-fokuseret indhold kan vi tiltrække erhvervsklienter der søger specifik juridisk assistance."),
          ("Overholder hjemmesiden advokatrådets regler?","Vi er bekendt med reglerne for advokatmarkedsføring og bygger inden for disse rammer."),
          ("Hvad koster en advokat-hjemmeside?","Fra 14.999 kr. — vi anbefaler Professionel-pakken til 19.999 kr. for advokatkontorer.")],
         "patrick-fore-H5Lf0nGyetk-unsplash.jpg","ruthson-zimmerman-Ws4wd-vJ9M0-unsplash.jpg",
         [("Webdesign til revisorer","/revisor"),("Lokal SEO","/ydelser/lokal-seo-koebenhavn")]),

        ("Murer","murer","🧱",
         "Hjemmesider til Murere — Fyld din kalender med murerjobs fra Google",
         "Kunder der søger murer i København finder den murer der rangerer øverst. Vi bygger en professionel hjemmeside der giver dig det forspring.",
         [("Hvad skaffer en murer-hjemmeside af kunder?","Med lokal SEO optimering dukker din virksomhed op øverst når folk søger 'murer København' — de fleste ringer til de øverste resultater."),
          ("Kan I vise mine murerprojekter?","Ja — et professionelt projekt-galleri er centralt i alle vores branche-sider."),
          ("Hvad koster en hjemmeside til murere?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting."),
          ("Hvor hurtigt kan I lave min hjemmeside?","Typisk under 14 dage fra bestilling til lancering.")],
         "gabriel-alenius-cPDTVCsbxcg-unsplash.jpg","austin-ramsey-rbi4q0-b-8g-unsplash.jpg",
         [("Webdesign til tømrere","/toemrer"),("Webdesign til elektrikere","/elektriker")]),

        ("Elektriker","elektriker","⚡",
         "Hjemmesider til Elektrikere — Få elektriker-jobs fra Google",
         "Når en sikring springer eller der skal trækkes ny el, søger kunderne på Google. Vi sikrer at din elektriker-virksomhed er den de finder og kontakter.",
         [("Virker lokal SEO for elektrikere?","Absolut. 'Elektriker København' søges hundredvis af gange dagligt. Med korrekt lokal SEO er din virksomhed øverst."),
          ("Kan hjemmesiden tage imod akutte henvendelser?","Ja, vi bygger en prominent kontaktformular og evt. telefonnummer øverst på siden for akutte opgaver."),
          ("Hvad koster en elektriker-hjemmeside?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting."),
          ("Ejer jeg min hjemmeside?","Ja, 100%. Ingen bindende abonnementer.")],
         "gabriel-alenius-cPDTVCsbxcg-unsplash.jpg","austin-ramsey-rbi4q0-b-8g-unsplash.jpg",
         [("Webdesign til VVS","/vvs"),("Webdesign til malere","/maler")]),

        ("Maler","maler","🎨",
         "Hjemmesider til Malere — Tiltræk maleropgaver fra Google",
         "Nye maleropgaver begynder med en Google-søgning. Vi bygger en visuelt imponerende hjemmeside der viser dine malerprojekter frem og overbeviser kunder om at vælge dig.",
         [("Kan jeg vise mine malerprojekter med billeder?","Ja — et stort, flot billedgalleri er centralt for maler-hjemmesider. Det viser din håndværksmæssige kvalitet."),
          ("Hvad er lokal SEO for malere?","Lokal SEO sikrer at din hjemmeside dukker op øverst når kunder søger 'maler København' eller 'maler [dit postnummer]'."),
          ("Hvad koster en maler-hjemmeside?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting."),
          ("Kan I hjælpe med Google Anmeldelser?","Ja, vi opsætter altid Google Business Profile og hjælper med at indhente anmeldelser.")],
         "gabriel-alenius-cPDTVCsbxcg-unsplash.jpg","unnamed__19_.jpg",
         [("Webdesign til tømrere","/toemrer"),("Webdesign til murere","/murer")]),

        ("VVS","vvs","🔧",
         "Hjemmesider til VVS-firmaer — Få VVS-jobs fra Google",
         "Når vandskaden opstår, ringer kunden til det første VVS-firma på Google. Vi sikrer at det er dig de finder og kontakter.",
         [("Virker lokal SEO for VVS-firmaer?","Ja — akutte VVS-opgaver søges konstant på Google. Med lokal SEO er du øverst."),
          ("Kan hjemmesiden vise mine VVS-ydelser?","Ja — vi strukturerer hjemmesiden med klare undersider for vandinstallation, fjernvarme, badeværelse og akutte opgaver."),
          ("Hvad koster en VVS-hjemmeside?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting."),
          ("Hvad er fordelen ved Framer frem for WordPress?","Framer leverer sub-1-sekunds loadtid og 97+ PageSpeed — afgørende for Google-placeringer.")],
         "gabriel-alenius-cPDTVCsbxcg-unsplash.jpg","austin-ramsey-rbi4q0-b-8g-unsplash.jpg",
         [("Webdesign til elektrikere","/elektriker"),("Webdesign til murere","/murer")]),

        ("Fysioterapeut","fysioterapeut","💪",
         "Hjemmesider til Fysioterapeuter — Fyld din bookingkalender fra Google",
         "Patienter søger fysioterapeut på Google. Vi bygger en professionel hjemmeside der giver din klinik et stærkt online nærvær og tiltrækker nye patienter lokalt.",
         [("Hvad skal en fysioterapeut-hjemmeside indeholde?","Dine behandlingstyper, priser, booking-mulighed, personaleprofiler og patientanmeldelser."),
          ("Kan hjemmesiden integreres med MitID/online booking?","Vi kan integrere med de fleste bookingsystemer via embed eller link til dit bookingsystem."),
          ("Rangerer klinikker godt på Google?","Med lokal SEO — ja. Vi optimerer for 'fysioterapeut København' og dit specifikke område."),
          ("Hvad koster det?","Fra 14.999 kr. inkl. lokal SEO og 1 år hosting.")],
         "gruescu-ovidiu-fWjqkOnfkgE-unsplash.jpg","unnamed__19_.jpg",
         [("Webdesign til tandlæger","/tandlaege"),("Webdesign til revisorer","/revisor")]),

        ("Revisor","revisor","📊",
         "Hjemmesider til Revisorer — Tiltræk erhvervsklienter via Google",
         "Erhvervsdrivende søger revisor på Google. Vi bygger en professionel, troværdig hjemmeside der positionerer dit revisionskontor som det naturlige valg i lokalområdet.",
         [("Hvad skal en revisor-hjemmeside indeholde?","Dine ydelser (årsregnskab, bogføring, rådgivning), virksomhedsprofil, medarbejdere og kontaktmuligheder."),
          ("Kan I hjælpe med SEO til revisor-søgninger?","Ja — vi optimerer for 'revisor København', 'regnskab København' og andre relevante søgetermer."),
          ("Hvad koster en revisor-hjemmeside?","Fra 14.999 kr. — vi anbefaler Professionel-pakken til 19.999 kr. for revisionskontorer."),
          ("Ejer jeg min hjemmeside?","Ja, 100%. Ingen bindende abonnementer eller lock-in.")],
         "1981-digital-oMe_FjZnHGU-unsplash.jpg","unnamed__19_.jpg",
         [("Webdesign til advokater","/advokat"),("Webdesign til fysioterapeuter","/fysioterapeut")]),

        ("Ejendomsmægler","ejendomsmaegler","🏠",
         "Hjemmesider til Ejendomsmæglere — Dominér Google lokalt",
         "Boligkøbere og sælgere søger ejendomsmægler på Google. Vi bygger en professionel hjemmeside der viser dine aktuelle ejendomme frem og tiltrækker seriøse henvendelser.",
         [("Kan hjemmesiden vise mine aktuelle boliger til salg?","Ja — vi kan integrere med ejendomsportaler eller bygge en simpel præsentation af udvalgte boliger."),
          ("Virker lokal SEO for ejendomsmæglere?","Absolut. 'Ejendomsmægler København' og lokale boligsøgninger er enormt konkurrenceudsatte — lokal SEO er afgørende."),
          ("Hvad koster en ejendomsmægler-hjemmeside?","Fra 14.999 kr. — vi anbefaler Professionel eller Premium+ til mæglere."),
          ("Ejer jeg hjemmesiden?","Ja, 100%. Du er ikke afhængig af dyre kæde-systemer.")],
         "unnamed__19_.jpg","1981-digital-oMe_FjZnHGU-unsplash.jpg",
         [("Webdesign til revisorer","/revisor"),("Webdesign til advokater","/advokat")]),

        ("Arkitekt","arkitekt","📐",
         "Hjemmesider til Arkitekter — Vis dine projekter professionelt online",
         "En arkitekt-hjemmeside er dit digitale portfolio. Vi bygger en visuelt overbevisende hjemmeside der præsenterer dine projekter i høj kvalitet og tiltrækker de rigtige klienter.",
         [("Hvad er vigtigt på en arkitekt-hjemmeside?","Et stærkt portfolio med høj-kvalitets billeder, klar præsentation af dine specialer og en professionel firma-profil."),
          ("Kan I lave en portfolio-hjemmeside?","Ja — vi er specialister i at bygge visuelt overbevisende portfolios i Framer med lynhurtige billeder."),
          ("Hvad koster en arkitekt-hjemmeside?","Fra 14.999 kr. Vi anbefaler Premium+-pakken til arkitektkontorer."),
          ("Kan I hjælpe med SEO til arkitekt-søgninger?","Ja — vi optimerer for 'arkitekt København' og specifikke byggetypesøgninger.")],
         "unnamed__19_.jpg","gabriel-alenius-cPDTVCsbxcg-unsplash.jpg",
         [("Webdesign til advokater","/advokat"),("Webdesign til ejendomsmæglere","/ejendomsmaegler")]),
    ]

    for name,slug,emoji,title,desc,faqs,img1,img2,cross in trades:
        write(f'{BASE}/{slug}.html', trade_page(name,slug,emoji,title,desc,faqs,img1,img2,cross))

    print(f"\n✅ All pages built successfully!")

if __name__ == '__main__':
    build()
