"""Small always-visible book strip inside the sign-up card, right above the email box."""
CSS='''/*bks*/.bks{display:flex;align-items:center;gap:12px;max-width:440px;margin:14px auto 4px;padding:10px 12px;border-radius:14px;background:rgba(22,18,31,.55);border:1px solid rgba(201,167,232,.25);text-decoration:none;color:#fbefd8;text-align:left}
.bks .cv2{display:flex;flex:0 0 auto}
.bks .cv2 img{width:38px;height:57px;object-fit:cover;border-radius:3px;box-shadow:0 6px 14px rgba(0,0,0,.55)}
.bks .cv2 img+img{margin-left:-10px;transform:rotate(5deg)}
.bks .cv2 img:first-child{transform:rotate(-4deg)}
.bks b{display:block;font:600 15px/1.25 "Fraunces",Georgia,serif}
.bks small{display:block;font-size:12.5px;color:#e8a3c3;font-weight:700;margin-top:2px}/*/bks*/
'''
def block(root):
    return f'''<!--bks--><a class="bks" href="{root}about/"><span class="cv2"><img src="{root}images/purple-south-cover.jpg" alt="The Purple South" width="38" height="57" loading="lazy"><img src="{root}images/monster-on-tv-cover.jpg" alt="The Monster on TV" width="38" height="57" loading="lazy"></span><span><b>The Purple South &amp; The Monster on TV</b><small>Two new books, coming soon. Be the first to know.</small></span></a><!--/bks-->'''
