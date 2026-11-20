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
.townnudge{text-align:center;margin:6px 0 0}.townnudge a{color:#e8a3c3;font-weight:700;font-size:15px;text-decoration:none;border-bottom:1px dashed rgba(232,163,195,.5)}
.tsheet{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;max-width:440px;margin:0 auto;padding:18px 16px 14px;border-radius:20px;background:rgba(31,26,43,.97);border:1px solid rgba(232,163,195,.45);box-shadow:0 20px 50px rgba(0,0,0,.55);transform:translateY(130%);transition:transform .45s cubic-bezier(.3,1.3,.5,1);color:#fbefd8}
.tsheet.up{transform:none}.tsheet h3{margin:0 30px 4px 0;font:600 20px/1.2 Fraunces,Georgia,serif}.tsheet p{margin:0 0 12px;font-size:14.5px;color:var(--muted)}
.tsheet .x{position:absolute;top:8px;right:8px;width:36px;height:36px;border:0;border-radius:50%;background:transparent;color:#fbefd8;font-size:22px;cursor:pointer}
.tsheet .row{display:grid;grid-template-columns:1fr;gap:8px}.tsheet input{padding:13px 14px;border-radius:12px;border:1px solid rgba(251,239,216,.25);background:#16121f;color:#fbefd8;font:500 16px Karla,sans-serif}
.tsheet button.go{padding:13px;border:0;border-radius:12px;background:linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a);color:#16121f;font:800 16px Karla,sans-serif;cursor:pointer}
.tsheet .st{margin:8px 0 0;font-weight:700;color:#e8a3c3;min-height:0}.tsheet .st:empty{display:none}
@media (prefers-reduced-motion:reduce){.tsheet{transition:none}}/*/town*/
'''
SHEET = '''<!--tsheet--><div class="tsheet" id="tsheet" role="dialog" aria-labelledby="tsh-h" hidden>
<button class="x" type="button" aria-label="Close">×</button>
<h3 id="tsh-h">Having fun? 👀</h3>
<p>Tell me your town. I'll send you its story when I dig into it.</p>
<div class="row"><input type="email" id="tsh-e" placeholder="Your email" autocomplete="email" aria-label="Email address">
<input type="text" id="tsh-t" placeholder="Your town" list="towns" autocomplete="address-level2" aria-label="Your town">
<button class="go" type="button">Sign me up</button></div><p class="st" role="status"></p></div><!--/tsheet-->
'''
JS = '''<!--tsjs--><script>(function(){
var K='mm_pages',ls=function(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}};
var f=document.querySelector('form.signup'),sh=document.getElementById('tsheet');if(!f||!sh)return;
var gc=function(p){try{window.goatcounter&&window.goatcounter.count({path:p,title:p,event:true})}catch(e){}};
f.addEventListener('submit',function(){ls('mm_signed','1');gc('signup-bottom')});
function open(src){if(!sh.hidden&&sh.classList.contains('up'))return;sh.hidden=false;requestAnimationFrame(function(){sh.classList.add('up')});gc('sheet-shown-'+src)}
function close(){sh.classList.remove('up');setTimeout(function(){sh.hidden=true},450);ls('mm_closed',String(Date.now()))}
sh.querySelector('.x').addEventListener('click',close);
document.querySelectorAll('[data-sheet]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();open('link')})});
sh.querySelector('.go').addEventListener('click',async function(){var e=document.getElementById('tsh-e'),t=document.getElementById('tsh-t'),st=sh.querySelector('.st'),b=this;
if(!e.value||!e.checkValidity()){st.textContent='Add your email first.';e.focus();return}
f.querySelector('[name=email]').value=e.value;var ft=f.querySelector('[name=town]');if(ft)ft.value=t.value;var sp=f.querySelector('[name=signup-spot]');if(sp&&sp.value.indexOf('sheet:')!==0)sp.value='sheet:'+sp.value;
b.disabled=true;st.textContent='Adding you…';
try{var r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()});if(!r.ok)throw 0;
st.textContent=t.value?"You're in. "+t.value+" is on my list.":"You're in. Talk soon.";ls('mm_signed','1');gc('signup-sheet');setTimeout(function(){sh.classList.remove('up')},2200)}
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
        s = re.sub(r'(<p class="hero-c">.*?</p>)', r'\1<p class="townnudge"><a href="#join" data-sheet>Want your town next? Tell me →</a></p>', s, count=1, flags=re.S)
    s = s.replace('</style>', CSS + '</style>', 1)
    s = s.replace('</body>', SHEET + JS + '</body>', 1)
    return s
