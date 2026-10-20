# Ateliê Paola Mancini · Hair & Makeup

Site de apresentação da Paola Mancini ([@paola_mancini_hairmakeup](https://www.instagram.com/paola_mancini_hairmakeup/)), maquiadora e penteadista especialista em noivas em São José dos Campos, SP.

Publicado em https://azeugral.github.io/paola-mancini/ (com `noindex` até a aprovação).

## Páginas

- `index.html`: hero, frase da bio, atendimentos, como funciona o Dia da Noiva, portfólio resumido, depoimentos, sobre, cursos e ateliê com mapa.
- `portfolio.html`: 79 fotos em grade 4:5 com filtros (Noivas, Penteados, Maquiagem, Editoriais) e foto ampliada.
- `cursos.html`: cursos de penteado (formação de penteadistas).
- `agendar.html`: formulário que monta a mensagem para o WhatsApp (12) 99224-6928.
- `404.html`

## Identidade

Tirada das artes do próprio Instagram (post "Noiva, excelência não é luxo. É tranquilidade."):
vinho `#5a1026`, champanhe/marfim, rosé e ouro `#b08548`. Playfair Display nos títulos, IBM Plex Sans no texto e Great Vibes no letreiro "Paola Mancini", que lembra o painel dourado do ateliê.
O fundo de seda com fios dourados foi gerado por IA (`_ref/fundo-seda.png`).

## Ferramentas

```
python -I tools/paginas.py     # monta portfolio/cursos/agendar/404 a partir de _partes/ e do cabeçalho/rodapé do index
python -I tools/processar.py   # recorta as fotos de ../_ref/ig e injeta a grade do portfólio
python -I tools/og.py          # prévia de link (og.jpg) e favicons
```

## CONFIRMAR antes do domínio

- [ ] **Logo oficial** em vetor/PNG (o letreiro do ateliê). Hoje o nome está composto em fonte script dourada.
- [ ] **WhatsApp**: usado (12) 99224-6928, que aparece em várias legendas (uma legenda traz 99224-6829, provável erro de digitação). O link w.app da bio está pausado.
- [ ] **Horário de atendimento** do ateliê (no site: "com horário marcado").
- [ ] **Agenda aberta**: legendas citam noivas 2026/2027 e 2027/2028; o selo diz "2027".
- [ ] **Teste de maquiagem/penteado** antes do casamento: oferece? Entra no pacote?
- [ ] **Atendimento fora do ateliê** (casa da noiva, hotel, local da festa) e taxa de deslocamento.
- [ ] **Valores** de noiva, madrinha, debutante e make social (não publicados).
- [ ] **Cursos**: formato (VIP/turma), carga horária, datas, valores, certificado.
- [ ] **Depoimentos**: tirados dos prints que ela postou (Júlia, Ketly, Ellen, Débora, Rochiely e uma noiva amiga de infância), com cortes para caber. Confirmar se pode usar os nomes.
- [ ] **Fotografia**: alguns posts sugerem que ela também fotografa (ensaios de Natal, Dia das Mães, casamentos, #tamagnonifotografia). Confirmar se é serviço dela e se entra no site.
- [ ] Créditos dos fotógrafos parceiros (Tamagnoni, Neto Paulo, Mauro Foto Pro, Estefani Lopes) se ela quiser.
- [ ] Domínio (sugestão: paolamancini.com.br) e remover o `noindex`.

Site por [L R G Z](https://lrgz.com.br).
