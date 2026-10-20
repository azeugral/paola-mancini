# Gera as imagens do site a partir de _ref/ig (extraído do Instagram).
# Uso: python -I tools/processar.py   (a partir de site/)
import json, os, re
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
REF = os.path.join(os.path.dirname(SITE), '_ref')
IG = os.path.join(REF, 'ig')
OUT = os.path.join(SITE, 'assets', 'p')
IMG = os.path.join(SITE, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

# (arquivo, categoria, legenda curta, foco vertical 0..1)
FOTOS = [
    # Noivas
    ('016-1', 'noivas', 'Noiva Thainara, making-of no ateliê', .35),
    ('016-3', 'noivas', 'Noiva Thainara, coque alto com tiara', .3),
    ('016-4', 'noivas', 'Noiva Thainara, finalização do penteado', .3),
    ('016-2', 'noivas', 'Noiva Thainara no salão do ateliê', .4),
    ('047-10', 'noivas', 'Editorial de noiva, ondas longas', .3),
    ('047-5', 'noivas', 'Editorial de noiva, ondas marcadas', .3),
    ('047-2', 'noivas', 'Editorial de noiva com buquê', .35),
    ('047-7', 'noivas', 'Editorial de noiva, luz natural', .3),
    ('083-1', 'noivas', 'Noiva com tiara e ondas soltas', .3),
    ('080-1', 'noivas', 'Noiva com tiara, renda e brilho', .3),
    ('087-1', 'noivas', 'Noiva com buquê no ateliê', .3),
    ('093-1', 'noivas', 'Noiva com cachos e tiara', .3),
    ('124-1', 'noivas', 'Noiva, make luminosa e tiara', .3),
    ('143-1', 'noivas', 'Noiva em estúdio, véu longo', .35),
    ('150-1', 'noivas', 'Noiva com véu, pele iluminada', .3),
    ('166-1', 'noivas', 'Noiva com coque alto e franja', .3),
    ('172-1', 'noivas', 'Noiva em estúdio, coque clássico', .35),
    ('175-1', 'noivas', 'Noiva com tulipas', .3),
    ('185-1', 'noivas', 'Noiva com coque baixo e buquê', .3),
    ('189-1', 'noivas', 'Noiva em ensaio ao ar livre', .35),
    ('191-1', 'noivas', 'Noiva no campo, vestido de cauda', .45),
    ('192-1', 'noivas', 'Noiva com cachos ao sol', .3),
    ('199-1', 'noivas', 'Ensaio de noiva no campo', .4),
    ('202-1', 'noivas', 'Noiva em estúdio escuro', .4),
    ('123-1', 'noivas', 'Noiva com coque e capa', .3),
    # Penteados
    ('026-1', 'penteados', 'Coque baixo texturizado', .5),
    ('030-1', 'penteados', 'Coque ruivo com volume', .45),
    ('039-1', 'penteados', 'Coque com marcações em técnica russa', .4),
    ('088-1', 'penteados', 'Semi preso em ondas', .45),
    ('095-1', 'penteados', 'Coque com ondas esculpidas', .45),
    ('097-1', 'penteados', 'Trança lateral volumosa', .45),
    ('098-1', 'penteados', 'Coque com trança para noivas', .45),
    ('111-1', 'penteados', 'Semi preso com laço do próprio cabelo', .45),
    ('113-1', 'penteados', 'Coque baixo com acessório', .45),
    ('117-1', 'penteados', 'Rabo trançado estruturado', .45),
    ('118-1', 'penteados', 'Rabo de cavalo com ondas', .45),
    ('153-1', 'penteados', 'Coque baixo clássico', .45),
    ('156-1', 'penteados', 'Semi preso loiro em ondas', .4),
    ('168-1', 'penteados', 'Coque bola clássico', .4),
    ('176-1', 'penteados', 'Coque ruivo esculpido', .45),
    ('177-1', 'penteados', 'Rabo com ondas e flores', .45),
    ('179-1', 'penteados', 'Semi preso com ondas longas', .45),
    ('181-1', 'penteados', 'Coque de cachos', .45),
    ('198-1', 'penteados', 'Coque alto em técnica russa', .45),
    ('201-1', 'penteados', 'Semi preso com cachos', .45),
    ('027-1', 'penteados', 'Treino de coque', .45),
    ('029-1', 'penteados', 'Ponytail com acabamento', .45),
    # Maquiagem
    ('001-1', 'make', 'Make com delineado gráfico', .3),
    ('004-1', 'make', 'Olhar intenso e pele luminosa', .35),
    ('012-1', 'make', 'Make marcante em tons quentes', .3),
    ('006-1', 'make', 'Make leve em tons dourados', .4),
    ('007-1', 'make', 'Make marrom e dourado', .4),
    ('031-1', 'make', 'Esfumado marrom com delineado', .35),
    ('032-1', 'make', 'Delineado agulha', .4),
    ('045-1', 'make', 'Make clássica em editorial', .35),
    ('063-1', 'make', 'Noiva de civil, make leve', .35),
    ('064-1', 'make', 'Make asiática para civil', .35),
    ('067-1', 'make', 'Boca vinho e pele acetinada', .4),
    ('068-1', 'make', 'Make glamour em tons terrosos', .4),
    ('069-1', 'make', 'Pele iluminada e lábios sofisticados', .4),
    ('105-1', 'make', 'Make para debutante', .35),
    ('106-1', 'make', 'Make suave com olhar marcado', .35),
    ('130-1', 'make', 'Make para ruiva', .35),
    ('149-1', 'make', 'Make de noiva com véu', .4),
    ('171-1', 'make', 'Make social para pele madura', .35),
    ('186-1', 'make', 'Make natural ao ar livre', .35),
    # Editoriais
    ('052-1', 'editoriais', 'Editorial Ouro, técnica russa', .3),
    ('056-1', 'editoriais', 'Editorial Ouro', .3),
    ('054-1', 'editoriais', 'Editorial Ouro, brilho e volume', .3),
    ('043-1', 'editoriais', 'Editorial Paola Mancini', .3),
    ('044-1', 'editoriais', 'Editorial de noiva com tatuagem', .3),
    ('041-1', 'editoriais', 'Editorial na chácara', .3),
    ('079-1', 'editoriais', 'Editorial ruiva com tulipas', .3),
    ('082-1', 'editoriais', 'Editorial em ondas loiras', .3),
    ('188-1', 'editoriais', 'Editorial ISA', .3),
    ('193-1', 'editoriais', 'Editorial no campo', .35),
    ('024-3', 'editoriais', 'Ensaio com @maurofotopro', .35),
    ('024-1', 'editoriais', 'Ensaio, coque duplo', .3),
    ('152-1', 'editoriais', 'Editorial noiva ruiva', .3),
]

HERO = ['016-1', '047-10', '185-1', '083-1']
EXTRA = {  # usadas em seções específicas
    'paola': ('022-1', .3), 'paola2': ('024-8', .4),
    'thai6': ('016-6', .35), 'thai5': ('016-5', .5),
}


def cortar(src, w, h, foco):
    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert('RGB')
    r = max(w / im.width, h / im.height)
    nw, nh = round(im.width * r), round(im.height * r)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = int((nh - h) * foco)
    return im.crop((x, y, x + w, y + h))


def nome(code):
    return code.replace('-', '_')


dados = []
for i, (code, cat, alt, foco) in enumerate(FOTOS, 1):
    src = os.path.join(IG, code + '.jpg')
    big = cortar(src, 960, 1200, foco)
    big.save(os.path.join(OUT, nome(code) + '.webp'), quality=80, method=6)
    big.resize((480, 600), Image.LANCZOS).save(os.path.join(OUT, nome(code) + '-p.webp'), quality=76, method=6)
    dados.append({'f': nome(code), 'c': cat, 'a': alt})

for code in HERO:
    cortar(os.path.join(IG, code + '.jpg'), 1040, 1300, .3).save(os.path.join(IMG, 'hero-' + nome(code) + '.webp'), quality=82, method=6)

for k, (code, foco) in EXTRA.items():
    cortar(os.path.join(IG, code + '.jpg'), 960, 1200, foco).save(os.path.join(IMG, k + '.webp'), quality=82, method=6)

# fundo de seda (gerado por IA, _ref/fundo-seda.png)
seda = Image.open(os.path.join(REF, 'fundo-seda.png')).convert('RGB')
seda.resize((1920, 1080), Image.LANCZOS).save(os.path.join(IMG, 'seda.webp'), quality=78, method=6)
cortar(os.path.join(REF, 'fundo-seda.png'), 900, 1600, .5).save(os.path.join(IMG, 'seda-m.webp'), quality=76, method=6)

# grade do portfólio injetada no HTML entre marcadores
CATS = {'noivas': 'Noivas', 'penteados': 'Penteados', 'make': 'Maquiagem', 'editoriais': 'Editoriais'}
itens = []
for n, d in enumerate(dados, 1):
    itens.append(
        f'      <figure class="foto" data-cat="{d["c"]}"><button type="button" data-full="assets/p/{d["f"]}.webp" aria-label="Ampliar: {d["a"]}">'
        f'<img src="assets/p/{d["f"]}-p.webp" alt="{d["a"]}" width="480" height="600" loading="lazy" decoding="async"></button>'
        f'<figcaption><span>{n:02d}</span>{CATS[d["c"]]}</figcaption></figure>')
html_path = os.path.join(SITE, 'portfolio.html')
if os.path.exists(html_path):
    html = open(html_path, encoding='utf-8').read()
    html = re.sub(r'(<!-- grade:inicio -->).*?(\s*<!-- grade:fim -->)', lambda m: m.group(1) + '\n' + '\n'.join(itens) + m.group(2), html, flags=re.S)
    open(html_path, 'w', encoding='utf-8').write(html)

print(len(dados), 'fotos;', {c: sum(1 for d in dados if d['c'] == c) for c in CATS})
