# Gera og.jpg (prévia de link) e os favicons. Uso: python -I tools/og.py (a partir de site/)
import os, base64, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(os.path.dirname(SITE), '_ref')
F = os.path.join(REF, 'fontes')
VINHO, OURO, OURO2 = (90, 16, 38), (176, 133, 72), (214, 185, 138)


def fonte(nome, tam, peso=None):
    f = ImageFont.truetype(os.path.join(F, nome), tam)
    if peso:
        try:
            f.set_variation_by_axes([peso] if 'Plex' not in nome else [100, peso])
        except Exception:
            pass
    return f


def ouro(tam_img, desenha):
    """Desenha texto como máscara e preenche com gradiente dourado."""
    m = Image.new('L', tam_img, 0)
    desenha(ImageDraw.Draw(m))
    g = Image.new('RGB', tam_img)
    w = tam_img[0]
    paradas = [(0, (139, 100, 49)), (.35, (201, 160, 95)), (.5, (232, 208, 160)), (.66, (176, 133, 72)), (1, (125, 88, 40))]
    gd = ImageDraw.Draw(g)
    for x in range(w):
        t = x / max(1, w - 1)
        for (a, ca), (b, cb) in zip(paradas, paradas[1:]):
            if a <= t <= b:
                k = (t - a) / (b - a)
                gd.line([(x, 0), (x, tam_img[1])], fill=tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
                break
    return g, m


# ---------- og.jpg ----------
W, H = 1200, 630
og = Image.open(os.path.join(REF, 'fundo-seda.png')).convert('RGB').resize((1120, 630), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
base = Image.new('RGB', (W, H), (244, 233, 226))
base.paste(og, (40, 0))
for i, (nome, x) in enumerate([('hero-016_1.webp', 0), ('hero-185_1.webp', W - 285)]):
    im = Image.open(os.path.join(SITE, 'assets', 'img', nome)).convert('RGB')
    im = im.resize((504, 630), Image.LANCZOS).crop((110, 0, 395, 630))
    mask = Image.new('L', (285, H), 255)
    md = ImageDraw.Draw(mask)
    for k in range(91):
        a = int(255 * k / 90)
        xx = 285 - 90 + k if i == 0 else 90 - k
        md.line([(xx, 0), (xx, H)], fill=255 - a)
    base.paste(im, (x, 0), mask)
d = ImageDraw.Draw(base)
cx = W // 2
pf = fonte('Playfair.ttf', 22, 500)
d.text((cx, 196), 'A T E L I Ê', font=pf, fill=OURO, anchor='mm')
gv = fonte('GreatVibes-Regular.ttf', 100)
g, m = ouro((W, H), lambda dd: dd.text((cx, 290), 'Paola Mancini', font=gv, fill=255, anchor='mm'))
base.paste(g, (0, 0), m)
d.line([(cx - 60, 372), (cx + 60, 372)], fill=OURO, width=1)
pl = fonte('Plex.ttf', 21, 500)
d.text((cx, 410), 'HAIR & MAKEUP  ·  NOIVAS', font=pl, fill=VINHO, anchor='mm')
d.text((cx, 446), 'São José dos Campos', font=fonte('PlayfairItalic.ttf', 24, 400), fill=(110, 90, 94), anchor='mm')
base.save(os.path.join(SITE, 'og.jpg'), quality=84, optimize=True, progressive=True)

# ---------- favicons ----------
MARFIM, CHAMP = (252, 248, 244), (240, 226, 217)


def icone(t, moldura=True):
    """P em script vinho, centralizado pela tinta, sobre marfim com moldura dourada fina."""
    S = 1024  # desenha grande e reduz no fim
    im = Image.new('RGB', (S, S), MARFIM)
    fundo = ImageDraw.Draw(im)
    for r in range(S // 2 * 14 // 10, 0, -4):  # brilho radial: marfim no centro, champanhe nas bordas
        k = min(1, r / (S * .72))
        fundo.ellipse([S / 2 - r, S / 2 - r * .95, S / 2 + r, S / 2 + r * 1.05],
                      fill=tuple(int(MARFIM[i] + (CHAMP[i] - MARFIM[i]) * k) for i in range(3)))
    # letra: máscara grande, recorta pela tinta e centraliza
    gm = Image.new('L', (S * 2, S * 2), 0)
    ImageDraw.Draw(gm).text((S, S), 'P', font=fonte('GreatVibes-Regular.ttf', int(S * 1.25)), fill=255, anchor='mm')
    gm = gm.filter(ImageFilter.MaxFilter(9 if moldura else 25))  # engrossa o traço; mais nas versões de aba
    gm = gm.crop(gm.getbbox())
    alvo = S * (.66 if moldura else .84)
    esc = alvo / max(gm.size)
    gm = gm.resize((round(gm.width * esc), round(gm.height * esc)), Image.LANCZOS)
    cor = Image.new('RGB', gm.size)
    cd = ImageDraw.Draw(cor)
    for y in range(gm.height):  # vinho com leve gradiente vertical
        k = y / max(1, gm.height - 1)
        cd.line([(0, y), (gm.width, y)], fill=tuple(int(a + (b - a) * k) for a, b in zip((122, 31, 57), (62, 10, 26))))
    x, y = (S - gm.width) // 2, (S - gm.height) // 2
    im.paste(cor, (x, y), gm)
    if moldura:
        g, m = ouro((S, S), lambda dd: dd.rectangle([S * .07, S * .07, S * .93, S * .93], outline=255, width=max(6, S // 90)))
        im.paste(g, (0, 0), m)
    return im.resize((t, t), Image.LANCZOS)

icone(180).save(os.path.join(SITE, 'apple-touch-icon.png'))
icone(32, False).save(os.path.join(SITE, 'favicon-32.png'))
icone(48, False).save(os.path.join(SITE, 'favicon.ico'), sizes=[(48, 48), (32, 32), (16, 16)])
buf = io.BytesIO(); icone(128, False).save(buf, 'PNG')
open(os.path.join(SITE, 'favicon.svg'), 'w').write(
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 128 128">'
    '<image width="128" height="128" xlink:href="data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode() + '"/></svg>')
print('og', os.path.getsize(os.path.join(SITE, 'og.jpg')) // 1024, 'KB')
