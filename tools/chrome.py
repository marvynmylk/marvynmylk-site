"""Site-wide menu and FAQ styling, injected by page_end.py."""
MENU=[("Explore Alabama politics","explore/","The hub: maps, stories and news"),
      ("Books & author","about/","Meet Marvyn and his books"),
      ("How to vote in Alabama","guides/how-to-vote-in-alabama.html","ID, absentee and polling hours"),
      ("How close was your race?","play/how-close-alabama-2026.html","Every 2026 legislative race"),
      ("For media","about/#media","Interviews, data and photos")]
CSS='''
/*chrome*/.mnb{position:fixed;top:max(12px,env(safe-area-inset-top));right:14px;z-index:60;display:flex;align-items:center;justify-content:center;width:42px;height:42px;padding:0;border-radius:50%;transition:transform .3s ease,opacity .3s;border:1px solid rgba(251,239,216,.2);background:rgba(22,18,31,.82);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#fbefd8;font:700 15px Karla,sans-serif;cursor:pointer}
.mnb.hide{transform:translateY(-70px);opacity:0}
.mnb i{display:block;width:16px;height:2px;background:currentColor;border-radius:2px;box-shadow:0 -5px 0 currentColor,0 5px 0 currentColor}
.mnv{position:fixed;inset:0;z-index:70;background:rgba(16,12,24,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);display:flex;flex-direction:column;padding:max(70px,env(safe-area-inset-top)) 22px 30px;opacity:0;pointer-events:none;transition:opacity .25s ease}
.mnv.open{opacity:1;pointer-events:auto}
.mnv .x{position:absolute;top:max(14px,env(safe-area-inset-top));right:16px;width:44px;height:44px;border-radius:50%;border:1px solid rgba(251,239,216,.2);background:transparent;color:#fbefd8;font-size:24px;cursor:pointer}
.mnv .home{display:flex;align-items:center;gap:10px;margin:0 0 26px;color:#fbefd8;text-decoration:none;font:600 20px "Fraunces",Georgia,serif}
.mnv .home img{width:40px;height:40px;border-radius:50%}
.mnv a.it{display:block;padding:16px 4px;border-bottom:1px solid rgba(251,239,216,.1);color:#fbefd8;text-decoration:none;opacity:0;transform:translateY(10px);transition:opacity .35s ease,transform .35s ease}
.mnv.open a.it{opacity:1;transform:none}
.mnv a.it b{display:block;font:600 24px/1.2 "Fraunces",Georgia,serif}
.mnv a.it:nth-of-type(2) b{background:linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.mnv a.it small{display:block;margin-top:3px;color:#bdb4c7;font:15px Karla,sans-serif}
.faq{display:grid;gap:10px;counter-reset:fq}
.faq details{border:1px solid rgba(251,239,216,.12)!important;border-radius:16px;padding:0!important;background:#1f1a2b;overflow:hidden;transition:border-color .2s}
.faq details:nth-child(3n+1){--fc:#c9a7e8}.faq details:nth-child(3n+2){--fc:#e8a3c3}.faq details:nth-child(3n){--fc:#f3b37a}
.faq details[open]{border-color:var(--fc)!important}
.faq summary{counter-increment:fq;position:relative;display:block!important;padding:15px 46px 15px 58px!important;font:600 16.5px/1.3 "Fraunces",Georgia,serif!important;color:#fbefd8;cursor:pointer;list-style:none}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:"Q";position:absolute;left:14px;top:50%;transform:translateY(-50%);width:30px;height:30px;border-radius:10px;display:grid;place-items:center;font:700 14px Karla,sans-serif;color:#16121f;background:var(--fc)}
.faq summary::after{content:"+"!important;position:absolute;right:16px;top:50%;transform:translateY(-50%);font:400 24px Karla,sans-serif;color:var(--fc)!important;transition:transform .25s}
.faq details[open] summary::after{transform:translateY(-50%) rotate(45deg)}
.faq details p{margin:0!important;padding:0 18px 16px 58px!important;font-size:15.5px!important;line-height:1.55;color:#d9cfe2!important;animation:fqin .3s ease}
@keyframes fqin{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}.acts{display:flex;flex-wrap:wrap;gap:8px}.act{flex:1 1 0;min-width:0;flex-direction:column;justify-content:flex-start;gap:7px;padding:12px 4px 10px;border-radius:14px;text-align:center}.acts>.act:first-child{flex:1 1 100%;flex-direction:row;align-items:center;gap:12px;padding:13px 14px;text-align:left;background:linear-gradient(135deg,rgba(201,167,232,.2),rgba(243,179,122,.16));border-color:rgba(232,163,195,.55)}.acts>.act:first-child strong{font-size:16px}.acts>.act:first-child small{display:block!important;font-size:13px}.acts>.act:first-child::after{content:"→";margin-left:auto;padding-left:6px;font-weight:700;font-size:20px;color:#f3b37a}.act svg{width:40px;height:40px;padding:9px;border-radius:50%}.act strong{font-size:12.5px;line-height:1.2}.act small{display:none}.acts .regb{flex:1 1 100%!important;border-color:rgba(232,163,195,.55)!important;background:linear-gradient(135deg,rgba(201,167,232,.2),rgba(243,179,122,.16))!important}
.dc.lock{border:1.5px solid rgba(226,72,84,.6)!important;box-shadow:0 0 26px rgba(226,72,84,.16)}.dc.lock.dlk{border-color:rgba(91,140,255,.6)!important;box-shadow:0 0 26px rgba(91,140,255,.16)}
.lk{display:flex;align-items:center;gap:12px;margin:10px 0 8px}.lk svg{flex:0 0 auto;width:46px;height:46px;padding:11px;border-radius:50%;background:rgba(226,72,84,.16);fill:#ff6b76;animation:lkg 2.6s ease-in-out infinite}
.lk b{font:600 26px/1.1 "Fraunces",Georgia,serif;color:#ff6b76}.dlk .lk svg{background:rgba(91,140,255,.16);fill:#8fb0ff;animation-name:lkb}.dlk .lk b{color:#8fb0ff}
@keyframes lkg{0%,100%{box-shadow:0 0 10px rgba(226,72,84,.3)}50%{box-shadow:0 0 0 6px rgba(226,72,84,.1),0 0 26px rgba(226,72,84,.6)}}
@keyframes lkb{0%,100%{box-shadow:0 0 10px rgba(91,140,255,.3)}50%{box-shadow:0 0 0 6px rgba(91,140,255,.1),0 0 26px rgba(91,140,255,.6)}}
.keyl{display:inline-flex;align-items:center;gap:8px;margin-top:10px;padding:8px 14px;border-radius:999px;background:rgba(243,179,122,.12);border:1px solid rgba(243,179,122,.45);color:#f3b37a!important;font-weight:700;font-size:14px;text-decoration:none!important}.keyl svg{width:18px;height:18px;fill:#f3b37a}
@media (prefers-reduced-motion:reduce){.lk svg{animation:none}}
/*/chrome*/
'''
def menu(root):
    items=''.join(f'<a class="it" href="{root}{u}" style="transition-delay:{60+i*50}ms"><b>{t}</b><small>{d}</small></a>' for i,(t,u,d) in enumerate(MENU))
    return f'''<!--menu--><button class="mnb" type="button" aria-label="Open menu" aria-expanded="false"><i></i></button>
<nav class="mnv" aria-label="Main menu" hidden><button class="x" type="button" aria-label="Close menu">×</button><a class="home" href="{root or './'}"><img src="{root}images/profile.webp" alt="">Marvyn Mylk</a>{items}</nav>
<script>(function(){{var b=document.querySelector('.mnb'),n=document.querySelector('.mnv');function set(o){{if(o)n.hidden=false;requestAnimationFrame(function(){{n.classList.toggle('open',o)}});b.setAttribute('aria-expanded',o);document.documentElement.style.overflow=o?'hidden':'';if(!o)setTimeout(function(){{if(!n.classList.contains('open'))n.hidden=true}},260)}}
b.addEventListener('click',function(){{set(true)}});n.querySelector('.x').addEventListener('click',function(){{set(false)}});n.addEventListener('click',function(e){{if(e.target.closest('a'))set(false)}});document.addEventListener('keydown',function(e){{if(e.key==='Escape')set(false)}});var ly=scrollY;addEventListener('scroll',function(){{var y=scrollY;b.classList.toggle('hide',y>ly&&y>120);ly=y}},{{passive:true}})}})();</script><!--/menu-->
'''
