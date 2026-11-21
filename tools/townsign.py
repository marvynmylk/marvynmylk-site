"""Tell me your town" sign-up. Idempotent; run by page_end.py on every page.
- Adds a town field to the one book-news form (Netlify emails every field, so the notification shows the town and the page).
- On article pages, the sign-up leads with "Want your town next?" (the home page keeps the author intro).
- A small sheet slides up on a reader's SECOND page (after some scrolling). It is not a second form: it fills in and
  sends the page's one book-news form. Closed = hidden for 30 days; never shown again after signing up.
- One quiet link under the big number on pages that have one opens the same sheet."""
import re
TOWNS = ['Huntsville', 'Madison', 'Decatur', 'Athens', 'Florence', 'Muscle Shoals', 'Sheffield', 'Tuscumbia', 'Hartselle',
         'Cullman', 'Scottsboro', 'Guntersville', 'Albertville', 'Arab', 'Boaz', 'Fort Payne', 'Harvest', 'Hazel Green',
         'Meridianville', 'Monrovia', 'Toney', 'New Market', 'Owens Cross Roads', 'Hampton Cove', 'Gurley', 'New Hope',
         'Triana', 'Moulton', 'Russellville', 'Rogersville', 'Killen', 'Priceville', 'Falkville', 'Ardmore', 'Elkmont',
         'Birmingham', 'Hoover', 'Tuscaloosa', 'Montgomery', 'Auburn', 'Opelika', 'Mobile', 'Gadsden', 'Anniston', 'Dothan',
         'Nashville', 'Franklin', 'Murfreesboro', 'Chattanooga', 'Knoxville', 'Memphis', 'Clarksville', 'Columbia',
         'Fayetteville', 'Lawrenceburg', 'Pulaski', 'Winchester', 'Tullahoma', 'Shelbyville', 'Hendersonville', 'Johnson City']
CSS = '''/*town*/.join input[name=town]{width:100%;text-align:center;padding:15px 16px;border-radius:14px;border:1px solid rgba(251,239,216,.25);background:#16121f;color:#fbefd8;font:500 17px Karla,sans-serif}
.townnudge{text-align:center;margin:28px 0 0}.townnudge a{color:#e8a3c3;font-weight:700;font-size:15px;text-decoration:none;border-bottom:1px dashed rgba(232,163,195,.5)}
.tsheet{position:fixed;left:10px;right:10px;bottom:10px;z-index:60;max-width:420px;margin:0 auto;border-radius:22px;overflow:hidden;background:linear-gradient(180deg,#241c34,#1a1526);box-shadow:0 24px 60px rgba(0,0,0,.6),0 0 0 1px rgba(232,163,195,.35);transform:translateY(120%);transition:transform .5s cubic-bezier(.3,1.25,.5,1);color:#fbefd8}
.tsheet.up{transform:none}
.tsheet .tmap{position:relative;height:104px;background:radial-gradient(120% 140% at 70% 10%,rgba(138,92,240,.35),transparent 60%),#1a1526}
.tsheet .tmap svg{position:absolute;inset:0;width:100%;height:100%}
.tsheet .tmap .c{fill:#2a2140;stroke:#4a3d66;stroke-width:.6}.tsheet .tmap .p{fill:#e8a3c3;opacity:.85}
.tsheet .tmap .q{transform-box:fill-box;transform-origin:50% 100%;animation:tqb 1.8s ease-in-out infinite}
.tsheet .tmap .ring{fill:none;stroke:#ffd60a;stroke-width:1.2;transform-box:fill-box;transform-origin:center;animation:tqr 1.8s ease-out infinite}
@keyframes tqb{50%{transform:translateY(-3px)}}@keyframes tqr{0%{opacity:.9;transform:scale(.4)}100%{opacity:0;transform:scale(2.2)}}
.tsheet .tmap::after{content:"";position:absolute;left:0;right:0;bottom:0;height:40px;background:linear-gradient(transparent,#241c34)}
.tsheet .in{padding:2px 18px 16px}
.tsheet h3{margin:0 34px 6px 0;font:600 22px/1.15 Fraunces,Georgia,serif}.tsheet h3 span{background:linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.tsheet p{margin:0 0 12px;font-size:14.5px;line-height:1.45;color:#cfc6dc}
.tsheet .x{position:absolute;top:10px;right:10px;z-index:2;width:34px;height:34px;border:0;border-radius:50%;background:rgba(22,18,31,.7);color:#fbefd8;font-size:20px;line-height:34px;cursor:pointer}
.tsheet input{width:100%;box-sizing:border-box;padding:14px 15px;border-radius:14px;border:1px solid rgba(251,239,216,.22);background:#120e19;color:#fbefd8;font:600 17px Karla,sans-serif}
.tsheet input:focus{outline:none;border-color:#e8a3c3;box-shadow:0 0 0 3px rgba(232,163,195,.2)}
.tsheet .chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 12px}.tsheet .chips button{padding:6px 11px;border-radius:999px;border:1px solid rgba(232,163,195,.4);background:rgba(232,163,195,.08);color:#f2d9e6;font:700 13px Karla,sans-serif;cursor:pointer}
.tsheet button.go{width:100%;padding:14px;border:0;border-radius:14px;background:linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a);color:#16121f;font:800 16px Karla,sans-serif;cursor:pointer;margin-top:10px}
.tsheet button.go:disabled{opacity:.6}
.tsheet .fine{margin:8px 0 0;text-align:center;font-size:12.5px;color:#9d93ad}
.tsheet .st{margin:8px 0 0;font-weight:700;color:#e8a3c3;text-align:center}.tsheet .st:empty{display:none}
.tsheet .step[hidden]{display:none}
.tsheet .done{text-align:center;padding:6px 0 4px}.tsheet .done b{display:block;font:600 22px/1.2 Fraunces,Georgia,serif;margin:6px 0 4px}
@media (prefers-reduced-motion:reduce){.tsheet{transition:none}}/*/town*/
'''
import json, os
def _map():
    T = os.path.dirname(os.path.abspath(__file__))
    B = json.load(open(os.path.join(T, 'storymap_base.json'))); P = json.load(open(os.path.join(T, 'pages.json')))
    c = ''.join(f'<path class="c" d="{x["d"]}"/>' for x in B['counties'])
    p = ''.join(f'<circle class="p" cx="{x["pin"][0]}" cy="{x["pin"][1]}" r="2.6"/>' for x in P if x.get('pin') and x['kind'] == 'point')
    q = ('<g transform="translate(385,40)"><circle class="ring" r="6"/><g class="q"><path d="M0,0 C-1.2,-2.6 -4.2,-4.6 -4.2,-8 A4.2,4.2 0 1 1 4.2,-8 C4.2,-4.6 1.2,-2.6 0,0Z" transform="scale(1.6)" fill="#ffd60a" stroke="#16121f" stroke-width=".5"/>'
         '<text y="-11.5" text-anchor="middle" font-family="Karla,sans-serif" font-weight="800" font-size="8" fill="#16121f">?</text></g></g>')
    return f'<svg viewBox="115 8 300 80" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{c}{p}{q}</svg>'
