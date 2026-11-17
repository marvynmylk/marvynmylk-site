import sys,re
CSS='''
.join{position:relative;margin:48px 0 0;padding:30px 22px 26px;border-radius:22px;background:radial-gradient(120% 90% at 50% 0%,rgba(150,90,220,.28),rgba(31,26,43,0) 70%),#1f1a2b;border:1px solid rgba(201,167,232,.28);text-align:center;overflow:hidden}
.join img{width:76px;height:76px;border-radius:50%;border:3px solid #e8a3c3;display:block;margin:0 auto 14px}
.join h2{margin:0 0 14px;font:600 clamp(28px,7vw,36px)/1.1 "Fraunces",Georgia,serif}
.join h2 span{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.join p{margin:0 auto 14px;max-width:34ch;font-size:17px;line-height:1.6}
.join p.why{color:var(--muted)}
.join form{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:20px auto 0;max-width:440px}
.join input[type=email]{flex:1 1 220px;min-width:0;padding:15px 16px;border-radius:14px;border:1px solid rgba(251,239,216,.25);background:#16121f;color:#fbefd8;font:500 17px Karla,sans-serif}
.join button{flex:0 0 auto;padding:15px 22px;border:0;border-radius:14px;background:linear-gradient(90deg,#c9a7e8,#e8a3c3 55%,#f3b37a);color:#16121f;font:700 17px Karla,sans-serif;cursor:pointer;min-height:48px}
.join button:disabled{opacity:.6}
.join .fine2{margin:14px 0 0;font-size:13px;color:var(--muted)}
.join .st{min-height:1.4em;margin:10px 0 0;font-weight:700;color:#e8a3c3}

.join form,.pitch form{display:grid;grid-template-columns:1fr;gap:10px;max-width:440px;margin:20px auto 0}
.join input[type=email],.pitch input[type=email]{width:100%;text-align:center}
.join button,.pitch button{width:100%}
.join .st,.pitch .st{min-height:0;margin:10px auto 0}
.join .st:empty,.pitch .st:empty{display:none}
.join .fine2,.pitch .fine2{margin:14px auto 0}
'''
def block(spot): return f'''<section class="join" id="join" aria-labelledby="join-h">
  <img src="../images/profile.webp" alt="Marvyn Mylk" width="76" height="76" loading="lazy">
  <h2 id="join-h">The South is <span>closer than you think.</span></h2>
  <p>I'm Marvyn. I live in North Alabama and track the races and numbers that show it. Get the next story in your inbox, plus a heads-up when my book comes out.</p>
  <form class="signup" name="book-news" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="book-news"><input type="hidden" name="signup-spot" value="{spot}">
    <p hidden><label>Leave this empty <input name="bot-field"></label></p>
    <label for="jemail" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Email address</label>
    <input id="jemail" name="email" type="email" placeholder="Your email" autocomplete="email" required>
    <button type="submit">Count me in</button>
  </form>
  <p class="st" role="status"></p>
  <p class="fine2">No spam. I'll never sell your email.</p>
</section>
'''
JS='''<script>
document.querySelectorAll('form.signup').forEach(function(f){var st=f.parentNode.querySelector('.st'),b=f.querySelector('button');
f.addEventListener('submit',async function(e){e.preventDefault();b.disabled=true;st.textContent='Adding you…';
try{var r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()});if(!r.ok)throw 0;st.textContent="You're in. Talk soon.";f.reset();}
catch(err){st.textContent='Something went wrong. Please try again.';}b.disabled=false;});});
</script>
'''
