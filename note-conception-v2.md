# Tomates 3D — conception v2 (grappes ovales, aimant en haut)

**Date :** 26 novembre 2026 — **pour validation visuelle AVANT réimpression**
**Déclencheur :** Léandre a imprimé la v1 et l'a testée : forme et principe
globalement corrects, mais 5 changements demandés (message retranscrit par
Joseph). Cette note répond point par point. **Aucun push GitHub ce round-ci.**
**Fichiers :** `tomates3d/v2/tomates_v2.py` (build123d 0.13), STL dans
`tomates3d/v2/stl/` (binaires) et `tomates3d/v2/stl-ascii/` (ASCII).
La v1 (`tomates.py`, `out/`) est intacte. Note publiée sur le site le
26 novembre 2026 (visionneuse v2 + STL ASCII).

## 1. Ce que Léandre a demandé → ce qui a changé

| # | Demande de Léandre | Réponse v2 |
|---|---|---|
| 1 | Forme ovale + vraies grappes, proche de la photo (tomates cerises allongées, sépales en étoile) | Tomate ovale 35 mm × Ø 25 mm (ratio ~1,5:1), 5 sépales en étoile intégrés au sommet ; grappe = rachis légèrement courbe + 7 pédicelles, 7 tomates pendantes |
| 2 | Plus SIMPLE — impossible de mettre les aimants dans la v1 | 1 seul logement par tomate, ouvert par le haut : on laisse tomber l'aimant dedans, le pin le retient. Aucune insertion en cours d'impression, pas de colle, pas de baïonnette |
| 3 | Aimants DIRECTEMENT contre la tige (v1 trop loin, pas de force ressentie) | Logement tout en haut du fruit, juste sous le point d'attache ; paroi latérale de 2,2 mm seulement entre l'aimant et l'extérieur au niveau du col |
| 4 | Tomates imprimables individuellement (mélanger vertes et rouges) | Chaque tomate s'imprime seule, puis se clipse sur le pin de la grappe ; la grappe (rachis + pédicelles + pins) s'imprime en une pièce, verte |
| 5 | Compatibilité avec l'arbre existant | Crochet en C en haut de la grappe, qui s'enclenche sur le bras de branche v1 (Ø 11 mm). Aucune modification de l'arbre. Le plot à aimants de la branche v1 n'est plus utilisé |

## 2. Dimensions (mm)

**Tomate** — coque ovale creuse, paroi 1,4 mm, longueur 35 mm (37,8 mm avec
les sépales), Ø max 25 mm, base plate Ø 8 mm. Sommet ouvert : manchon
(alésage Ø 7,2, de z = 28,4 à 35,5), 5 sépales (~51°, épaisseur 1 mm) intégrés,
imprimables sans support.

⚠️ **Écart d'enveloppe à valider :** la v1 faisait Ø 33 mm, taille que la
pince du robot attend. La v2 fait Ø 25 mm (plus proche de la vraie tomate
cerise allongée de la photo). Plus petit = pas de collision avec la pince,
mais **la prise par la pince avec la forme ovale n'a pas été testée** —
c'est le point nº 1 du test de premier article (§ 6).

**Logement d'aimant** — juste sous le manchon, tout en haut : Ø 6,4 mm
(aimant Ø 6,00 → jeu diamétral 0,4), profondeur 4,4 mm = **1 aimant** (2,0 mm)
ou **2 empilés** (4,0 mm + 0,4 de jeu). Ouvert par le haut : l'aimant Ø 6,00
passe par l'alésage Ø 7,2 du manchon.

**Pin (grappe)** — pointe conique Ø 6,8 (jeu 0,4 dans le manchon),
cran de retenue Ø 7,7 (saillie 0,45 mm, centré sur la rainure du manchon
une fois inséré), collerette Ø 10 mm (appui sur le sommet du col), tige
soudée au coude du pédicelle. Le cran s'engage avec une légère friction
(intersection mesurée 3,7 mm³ à mi-course, 0 une fois inséré : c'est
l'encliquetage attendu, pas une collision).

**Grappe** — rachis légèrement courbe (points (0,0,0), (2,5,0,55), (4,0,110),
(1,5,0,164)), hauteur totale 194 mm avec le crochet. 7 pédicelles
(z = 16/40/64/88/112/136/160, pas 24 mm, azimuts alternés 75/280/110/245/
95/285/80°), bras de 19 mm, coude sphère r 2,8, pin pendant 14 mm sous le
coude (le bras passe 2,5 mm au-dessus des sépales). Tomates tournées de
+36° sur leur pin pour éloigner les sépales des bras.

**Crochet** — sangle en C, rayon intérieur 5,9 mm (bras de branche Ø 11 mm),
section 5,2 × 5,2 mm, ouverture de 100° tournée vers +Y : enfichage latéral
sur le bras, le bras s'assied dans l'anneau (jeu 0 vérifié une fois assis,
ouverture libre vérifiée). Col Ø 5,2 (z 162–175) + bout de tige Ø 4,4
(z 180–194) : le crochet est pris en sandwich, il ne peut pas glisser.

## 3. Aimants — placement et stock

- **1 aimant par tomate** (2 maximum, empilés dans le même logement).
- Par grappe (7 tomates) : **7 aimants**. Par arbre complet (6 branches /
  6 grappes = 42 tomates) : **42 aimants**.
- Stock : 1 000 achetés, 532 utilisés → **468 restants**.
  Après 40 tomates × 1 aimant : **428 restants**.
  Après un arbre complet (42 tomates) : **426 restants**.
- La branche v1 n'a plus besoin de ses 2 aimants (plot inutilisé) : économie
  de 12 aimants par arbre par rapport à la v1.

## 4. Assemblage pas à pas

1. Imprimer les tomates (rouges et/ou vertes) et la grappe (verte).
2. Prendre **1 aimant** et le laisser **tomber dans le manchon** de la
   tomate, par le haut. Il s'arrête au fond du logement. (Option : en
   mettre un 2e par-dessus.)
