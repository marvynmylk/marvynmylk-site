"""Every story on the site, for the menu's story list and the "More stories near here" list.
Built by walking the site's pages (same rules as sitemap.py). Titles come from tools/pages.json
when listed there, otherwise from the page's <h1>. Thumbnails are each page's og:image."""
import os, re, json, html, math
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
PAGES = {p['path']: p for p in json.load(open(T + '/pages.json'))}
ORDER = list(PAGES)
SKIP = {'index.html', 'explore/index.html', 'about/index.html'}
GROUPS = [('towns', 'Towns & counties'), ('districts', 'Districts'), ('state', 'Statewide'), ('people', 'People')]

def _group(path, p):
    if path.startswith('people/'): return 'people'
    if path.startswith('districts/'): return 'districts'
    if '-county/' in path: return 'towns'
    if p and p['kind'] in ('point', 'area') and 'District' not in p.get('label', ''): return 'towns'
    return 'state'

def _load():
    out = []
    for d, _, fs in os.walk(R):
        if any(x in d for x in ('/.git', '/tools', '/node_modules')): continue
        for f in fs:
            if not f.endswith('.html'): continue
            path = os.path.relpath(os.path.join(d, f), R)
            if path in SKIP: continue
            s = open(os.path.join(d, f)).read()
            p = PAGES.get(path)
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
            t = p['title'] if p else (html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip().rstrip('.') if h1 else f)
            img = re.search(r'og:image" content="[^"]*/images/([^"]+)"', s)
            desc = re.search(r'name="description" content="([^"]*)"', s)
            out.append(dict(path=path, t=t, img=img.group(1) if img else 'share.jpg', g=_group(path, p),
                            b=(p or {}).get('blurb') or '', pin=(p or {}).get('pin'),
                            k=html.unescape(desc.group(1)) if desc else '',
                            o=ORDER.index(path) if path in PAGES else -1))
    return out

ALL = _load()

def nearby(cur, n=6):
    me = next((x for x in ALL if x['path'] == cur), None)
    rest = [x for x in ALL if x['path'] != cur and x['g'] != 'people']
    if me and me['pin']:
        loc = sorted([x for x in rest if x['pin']], key=lambda x: math.dist(x['pin'], me['pin']))
        return loc[:n - 1] + sorted([x for x in rest if not x['pin'] and x['o'] >= 0], key=lambda x: -x['o'])[:1]
    return sorted([x for x in rest if x['o'] >= 0], key=lambda x: -x['o'])[:n]

CSS = '''/*stl*/.stl{margin:22px 0 0}.stl h3{margin:0 0 10px;font:600 20px/1.2 "Fraunces",Georgia,serif}
.stl a.r{display:flex;gap:12px;align-items:center;padding:9px 0;border-top:1px solid var(--line);color:var(--cream);text-decoration:none}
.stl a.r img{flex:0 0 auto;width:96px;height:auto;aspect-ratio:1200/630;object-fit:cover;border-radius:9px}
.stl a.r b{display:block;font:600 15.5px/1.25 "Fraunces",Georgia,serif}.stl a.r small{display:block;margin-top:3px;font:700 12.5px Karla,sans-serif;color:#e8a3c3}
.stl .all{display:block;width:100%;margin:12px 0 0;padding:13px;border-radius:14px;border:1px solid rgba(232,163,195,.5);background:rgba(232,163,195,.08);color:#fbefd8;font:700 15px Karla,sans-serif;cursor:pointer}
/*/stl*/'''

def near_block(cur, root):
    items = nearby(cur)
    if not items: return ''
    me = next((x for x in ALL if x['path'] == cur), None)
    head = 'More stories near here' if me and me['pin'] else 'More stories'
    rows = ''.join(f'<a class="r" href="{root}{x["path"]}"><img src="{root}images/{x["img"]}" alt="" loading="lazy" width="1200" height="630"><span><b>{html.escape(x["t"])}</b>'
                   + (f'<small>{html.escape(x["b"])}</small>' if x['b'] else '') + '</span></a>' for x in items)
    return (f'<div class="stl"><h3>{head}</h3>{rows}'
            f'<button type="button" class="all" data-allstories>See all {len(ALL)} stories</button></div>')

