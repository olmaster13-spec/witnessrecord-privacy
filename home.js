/* Home page motion. Everything here is enhancement: with this file missing the
   page still reads top to bottom and the stage rests on a finished frame. */
(function () {
  var d = document;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var narrow = window.matchMedia('(max-width: 900px)');

  /* Reveal on scroll ----------------------------------------------------- */
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* Hero: the whole story in about thirteen seconds, on a loop ------------ */
  var hero = d.querySelector('.h-hero .stage');
  if (hero && !reduce && 'IntersectionObserver' in window) {
    var seq = [[3, 2600], [4, 1700], [5, 6200], [7, 3800]];
    var i = 0, timer = null;
    var run = function () {
      hero.setAttribute('data-step', seq[i][0]);
      timer = setTimeout(function () { i = (i + 1) % seq.length; run(); }, seq[i][1]);
    };
    new IntersectionObserver(function (entries) {
      clearTimeout(timer);
      if (entries[0].isIntersecting) { i = 0; run(); }
    }, { threshold: 0.2 }).observe(hero);
  }

  /* Walkthrough: the step nearest the reading line drives the phone ------- */
  var tour = d.querySelector('.tour');
  if (tour) {
    var stage = tour.querySelector('.stage');
    var steps = [].slice.call(tour.querySelectorAll('.tour-step'));
    var current = null, ticking = false;
    var update = function () {
      ticking = false;
      var line = window.innerHeight * (narrow.matches ? 0.8 : 0.5);
      var best = null, bestDist = Infinity;
      steps.forEach(function (s) {
        var r = s.getBoundingClientRect();
        var mid = narrow.matches ? r.top + Math.min(r.height, 150) / 2 : r.top + r.height / 2;
        var dist = Math.abs(mid - line);
        if (dist < bestDist) { bestDist = dist; best = s; }
      });
      if (best && best !== current) {
        if (current) current.classList.remove('is-on');
        best.classList.add('is-on');
        current = best;
        stage.setAttribute('data-step', best.getAttribute('data-step'));
      }
    };
    var onScroll = function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  /* Statement: words light as the paragraph crosses the screen ------------ */
  var mt = d.querySelector('.manifesto-text');
  if (mt && !reduce) {
    var words = mt.textContent.trim().split(/\s+/);
    mt.textContent = '';
    var spans = words.map(function (w, n) {
      var s = d.createElement('span');
      s.className = 'mw';
      s.textContent = w;
      mt.appendChild(s);
      if (n < words.length - 1) mt.appendChild(d.createTextNode(' '));
      return s;
    });
    var lit = -1, mtTick = false;
    var light = function () {
      mtTick = false;
      var r = mt.getBoundingClientRect(), vh = window.innerHeight;
      var p = (vh * 0.82 - r.top) / (r.height + vh * 0.38);
      var n = Math.round(Math.max(0, Math.min(1, p)) * spans.length);
      if (n === lit) return;
      spans.forEach(function (s, k) { s.classList.toggle('on', k < n); });
      lit = n;
    };
    window.addEventListener('scroll', function () {
      if (!mtTick) { mtTick = true; requestAnimationFrame(light); }
    }, { passive: true });
    light();
  }
})();
