"""Animated counters (.cnt with data-to) show their real number in the page itself, so readers
without scripts, link previews and search engines see it. A small script resets them to 0 just
before they count up (skipped for reduced motion)."""
import re
JS = ('<!--cntz--><script>(function(){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;'
      'document.querySelectorAll(".cnt[data-to]").forEach(function(e){var r=e.getBoundingClientRect();'
      'if(r.top>innerHeight||r.bottom<0)e.textContent=(e.dataset.pre||"")+(e.dataset.plus?"+":"")+"0"+(e.dataset.suf||"")})})();</script><!--/cntz-->')
def apply(s):
    s = re.sub(r'<!--cntz-->.*?<!--/cntz-->', '', s, flags=re.S)
    def rep(m):
        a = m.group(2)
        to = re.search(r'data-to="(-?[\d.]+)"', a)
        if not to: return m.group(0)
        v = float(to.group(1)); txt = f'{v:,.0f}' if v == int(v) else f'{v:,}'
        pre = re.search(r'data-pre="([^"]*)"', a); suf = re.search(r'data-suf="([^"]*)"', a)
        plus = '+' if 'data-plus' in a else ''
        return f'<{m.group(1)}{a}>{pre.group(1) if pre else ""}{plus}{txt}{suf.group(1) if suf else ""}</{m.group(1)}>'
    s2 = re.sub(r'<(b|span|strong|div)((?=[^>]*class="[^"]*\bcnt\b)[^>]*)>[^<]*</\1>', rep, s)
    if s2 != s or 'class="cnt' in s: s2 = s2.replace('</body>', JS + '</body>', 1)
    return s2
