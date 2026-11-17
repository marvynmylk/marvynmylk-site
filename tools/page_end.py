"""Give a page the standard ending: the moving sign-up (book-news Netlify form) and the wordmark footer with site map.
Usage: python3 tools/page_end.py <page.html>
Pages in subfolders (articles/, play/, madison-county/) link back with ../; the landing page (index.html) uses #read-h."""
import sys, os, re, json, subprocess
T=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,T)
import orbit, footer
ns={}; exec(open(T+'/signup.py').read(),ns)
p=sys.argv[1]; landing=os.path.basename(p)=='index.html' and os.path.dirname(os.path.abspath(p))==os.path.dirname(T)
root='' if landing else '../'
s=open(p).read()
# 1. sign-up form (one per page)
if 'class="join"' not in s:
    spot=os.path.splitext(os.path.basename(p))[0]
    s=s.replace('</style>',ns['CSS']+'</style>',1)
    i=s.index('<div class="fineprint">') if '<div class="fineprint">' in s else s.index('</article>')
    s=s[:i]+ns['block'](spot)+s[i:]
    s=s.replace('<script data-goatcounter',ns['JS']+'<script data-goatcounter',1)
# 2. floating chips around the profile photo
if 'id="orb"' not in s:
    m=re.search(r'<img (?:class="jpic" )?src="'+re.escape(root)+r'images/profile\.webp" alt="Marvyn Mylk" width="76" height="76" loading="lazy">',s)
    s=s[:m.start()]+orbit.stage(root)+s[m.end():]
    s=s.replace('</style>',orbit.CSS+'</style>',1)
    s=s.replace('<script data-goatcounter',orbit.JS%(json.dumps(root),json.dumps(orbit.YOU),json.dumps(orbit.BOOKS))+'<script data-goatcounter',1)
open(p,'w').write(s)
# 3. footer
subprocess.run([sys.executable,T+'/footer.py',p,'#read-h' if landing else '../'],check=True)
print('page end ok',p)
