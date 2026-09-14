# -*- coding: utf-8 -*-
"""Le carrousel « équipe » — un cover-flow maison.

Le composant d'origine (@subhanhq/amicro card-cover-flow) est du React +
Tailwind ; le site est en HTML statique. L'effet est refait ici en vanilla :
perspective, rotation, profondeur, défilement automatique.

Un seul bloc, utilisé à deux endroits — l'accueil (injecté dans index.html,
qui n'est pas régénéré) et la page Offres (via assistants.hub()). Il embarque
sa feuille et son script : il ne dépend d'aucun style de page.
"""

EQUIPE = [
    ('client', u'Assistant Client',
     u'Il transforme vos demandes en opportunités.',
     u'Répond aux demandes entrantes, qualifie vos prospects et prend vos '
     u'rendez-vous, 24h/24.',
     u'Demandes entrantes · Qualification · RDV',
     'assistant-client.html'),
    ('commercial', u'Assistant Commercial',
     u'Il prépare et suit vos devis.',
     u'Crée vos devis à partir d’un email, d’une photo ou d’une note vocale, '
     u'puis relance vos clients jusqu’à leur réponse.',
     u'Création · Signature · Relances',
     'assistant-commercial.html'),
    ('facturation', u'Assistant Facturation',
     u'Il gère vos factures dès qu’un devis est signé.',
     u'Crée vos factures avec les bonnes mentions, gère les acomptes et situations, '
     u'puis garde vos documents organisés.',
     u'Facturation · Acomptes · Archivage',
     'assistant-facturation.html'),
    ('tresorerie', u'Assistant Trésorerie',
     u'Il vous aide à récupérer votre argent.',
     u'Relance vos impayés, prépare les échéances et vous donne une vision de votre '
     u'trésorerie à venir.',
     u'Impayés · Encaissements · Prévisions',
     'assistant-tresorerie.html'),
    ('administratif', u'Assistant Administratif',
     u'Il met de l’ordre dans votre boîte mail.',
     u'Trie vos emails, extrait les informations importantes et vous alerte uniquement '
     u'sur ce qui mérite votre attention.',
     u'Emails · Documents · Alertes',
     'assistant-administratif.html'),
]

# Pas encore livrés : ils tournent dans le carrousel comme les autres, mais
# marqués « Bientôt » et sans lien — leur fiche n'existe pas. Le jour où elle
# existe, il suffit de déplacer la ligne dans EQUIPE avec son href.
A_VENIR = [
    ('chantier', u'Assistant Chef de chantier',
     u'Vos plannings tiennent. Vos comptes rendus s’écrivent seuls.',
     u'Tient le planning de vos équipes, suit l’avancement de chaque chantier et '
     u'rédige les comptes rendus de journée.',
     u'Plannings · Avancement · Comptes rendus',
     None),
    ('stock', u'Assistant Gestion de stock',
     u'Vous savez ce qu’il reste et ce qu’il faut commander.',
     u'Suit vos stocks de matériel et de matériaux, vous alerte avant la rupture et '
     u'prépare vos commandes fournisseurs.',
     u'Stocks · Alertes · Commandes',
     None),
]

FLECHE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

TOUS = EQUIPE + A_VENIR

CARTE = u'''      <li class="crew-c" data-i="%(i)d">
        <%(ouvre)s>
          <span class="crew-vis">
            <img src="perso/assistant-%(slug)s.webp" alt="" width="430" height="1400"
                 loading="lazy" decoding="async">%(pastille)s
          </span>
          <span class="crew-txt">
            <b>%(nom)s</b>
            <span class="crew-h">%(accroche)s</span>
            <span class="crew-p">%(resume)s</span>
            <span class="crew-tags">%(tags)s</span>
            <span class="crew-go%(go_cl)s">%(go)s</span>
          </span>
        </%(ferme)s>
      </li>'''

