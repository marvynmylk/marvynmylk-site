import sys
import os
SP=os.path.dirname(os.path.abspath(__file__))
W,H,D=open(SP+'/wordmark_path.txt').read().split(None,2)
def mark(cls='wm'):
    return f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="Marvyn Mylk"><defs><linearGradient id="wmg" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#c9a7e8"/><stop offset=".55" stop-color="#e8a3c3"/><stop offset="1" stop-color="#f3b37a"/></linearGradient></defs><path fill="url(#wmg)" fill-rule="evenodd" d="{D.strip()}"/></svg>'
CSS='''
/*foot*/.sitefoot{margin-top:40px;padding:30px max(20px,env(safe-area-inset-left,0px)) 40px;text-align:center;background:#1f1a2b;border-top:1px solid rgba(251,239,216,.14)}
.sitefoot .wm{display:block;width:min(210px,58vw);height:auto;margin:0 auto 12px;overflow:visible;filter:drop-shadow(0 0 18px rgba(232,163,195,.35))}
.sitefoot .sl{margin:0 auto;max-width:30ch;font:600 17px/1.35 "Fraunces",Georgia,serif;color:#fbefd8}
.sitefoot .sl b{font-weight:600;background:linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.sitefoot .vm{display:inline-block;margin-top:18px;font:700 16px Karla,sans-serif;color:#fbefd8;text-decoration:underline;text-decoration-color:#e8a3c3;text-decoration-thickness:2px;text-underline-offset:5px}
.sitefoot small{display:block;margin-top:12px;font:12.5px Karla,sans-serif;color:#7d7489}
.sitefoot details.smw{max-width:600px;margin:16px auto 0}
.sitefoot details.smw summary{list-style:none;cursor:pointer;display:inline-block;font:700 14px Karla,sans-serif;color:#bdb4c7;text-decoration:underline;text-decoration-color:#e8a3c3;text-underline-offset:4px}
.sitefoot details.smw summary::-webkit-details-marker{display:none}
.sitefoot .smap{display:grid;grid-template-columns:1fr 1fr;gap:16px 14px;margin:16px 0 0;padding-top:16px;border-top:1px solid rgba(251,239,216,.1);text-align:left}
.sitefoot .smap h3{margin:0 0 8px;font:600 14px "Fraunces",Georgia,serif;color:#fbefd8}
.sitefoot .smap ul{list-style:none;margin:0;padding:0}
.sitefoot .smap li{margin:0 0 6px}
.sitefoot .smap a{font:500 12.5px/1.35 Karla,sans-serif;color:#bdb4c7;text-decoration:none}
.sitefoot .smap a:hover{color:#e8a3c3}
@media (min-width:700px){.sitefoot .smap{grid-template-columns:repeat(4,1fr)}}
/*/foot*/
'''

