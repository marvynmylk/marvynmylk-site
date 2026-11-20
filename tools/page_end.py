"""Give a page the standard ending: the moving sign-up (book-news Netlify form) and the wordmark footer with site map.
Usage: python3 tools/page_end.py <page.html>
Pages in subfolders (articles/, play/, madison-county/) link back with ../; the landing page (index.html) uses #read-h."""
import sys, os, re, json, subprocess
T=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,T)
import orbit, footer, storymap, chrome, candcolor, bookstrip, lockmap, shift
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
# 3. story map above the sign-up (rebuilt every run so new pages appear)
s=re.sub(r'<!--storymap-->.*?<!--/storymap-->\n?','',s,flags=re.S)
s=re.sub(r'\n?(/\*smx\*/)?\.smx\{.*?(\.smx \.here\{animation:none\}\}(/\*/smx\*/)?)','',s,count=1,flags=re.S)
s=s.replace('</style>',storymap.CSS+'</style>',1)
cur=os.path.relpath(os.path.abspath(p),os.path.dirname(T)).replace(os.sep,'/')
s=lockmap.apply(s,cur)
s=shift.apply(s)
blk=storymap.block(cur,root,home=(cur=='index.html'))
if landing: blk='<!--storymap--><div class="wrap narrow">'+blk.replace('<!--storymap-->','',1).replace('<!--/storymap-->','',1)+'</div><!--/storymap-->\n'
if 'data-hub="1"' not in s:
    i=s.index('<section class="join"'); s=s[:i]+blk+s[i:]
# 4. menu + FAQ styles
s=re.sub(r'\n?/\*chrome\*/.*?/\*/chrome\*/','',s,flags=re.S)
s=s.replace('</style>',chrome.CSS+'</style>',1)
s=re.sub(r'<!--menu-->.*?<!--/menu-->\n?','',s,flags=re.S)
s=s.replace('<body>','<body>\n'+chrome.menu(root),1)
open(p,'w').write(s)
# 4b. book strip above the email box
s=open(p).read()
s=re.sub(r'/\*bks\*/.*?/\*/bks\*/\n?','',s,flags=re.S); s=s.replace('</style>',bookstrip.CSS+'</style>',1)
s=re.sub(r'<!--bks-->.*?<!--/bks-->','',s,flags=re.S)
j=s.index('<section class="join"'); k=s.index('<form class="signup"',j)
s=s[:k]+bookstrip.block(root)+'\n'+s[k:]
open(p,'w').write(s)
# 5. party colors on candidate names in body copy
s=open(p).read()
s=re.sub(r'\n?/\*cand\*/.*?/\*/cand\*/\n?','',s,flags=re.S)
s=s.replace('</style>',candcolor.CSS+'</style>',1)
s=candcolor.color(s)
s=candcolor.avatars(s,root)
open(p,'w').write(s)
# 6. footer
subprocess.run([sys.executable,T+'/footer.py',p,'#read-h' if landing else '../'],check=True)
print('page end ok',p)
