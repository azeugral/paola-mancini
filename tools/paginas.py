# Monta as páginas internas a partir de _partes/ (cabeçalho e rodapé vêm do index.html).
# Uso: python -I tools/paginas.py && python -I tools/processar.py
import os, re, html

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(SITE, '_partes')
ler = lambda n: open(os.path.join(P, n), encoding='utf-8').read()
head, nav, foot = ler('head.html'), ler('nav.html'), ler('foot.html')
URL = 'https://azeugral.github.io/paola-mancini/'

for nome in ['portfolio.html', 'cursos.html', 'agendar.html', '404.html']:
    meta, corpo = ler(nome).split('---\n', 1)
    m = dict(l.split(': ', 1) for l in meta.strip().splitlines())
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>' + html.escape(m['title']) + '</title>', h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda x: x.group(1) + html.escape(m['desc']), h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x.group(1) + html.escape(m['title']), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda x: x.group(1) + URL + (m['atual'] if m['atual'] != '404.html' else ''), h)
    h = re.sub(r'<link rel="preload" as="image"[^>]*>\n', '', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', h, flags=re.S)
    if nome == '404.html':
        h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/paola-mancini/">')
    n = nav.replace('href="' + m['atual'] + '"', 'href="' + m['atual'] + '" aria-current="page"', 1)
    open(os.path.join(SITE, nome), 'w', encoding='utf-8').write(h + n + corpo + '\n' + foot)
    print('ok', nome)
