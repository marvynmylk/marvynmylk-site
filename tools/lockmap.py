"""Small district maps on the "Republican lock" cards. Shapes are in tools/lockmaps.json."""
import json, os, re
D = json.load(open(os.path.join(os.path.dirname(__file__), 'lockmaps.json')))
CSS = ('/*lkmap*/.lkmap{display:block;width:100%;height:130px;margin:0 0 14px;border-radius:12px;background:#17121f;border:1px solid rgba(226,72,84,.25)}'
       '.lkmap .co{fill:#221b30;stroke:#5a4c78;stroke-width:.45}.lkmap .ds{fill:rgba(226,72,84,.55);stroke:#ff8a94;stroke-width:.8}'
       '.lkban{display:flex;align-items:center;gap:8px;margin:14px -4px 0;padding:10px 12px;border-radius:10px;background:rgba(45,110,255,.12);border:1px solid rgba(143,176,255,.3);color:#cfdcff;font:700 14px/1.3 Karla,sans-serif;text-decoration:none}.lkban b{color:#8fb0ff}'
       '.lkmap text{font:700 4.6px Karla,sans-serif;fill:#fbefd8;paint-order:stroke;stroke:#17121f;stroke-width:1.4px}/*/lkmap*/')
PIN = 'M0,0 C-1.2,-2.6 -4.2,-4.6 -4.2,-8 A4.2,4.2 0 1 1 4.2,-8 C4.2,-4.6 1.2,-2.6 0,0Z'

def svg(key, town, cur=None):
    m = D['maps'][key]
    out = (f'<svg class="lkmap" viewBox="0 0 {m["w"]} {m["h"]}" preserveAspectRatio="xMidYMid meet" role="img" '
           f'aria-label="Map of {key.replace("-", " district ")}"><path class="co" d="{m["co"]}"/><path class="ds" d="{m["d"]}"/>')
    if town:
        name, lon, lat = town
        lon, lat = D.get('pinfix', {}).get(cur, {}).get(key, [lon, lat])
        x = (lon - m['minx']) * D['K'] * m['sc']; y = (m['maxy'] - lat) * m['sc']
        out += (f'<g transform="translate({x:.1f},{y:.1f}) scale(.9)"><path d="{PIN}" fill="#ffd60a" stroke="#17121f" stroke-width=".6"/>'
                f'<circle cy="-8" r="1.5" fill="#17121f"/></g><text x="{x + 5:.1f}" y="{y - 3:.1f}">{name}</text>')
    return out + '</svg>'

def apply(s, cur):
    s = re.sub(r'<svg class="lkmap".*?</svg>', '', s, flags=re.S)
    s = re.sub(r'/\*lkmap\*/.*?/\*/lkmap\*/', '', s, flags=re.S)
    s = re.sub(r'<a class="lkban".*?</a>', '', s, flags=re.S)
    town = D['towns'].get(cur)
    def rep(mt):
        h = mt.group(2)
        k = re.search(r'State (House|Senate),? District (\d+)', h)
        key = k and f'{k.group(1).lower()}-{k.group(2)}'
        if not key or key not in D['maps']: return mt.group(0)
        return mt.group(1) + svg(key, town, cur) + mt.group(2)
    s2 = re.sub(r'(<div class="dc rv lock[^"]*">)(<h3>[^<]*</h3>)', rep, s)
    root = '../' * cur.count('/')
    WON = {'house-3', 'house-44', 'house-46', 'house-73', 'house-79', 'house-104'}
    href = f'{root}articles/jones-won-no-democrat-ran-alabama-2026.html'
    def addban(m):
        k = re.search(r'State (House|Senate),? District (\d+)', m.group(0))
        key = k and f'{k.group(1).lower()}-{k.group(2)}'
        txt = ('<b>Doug Jones won this district.</b> No Democrat ran for it. It\'s one of 6 like that →' if key in WON
               else 'No Democrat ran here. In <b>6 districts</b> like this, voters picked Doug Jones anyway →')
        return m.group(0) + f'<a class="lkban" href="{href}"><span>{txt}</span></a>'
    s2 = re.sub(r'<div class="dc rv lock[^"]*">.*?<a class="keyl"[^>]*>.*?</a>', addban, s2, flags=re.S)
    if s2 != s: s2 = s2.replace('</style>', CSS + '</style>', 1)
    return s2
