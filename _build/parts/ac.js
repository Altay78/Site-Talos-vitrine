/* ═══ 2 · LES MISSIONS — trois onglets, un seul écran ═══════════════════ */
(function(){
  var list = document.querySelector('.ac-miss-list');
  var screen = document.getElementById('acScreen');
  if (!list || !screen) return;

  var tabs = [].slice.call(list.querySelectorAll('.ac-mission'));
  var shots = [].slice.call(screen.querySelectorAll('img'));

  function show(tab){
    for (var i = 0; i < tabs.length; i++){
      var on = tabs[i] === tab;
      tabs[i].setAttribute('aria-selected', on ? 'true' : 'false');
      tabs[i].tabIndex = on ? 0 : -1;
    }
    for (var j = 0; j < shots.length; j++){
      shots[j].classList.toggle('on', shots[j].getAttribute('data-m') === tab.getAttribute('data-m'));
    }
    screen.setAttribute('aria-labelledby', tab.id);
  }

  for (var k = 0; k < tabs.length; k++){
    tabs[k].tabIndex = tabs[k].getAttribute('aria-selected') === 'true' ? 0 : -1;
    tabs[k].addEventListener('click', function(){ show(this); });
    /* survol : on ne change l'écran que si l'appareil a un vrai pointeur,
       sinon le premier effleurement tactile déclencherait le changement */
    tabs[k].addEventListener('mouseenter', function(){
      if (window.matchMedia('(hover:hover) and (pointer:fine)').matches) show(this);
    });
  }

  /* flèches : déplacement clavier attendu dans un groupe d'onglets */
  list.addEventListener('keydown', function(e){
    var i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    var n = null;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
    if (e.key === 'ArrowUp'   || e.key === 'ArrowLeft')  n = tabs[(i - 1 + tabs.length) % tabs.length];
    if (e.key === 'Home') n = tabs[0];
    if (e.key === 'End')  n = tabs[tabs.length - 1];
    if (!n) return;
    e.preventDefault();
    show(n);
    n.focus();
  });
})();


/* ═══ 3 · LE SCÉNARIO — quel onglet est au-dessus de la pile ════════════ */
(function(){
  var steps = [].slice.call(document.querySelectorAll('#acSteps .ac-step'));
  if (!steps.length) return;

  var wide = window.matchMedia('(min-width:961px)');
  var ticking = false;

  function stickTop(){
    var v = parseFloat(getComputedStyle(steps[0]).top);
    return isNaN(v) ? 0 : v;
  }

  function paint(){
    ticking = false;
    var act = -1;
    if (wide.matches){
      var line = stickTop() + 1;
      for (var i = 0; i < steps.length; i++){
        if (steps[i].getBoundingClientRect().top <= line) act = i;
      }
      if (act < 0) act = 0;
    }
    for (var j = 0; j < steps.length; j++) steps[j].classList.toggle('is-on', j === act);
  }

  function onScroll(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(paint);
  }

  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  paint();
})();
