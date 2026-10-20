// Paola Mancini · Hair & Makeup — Site por L R G Z
(function () {
  var d = document, WA = '5512992246928';
  d.documentElement.classList.remove('sem-js');

  // nav: sombra ao rolar + barra fixa no mobile
  var nav = d.querySelector('.nav'), barra = d.querySelector('.barra');
  function rolar() {
    var y = window.scrollY;
    if (nav) nav.classList.toggle('sombra', y > 8);
    if (barra) barra.classList.toggle('on', y > window.innerHeight * .6);
  }
  window.addEventListener('scroll', rolar, { passive: true });
  rolar();

  // menu mobile
  var mb = d.querySelector('.menu-btn'), gav = d.getElementById('gaveta');
  function fecha() { if (!gav) return; gav.hidden = true; mb.setAttribute('aria-expanded', 'false'); d.body.style.overflow = ''; }
  if (mb && gav) {
    mb.addEventListener('click', function () {
      var abrir = gav.hidden;
      gav.hidden = !abrir;
      mb.setAttribute('aria-expanded', String(abrir));
      d.body.style.overflow = abrir ? 'hidden' : '';
    });
    gav.addEventListener('click', function (e) { if (e.target.closest('a')) fecha(); });
    window.addEventListener('resize', function () { if (window.innerWidth > 900) fecha(); });
  }

  // hero: fotos trocam sozinhas
  var slides = d.querySelectorAll('.quadro .slides img'), marcas = d.querySelectorAll('.quadro .marcas i'), leg = d.querySelector('.quadro .leg');
  if (slides.length > 1 && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var at = 0;
    setInterval(function () {
      if (d.hidden) return;
      slides[at].classList.remove('on'); if (marcas[at]) marcas[at].classList.remove('on');
      at = (at + 1) % slides.length;
      var img = slides[at];
      if (img.loading === 'lazy') img.loading = 'eager';
      img.classList.add('on'); if (marcas[at]) marcas[at].classList.add('on');
      if (leg) leg.textContent = img.dataset.leg || '';
    }, 5200);
  }

  // revelar ao rolar
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('vis'); });

  // filtros do portfólio
  var fbs = d.querySelectorAll('.filtros button'), fotos = d.querySelectorAll('.grade-fotos .foto');
  fbs.forEach(function (b) {
    b.addEventListener('click', function () {
      var c = b.dataset.f;
      fbs.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      var n = 0;
      fotos.forEach(function (f) {
        var ok = c === 'todos' || f.dataset.cat === c;
        f.hidden = !ok;
        if (ok) { n++; var s = f.querySelector('figcaption span'); if (s) s.textContent = (n < 10 ? '0' : '') + n; }
      });
    });
  });

  // lightbox
  var lb = d.getElementById('lb');
  if (lb) {
    var li = lb.querySelector('img'), lp = lb.querySelector('p'), lista = [], pos = 0, ultimo = null;
    function mostra(i) {
      pos = (i + lista.length) % lista.length;
      var b = lista[pos];
      li.src = b.dataset.full; li.alt = b.querySelector('img').alt; lp.textContent = li.alt;
    }
    function abre(b) {
      lista = Array.prototype.filter.call(d.querySelectorAll('.foto button[data-full]'), function (x) { return !x.closest('.foto').hidden; });
      ultimo = b; lb.hidden = false; d.body.style.overflow = 'hidden';
      mostra(lista.indexOf(b)); lb.querySelector('.x').focus();
    }
    function fechaLb() { lb.hidden = true; d.body.style.overflow = ''; li.removeAttribute('src'); if (ultimo) ultimo.focus(); }
    d.addEventListener('click', function (e) { var b = e.target.closest('.foto button[data-full]'); if (b) abre(b); });
    lb.querySelector('.x').addEventListener('click', fechaLb);
    lb.querySelector('.ant').addEventListener('click', function () { mostra(pos - 1); });
    lb.querySelector('.prox').addEventListener('click', function () { mostra(pos + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) fechaLb(); });
    d.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') fechaLb();
      if (e.key === 'ArrowLeft') mostra(pos - 1);
      if (e.key === 'ArrowRight') mostra(pos + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) mostra(pos + (dx < 0 ? 1 : -1));
    });
  }

  // agendamento: monta a mensagem do WhatsApp
  var form = d.getElementById('form-agenda');
  if (form) {
    var p = new URLSearchParams(location.search).get('servico');
    if (p) { var r = form.querySelector('input[name=servico][value="' + p + '"]'); if (r) r.checked = true; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form), linhas = ['Olá, Paola! Vim pelo site e gostaria de um orçamento.', ''];
      function add(rotulo, v) { v = (v || '').toString().trim(); if (v) linhas.push(rotulo + ': ' + v); }
      add('Nome', f.get('nome'));
      add('Atendimento', f.get('servico'));
      var dt = f.get('data');
      if (dt) { var a = dt.split('-'); dt = a[2] + '/' + a[1] + '/' + a[0]; }
      add('Data do evento', dt);
      add('Horário da cerimônia', f.get('hora'));
      add('Local do evento', f.get('local'));
      add('Quantas pessoas', f.get('pessoas'));
      add('Observações', f.get('obs'));
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(linhas.join('\n')), '_blank', 'noopener');
    });
  }

  var ano = d.getElementById('ano'); if (ano) ano.textContent = new Date().getFullYear();
})();
