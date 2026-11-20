"""Show the move left (or right) on stacked comparison bars (.chart.cty).
Each bar after the first gets a dashed mark where the red/blue split was on the FIRST bar,
and an arrow from there to where it is now, labeled with the change in margin. Idempotent."""
import re
CSS = ('/*shift*/.cbar .gh{position:absolute;top:-9px;bottom:-9px;width:0;border-left:2px dashed rgba(251,239,216,.85);z-index:2}'
       '.cbar .mv{position:absolute;top:50%;height:4px;margin-top:-2px;background:#fbefd8;border-radius:2px;z-index:3;box-shadow:0 0 0 2px rgba(22,18,31,.55);transform-origin:right;transform:scaleX(0);transition:transform .9s .5s cubic-bezier(.3,.7,.3,1)}'
       '.cbar .mv.rt{transform-origin:left}'
       '.cbar .mv::before{content:"";position:absolute;top:50%;width:0;height:0;border:7px solid transparent;margin-top:-7px}'
       '.cbar .mv.lf::before{left:-11px;border-right:9px solid #fbefd8;border-left:0}.cbar .mv.rt::before{right:-11px;border-left:9px solid #fbefd8;border-right:0}'
       '.rv.on .cbar .mv,.rv.in .cbar .mv{transform:scaleX(1)}'
       '.cbar .ml{position:absolute;top:calc(100% + 8px);transform:translateX(-50%);white-space:nowrap;padding:3px 10px;border-radius:999px;font:800 13px Karla,sans-serif;z-index:3}'
       '.cbar .ml.lf{background:#2d6eff;color:#fff}.cbar .ml.rt{background:#e24854;color:#fff}'
       '.chart.cty .cb+.cb{margin-top:6px}.chart.cty .cb.hasmv .cn{margin-top:40px}/*/shift*/')

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
    if used: s = s.replace('</style>', CSS + '</style>', 1)
    return s