cartes = []
for i, (slug, nom, accroche, resume, tags, href) in enumerate(TOUS):
    soon = href is None
    cartes.append(CARTE % dict(
        i=i, slug=slug, nom=nom, accroche=accroche, resume=resume, tags=tags,
        ouvre=(u'span class="crew-x"' if soon else u'a href="%s"' % href),
        ferme=(u'span' if soon else u'a'),
        pastille=(u'\n            <i class="crew-soon">Bientôt</i>' if soon else u''),
        go_cl=(u' pending' if soon else u''),
        go=(u'En préparation' if soon else u'Découvrir %s' % FLECHE)))

dots = u''.join(u'<button type="button" role="tab" aria-label="%s"%s></button>'
                % (e[1], u' aria-selected="true"' if i == 0 else u' aria-selected="false"')
                for i, e in enumerate(TOUS))

CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 6l-6 6 6 6"/></svg>')

BLOC = u'''
<!-- ═══ ÉQUIPE — carrousel cover-flow ══════════════════════════════════════ -->
<style id="crew-css">
.t-crew{--bronze:#E0631F;--bronze-2:#F4823E;--bronze-rgb:224,99,31;
  --parch:#F6EEE7;--lin:#AB9F95;--ink:#140F0C;--ink-2:#1C1611;--ink-3:#241B15;
  --line:rgba(246,238,231,.08);--line-2:rgba(246,238,231,.15);
  --e:cubic-bezier(.16,1,.3,1);
  position:relative;overflow:hidden;padding:96px 0 104px;
  background:var(--ink);color:var(--parch);
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
html[data-theme="light"] .t-crew{--bronze:#C5531C;--bronze-2:#E0631F;--bronze-rgb:197,83,28;
  --parch:#1C1310;--lin:#6E6058;--ink:#FBF6F2;--ink-2:#FFFFFF;--ink-3:#F4EBE3;
  --line:rgba(40,25,16,.12);--line-2:rgba(40,25,16,.22)}
.t-crew::before{content:"";position:absolute;inset:auto 0 -30% 0;height:70%;pointer-events:none;
  background:radial-gradient(60% 60% at 50% 40%,rgba(var(--bronze-rgb),.16) 0%,transparent 70%)}

.crew-head{position:relative;max-width:1180px;margin:0 auto 44px;padding:0 24px;text-align:center}
.crew-k{margin:0 0 14px;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--bronze)}
.crew-head h2{margin:0 0 14px;font-size:clamp(30px,3.4vw,46px);line-height:1.06;
  letter-spacing:-1.6px;font-weight:800;color:var(--parch)}
.crew-head h2 em{font-style:normal;color:var(--bronze)}
.crew-head p{margin:0 auto;max-width:52ch;font-size:16.5px;line-height:1.6;color:var(--lin)}

/* la scène : les cartes tournent autour de celle du centre */
.crew-stage{position:relative;height:clamp(540px,52vw,620px);
  perspective:1500px;perspective-origin:50% 45%}
.crew-track{list-style:none;margin:0;padding:0;position:absolute;inset:0;
  transform-style:preserve-3d}
.crew-c{position:absolute;top:0;left:50%;width:clamp(252px,26vw,312px);height:100%;
  margin-left:calc(clamp(252px,26vw,312px) / -2);
  transition:transform .62s var(--e),opacity .62s var(--e),filter .62s var(--e);
  will-change:transform}
.crew-c a,.crew-c .crew-x{display:flex;flex-direction:column;height:100%;overflow:hidden;
  border-radius:26px;text-decoration:none;color:inherit;
  background:var(--ink-2);border:1px solid var(--line);
  box-shadow:0 30px 70px -30px rgba(0,0,0,.8)}
html[data-theme="light"] .crew-c a,
html[data-theme="light"] .crew-c .crew-x{box-shadow:0 30px 70px -34px rgba(40,25,16,.34)}
.crew-c[data-act] a,.crew-c[data-act] .crew-x{border-color:rgba(var(--bronze-rgb),.42);
  box-shadow:0 34px 80px -26px rgba(var(--bronze-rgb),.42)}

.crew-vis{position:relative;display:block;height:50%;overflow:hidden;
  background:radial-gradient(120% 84% at 50% 4%,rgba(var(--bronze-rgb),.20) 0%,transparent 70%)}
.crew-vis img{position:absolute;left:50%;top:10px;transform:translateX(-50%);
  height:640px;width:auto;max-width:none}
/* le fondu du bas est un voile, pas un mask-image : dans un contexte 3D
   (la scène est en preserve-3d) le masque n'est pas peint. */
.crew-vis::after{content:"";position:absolute;left:0;right:0;bottom:0;height:38%;
  pointer-events:none;
  background:linear-gradient(180deg,color-mix(in srgb,var(--ink-2),transparent 100%),var(--ink-2))}
.crew-soon{position:absolute;top:12px;right:12px;z-index:2;font-style:normal;
  font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  padding:4px 9px;border-radius:100px;
  color:color-mix(in oklab,var(--bronze) 74%,var(--parch));
  background:color-mix(in srgb,var(--ink) 88%,transparent);
  border:1px solid rgba(var(--bronze-rgb),.42)}
.crew-txt{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}
.crew-txt b{margin:0 0 6px;font-size:18.5px;line-height:1.15;letter-spacing:-.6px;
  font-weight:800;color:var(--parch)}
/* l'accroche : la phrase qu'on retient, au-dessus de l'explication */
.crew-h{margin:0;font-size:14.5px;line-height:1.3;font-weight:700;
  letter-spacing:-.2px;color:var(--parch)}
/* l'explication : ce que l'assistant fait vraiment */
.crew-p{flex:1;margin:8px 0 0;font-size:12.8px;line-height:1.5;color:var(--lin)}
/* les trois mots-clés, sur leur propre ligne au-dessus du lien */
.crew-tags{margin-top:12px;padding-top:10px;border-top:1px solid var(--line);
  font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:10.5px;
  letter-spacing:.04em;line-height:1.5;color:var(--lin)}
.crew-go{display:inline-flex;align-items:center;gap:7px;margin-top:12px;
  font-size:13.5px;font-weight:700;color:var(--bronze)}
.crew-go svg{width:14px;height:14px}
.crew-go.pending{color:var(--lin);font-weight:600}
.crew-c .crew-x{cursor:default}

/* flèches et pastilles */
.crew-nav{position:absolute;top:50%;z-index:20;display:grid;place-items:center;
  width:48px;height:48px;margin-top:-24px;padding:0;border-radius:50%;cursor:pointer;
  color:var(--parch);background:color-mix(in srgb,var(--ink-3) 88%,transparent);
  border:1px solid var(--line-2);backdrop-filter:blur(10px);
  transition:transform .25s var(--e),border-color .25s var(--e)}
.crew-nav:hover{transform:scale(1.07);border-color:rgba(var(--bronze-rgb),.55)}
.crew-nav:focus-visible{outline:3px solid var(--bronze);outline-offset:3px}
.crew-nav svg{width:20px;height:20px}
.crew-nav.p{left:max(16px,calc(50% - 640px))}
.crew-nav.n{right:max(16px,calc(50% - 640px))}
.crew-nav.n svg{transform:rotate(180deg)}
.crew-foot{margin:30px auto 0;max-width:46ch;padding:0 24px;text-align:center;
  font-size:15.5px;line-height:1.6;font-weight:700;color:var(--parch)}
.crew-foot span{display:block;font-weight:400;color:var(--lin)}
.crew-dots{display:flex;justify-content:center;gap:9px;margin-top:34px}
.crew-dots button{width:8px;height:8px;padding:0;border:0;border-radius:50%;cursor:pointer;
  background:var(--line-2);transition:width .3s var(--e),background .3s var(--e)}
.crew-dots button[aria-selected="true"]{width:26px;border-radius:100px;background:var(--bronze)}
.crew-dots button:focus-visible{outline:3px solid var(--bronze);outline-offset:3px}

/* sans son titre (page Offres, où l'en-tête est déjà là) il colle au-dessus */
.t-crew.nu{padding-top:4px}
@media (max-width:760px){
  .t-crew{padding:72px 0 84px}
  .crew-stage{height:clamp(520px,140vw,580px)}
  .crew-nav{width:42px;height:42px;margin-top:-21px}
}
@media (prefers-reduced-motion:reduce){
  .crew-c,.crew-nav,.crew-dots button{transition:none}
}
</style>

<section class="t-crew" aria-labelledby="crew-t">
  <div class="crew-head">
    <p class="crew-k">L'équipe Talos</p>
    <h2 id="crew-t">Vos Agents IA, <em>à la carte</em>.</h2>
    <p>Chaque assistant Talos a un rôle précis : attirer et qualifier vos demandes,
      préparer vos devis, gérer vos factures, suivre votre trésorerie ou organiser vos
      emails… Choisissez ceux dont vous avez besoin.</p>
  </div>

  <div class="crew-stage" id="crew">
    <button class="crew-nav p" type="button" aria-label="Assistant précédent">@@CHEV@@</button>
    <ul class="crew-track">
@@CARTES@@
    </ul>
    <button class="crew-nav n" type="button" aria-label="Assistant suivant">@@CHEV@@</button>
  </div>

  <div class="crew-dots" role="tablist" aria-label="Choisir un assistant">@@DOTS@@</div>

  <p class="crew-foot">Commencez avec les assistants dont vous avez besoin.<span>Ajoutez-en d’autres au fur et à mesure que votre entreprise grandit.</span></p>
</section>

<script>
/* Carrousel « cover-flow » : la carte du centre est droite, les autres
   pivotent et reculent. Tout se joue en transform (aucun reflow). */
(function(){
  var st=document.getElementById('crew'); if(!st) return;
  var cards=[].slice.call(st.querySelectorAll('.crew-c')),
      dots=[].slice.call(document.querySelectorAll('.crew-dots button')),
      n=cards.length, cur=0, timer=null,
      calme=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function place(){
    cards.forEach(function(c,i){
      var d=i-cur;                       /* distance signée la plus courte */
      if(d> n/2) d-=n; if(d< -n/2) d+=n;
      var a=Math.abs(d), vu=a<=2;
      c.style.transform='translateX('+(d*68)+'%) translateZ('+(-a*230)+'px) '
        +'rotateY('+(d*-26)+'deg) scale('+(1-a*0.04)+')';
      c.style.opacity = vu ? (a===0?1:(a===1?.66:.26)) : 0;
      c.style.zIndex  = String(50-a);
      c.style.filter  = a===0 ? 'none' : 'saturate(.72)';
      c.style.pointerEvents = vu ? 'auto' : 'none';
      if(a===0){ c.setAttribute('data-act',''); } else { c.removeAttribute('data-act'); }
    });
    dots.forEach(function(b,i){ b.setAttribute('aria-selected', i===cur?'true':'false'); });
  }
  function go(i){ cur=(i%n+n)%n; place(); }
  function suivant(){ go(cur+1); }

  function lance(){ if(calme||timer) return; timer=setInterval(suivant,4200); }
  function arrete(){ clearInterval(timer); timer=null; }

  st.querySelector('.crew-nav.p').addEventListener('click',function(){go(cur-1);arrete();lance();});
  st.querySelector('.crew-nav.n').addEventListener('click',function(){go(cur+1);arrete();lance();});
  dots.forEach(function(b,i){ b.addEventListener('click',function(){go(i);arrete();lance();}); });
  cards.forEach(function(c,i){ c.addEventListener('click',function(e){
    if(i!==cur){ e.preventDefault(); go(i); arrete(); lance(); }
  }); });
  st.addEventListener('mouseenter',arrete); st.addEventListener('mouseleave',lance);
  st.addEventListener('focusin',arrete);    st.addEventListener('focusout',lance);
  st.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){ go(cur-1); } else if(e.key==='ArrowRight'){ go(cur+1); }
  });
  /* on n'anime que si la section est à l'écran */
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      es[0].isIntersecting ? lance() : arrete();
    },{threshold:.25}).observe(st);
  } else { lance(); }
  place();
})();
</script>
'''
BLOC = (BLOC.replace('@@CARTES@@', u'\n'.join(cartes))
            .replace('@@DOTS@@', dots)
            .replace('@@CHEV@@', CHEV))



