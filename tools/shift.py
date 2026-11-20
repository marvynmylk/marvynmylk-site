"""Show the move left (or right) on stacked comparison bars (.chart.cty).
Each bar after the first gets a dashed mark where the red/blue split was on the FIRST bar,
and an arrow from there to where it is now, labeled with the change in margin. Idempotent."""
import re
CSS = ('/*shift*/.chart.cty{padding:18px 16px}.chart.cty .cb{margin:0 0 18px}.chart.cty .ct2{margin-bottom:6px}.chart.cty .win{font-size:12.5px;padding:3px 9px}.chart.cty .race{font-size:13px}.chart.cty .cn{font-size:13.5px;margin-top:6px}.chart.cty .cn strong{font-size:17px}.chart.cty .cbar{height:26px}'
       '.cbar .gh{position:absolute;top:-4px;bottom:-4px;width:0;border-left:2px dashed rgba(207,224,255,.5);z-index:2;opacity:0}'
       '.cbar .mv{position:absolute;top:50%;height:3px;margin-top:-1.5px;background:#cfe0ff;border-radius:2px;z-index:3;opacity:0;transform-origin:right;transform:scaleX(0);filter:drop-shadow(0 0 4px rgba(143,176,255,.9))}'
       '.cbar .mv.rt{transform-origin:left;background:#ffd0d4}'
       '.cbar .mv::before{content:"";position:absolute;top:50%;width:0;height:0;border:5px solid transparent;margin-top:-5px}'
       '.cbar .mv.lf::before{left:-7px;border-right:7px solid #cfe0ff;border-left:0}.cbar .mv.rt::before{right:-7px;border-left:7px solid #ffd0d4;border-right:0}'
       '.rv.on .cbar .mv,.rv.in .cbar .mv{animation:mvA 3.4s .4s ease-out forwards}'
       '.rv.on .cbar .gh,.rv.in .cbar .gh{animation:mvG 3.4s .4s ease-out forwards}'
       '@keyframes mvA{0%{opacity:0;transform:scaleX(0)}30%{opacity:1;transform:scaleX(1)}70%{opacity:1;transform:scaleX(1)}100%{opacity:0;transform:scaleX(1)}}'
       '@keyframes mvG{0%{opacity:0}20%{opacity:1}70%{opacity:1}100%{opacity:.35}}'
       '@media (prefers-reduced-motion:reduce){.rv.on .cbar .mv,.rv.in .cbar .mv{animation:none}.cbar .gh{opacity:.35}}'
       '.cbar .ml{display:none}/*/shift*/')


BAR = re.compile(r'<div class="cbar"><i class="r" style="width:([\d.]+)%"></i>(?:<i class="o" style="width:([\d.]+)%"></i>)?<i class="d" style="width:([\d.]+)%"></i>')

def apply(s):
    s = re.sub(r'<i class="gh"[^>]*></i>|<i class="mv[^"]*"[^>]*></i>|<span class="ml[^"]*"[^>]*>[^<]*</span>', '', s)
    s = s.replace('<div class="cb hasmv">', '<div class="cb">')
    s = re.sub(r'/\*shift\*/.*?/\*/shift\*/', '', s, flags=re.S)
    out, pos, used = [], 0, False
    heroes=[int(a or b) for a,b in re.findall(r'class="cnt"[^>]*data-to="(\d+)"|data-to="(\d+)"[^>]*class="cnt"', s)]
    for m in re.finditer(r'<div class="chart cty[^"]*"[^>]*>', s):
        if m.start() < pos: continue
        end = s.find('<p class="note"', m.end())
        nxt = s.find('<div class="chart', m.end())
        if end < 0 or (0 <= nxt < end): end = nxt if nxt >= 0 else len(s)
        block = s[m.end():end]
        bars = list(BAR.finditer(block))
        if len(bars) < 2:
            continue
        r0, o0, d0 = (float(x or 0) for x in bars[0].groups()); base = r0 + o0
        m0 = r0 - d0
        nb, last = [], 0
        for i, b in enumerate(bars):
            nb.append(block[last:b.end()]); last = b.end()
            if i == 0: continue
            r, o, d = (float(x or 0) for x in b.groups()); here = r + o
            shift = abs((r - d) - m0)
            if shift < 1: continue
            near=[h for h in heroes if abs(h-shift)<=1]
            shift=near[0] if near else round(shift)
            lf = here < base; c = 'lf' if lf else 'rt'
            lo, hi = sorted((base, here))
            word = 'left' if lf else 'right'
            nb.append(f'<i class="gh" style="left:{base:.1f}%"></i><i class="mv {c}" style="left:{lo:.1f}%;width:{hi - lo:.1f}%"></i>'
                      f'<span class="ml {c}" style="left:{(lo + hi) / 2:.1f}%">{"← " if lf else ""}{shift} points {word}{"" if lf else " →"}</span>')
            used = True
        nb.append(block[last:])
        block = ''.join(nb)
        # give bars with arrows room for the label
        block = re.sub(r'<div class="cb">(?=(?:(?!<div class="cb">).)*?<i class="mv)', '<div class="cb hasmv">', block, flags=re.S)
        out.append(s[pos:m.end()]); out.append(block); pos = end
    out.append(s[pos:])
    s = ''.join(out)
    if used or 'class="chart cty' in s: s = s.replace('</style>', CSS + '</style>', 1)
    return s
