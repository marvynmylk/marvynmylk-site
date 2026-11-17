import sys, json
YOU=["Grew up on a Tennessee gravel road","Editor, data nerd, therapy veteran","From a nervous first post to 4 million views",
     "No doom-scrolling required","Your new favorite Southern nerd","Hope, with receipts","Maps that make you gasp",
     "Small towns moving left","Neighbors who ran, and won","The history they skipped in school","The math they don't show you",
     "Races decided by a few hundred votes","Charts you'll screenshot","Good news from the South","Proof you're not the only one",
     "The South, up close","Purple, not red","Logic and empathy, same sentence","Not giving up on the South",
     "Author of two books, written by human hands","Southern, born and stubborn"]
BOOKS=[("ps","The South is purple. Let me prove it."),("ps","Hope is the only thing stronger than fear."),("ps","Why 21 million Southern voters stayed home."),
       ("mo","Big Brother in orbit."),("mo","Her eyes glow with every feeling."),("mo","Who decides who the monster is?")]
CSS='''
.orb{position:relative;height:300px;margin:-6px -8px 10px}
.orb .me{position:absolute;left:50%;top:50%;width:96px;height:96px;margin:-48px 0 0 -48px;border-radius:50%;border:3px solid #e8a3c3;box-shadow:0 0 0 8px rgba(232,163,195,.08),0 0 40px rgba(201,167,232,.35);z-index:2}
.orb .chip{position:absolute;max-width:47%;display:flex;align-items:center;gap:8px;padding:8px 11px;border-radius:14px;font:700 13.5px/1.25 Karla,sans-serif;color:#fbefd8;text-align:left;cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;
 background:linear-gradient(#1f1a2b,#1f1a2b) padding-box,linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a) border-box;border:1.5px solid transparent;box-shadow:0 10px 22px -10px rgba(0,0,0,.8);
 animation:cin .7s cubic-bezier(.3,1.4,.5,1) both,cfl 5s ease-in-out .7s infinite alternate}
.orb .chip.bk{padding:7px 14px 7px 7px;gap:11px;font-size:14.5px}
.orb .chip.wide{left:0;right:0;margin:0 auto;width:max-content;max-width:88%}.orb .chip.top{top:1%}.orb .chip.bot{bottom:1%}
.orb .chip.bk img{flex:0 0 auto;width:34px;height:51px;object-fit:cover;border-radius:3px;box-shadow:0 4px 10px rgba(0,0,0,.5)}
.orb .chip.ps{background:linear-gradient(#241a33,#241a33) padding-box,linear-gradient(135deg,#b07cff,#e8a3c3) border-box;box-shadow:0 0 18px -4px rgba(176,124,255,.6)}
.orb .chip.mo{background:linear-gradient(#141c30,#141c30) padding-box,linear-gradient(135deg,#2f6fd6,#7fb0ff) border-box;box-shadow:0 0 18px -4px rgba(47,111,214,.7)}
.orb .chip small{display:block;font-weight:500;font-size:11.5px;color:#bdb4c7;margin-top:2px}
.orb .chip.out{animation:cout .9s ease forwards}
.orb .chip.pop{animation:cpop .35s ease forwards}
.orb .s0{left:0;top:2%}.orb .s1{right:0;top:6%}.orb .s2{left:0;top:38%;max-width:calc(50% - 60px)}.orb .s3{right:0;top:42%;max-width:calc(50% - 60px)}.orb .s4{left:2%;bottom:2%}.orb .s5{right:2%;bottom:4%}
@keyframes cin{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:none}}
@keyframes cfl{from{translate:0 -3px}to{translate:0 4px}}
@keyframes cout{to{opacity:0;transform:scale(.85)}}
@keyframes cpop{50%{transform:scale(1.15)}to{opacity:0;transform:scale(1.4)}}
@media (prefers-reduced-motion:reduce){.orb .chip{animation:none}}
'''
def stage(root):
    return f'<div class="orb" id="orb" aria-hidden="true"><img class="me" src="{root}images/profile.webp" alt="" width="96" height="96"></div>'
JS='''<script>
(function(){var o=document.getElementById('orb');if(!o)return;
var R=%s,Y=%s,B=%s,slots=[0,0,0,0,0,0],rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function sh(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),x=a[i];a[i]=a[j];a[j]=x}return a}
var YQ=sh(Y.slice()),BQ=sh(B.slice()),yi=0,bi=0,n=0;
function free(){var f=[];slots.forEach(function(v,i){if(!v)f.push(i)});return f}
function make(cls,html,occ){var c=document.createElement('div');c.className='chip '+cls;c.innerHTML=html;c.style.animationDelay='0s,'+(Math.random()*1.5).toFixed(2)+'s';occ.forEach(function(i){slots[i]=1});o.appendChild(c);
var life=setTimeout(function(){kill(c,occ,'out')},rm?999999:7500+Math.random()*2500);
c.addEventListener('click',function(){clearTimeout(life);kill(c,occ,'pop');setTimeout(spawn,250)})}
function spawn(){n++;var rows=[[0,1,'top'],[4,5,'bot']].filter(function(r){return!slots[r[0]]&&!slots[r[1]]});
if(n%%3===0&&rows.length){var r=rows[Math.floor(Math.random()*rows.length)],b=BQ[bi%%BQ.length];bi++;
make('bk wide '+r[2]+' '+b[0],'<img src="'+R+'images/'+(b[0]==='ps'?'purple-south-cover.jpg':'monster-on-tv-cover.jpg')+'" alt=""><span>'+b[1]+'<small>'+(b[0]==='ps'?'The Purple South':'The Monster on TV')+'</small></span>',[r[0],r[1]]);return}
var f=free();if(!f.length)return;var s=f[Math.floor(Math.random()*f.length)];make('s'+s,YQ[yi%%YQ.length],[s]);yi++}
function kill(c,occ,cls){if(c.dataset.d)return;c.dataset.d=1;c.classList.add(cls);setTimeout(function(){c.remove();occ.forEach(function(i){slots[i]=0})},cls==='out'?920:460)}
for(var q=0;q<(rm?6:4);q++)setTimeout(spawn,q*600);
if(!rm)setInterval(function(){if(!document.hidden&&free().length>1)spawn()},2300);
})();
</script>
'''
if __name__=='__main__':
    p,root=sys.argv[1],sys.argv[2]; s=open(p).read()
    if 'id="orb"' in s: sys.exit('has orb')
    old=f'<img src="{root}images/profile.webp" alt="Marvyn Mylk" width="76" height="76" loading="lazy">'
    assert old in s
    s=s.replace(old,stage(root),1).replace('</style>',CSS+'</style>',1)
    s=s.replace('<script data-goatcounter',JS%(json.dumps(root),json.dumps(YOU),json.dumps(BOOKS))+'<script data-goatcounter',1)
    open(p,'w').write(s); print('ok')