SUGG = ['Hartselle', 'Albertville', 'Fort Payne', 'Cullman', 'Nashville']
SHEET = ('<!--tsheet--><div class="tsheet" id="tsheet" role="dialog" aria-labelledby="tsh-h" hidden>'
 '<button class="x" type="button" aria-label="Close">×</button><div class="tmap">' + _map() + '</div><div class="in">'
 '<div class="step" data-s="1"><h3 id="tsh-h">Is your town <span>missing?</span></h3>'
 "<p>Tell me a place in Alabama or Tennessee you want to see here. I'll dig into it.</p>"
 '<input type="text" id="tsh-t" placeholder="Town or neighborhood" list="towns" autocomplete="address-level2" aria-label="Town or neighborhood">'
 '<div class="chips">' + ''.join(f'<button type="button">{t}</button>' for t in SUGG) + '</div>'
 '<button class="go nx" type="button">Next →</button></div>'
 '<div class="step" data-s="2" hidden><h3>Where should I <span>send it?</span></h3>'
 "<p class=\"why\">I'll email you when it's up, plus a heads-up when my books come out.</p>"
 '<input type="email" id="tsh-e" placeholder="Your email" autocomplete="email" aria-label="Email address">'
 '<button class="go sb" type="button">Send it to me</button><p class="fine">No spam. I\'ll never sell your email.</p></div>'
 '<div class="step done" data-s="3" hidden><div style="font-size:30px">💜</div><b class="dh">Got it.</b><p>I\'ll let you know when it\'s up.</p></div>'
 '<p class="st" role="status"></p></div></div><!--/tsheet-->\n')
