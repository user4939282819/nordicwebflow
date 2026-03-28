# NordicWebFlow — Static Site

Production website for [nordicwebflow.com](https://nordicwebflow.com) hosted on Cloudflare Pages.

## Stack
- Pure HTML + CSS (no build step)
- Hosted on Cloudflare Pages (auto-deploys on push to `main`)
- DNS on Cloudflare

## Folder structure

```
/
├── index.html
├── priser.html
├── cases.html
├── kontakt.html
├── faa-et-tilbud.html
├── tak.html
├── 404.html
├── legal.html
├── performancechecker.html
├── ydelser.html
├── ydelser/
│   ├── lynhurtige-hjemmesider-framer.html
│   ├── lokal-seo-koebenhavn.html
│   ├── google-meta-ads-koebenhavn.html
│   └── drift-og-sikkerhed.html
├── toemrer.html
├── tandlaege.html
├── advokat.html
├── murer.html
├── elektriker.html
├── maler.html
├── vvs.html
├── fysioterapeut.html
├── revisor.html
├── ejendomsmaegler.html
├── arkitekt.html
├── style.css
├── favicon.svg
├── robots.txt
├── sitemap.xml
├── _redirects      ← Cloudflare Pages routing
├── _headers        ← Cloudflare Pages cache headers
└── images/         ← Upload images here manually
    ├── diego.jpg
    ├── wenneke.jpg
    ├── case-wenneke.jpg
    ├── hero-laptop.jpg
    ├── carpenter.jpg
    ├── carpenter2.jpg
    ├── lawyer.jpg
    ├── lawyer2.jpg
    ├── dental.jpg
    ├── dental2.jpg
    ├── analytics.jpg
    ├── office.jpg
    ├── doctor.jpg
    └── og-default.jpg
```

## Image upload guide

Upload your images to the `/images/` folder on GitHub with these exact filenames:

| Filename | Source file |
|---|---|
| `diego.jpg` | `1771542850470.jpg` |
| `wenneke.jpg` | Benjamin avatar photo |
| `case-wenneke.jpg` | `Image.png` (Wenneke website mockup) |
| `hero-laptop.jpg` | `azwedo-l-lc-6uR0dkm3ya0-unsplash.jpg` |
| `carpenter.jpg` | `gabriel-alenius-cPDTVCsbxcg-unsplash.jpg` |
| `carpenter2.jpg` | `austin-ramsey-rbi4q0-b-8g-unsplash.jpg` |
| `lawyer.jpg` | `patrick-fore-H5Lf0nGyetk-unsplash.jpg` |
| `lawyer2.jpg` | `ruthson-zimmerman-Ws4wd-vJ9M0-unsplash.jpg` |
| `dental.jpg` | `katarzyna-zygnerska-44jaETSVX2I-unsplash.jpg` |
| `dental2.jpg` | `jonathan-borba-v_2FRXEba94-unsplash.jpg` |
| `analytics.jpg` | `1981-digital-oMe_FjZnHGU-unsplash.jpg` |
| `office.jpg` | `unnamed__19_.jpg` |
| `doctor.jpg` | `gruescu-ovidiu-fWjqkOnfkgE-unsplash.jpg` |
| `og-default.jpg` | Any good wide image of your work |

## Deploy

1. Push to `main` on GitHub
2. Cloudflare Pages auto-deploys in ~30 seconds
3. Site live at nordicwebflow.com

## Regenerate pages

If you need to rebuild all pages after changes to build.py:

```bash
python3 generate_all.py
```

Then commit and push.