3. Présenter la tomate sous le pin de la grappe, bien dans l'axe.
4. Pousser la tomate sur le pin : la pointe conique guide, le cran
   s'enclenche dans la rainure (petit « clic » de friction), la collerette
   vient en appui sur le sommet du col. **Le pin retient l'aimant** dans
   son logement : rien ne peut sortir.
5. Répéter pour les 7 pédicelles (mélanger rouges et vertes à volonté).
6. Accrocher la grappe à la branche : présenter l'ouverture du crochet
   face au bras (côté +Y), pousser latéralement jusqu'à ce que le bras
   s'assoie dans l'anneau. Pour retirer : tirer latéralement vers +Y.
7. **Démontage d'une tomate :** tirer droit vers le bas, le cran lâche.
   L'aimant reste dans son logement (plancher de 2 mm sous le logement,
   pin au-dessus quand la tomate est en place).

**Mécanisme de cueillette :** le robot approche sa tige métallique près du
haut du fruit → l'aimant (à 2,2 mm de la surface au col, reposant sur le
plancher de son logement) l'attire → en tirant, le cran de retenue lâche
**avant** que l'attraction magnétique ne lâche (intention de conception —
force réelle non mesurée, voir § 7). La tomate se détache de la grappe,
l'aimant reste dans la tomate.

## 5. Réglages d'impression (PLA)

| Pièce | Orientation | Supports | Couche | Parois | Remplissage | Couleur |
|---|---|---|---|---|---|---|
| Tomate | Ouverture vers le haut | Aucun | 0,2 mm | 3 | 20–25 % | rouge / vert |
| Grappe | Debout (Z vertical, crochet en haut) | Sous les bras uniquement (supports arborescents / « touchant le plateau ») | 0,2 mm | 3 | 20–25 % | vert |

- Tolérances : les jeux (0,4 mm aimant/logement, 0,4 mm pin/manchon) sont
  prévus pour le FDM. Si le pin est trop lâche/serré sur l'imprimante de
  Léandre, ajuster `PIN_R` (3,4) ou `BORE_R` (3,6) dans le script.
- Ne pas mettre de support dans le manchon ni dans le logement d'aimant.

## 6. Test de premier article (AVANT les grappes entières)

1. **1 tomate + 1 pin** (imprimer la grappe n'est pas nécessaire : le pin
   seul fait 15,6 mm — on peut l'imprimer séparément pour l'essai, ou
   couper un pédicelle d'une grappe test).
   Vérifier : l'aimant tombe bien dans le logement ; le pin s'enfonce et le
   cran s'enclenche ; la tomate tient tête en bas ; une traction droite
   la décroche sans forcer ; **la pince du robot attrape bien la forme
   ovale Ø 25 mm**.
2. **1 crochet sur 1 bras de branche** : l'enfichage latéral, la tenue
   (la grappe ne doit pas tourner ni glisser), le retrait.
3. Ensuite seulement : grappes entières, puis arbre complet.

## 7. Vérifications faites — et limites honnêtes

**Vérifié par le script** (`tomates_v2.py`, assertions) :
- Solides valides, STL **étanches** (tomate 22 964 tris, vol 4 574,8 mm³ ;
  grappe 84 850 tris, vol 9 696,1 mm³ — 8 triangles dégénérés du mailleur
  retirés, volume inchangé).
- Plancher du logement vérifié : matière pleine sous z = 24, logement vide
  au-dessus — l'aimant repose bien au fond du logement.
- Assemblage pin : 0,000 mm³ à l'entrée et inséré, 3,729 mm³ à mi-course
  (encliquetage du cran).
- Grappe + 7 tomates : aucune collision (hors pins).
- Crochet + bras : 0,000 mm³ une fois assis ; ouverture libre côté +Y,
  anneau présent côté −Y.
- Jeux aimant/logement et pin/manchon cohérents avec les tolérances FDM.

**Non testé (à déclarer) :**
- Force d'arrachement réelle (cran vs attraction magnétique) — non
  mesurable sans le vrai robot et la vraie tige.
- Tenue selon l'imprimante de Léandre (retrait PLA, tolérances réelles).
- Prise par la pince du robot avec la forme ovale Ø 25 mm (voir § 2).
- Rendu visuel réel et comportement des sépales à l'impression.

## 8. Rendus joints

- `v2-tomate.png`, `v2-tomate2.png` — tomate seule, deux angles.
- `v2-coupe.png` — demi-tomate : logement + aimant en place + pin à l'entrée.
- `v2-eclate.png` — vue éclatée : tomate / aimant / pin séparés.
- `v2-grappe.png` — grappe complète, 4 tomates rouges + 3 vertes.
- `v2-branche.png` — grappe accrochée à une branche de l'arbre v1.
- `v2-grappe-360.gif` — grappe en rotation (24 vues).
- `apercu-360.html` — page autonome (tourne toute seule, glisser pour
  tourner, molette pour zoomer) : ouvrir dans un navigateur, aucune
  installation requise.