JS = '''<!--tsjs--><script>(function(){
var K='mm_pages',ls=function(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}};
var f=document.querySelector('form.signup'),sh=document.getElementById('tsheet');if(!f||!sh)return;
var gc=function(p){try{window.goatcounter&&window.goatcounter.count({path:p,title:p,event:true})}catch(e){}};
f.addEventListener('submit',function(){ls('mm_signed','1');gc('signup-bottom')});
var st=sh.querySelector('.st'),t=document.getElementById('tsh-t'),e=document.getElementById('tsh-e');
function step(n){sh.querySelectorAll('.step').forEach(function(x){x.hidden=x.dataset.s!=n});st.textContent='';var i=sh.querySelector('.step[data-s="'+n+'"] input');if(i&&sh.classList.contains('up'))setTimeout(function(){i.focus()},50)}
function open(src){if(!sh.hidden&&sh.classList.contains('up'))return;sh.hidden=false;requestAnimationFrame(function(){sh.classList.add('up')});gc('sheet-shown-'+src)}
function close(){sh.classList.remove('up');setTimeout(function(){sh.hidden=true},500);ls('mm_closed',String(Date.now()))}
sh.querySelector('.x').addEventListener('click',close);
document.querySelectorAll('[data-sheet]').forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();open('link')})});
sh.querySelectorAll('.chips button').forEach(function(b){b.addEventListener('click',function(){t.value=b.textContent;step(2)})});
sh.querySelector('.nx').addEventListener('click',function(){if(!t.value.trim()){st.textContent='Type a town, or tap one above.';t.focus();return}step(2)});
t.addEventListener('keydown',function(ev){if(ev.key=='Enter'){ev.preventDefault();sh.querySelector('.nx').click()}});
e.addEventListener('keydown',function(ev){if(ev.key=='Enter'){ev.preventDefault();sh.querySelector('.sb').click()}});
sh.querySelector('.sb').addEventListener('click',async function(){var b=this;
if(!e.value||!e.checkValidity()){st.textContent='Add your email so I can send it.';e.focus();return}
f.querySelector('[name=email]').value=e.value;var ft=f.querySelector('[name=town]');if(ft)ft.value=t.value;var sp=f.querySelector('[name=signup-spot]');if(sp&&sp.value.indexOf('sheet:')!==0)sp.value='sheet:'+sp.value;
b.disabled=true;st.textContent='Sending…';
try{var r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()});if(!r.ok)throw 0;
sh.querySelector('.dh').textContent=t.value.trim()+' is on my list.';step(3);ls('mm_signed','1');gc('signup-sheet');setTimeout(function(){sh.classList.remove('up')},3200)}
catch(x){st.textContent='Something went wrong. Please try again.'}b.disabled=false});
var seen=[];try{seen=JSON.parse(ls(K)||'[]')}catch(x){}var here=location.pathname;if(seen.indexOf(here)<0){seen.push(here);ls(K,JSON.stringify(seen.slice(-50)))}
var closed=+(ls('mm_closed')||0);if(ls('mm_signed')||Date.now()-closed<2592e6||seen.length<2)return;
var done=false;function chk(){if(done)return;var y=window.scrollY+innerHeight,h=document.documentElement.scrollHeight;var j=document.getElementById('join');
if(j&&j.getBoundingClientRect().top<innerHeight)return;if(y/h>.4){done=true;open('auto')}}
addEventListener('scroll',chk,{passive:true});addEventListener('scroll',function(){var j=document.getElementById('join');if(j&&sh.classList.contains('up')&&j.getBoundingClientRect().top<innerHeight*.8)sh.classList.remove('up')},{passive:true});setTimeout(chk,12000)})();</script><!--/tsjs-->
'''
DATALIST = '<datalist id="towns">' + ''.join(f'<option value="{t}">' for t in TOWNS) + '</datalist>'

def apply(s, landing):
    s = re.sub(r'\n?/\*town\*/.*?/\*/town\*/\n?', '', s, flags=re.S)
    s = re.sub(r'<!--tsheet-->.*?<!--/tsheet-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--tsjs-->.*?<!--/tsjs-->\n?', '', s, flags=re.S)
    s = re.sub(r'<p class="townnudge">.*?</p>', '', s)
    if 'form class="signup"' not in s: return s
    # town field + datalist
    s = re.sub(r'<label for="jtown"[^>]*>.*?</label><input id="jtown"[^>]*>', '', s)
    s = re.sub(r'<datalist id="towns">.*?</datalist>', '', s)
    s = s.replace('autocomplete="email" required>',
                  'autocomplete="email" required><label for="jtown" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Your town</label><input id="jtown" name="town" type="text" placeholder="Your town" list="towns" autocomplete="address-level2">' + DATALIST, 1)
    s = re.sub(r'(<form class="signup".*?<button type="submit">)[^<]*(</button>)', r'\1Sign me up\2', s, count=1, flags=re.S)
    if not landing:
        s = re.sub(r'<h2 id="join-h">.*?</h2>', '<h2 id="join-h">Want <span>your town next?</span></h2>', s, count=1, flags=re.S)
        s = re.sub(r'(<h2 id="join-h">.*?</h2>\s*)<p>.*?</p>', r"\1<p>Sign up and tell me your town. I'll send you its story when I dig into it, plus a heads-up when my books come out.</p>", s, count=1, flags=re.S)
        # one quiet link under the big number
        s = re.sub(r'(<h2>What you can do</h2>)', r'<p class="townnudge"><a href="#join" data-sheet>Is your town missing? Tell me →</a></p>\1', s, count=1)
    s = s.replace('</style>', CSS + '</style>', 1)
    s = s.replace('</body>', SHEET + JS + '</body>', 1)
    return s
