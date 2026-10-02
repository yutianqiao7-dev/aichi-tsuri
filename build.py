"""src.html に潮汐の調和定数 harm.json を埋め込んでビルドする。
- aichi-tsuri.html : Claude の Artifact 用（ページの外枠は Artifact 側が付ける）
- docs/index.html  : GitHub Pages 用（外枠・PWA 設定つき）
"""
import json, pathlib

d = pathlib.Path(__file__).parent
body = (d / "src.html").read_text(encoding="utf-8").replace("__HARM__", (d / "harm.json").read_text())
(d / "aichi-tsuri.html").write_text(body, encoding="utf-8")

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="愛知県の潮汐・天気・風から、いま釣れやすい魚と釣り場、仕掛けとエサがわかる釣りアプリ">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="潮どき愛知">
<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
docs = d / "docs"
docs.mkdir(exist_ok=True)
(docs / "index.html").write_text(HEAD + body + "\n</body>\n</html>\n", encoding="utf-8")
(docs / "manifest.webmanifest").write_text(json.dumps({
    "name": "潮どき愛知", "short_name": "潮どき愛知", "lang": "ja", "start_url": "./", "scope": "./",
    "display": "standalone", "background_color": "#eef3f2", "theme_color": "#0f3a4a",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
}, ensure_ascii=False, indent=2), encoding="utf-8")
(docs / ".nojekyll").write_text("")

# ひまつぶしアプリ（ウキまち）: 魚データは src.html の FISH・TACKLE をそのまま使う
import re
src = (d / "src.html").read_text(encoding="utf-8")
fish = re.search(r"const FISH = \[.*?\r?\n\];", src, re.S).group(0)
tackle = re.search(r"const TACKLE = \{.*?\r?\n\};", src, re.S).group(0)
hima = (d / "hima_src.html").read_text(encoding="utf-8").replace("__FISHDATA__", fish + "\n" + tackle)
(docs / "hima").mkdir(exist_ok=True)
hhead = (HEAD.replace('href="manifest.webmanifest"', 'href="../manifest.webmanifest"')
             .replace('href="icon-', 'href="../icon-')
             .replace("潮汐・天気・風から、いま釣れやすい魚と釣り場、仕掛けとエサがわかる釣りアプリ", "釣りの待ち時間に遊べるウキ釣りゲームと魚クイズ"))
(docs / "hima" / "index.html").write_text(hhead + hima + "\n</body>\n</html>\n", encoding="utf-8")
(d / "ukimachi.html").write_text(hima, encoding="utf-8")
print("built", len(body))
