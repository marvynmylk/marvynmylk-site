"""The 'Explore North Alabama' story map that sits above the sign-up on every page.
Pins and cards come from tools/pages.json, so adding a page there puts it on every page's map
(re-run tools/page_end.py on every page)."""
import json, os, html
T=os.path.dirname(os.path.abspath(__file__))
B=json.load(open(T+'/storymap_base.json'))
PAGES=json.load(open(T+'/pages.json'))
VB=[100,-4,300,206]   # North Alabama, the Shoals to Jackson and Gadsden
CSS='''
/*smx*/.smx{margin:36px 0 0}
.smx h2{margin:0 0 4px}.smx .sub2{margin:0 0 12px;color:var(--muted);font-size:14.5px}
.smx .sub{margin:0 0 14px;color:var(--muted);font-size:15px}
.smx .mapbox{position:relative;border-radius:18px;overflow:hidden;background:#1a1526;border:1px solid var(--line);touch-action:pan-y}
.smx .mapbox.zoomed{touch-action:none}.smx .mapbox svg{cursor:grab}
.smx .zm{position:absolute;right:8px;bottom:8px;display:flex;flex-direction:column;gap:6px}
.smx .zm button{width:34px;height:34px;border-radius:10px;border:1px solid rgba(251,239,216,.2);background:rgba(22,18,31,.85);color:#fbefd8;font:700 18px/1 Karla,sans-serif;cursor:pointer}
.smx svg{display:block;width:100%;height:auto}
.smx .cty{fill:#2a2438;stroke:#16121f;stroke-width:.6;transition:fill .5s ease}
.smx .cty.home{fill:#342c47}.smx .cty.hl{fill:#4b3b7a}
.smx .cl{font:700 5.2px Karla,sans-serif;fill:rgba(251,239,216,.35);text-anchor:middle;pointer-events:none}
.smx .pin{cursor:pointer;transform-box:fill-box;transform-origin:50% 100%;opacity:0;transform:translateY(-6px) scale(.3);transition:opacity .45s ease,transform .55s cubic-bezier(.3,1.6,.5,1)}
.smx.on .pin{opacity:1;transform:none}
.smx .pin path{fill:url(#smg);stroke:#16121f;stroke-width:.7}
.smx .pin circle{fill:#16121f}
.smx .pin.sel path{fill:#fbefd8}
.smx .pin text{font:700 4px Karla,sans-serif;fill:#fbefd8;paint-order:stroke;stroke:#16121f;stroke-width:1.4px;opacity:0;transition:opacity .2s}
.smx .pin.sel text,.smx .pin:hover text{opacity:1}
.smx .here{fill:none;stroke:#f3b37a;stroke-width:.8;transform-box:fill-box;transform-origin:center;animation:smxp 1.8s ease-out infinite}
@keyframes smxp{from{transform:scale(.6);opacity:1}to{transform:scale(2.2);opacity:0}}
.smx .card{display:flex;gap:12px;align-items:center;margin:12px 0 0;padding:10px;border-radius:16px;background:var(--ink-2);border:1px solid var(--line);color:var(--cream);text-decoration:none;animation:smxc .35s ease}
.smx .card img{flex:0 0 auto;width:92px;height:auto;aspect-ratio:1200/630;object-fit:cover;border-radius:10px}
.smx .card b{display:block;font:600 15px/1.25 "Fraunces",Georgia,serif}
.smx .card small{display:none}
.smx .card em{display:block;font-style:normal;font-weight:700;font-size:13.5px;color:#e8a3c3;margin-top:5px}
@keyframes smxc{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.smx .state{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:10px -20px 0;padding:2px 20px 6px}
.smx .state::-webkit-scrollbar{display:none}
.smx .state a{flex:0 0 auto;padding:8px 13px;border-radius:999px;background:var(--ink-2);border:1px solid var(--line);color:var(--cream);text-decoration:none}
.smx .state a.cur{border-color:#f3b37a}
.smx .state img{display:none}
.smx .state b{display:block;white-space:nowrap;font:700 13px/1.2 Karla,sans-serif; "Fraunces",Georgia,serif}
.smx .hint{font-size:12.5px;color:var(--muted);margin:8px 0 0;text-align:center}
.smx .strip{position:relative;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;margin:12px -20px 0;padding:2px 20px 8px;scroll-padding:0 20px}
.smx .strip::-webkit-scrollbar{display:none}
.smx .sc{flex:0 0 148px;scroll-snap-align:start;color:var(--cream);text-decoration:none;border-radius:14px;padding:6px 6px 8px;background:var(--ink-2);border:1.5px solid var(--line);transition:border-color .3s,transform .3s}
.smx .sc img{display:block;width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;border-radius:9px}
.smx .sc b{display:-webkit-box;-webkit-line-clamp:3;min-height:3.75em;-webkit-box-orient:vertical;overflow:hidden;margin:7px 2px 0;font:600 13.5px/1.25 "Fraunces",Georgia,serif}
.smx .sc.cur{border-color:#e8a3c3;transform:translateY(-2px)}.smx .sc.me{border-color:#f3b37a}
.smx .sc small{display:block;margin:4px 2px 0;font:700 11.5px Karla,sans-serif;color:#e8a3c3}
@media (prefers-reduced-motion:reduce){.smx .pin{opacity:1;transform:none;transition:none}.smx .here{animation:none}}/*/smx*/
'''
PIN='M0,0 C-1.2,-2.6 -4.2,-4.6 -4.2,-8 A4.2,4.2 0 1 1 4.2,-8 C4.2,-4.6 1.2,-2.6 0,0Z'
def block(cur, root, home=False):
    pts=[p for p in PAGES if p['kind'] in ('point','area')]
    st=[p for p in PAGES if p['kind']=='state']
    sel=next((i for i,p in enumerate(pts) if p['path']==cur),0)
    svg=f'<svg viewBox="{" ".join(map(str,VB))}" role="img" aria-label="Map of North Alabama with pins for each local story"><defs><linearGradient id="smg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8a3c3"/><stop offset="1" stop-color="#c9a7e8"/></linearGradient></defs>'
    svg+=''.join(f'<path class="cty{" home" if c["n"]=="Madison" else ""}" data-c="{html.escape(c["n"])}" d="{c["d"]}"/>' for c in B['counties'])
    svg+=''.join(f'<text class="cl" x="{c["cx"]+(-14 if c["n"]=="Madison" else 0)}" y="{c["cy"]+ (26 if c["n"]=="Madison" else 0)}">{html.escape(c["n"])}</text>' for c in B['counties'])
    for i,p in enumerate(pts):
        x,y=p['pin']; here=p['path']==cur
        svg+=f'<g transform="translate({x},{y}) scale(1.5)"><g class="pin{" sel" if i==sel else ""}" data-i="{i}" style="transition-delay:{120+i*140}ms" tabindex="0" role="button" aria-label="{html.escape(p["title"])}">'
        if here: svg+='<circle class="here" cx="0" cy="-8" r="5"/>'
        svg+=f'<path d="{PIN}"/><circle cx="0" cy="-8" r="1.6"/><text x="{-5.5 if x>VB[0]+VB[2]-70 else 5.5}" y="-6" text-anchor="{"end" if x>VB[0]+VB[2]-70 else "start"}">{html.escape(("You are here · " if here else "")+p["label"])}</text></g></g>'
    svg+='</svg>'
    data=[dict(t=p['title'],b=p['blurb'],u=root+p['path'],img=root+'images/'+p['img'],c=p.get('counties',[]),here=p['path']==cur) for p in pts]
    states=''.join(f'<a href="{root}{p["path"]}"{" class=cur" if p["path"]==cur else ""}><img src="{root}images/{p["img"]}" alt="" loading="lazy" width="1200" height="630"><b>{html.escape(p["title"])}</b></a>' for p in st)
    js='''<script>(function(){var s=document.getElementById('smx');if(!s)return;var D=%s,card=s.querySelector('.card'),pins=s.querySelectorAll('.pin');
function show(i){var d=D[i];pins.forEach(function(p){p.classList.toggle('sel',p.dataset.i==i)});s.querySelectorAll('.cty').forEach(function(c){c.classList.toggle('hl',d.c.indexOf(c.dataset.c)>-1)});
card.href=d.u;card.innerHTML='<img src="'+d.img+'" alt=""><span><b>'+d.t+'</b><small>'+d.b+'</small><em>'+(d.here?'You\\u2019re on this page':'Read it \\u2192')+'</em></span>';card.style.animation='none';card.offsetHeight;card.style.animation=''}
pins.forEach(function(p){p.addEventListener('click',function(){show(+p.dataset.i)});p.addEventListener('keydown',function(e){if(e.key==='Enter')show(+p.dataset.i)})});

var box=s.querySelector('.mapbox'),sv=box.querySelector('svg'),V0=sv.getAttribute('viewBox').split(' ').map(Number),V=V0.slice();
function apply(){var mw=V0[2]/6;V[2]=Math.min(V0[2],Math.max(mw,V[2]));V[3]=V[2]*V0[3]/V0[2];V[0]=Math.min(V0[0]+V0[2]-V[2],Math.max(V0[0],V[0]));V[1]=Math.min(V0[1]+V0[3]-V[3],Math.max(V0[1],V[1]));sv.setAttribute('viewBox',V.join(' '));box.classList.toggle('zoomed',V[2]<V0[2]-0.5);
var k=V[2]/V0[2];s.querySelectorAll('.pin').forEach(function(p){p.parentNode.setAttribute('transform',p.parentNode.dataset.t+' scale('+(1.5*Math.max(k,.35))+')')})}
s.querySelectorAll('.pin').forEach(function(p){var t=p.parentNode.getAttribute('transform');p.parentNode.dataset.t=t.replace(/ scale\\([^)]*\\)/,'')});
function zoom(f,cx,cy){var r=sv.getBoundingClientRect();var px=cx==null?.5:(cx-r.left)/r.width,py=cy==null?.5:(cy-r.top)/r.height;var x=V[0]+V[2]*px,y=V[1]+V[3]*py;V[2]*=f;V[3]*=f;V[0]=x-V[2]*px;V[1]=y-V[3]*py;apply()}
function selc(){var p=s.querySelector('.pin.sel');if(!p)return[null,null];var r=p.getBoundingClientRect();return[r.left+r.width/2,r.bottom]}
box.querySelector('[data-z=in]').addEventListener('click',function(){var c=selc();zoom(.6,c[0],c[1])});box.querySelector('[data-z=out]').addEventListener('click',function(){zoom(1/.6)});
sv.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey&&V[2]>=V0[2]-.5&&e.deltaY>0)return;e.preventDefault();zoom(e.deltaY<0?.85:1/.85,e.clientX,e.clientY)},{passive:false});
var pts={},last=null,pd=null,moved=false;
sv.addEventListener('pointerdown',function(e){pts[e.pointerId]=e;moved=false;if(Object.keys(pts).length===1)last={x:e.clientX,y:e.clientY}});
sv.addEventListener('pointermove',function(e){if(!pts[e.pointerId])return;pts[e.pointerId]=e;var a=Object.values(pts),r=sv.getBoundingClientRect();
if(a.length===2){var d=Math.hypot(a[0].clientX-a[1].clientX,a[0].clientY-a[1].clientY);if(pd){zoom(pd/d,(a[0].clientX+a[1].clientX)/2,(a[0].clientY+a[1].clientY)/2);moved=true}pd=d;return}
if(last&&box.classList.contains('zoomed')){var dx=e.clientX-last.x,dy=e.clientY-last.y;if(Math.abs(dx)+Math.abs(dy)>3)moved=true;V[0]-=dx*V[2]/r.width;V[1]-=dy*V[3]/r.height;apply();last={x:e.clientX,y:e.clientY}}});
function up(e){delete pts[e.pointerId];pd=null;if(!Object.keys(pts).length)last=null}
sv.addEventListener('pointerup',up);sv.addEventListener('pointercancel',up);sv.addEventListener('click',function(e){if(moved){e.stopPropagation();e.preventDefault()}},true);
sv.addEventListener('dblclick',function(e){e.preventDefault();zoom(.6,e.clientX,e.clientY)});
new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){s.classList.add('on');o.disconnect()}})},{threshold:.1}).observe(s);show(%d)})();</script>'''%(json.dumps(data),sel)
    if True:
        allp=pts+st
        strip=''.join(f'<a class="sc{" me" if p["path"]==cur else ""}" href="{root}{p["path"]}" data-i="{i if i<len(pts) else -1}"><img src="{root}images/{p["img"]}" alt="" loading="lazy" width="1200" height="630"><b>{html.escape(p["title"])}</b></a>' for i,p in enumerate(allp))
        js=js.replace("card.href=d.u;card.innerHTML='<img src=\"'+d.img+'\" alt=\"\"><span><b>'+d.t+'</b><small>'+d.b+'</small><em>'+(d.here?'You\\u2019re on this page':'Read it \\u2192')+'</em></span>';card.style.animation='none';card.offsetHeight;card.style.animation=''","var st=s.querySelector('.strip'),sc=st.querySelector('.sc[data-i=\"'+i+'\"]');st.querySelectorAll('.sc').forEach(function(c){c.classList.toggle('cur',c===sc)});if(sc&&!quiet){lock=Date.now();st.scrollTo({left:sc.offsetLeft-20,behavior:'smooth'})}")
        js=js.replace("function show(i){","var lock=0,quiet=false;function show(i){")
        js=js.replace("show(%d)})();</script>"%sel,"show(%d);var st=s.querySelector('.strip'),tm;var hh=st.querySelector('.sc.me');if(hh&&hh.dataset.i==='-1'){lock=Date.now();st.scrollLeft=hh.offsetLeft-20}st.addEventListener('scroll',function(){clearTimeout(tm);tm=setTimeout(function(){if(Date.now()-lock<900)return;var best=null,bd=1e9;st.querySelectorAll('.sc').forEach(function(c){var d=Math.abs(c.offsetLeft-20-st.scrollLeft);if(d<bd){bd=d;best=c}});if(best&&best.dataset.i!=='-1'){quiet=true;show(+best.dataset.i);quiet=false}},120)},{passive:true})})();</script>"%sel)
        return f'''<!--storymap--><section class="smx" id="smx" aria-labelledby="smx-h">
<h2 id="smx-h">{"Dig into the data" if home else "Explore North Alabama"}</h2>
<p class="sub2">Tap a pin to find its story, or swipe through all {len(allp)}.</p>
<div class="mapbox">{svg}<div class="zm"><button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button></div></div>
<div class="strip">{strip}</div>
</section>
{js}<!--/storymap-->
'''
    return f'''<!--storymap--><section class="smx" id="smx" aria-labelledby="smx-h">
<h2 id="smx-h">Explore North Alabama</h2>
<p class="sub2">Nearby towns and districts. Tap a pin.</p>
<div class="mapbox">{svg}<div class="zm"><button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button></div></div>
<a class="card" href="#"></a>
<div class="state">{states}</div>
</section>
{js}<!--/storymap-->
'''
