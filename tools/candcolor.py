"""Color candidate names in body copy by party (blue/red gradient). Idempotent."""
import re
D=['Nell Brown','Robert Hunter','Jim Toomey','Toomey','Amanda Pusczek','Pusczek','Rick Pressnell','Pressnell','Doug Jones','Jones','Kamala Harris','Harris','Joe Biden','Biden','Allison Montgomery','Andrew Sneed','Sneed','Jared Sluss','Sluss','Marilyn Lands','Lands','Forrest Satterfield','Satterfield','Everett Wess','Wess','Hanu Karlapalem','Karlapalem','John Dickey','Dickey','Phillip Ensler','Janine Jordan','James Linderholm','Linderholm','Jessie Barcala','Barcala','Bobby Martin']
R=['Robert Aderholt','Aderholt','Maurice McCaney','McCaney','Kerry Underwood','Ben Harrison','Tim Melson','Melson','Tommy Tuberville','Tuberville','Donald Trump','Trump','Phillip Rigsby','Rigsby','Dale Strong','Strong','Sam Givhan','Givhan','Rex Reynolds','Reynolds','Aaron Thomas','Barry Moore','Parker Duncan Moore','Arthur Orr','Wes Kitchens','Danny Crawford','James Lomax','Bob Riley','Patrick Johnson','Andy Whitt','Danny Crawford','Danny F. Crawford','Larry Stutts','Stutts']
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
 'Tuberville':'tuberville','Sluss':'sluss','Givhan':'givhan','Sneed':'sneed','Rigsby':'rigsby','Satterfield':'satterfield'}
AVCSS='''/*cav*/.cav{display:inline-block;width:1.25em;height:1.25em;border-radius:50%;object-fit:cover;vertical-align:-.28em;margin:0 .28em 0 .05em;border:1.5px solid}
.cav.d{border-color:#6f9bff}.cav.r{border-color:#ff5a68}/*/cav*/
'''
def avatars(html, root):
    html=re.sub(r'<img class="cav[^>]*>','',html)
    html=re.sub(r'\n?/\*cav\*/.*?/\*/cav\*/\n?','',html,flags=re.S)
    seen=set()
    def rep(m):
        party,name=m.group(1),m.group(2)
        key=FACES.get(name)
        if not key or key in seen: return m.group(0)
        seen.add(key)
        return f'<img class="cav {party}" src="{root}images/people/{key}.webp" alt="" width="20" height="20" loading="lazy">'+m.group(0)
    html=re.sub(r'<span class="cand (d|r)">([^<]+?)(?:\'s)?</span>',rep,html)
    if seen: html=html.replace('</style>',AVCSS+'</style>',1)
    return html