BLOC = u'''
<!-- ═══ ÉQUIPE — carrousel cover-flow ══════════════════════════════════════ -->
<style id="crew-css">
.t-crew{--bronze:#E0631F;--bronze-2:#F4823E;--bronze-rgb:224,99,31;
  --parch:#F6EEE7;--lin:#AB9F95;--ink:#140F0C;--ink-2:#1C1611;--ink-3:#241B15;
  --line:rgba(246,238,231,.08);--line-2:rgba(246,238,231,.15);
  --e:cubic-bezier(.16,1,.3,1);
  position:relative;overflow:hidden;padding:96px 0 104px;
  background:var(--ink);color:var(--parch);
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
html[data-theme="light"] .t-crew{--bronze:#C5531C;--bronze-2:#E0631F;--bronze-rgb:197,83,28;
  --parch:#1C1310;--lin:#6E6058;--ink:#FBF6F2;--ink-2:#FFFFFF;--ink-3:#F4EBE3;
  --line:rgba(40,25,16,.12);--line-2:rgba(40,25,16,.22)}
.t-crew::before{content:"";position:absolute;inset:auto 0 -30% 0;height:70%;pointer-events:none;
  background:radial-gradient(60% 60% at 50% 40%,rgba(var(--bronze-rgb),.16) 0%,transparent 70%)}

.crew-head{position:relative;max-width:1180px;margin:0 auto 44px;padding:0 24px;text-align:center}
.crew-k{margin:0 0 14px;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--bronze)}
.crew-head h2{margin:0 0 14px;font-size:clamp(30px,3.4vw,46px);line-height:1.06;
  letter-spacing:-1.6px;font-weight:800;color:var(--parch)}
.crew-head h2 em{font-style:normal;
  background:linear-gradient(100deg,#FFE7D4 0%,var(--bronze-2) 48%,var(--bronze) 100%);
  background-size:220% 100%;-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent;
  animation:crewGrad 6s ease-in-out infinite}
html[data-theme="light"] .crew-head h2 em{
  background:linear-gradient(100deg,#8E3208 0%,var(--bronze) 50%,#F0873F 100%);
  background-size:220% 100%;-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent}
@keyframes crewGrad{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.crew-head p{margin:0 auto;max-width:52ch;font-size:16.5px;line-height:1.6;color:var(--lin)}

/* la scène : les cartes tournent autour de celle du centre */
.crew-stage{position:relative;height:clamp(540px,52vw,620px);
  perspective:1500px;perspective-origin:50% 45%}
.crew-track{list-style:none;margin:0;padding:0;position:absolute;inset:0;
  transform-style:preserve-3d}
.crew-c{position:absolute;top:0;left:50%;width:clamp(252px,26vw,312px);height:100%;
  margin-left:calc(clamp(252px,26vw,312px) / -2);
  transition:transform .62s var(--e),opacity .62s var(--e),filter .62s var(--e);
  will-change:transform}
.crew-c a,.crew-c .crew-x{display:flex;flex-direction:column;height:100%;overflow:hidden;
  border-radius:26px;text-decoration:none;color:inherit;
  background:var(--ink-2);border:1px solid var(--line);
  box-shadow:0 30px 70px -30px rgba(0,0,0,.8)}
html[data-theme="light"] .crew-c a,
html[data-theme="light"] .crew-c .crew-x{box-shadow:0 30px 70px -34px rgba(40,25,16,.34)}
.crew-c[data-act] a,.crew-c[data-act] .crew-x{border-color:rgba(var(--bronze-rgb),.42);
  box-shadow:0 34px 80px -26px rgba(var(--bronze-rgb),.42)}

.crew-vis{position:relative;display:block;height:50%;overflow:hidden;
  background:radial-gradient(120% 84% at 50% 4%,rgba(var(--bronze-rgb),.20) 0%,transparent 70%)}
.crew-vis img{position:absolute;left:50%;top:10px;transform:translateX(-50%);
  height:640px;width:auto;max-width:none}
/* le fondu du bas est un voile, pas un mask-image : dans un contexte 3D
   (la scène est en preserve-3d) le masque n'est pas peint. */
.crew-vis::after{content:"";position:absolute;left:0;right:0;bottom:0;height:38%;
  pointer-events:none;
  background:linear-gradient(180deg,color-mix(in srgb,var(--ink-2),transparent 100%),var(--ink-2))}
.crew-soon{position:absolute;top:12px;right:12px;z-index:2;font-style:normal;
  font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  padding:4px 9px;border-radius:100px;
  color:color-mix(in oklab,var(--bronze) 74%,var(--parch));
  background:color-mix(in srgb,var(--ink) 88%,transparent);
  border:1px solid rgba(var(--bronze-rgb),.42)}
.crew-txt{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}
.crew-txt b{margin:0 0 6px;font-size:18.5px;line-height:1.15;letter-spacing:-.6px;
  font-weight:800;color:var(--parch)}
/* l'accroche : la phrase qu'on retient, au-dessus de l'explication */
.crew-h{margin:0;font-size:14.5px;line-height:1.3;font-weight:700;
  letter-spacing:-.2px;color:var(--parch)}
/* l'explication : ce que l'assistant fait vraiment */
.crew-p{flex:1;margin:8px 0 0;font-size:12.8px;line-height:1.5;color:var(--lin)}
/* les trois mots-clés, sur leur propre ligne au-dessus du lien */
.crew-tags{margin-top:12px;padding-top:10px;border-top:1px solid var(--line);
  font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:10.5px;
  letter-spacing:.04em;line-height:1.5;color:var(--lin)}
.crew-go{display:inline-flex;align-items:center;gap:7px;margin-top:12px;
  font-size:13.5px;font-weight:700;color:var(--bronze)}
.crew-go svg{width:14px;height:14px}
.crew-go.pending{color:var(--lin);font-weight:600}
.crew-c .crew-x{cursor:default}

/* flèches et pastilles */
.crew-nav{position:absolute;top:50%;z-index:20;display:grid;place-items:center;
  width:48px;height:48px;margin-top:-24px;padding:0;border-radius:50%;cursor:pointer;
  color:var(--parch);background:color-mix(in srgb,var(--ink-3) 88%,transparent);
  border:1px solid var(--line-2);backdrop-filter:blur(10px);
  transition:transform .25s var(--e),border-color .25s var(--e)}
.crew-nav:hover{transform:scale(1.07);border-color:rgba(var(--bronze-rgb),.55)}
.crew-nav:focus-visible{outline:3px solid var(--bronze);outline-offset:3px}
.crew-nav svg{width:20px;height:20px}
.crew-nav.p{left:max(16px,calc(50% - 640px))}
.crew-nav.n{right:max(16px,calc(50% - 640px))}
.crew-nav.n svg{transform:rotate(180deg)}
.crew-foot{margin:30px auto 0;max-width:46ch;padding:0 24px;text-align:center;
  font-size:15.5px;line-height:1.6;font-weight:700;color:var(--parch)}
.crew-foot span{display:block;font-weight:400;color:var(--lin)}
.crew-dots{display:flex;justify-content:center;gap:9px;margin-top:34px}
.crew-dots button{width:8px;height:8px;padding:0;border:0;border-radius:50%;cursor:pointer;
  background:var(--line-2);transition:width .3s var(--e),background .3s var(--e)}
.crew-dots button[aria-selected="true"]{width:26px;border-radius:100px;background:var(--bronze)}
.crew-dots button:focus-visible{outline:3px solid var(--bronze);outline-offset:3px}

/* sans son titre (page Offres, où l'en-tête est déjà là) il colle au-dessus */
.t-crew.nu{padding-top:4px}
@media (max-width:760px){
  .t-crew{padding:72px 0 84px}
  .crew-stage{height:clamp(520px,140vw,580px)}
  .crew-nav{width:42px;height:42px;margin-top:-21px}
}
@media (prefers-reduced-motion:reduce){
  .crew-c,.crew-nav,.crew-dots button{transition:none}
}
</style>

<section class="t-crew" aria-labelledby="crew-t">
  <div class="crew-head">
    <p class="crew-k">L'équipe Talos</p>
    <h2 id="crew-t">Vos Agents IA, <em>à la carte</em>.</h2>
    <p>Chaque assistant Talos a un rôle précis : attirer et qualifier vos demandes,
      préparer vos devis, gérer vos factures, suivre votre trésorerie ou organiser vos
      emails… Choisissez ceux dont vous avez besoin.</p>
  </div>

  <div class="crew-stage" id="crew">
    <button class="crew-nav p" type="button" aria-label="Assistant précédent">@@CHEV@@</button>
    <ul class="crew-track">
@@CARTES@@
    </ul>
    <button class="crew-nav n" type="button" aria-label="Assistant suivant">@@CHEV@@</button>
  </div>

  <div class="crew-dots" role="tablist" aria-label="Choisir un assistant">@@DOTS@@</div>

  <p class="crew-foot">Commencez avec les assistants dont vous avez besoin.<span>Ajoutez-en d’autres au fur et à mesure que votre entreprise grandit.</span></p>
</section>

<script>
/* Carrousel « cover-flow » : la carte du centre est droite, les autres
   pivotent et reculent. Tout se joue en transform (aucun reflow). */
(function(){
  var st=document.getElementById('crew'); if(!st) return;
  var cards=[].slice.call(st.querySelectorAll('.crew-c')),
      dots=[].slice.call(document.querySelectorAll('.crew-dots button')),
      n=cards.length, cur=0, timer=null,
      calme=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function place(){
    cards.forEach(function(c,i){
      var d=i-cur;                       /* distance signée la plus courte */
      if(d> n/2) d-=n; if(d< -n/2) d+=n;
      var a=Math.abs(d), vu=a<=2;
      c.style.transform='translateX('+(d*68)+'%) translateZ('+(-a*230)+'px) '
        +'rotateY('+(d*-26)+'deg) scale('+(1-a*0.04)+')';
      c.style.opacity = vu ? (a===0?1:(a===1?.66:.26)) : 0;
      c.style.zIndex  = String(50-a);
      c.style.filter  = a===0 ? 'none' : 'saturate(.72)';
      c.style.pointerEvents = vu ? 'auto' : 'none';
      if(a===0){ c.setAttribute('data-act',''); } else { c.removeAttribute('data-act'); }
    });
    dots.forEach(function(b,i){ b.setAttribute('aria-selected', i===cur?'true':'false'); });
  }
  function go(i){ cur=(i%n+n)%n; place(); }
  function suivant(){ go(cur+1); }

  function lance(){ if(calme||timer) return; timer=setInterval(suivant,4200); }
  function arrete(){ clearInterval(timer); timer=null; }

  st.querySelector('.crew-nav.p').addEventListener('click',function(){go(cur-1);arrete();lance();});
  st.querySelector('.crew-nav.n').addEventListener('click',function(){go(cur+1);arrete();lance();});
  dots.forEach(function(b,i){ b.addEventListener('click',function(){go(i);arrete();lance();}); });
  cards.forEach(function(c,i){ c.addEventListener('click',function(e){
    if(i!==cur){ e.preventDefault(); go(i); arrete(); lance(); }
  }); });
  st.addEventListener('mouseenter',arrete); st.addEventListener('mouseleave',lance);
  st.addEventListener('focusin',arrete);    st.addEventListener('focusout',lance);
  st.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){ go(cur-1); } else if(e.key==='ArrowRight'){ go(cur+1); }
  });
  /* on n'anime que si la section est à l'écran */
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      es[0].isIntersecting ? lance() : arrete();
    },{threshold:.25}).observe(st);
  } else { lance(); }
  place();
})();
</script>
'''
BLOC = (BLOC.replace('@@CARTES@@', u'\n'.join(cartes))
            .replace('@@DOTS@@', dots)
            .replace('@@CHEV@@', CHEV))


def bloc(avec_titre=True):
    """Le bloc complet, ou sa version nue pour la page Offres : sans l'en-tête
    ni la phrase de clôture, que la page porte déjà."""
    b = BLOC
    if not avec_titre:
        i = b.index('<div class="crew-head">')
        j = b.index('</div>', b.index('Choisissez ceux dont vous avez besoin')) + 6
        b = (b[:i] + b[j:]).replace('<section class="t-crew"', '<section class="t-crew nu"')
        i = b.index('<p class="crew-foot">')
        b = b[:i] + b[b.index('</p>', i) + 4:]
    return b
