# Tomates 3D — note de conception v2.1 (26 novembre 2026)

**Décision finale de Léandre (26 nov. 2026, 13 h 05) : le pédoncule est FIXE
sur l'arbre/grappe ; c'est la TOMATE qui est détachable du pédoncule.**
La version v2.1 « pédoncule détachable qui s'arrache avec la tomate »
(brief de 12 h 51) a été ABANDONNÉE sur décision de Léandre et n'a pas
été construite. Le pin v2 n'a plus de rôle séparé.

## Mécanisme (cueillette par le robot)

1. La tomate pend sous le pédoncule, tenue uniquement par 2 aimants qui
   se collent : 1 dans la tomate + 1 dans le bout du pédoncule.
2. Le robot (pince ou aspirateur) saisit la tomate et tire vers le bas :
   la tomate glisse hors du doigt et se détache ; le doigt reste sur
   la grappe. Aucun cran mécanique, juste un centrage léger.
3. **Tape (Léandre)** : un morceau de ruban adhésif posé sur UNE face
   d'aimant sert de séparateur/cale : il réduit la force d'attraction
   pour faciliter le détachage. Régler en ajoutant/retirant du tape,
   sans mesure imposée — à tester sur le premier article.

## Dimensions

- **Tomate : inchangée v2** — ovale 35 mm × Ø 25 mm, 5 sépales.
  Logement d'aimant ouvert par le haut, Ø 6,4 × 4,4 mm, **plancher de
  2 mm** sous le logement (sans plancher, l'aimant tomberait dans la
  coque creuse — bogue v2, corrigé et vérifié par sonde). Paroi 2,2 mm
  au col. Impression ouverture vers le haut, sans supports.
- **Doigt (bout du pédoncule, partie de la grappe)** : doigt lisse
  Ø 7,0 mm qui descend dans le manchon de la tomate (jeu 0,2 mm),
  pastille Ø 9,0 mm posée sur le sommet du col, tige Ø 5,2 mm jusqu'au
  coude. Logement d'aimant **Ø 6,0 mm** (presse légère — les trous FDM
  sortent ~0,1–0,2 mm plus petits ; si l'aimant est lâche, une pointe
  de colle), profondeur 1,2 mm, aimant dépassant de 0,8 mm sous le
  doigt, face à l'aimant de la tomate à **2,2 mm** de distance.
- **Grappe : inchangée v2** — rachis courbe + 7 doigts en une seule
  pièce verte, crochet en C inchangé (bras v1 Ø 11 mm), arbre v1
  inchangé. Pas 24 mm entre pédicelles. Azimuts re-espacés (≥ 55°
  entre pédicelles du même côté) car l'unité pend plus bas qu'en v2.
- **Aimants** : disques néodyme N52, 6,00 × 2,00 mm (± 0,1).

## Polarité — vérifier à l'assemblage

L'aimant du pédoncule doit ATTIRER celui de la tomate. Si ça repousse,
retourner l'aimant du pédoncule et marquer sa face extérieure.
Ne pas coller les aimants avant d'avoir vérifié l'attraction.

## Assemblage

1. Laisser tomber l'aimant dans le logement de la tomate (par le haut).
2. Enfoncer l'aimant dans le logement du doigt (face affleurante, 0,8 mm
   dépassant sous le doigt).
3. Glisser la tomate sur le doigt : les 2 aimants se collent face à
   face et tiennent la tomate. Accrocher le crochet latéralement sur
   le bras de la branche.

## Aimants et stock

2 par position (1 tomate + 1 pédoncule) → **14 par grappe, 84 par
arbre complet**. Stock : 468 restants → 384 après un arbre complet.
Repli si la tenue est trop faible : 2e aimant empilé dans la tomate
(distance aimants 0,2 mm au lieu de 2,2 mm).

## Réglages d'impression

PLA — 0,2 mm, 3 parois, 20–25 %. Tomate : ouverture vers le haut, sans
supports. Grappe : debout, supports sous les bras uniquement.

## Changements vs v2, point par point

- Pédoncule : fixe (partie de la grappe) au lieu d'être tenu par un pin.
- Pin v2 : supprimé — remplacé par le doigt porte-aimant.
- Nouveau logement d'aimant dans le bout du pédoncule (Ø 6,0 mm).
- Plus de cran de retenue : glissement libre, tenue par les aimants.
- Tomate, sépales, grappe, crochet, arbre : inchangés.
- Azimuts des pédicelles re-espacés (collisions évitées).

## Test de premier article (recommandé)

1 tomate + 1 doigt (imprimer un bout de grappe ou la grappe) :
polarité, tenue en secouant doucement, détachage à la main, puis tape
sur une face si c'est trop dur à détacher.

## Limites honnêtes

Force de détachage non mesurée (pas de vrai robot) ; effet du tape non
testé ; prise pince/aspirateur sur Ø 25 mm non testée (v1 : Ø 33 mm) ;
tenue selon l'imprimante de Léandre.

## Fichiers

`tomate-v21.stl`, `grappe-v21.stl`, `tomates_v21.py` (script build123d
0.13 qui régénère les STL, vérifications incluses). STL validés :
étanches (trimesh), plancher du logement tomate vérifié par sonde,
logement du doigt vide + anneau présent, aucune collision grappe +
7 tomates, crochet + bras vérifiés.
