// Tests du moteur du calculateur TVA BTP (parts/tva.js).
//   node --test _build/test_tva.mjs
// Chaque cas renvoie à la règle officielle qu'il vérifie.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const src = readFileSync(new URL('./parts/tva.js', import.meta.url), 'utf8');
const ctx = { document: { getElementById: () => null } };
vm.createContext(ctx);
vm.runInContext(src, ctx);
const decide = (r) => ctx.tvaDecide({
  local: 'logement', mixte50: 'oui', age: 'plus2', trav: 'amelioration', pacOk: false,
  surface: false, remiseNeuf: false, secondOeuvre: false, electro: false,
  clientAchete: false, soustraitance: false, ...r,
});

const cas = [
  // [description, réponses, taux attendu, mention attendue]
  ['rénovation courante dans un logement de plus de 2 ans → 10 % (279-0 bis)', {}, 10, '279'],
  ['rénovation énergétique → 5,5 % (278-0 bis A)', { trav: 'energie' }, 5.5, '278'],
  ['logement de moins de 2 ans → 20 %', { age: 'moins2' }, 20, null],
  ['rénovation énergétique, logement de moins de 2 ans → 20 %', { trav: 'energie', age: 'moins2' }, 20, null],
  ['local professionnel → 20 %', { local: 'pro', trav: 'energie' }, 20, null],
  ['local pro qui devient un logement → taux réduit', { local: 'pro-vers-logement' }, 10, '279'],
  ['construction ou surélévation → 20 %', { trav: 'neuf' }, 20, null],
  ['espaces verts → 20 % (279-0 bis 2 bis)', { trav: 'jardin' }, 20, null],
  ['surface de plancher +10 % → 20 %', { surface: true }, 20, null],
  ['remise à neuf de la structure → 20 %', { remiseNeuf: true }, 20, null],
  ['2/3 de chaque élément de second œuvre → 20 %', { secondOeuvre: true, trav: 'energie' }, 20, null],
  ['chaudière gaz ou fioul → 20 % depuis le 01/03/2025', { trav: 'chaudiere-fossile' }, 20, null],
  ['PAC air/air sans les critères 2026 → 20 %', { trav: 'pac-air-air' }, 20, null],
  ['PAC air/air conforme aux critères 2026 → 5,5 %', { trav: 'pac-air-air', pacOk: true }, 5.5, '278'],
  ['matériel handicap → 5,5 %, même logement récent', { trav: 'handicap', age: 'moins2' }, 5.5, null],
  ['sous-traitance → autoliquidation, 0 % facturé', { soustraitance: true, trav: 'energie' }, 0, null],
  ['local mixte à 50 % ou plus d\'habitation → taux réduit sur tout', { local: 'mixte', mixte50: 'oui' }, 10, '279'],
];

for (const [nom, r, taux, mention] of cas) {
  test(nom, () => {
    const d = decide(r);
    assert.equal(d.taux, taux);
    assert.equal(d.mention, mention);
  });
}

test('local mixte sous 50 % → taux réduit ventilé avec 20 %', () => {
  const d = decide({ local: 'mixte', mixte50: 'non' });
  assert.equal(d.taux, 10);
  assert.equal(d.ventile, true);
});

test('électroménager et matériel du client → alertes, taux inchangé', () => {
  const d = decide({ electro: true, clientAchete: true });
  assert.equal(d.taux, 10);
  assert.equal(d.alertes.length, 2);
});

test('la sous-traitance prime sur tout le reste', () => {
  assert.equal(decide({ soustraitance: true, local: 'pro', trav: 'neuf' }).autoliq, true);
});