def menu_list(root, cur):
    secs = ''
    for g, name in GROUPS:
        xs = [x for x in ALL if x['g'] == g]
        xs.sort(key=lambda x: (x['o'] < 0, -x['o'], x['t'])) if g != 'people' else xs.sort(key=lambda x: x['t'].split()[-1])
        li = ''.join(f'<a href="{root}{x["path"]}"{" aria-current=page" if x["path"] == cur else ""} data-k="{html.escape((x["t"] + " " + x["k"] + " " + x["path"]).lower())}"><img src="{root}images/{x["img"]}" alt="" loading="lazy" width="1200" height="630"><span>{html.escape(x["t"])}</span></a>' for x in xs)
        secs += f'<div class="msg"><h4>{name} <span>{len(xs)}</span></h4><div class="ml">{li}</div></div>'
    return (f'<div class="mst" id="allstories"><h3>All {len(ALL)} stories</h3>'
            f'<input type="search" class="mss" placeholder="Search a town, district or name" aria-label="Search stories" autocomplete="off">'
            f'{secs}<p class="mse" hidden>No story yet. <a href="#join">Ask for your town →</a></p></div>')

MENU_CSS = '''.mnv{overflow-y:auto;-webkit-overflow-scrolling:touch}
.mst{margin:26px 0 10px}.mst h3{margin:0 0 10px;font:600 22px/1.2 "Fraunces",Georgia,serif;color:#fbefd8}
.mss{width:100%;box-sizing:border-box;padding:13px 15px;border-radius:14px;border:1px solid rgba(251,239,216,.2);background:#1f1a2b;color:#fbefd8;font:16px Karla,sans-serif}
.mss:focus{outline:none;border-color:#e8a3c3}
.msg{margin:18px 0 0}.msg h4{margin:0 0 8px;font:700 13px Karla,sans-serif;letter-spacing:.02em;color:#e8a3c3}.msg h4 span{color:#8f86a0;font-weight:500}
.ml{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -22px;padding:0 22px 6px;scroll-padding:0 22px;scrollbar-width:none}.ml::-webkit-scrollbar{display:none}
.ml a{flex:0 0 62%;max-width:240px;scroll-snap-align:start;color:#fbefd8;text-decoration:none;font:600 14px/1.25 Karla,sans-serif}
.ml a img{display:block;width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;border-radius:12px;border:1px solid rgba(251,239,216,.12);background:#1f1a2b}
.ml a span{display:block;margin-top:7px}
.ml a[aria-current] img{border:2px solid #f3b37a}.ml a.hide,.msg.hide{display:none}
.mse{margin:16px 0 0;color:#bdb4c7}.mse a{color:#e8a3c3}'''

MENU_JS = '''<script>(function(){var n=document.querySelector('.mnv'),q=n&&n.querySelector('.mss');if(!q)return;
q.addEventListener('input',function(){var v=q.value.trim().toLowerCase(),any=false;n.querySelectorAll('.msg').forEach(function(g){var c=0;g.querySelectorAll('.ml a').forEach(function(a){var k=a.dataset.k,ok=!v||v.split(/\\s+/).every(function(w){return /^\\d+$/.test(w)?new RegExp('(^|\\D)'+w+'(\\D|$)').test(k):k.indexOf(w)>-1});a.classList.toggle('hide',!ok);if(ok)c++});g.classList.toggle('hide',!c);if(c)any=true});n.querySelector('.mse').hidden=any});
document.addEventListener('click',function(e){var b=e.target.closest('[data-allstories]');if(!b)return;e.preventDefault();document.querySelector('.mnb').click();setTimeout(function(){var a=document.getElementById('allstories');a.scrollIntoView({block:'start'});},280)});})();</script>'''
