"""Builds the site from src/template.html.  Run:  python3 src/build.py
   repo root (index.html, sw.js)       -> the installable web app served by GitHub Pages
   build/letter-call-timer.html         -> single-file copy for claude.ai (Google Fonts, no service worker)"""
import hashlib, json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
src = open(os.path.join(ROOT, 'template.html')).read()
v = open(os.path.join(ROOT, 'voices.js')).read().strip()
assert v.startswith('const VOICE_DATA=')
src = src.replace('/*__VOICE_DATA__*/', 'window.VOICE_DATA=' + v[len('const VOICE_DATA='):])
os.makedirs(os.path.join(SITE, 'build'), exist_ok=True)
open(os.path.join(SITE, 'build', 'letter-call-timer.html'), 'w').write(src)

# ---- installable app ----
i = src.index('<div class="app"')
head, body = src[:i], src[i:]
gf_start = head.index('<link rel="preconnect"'); gf_end = head.index('<style>')
head = head[:gf_start] + head[gf_end:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
head = head.replace('<meta name="theme-color" content="#0b1416">\n', '')
fonts = """<style>
@font-face{font-family:"Barlow Semi Condensed";font-style:normal;font-weight:500;font-display:swap;src:url(fonts/barlow-semi-condensed-500.woff2) format("woff2")}
@font-face{font-family:"Barlow Semi Condensed";font-style:normal;font-weight:600;font-display:swap;src:url(fonts/barlow-semi-condensed-600.woff2) format("woff2")}
@font-face{font-family:"Barlow Semi Condensed";font-style:normal;font-weight:700;font-display:swap;src:url(fonts/barlow-semi-condensed-700.woff2) format("woff2")}
@font-face{font-family:"Big Shoulders Display";font-style:normal;font-weight:700 900;font-display:swap;src:url(fonts/big-shoulders-display.woff2) format("woff2")}
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}
</style>
"""
pre = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="HIIT reaction timer that calls random letters in a British voice.">
<meta name="theme-color" content="#0b1416" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#e7eeeb" media="(prefers-color-scheme: light)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Letter Call">
<link rel="preload" href="fonts/big-shoulders-display.woff2" as="font" type="font/woff2" crossorigin>
"""
body = body.replace('<script>\nwindow.VOICE_DATA=', '<script>window.LCT_PWA = true;</script>\n<script>\nwindow.VOICE_DATA=', 1)
assert 'LCT_PWA = true' in body
app = SITE
open(os.path.join(app, 'index.html'), 'w').write(pre + fonts + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

assets = ['./', './index.html', './manifest.webmanifest'] + \
  ['./icons/' + f for f in sorted(os.listdir(os.path.join(app, 'icons')))] + \
  ['./fonts/' + f for f in sorted(os.listdir(os.path.join(app, 'fonts')))]
h = hashlib.sha256()
for a in assets[1:]:
    h.update(open(os.path.join(app, a[2:]), 'rb').read())
sw = open(os.path.join(ROOT, 'sw.template.js')).read().replace('__VERSION__', h.hexdigest()[:10]).replace('__ASSETS__', json.dumps(assets, indent=2))
open(os.path.join(app, 'sw.js'), 'w').write(sw)
print('artifact', len(src), '| app/index.html', os.path.getsize(os.path.join(app, 'index.html')), '| cache', h.hexdigest()[:10], len(assets), 'files')
