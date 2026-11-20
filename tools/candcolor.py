"""Color candidate names in body copy by party (blue/red gradient). Idempotent."""
import re
D=['Nell Brown','Robert Hunter','Jim Toomey','Toomey','Amanda Pusczek','Pusczek','Rick Pressnell','Pressnell','Doug Jones','Jones','Kamala Harris','Harris','Joe Biden','Biden','Allison Montgomery','Andrew Sneed','Sneed','Jared Sluss','Sluss','Marilyn Lands','Lands','Forrest Satterfield','Satterfield','Everett Wess','Wess','Hanu Karlapalem','Karlapalem','John Dickey','Dickey','Phillip Ensler','Janine Jordan','James Linderholm','Linderholm','Jessie Barcala','Barcala','Bobby Martin']
R=['Brock Colvin','Jamie Kiel','Jeana Ross','Mike Kirkland','Scott Stadthagen','Ritchie Whorton','David Faulkner','Danny Garrett','Kenneth Paschal','Margie Wilcox','Joe Lovvorn','Andy Whitt','Lloyd Peeples','Jay Hovey','Robert Aderholt','Aderholt','Maurice McCaney','McCaney','Kerry Underwood','Ben Harrison','Tim Melson','Melson','Tommy Tuberville','Tuberville','Donald Trump','Trump','Phillip Rigsby','Rigsby','Dale Strong','Strong','Sam Givhan','Givhan','Rex Reynolds','Reynolds','Aaron Thomas','Barry Moore','Parker Duncan Moore','Arthur Orr','Wes Kitchens','Danny Crawford','James Lomax','Bob Riley','Patrick Johnson','Andy Whitt','Danny Crawford','Danny F. Crawford','Larry Stutts','Stutts']
NAMES=sorted([(n,'d') for n in D]+[(n,'r') for n in R],key=lambda x:-len(x[0]))
RX=re.compile(r"(?<![\w-])("+'|'.join(re.escape(n) for n,_ in NAMES)+r")(?:'s)?(?![\w-])")
PARTY=dict(NAMES)
# Last names that are also places: only color them when used as a person (followed by a verb or vote count)
PLACE={'Montgomery':'d'}
RXP=re.compile(r"(?<![\w-])(?<!Allison )(Montgomery)(?:'s)?(?= (?:carried|won|beat|got|held|flipped|led|kept|took|\d))")
CSS='''/*cand*/.cand{font-weight:700;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.cand.d{background-image:linear-gradient(90deg,#6f9bff,#b9ccff)}.cand.r{background-image:linear-gradient(90deg,#ff5a68,#ffb0a8)}/*/cand*/
'''
SKIPTAG={'script','style','svg','a','h1','h2','h3','button','title','option','select','textarea','summary','head','em'}
SKIPCLASS=('faceoff','dc','pcard','hc','card','nc','smx','join','sitefoot','mnv','orb','cbar','cn','pbar','bn','vb','pb','push','lost','stats','facts','who','tile','q','bk2','answer','hero','ahero','cty','win','race','tl','quotes','cand','nw','state','grow','gap','dl','connect','fv','flips','slope')
VOID={'img','br','hr','input','meta','link','source','wbr','path','circle','line','rect','stop','use'}
def color(html):
    a=html.find('<article'); b=html.rfind('</article>')
    if a<0 or b<0: return html
    seg=html[a:b]; out=[]; stack=[]
    for tok in re.split(r'(<[^>]+>)',seg):
        if tok.startswith('<'):
            m=re.match(r'<(/?)([a-zA-Z0-9]+)([^>]*)>',tok)
            if m:
                close,tag,attrs=m.group(1),m.group(2).lower(),m.group(3)
                if close:
                    while stack:
                        t,_=stack.pop()
                        if t==tag: break
                elif tag not in VOID and not attrs.rstrip().endswith('/'):
                    cl=re.search(r'class="([^"]*)"',attrs); stack.append((tag,cl.group(1).split() if cl else []))
            out.append(tok); continue
        skip=any(t in SKIPTAG or any(c in SKIPCLASS for c in cls) for t,cls in stack)
        inbody=any(t in ('p','li') for t,_ in stack)
        if skip or not inbody or not tok.strip(): out.append(tok); continue
        t=RX.sub(lambda m:f'<span class="cand {PARTY[m.group(1)]}">{m.group(0)}</span>',tok)
        t=RXP.sub(lambda m:f'<span class="cand {PLACE[m.group(1)]}">{m.group(0)}</span>',t)
        out.append(t)
    return html[:a]+''.join(out)+html[b:]

