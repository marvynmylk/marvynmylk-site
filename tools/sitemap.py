"""Write sitemap.xml and robots.txt listing every page. Run after adding pages: python3 tools/sitemap.py"""
import os, subprocess, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(set(subprocess.check_output(['git', 'ls-files', '*.html'], cwd=R).decode().split()) |
               {os.path.relpath(os.path.join(d, f), R) for d, _, fs in os.walk(os.path.join(R, 'people')) for f in fs if f.endswith('.html')})
today = datetime.date.today().isoformat()
def loc(f):
    u = f[:-len('index.html')] if f.endswith('index.html') else f
    return 'https://marvynmylk.com/' + u
urls = ''.join(f'<url><loc>{loc(f)}</loc><lastmod>{today}</lastmod></url>\n' for f in files if not f.startswith(('tools/', 'node_modules/')))
open(os.path.join(R, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
open(os.path.join(R, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://marvynmylk.com/sitemap.xml\n')
print(urls.count('<url>'), 'pages')