MAP=[("Stories",[("Alabama almost elected a Democratic governor","articles/alabama-governor-2026-tuberville-jones-county-results.html"),("Every precinct in Madison County moved left","articles/madison-county-precinct-shifts-2026.html"),("How many Alabamians didn't vote in 2024?","articles/alabama-voters-who-stayed-home-2024.html"),("Is Huntsville turning blue?","articles/is-huntsville-turning-blue.html"),("Alabama's 5th District, 2026","articles/alabama-5th-congressional-district-2026.html"),("Morgan County: Strong vs. Sneed","articles/morgan-county-dale-strong-andrew-sneed-2026.html")]),
 ("Explore",[("Explore Alabama politics","explore/"),("How close was your race?","play/how-close-alabama-2026.html"),("Jones won 6 districts where no Democrat ran","articles/jones-won-no-democrat-ran-alabama-2026.html"),("How to run for office","articles/how-to-run-for-office-in-alabama.html"),("How to vote in Alabama","guides/how-to-vote-in-alabama.html"),("House District 10","districts/alabama-house-district-10.html"),("House District 25","districts/alabama-house-district-25.html"),("Senate District 7","districts/alabama-senate-district-7.html"),("House District 8","districts/alabama-house-district-8.html"),("House District 21","districts/alabama-house-district-21.html"),("County Commission District 1","districts/madison-county-commission-district-1.html"),("Madison, town by town","madison-county/madison.html"),("Monrovia, town by town","madison-county/monrovia.html"),("Hampton Cove","madison-county/hampton-cove.html"),("Decatur","morgan-county/decatur.html"),("South Huntsville","madison-county/south-huntsville.html"),("Athens","limestone-county/athens.html"),("Florence","lauderdale-county/florence.html"),("Muscle Shoals","colbert-county/muscle-shoals.html"),("Pelham","shelby-county/pelham.html"),("Meridianville, town by town","madison-county/meridianville.html")]),
 ("People",[("Doug Jones","people/doug-jones.html"),("Tommy Tuberville","people/tommy-tuberville.html"),("Dale Strong","people/dale-strong.html"),("Andrew Sneed","people/andrew-sneed.html"),("Jared Sluss","people/jared-sluss.html"),("Sam Givhan","people/sam-givhan.html"),("Allison Montgomery","people/allison-montgomery.html"),("Phillip Rigsby","people/phillip-rigsby.html"),("Marilyn Lands","people/marilyn-lands.html"),("Aaron Thomas","people/aaron-thomas.html"),("Janine Jordan","people/janine-jordan.html"),("Patrick Johnson","people/patrick-johnson.html"),("Forrest Satterfield","people/forrest-satterfield.html"),("Rex Reynolds","people/rex-reynolds.html")]),
 ("Books",[("About Marvyn","about/"),("The Purple South","about/"),("The Monster on TV","about/"),("For media","about/#media")]),
 ("Follow",[("TikTok","https://www.tiktok.com/@betterargument"),("Instagram","https://www.instagram.com/authormarvynmylk"),("Threads","https://www.threads.net/@marvynmylk")])]
def smap(root):
    out='<nav class="smap" aria-label="Site map">'
    for h,links in MAP:
        out+=f'<div><h3>{h}</h3><ul>'
        for t,u in links:
            href=u if u.startswith('http') else (root+u if not u.startswith('#') else (root or '')+u)
            ext=' target="_blank" rel="noopener"' if u.startswith('http') else ''
            out+=f'<li><a href="{href}"{ext}>{t}</a></li>'
        out+='</ul></div>'
    return out+'</nav>'
def block(home, label='View more', root='../'):
    return f'''<footer class="sitefoot">
<a href="{home}" aria-label="Marvyn Mylk home">{mark()}</a>
<p class="sl">Elections are decided by a handful of votes. <b>Be a voter.</b></p>
<details class="smw"><summary>Site map</summary>{smap(root)}</details>
<small>© 2026 Marvyn Mylk</small>
</footer>
'''
if __name__=='__main__':
    p,home=sys.argv[1],sys.argv[2]; label=sys.argv[3] if len(sys.argv)>3 else 'View more'; root='' if home.startswith('#') else '../'
    s=open(p).read()
    import re
    if 'class="sitefoot"' in s:
        s=re.sub(r'<footer class="sitefoot">.*?</footer>\n',block(home,label,root),s,count=1,flags=re.S)
        s=re.sub(r'/\*foot\*/.*?/\*/foot\*/\n?','',s,flags=re.S)
        s=re.sub(r'\n\.sitefoot\{.*?(@media \(min-width:700px\)\{\.sitefoot \.smap\{grid-template-columns:repeat\(4,1fr\)\}\}|\.sitefoot small\{[^}]*\})','',s,flags=re.S)
        s=s.replace('</style>',CSS+'</style>',1)
        open(p,'w').write(s); print('updated',p); sys.exit()
    s=s.replace('</style>',CSS+'</style>',1)
    if '<footer>' in s:   # landing page: replace old footer
        a=s.index('<footer>'); b=s.index('</footer>')+len('</footer>')
        s=s[:a]+block(home,label,root)+s[b:]
    else:
        s=s.replace('</main>','</main>\n'+block(home,label,root),1)
    open(p,'w').write(s); print('ok',p)