# Small face next to a candidate's name, first mention per page, so readers learn who's who.
FACES={'Doug Jones':'jones','Tommy Tuberville':'tuberville','Marilyn Lands':'lands','Allison Montgomery':'montgomery',
 'Phillip Rigsby':'rigsby','Jared Sluss':'sluss','Sam Givhan':'givhan','Andrew Sneed':'sneed','Dale Strong':'strong',
 'Janine Jordan':'jordan','Patrick Johnson':'johnson','Forrest Satterfield':'satterfield','Rex Reynolds':'reynolds','Aaron Thomas':'thomas',
 'Tuberville':'tuberville','Sluss':'sluss','Givhan':'givhan','Sneed':'sneed','Rigsby':'rigsby','Satterfield':'satterfield',
 'Jones':'jones','Strong':'strong','Lands':'lands','Montgomery':'montgomery','Jordan':'jordan','Johnson':'johnson','Reynolds':'reynolds','Thomas':'thomas'}
AVCSS='''/*cav*/.cav{display:inline-block;width:1.25em;height:1.25em;border-radius:50%;object-fit:cover;vertical-align:-.28em;margin:0 .28em 0 .05em;border:1.5px solid}
.cav.d{border-color:#6f9bff}.cav.r{border-color:#ff5a68}/*/cav*/
'''
def avatars(html, root, cur=''):
    own={'people/janine-jordan.html':'jordan','people/forrest-satterfield.html':'satterfield','people/marilyn-lands.html':'lands'}.get(cur)
    html=re.sub(r'<img class="cav[^>]*>','',html)
    html=re.sub(r'\n?/\*cav\*/.*?/\*/cav\*/\n?','',html,flags=re.S)
    seen=set(); used=[False]
    def rep(m):
        if m.group(0).startswith('<h2'):
            seen.clear(); return m.group(0)
        party,name=m.group(2),m.group(3)
        key=FACES.get(name)
        if not key or key in seen or key==own: return m.group(0)
        seen.add(key); used[0]=True
        return f'<img class="cav {party}" src="{root}images/people/{key}.webp" alt="" width="20" height="20" loading="lazy">'+m.group(0)
    html=re.sub(r'<h2[\s>]|(<span class="cand (d|r)">([^<]+?)(?:\'s)?</span>)',rep,html)
    if used[0]: html=html.replace('</style>',AVCSS+'</style>',1)
    return html

# Candidate names link to their profile page (people/<slug>.html), except on the profile itself.
PROFILES={'Janine Jordan':'janine-jordan','Forrest Satterfield':'forrest-satterfield','Satterfield':'forrest-satterfield','Marilyn Lands':'marilyn-lands','Lands':'marilyn-lands'}
LCSS='''/*pl*/a.pl{text-decoration:none;color:inherit}a.pl .cand{background-size:100% 100%;border-bottom:1.5px dotted currentColor}a.pl:hover .cand{filter:brightness(1.2)}/*/pl*/
'''
def link(html, root, cur):
    html=re.sub(r'<a class="pl" href="[^"]*">((?:<img class="cav[^>]*>)?<span class="cand [dr]">[^<]*</span>)</a>',r'\1',html)
    html=re.sub(r'\n?/\*pl\*/.*?/\*/pl\*/\n?','',html,flags=re.S)
    used=[False]
    def rep(m):
        slug=PROFILES.get(m.group(3))
        if not slug or cur==f'people/{slug}.html': return m.group(0)
        used[0]=True
        return f'<a class="pl" href="{root}people/{slug}.html">{m.group(0)}</a>'
    html=re.sub(r'(<img class="cav[^>]*>)?<span class="cand (d|r)">([^<]+?)(?:\'s)?</span>',rep,html)
    if used[0]: html=html.replace('</style>',LCSS+'</style>',1)
    return html
