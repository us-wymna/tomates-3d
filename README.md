# Tomates 3D modulaires — entraînement du robot à cueillir

## Version 2.1 — pédoncule fixe, tomate détachable par aimants (26 novembre 2026)

La v2.1 est la version actuelle du site (décision finale de Léandre) :
le pédoncule est FIXE sur la grappe et c'est la TOMATE qui se détache,
tenue par 2 aimants qui se collent (1 dans la tomate + 1 dans le bout
du pédoncule, sans cran mécanique). Du tape sur une face d'aimant sert
de séparateur pour faciliter le détachage. La version « pédoncule
détachable qui s'arrache avec la tomate » a été abandonnée.

- Visionneuse : `index.html` — fichiers : `stl/tomate-v21.stl`, script
  `tomates_v21.py`, note `note-conception-v21.md`. La grappe
  (`stl/grappe-v21.stl`, 12,6 Mo) est trop lourde pour être hébergée
  ici (rejet 413, comme la v2) : le script la régénère.
- Aimants : 2 par position, 14 par grappe, 84 par arbre (468 restants).
- ⚠️ Prise par la pince / aspirateur sur Ø 25 mm non testée ; force de
  détachage et effet du tape non mesurés — tester 1 tomate + 1 doigt
  avant les grappes entières.

## Version 2 — grappes ovales (26 novembre 2026)

La v2 a été remplacée par la v2.1 (ci-dessus) : tomate ovale 35 × Ø 25 mm, 5 sépales,
1 seul aimant logé tout en haut (retenu par le pin), grappe de 7 tomates
imprimées séparément (mélange rouges/vertes), crochet en C sur les branches
de l'arbre v1 (inchangé).

- Visionneuse : `index.html` — fichiers : `stl/tomate-v2.stl`, script
  `tomates_v2.py`, note `note-conception-v2.md` (dimensions, aimants,
  assemblage, test de premier article). La grappe (`stl/grappe-v2.stl`,
  13,6 Mo) est trop lourde pour être hébergée ici : elle est dans le zip v2.
- ⚠️ La prise par la pince avec la forme ovale Ø 25 mm (v1 : Ø 33 mm) n'a pas
  encore été testée — tester 1 tomate + 1 pin avant les grappes entières.
- La v1 reste disponible : `v1.html` et ses fichiers. La simulation
  (`simulation.html`) montre toujours la v1.

---
Tomate creuse en 2 modules (corps + tige) qui s'assemblent par baïonnette, et arbre imprimé en segments. Le robot tire la tomate : elle se détache à l'arbre grâce aux aimants, jamais au milieu.

Ouvre `index.html` (ou le site déployé) pour voir le modèle en 360° et télécharger les fichiers.

Ouvre `simulation.html` pour voir le robot sortir de la maison, traverser le champ, cueillir 5 tomates rouges + 8 vertes et vider son panier dans le grand bac — en tailles réelles, avec les mesures au clic.

## Fichiers

| Fichier | Quantité | Rôle |
|---|---|---|
| `stl/tomate-corps.stl` | ×40 (20 rouges + 20 vertes) | Corps creux, 10 logements d'aimants |
| `stl/tomate-tige.stl` | ×40 | Tige + calice, baïonnette, logement de 3 aimants |
| `stl/arbre-base.stl` | ×1 | Base Ø 140 mm |
| `stl/arbre-tronc-segment.stl` | ×3 | Tronçon de tronc, 130 mm de haut (2 trous de branche chacun) |
| `stl/arbre-branche.stl` | ×6 | Branche + plot à 2 aimants |
| `tomates.py` | — | Script paramétrique (build123d) qui régénère les STL |
| `index.html` | — | Visionneuse 360° + téléchargements |
| `simulation.html` | — | Simulation 3D de la récolte autonome (maison, champ, 5 rouges + 8 vertes, mesures au clic) |

## Aimants

Disques néodyme N52 de 6,00 × 2,00 mm (± 0,1 mm).

- Corps : 10 aimants, tous dans le même sens (même face vers l'extérieur).
- Tige : 3 aimants empilés dans le logement au bout de la tige.
- Branche : 2 aimants empilés dans le logement sous le plot.
- Total : 532 aimants pour 40 tomates + 1 arbre.
- **Polarité** : avant de coller, vérifie que la tige et la branche s'attirent. Si ça se repousse, retourne les aimants d'un côté.
- Une goutte de super glue par aimant, c'est plus sûr.

## Assemblage

1. Mets les 10 aimants dans le corps (par l'ouverture du haut).
2. Enfonce la tige dans le corps (les 2 ergots dans les 2 encoches du bord), puis tourne d'environ 60° pour verrouiller. En tirant, ça ne se sépare pas : la tomate se détache à l'arbre, pas au milieu.
3. Pour ouvrir : tourne en sens inverse, puis tire.
4. Arbre : emboîte les 3 tronçons dans la base puis l'un dans l'autre, en tournant chaque tronçon d'environ 60° pour décaler les branches. Enfonce les 6 branches (2 par tronçon).

## Impression (PLA)

- Couche 0,2 mm, 3 parois, remplissage 20-25 %. Pas de supports.
- Corps : ouverture vers le haut. Tige : embout vers le bas. Base : à plat. Tronçon : debout, embout vers le bas.
- **Branche : à l'envers**, le plot rond vers le haut (la poche d'aimant s'ouvre vers le haut).
- Tailles : tomate ~33 mm de large, ~50 mm de haut assemblée. Arbre ~39 cm de haut, base 14 cm de diamètre. Le slicer indiquera le poids exact de PLA.

## Modifier le modèle

Toutes les dimensions sont en haut de `tomates.py` (build123d) :

```sh
python tomates.py
```

Ça régénère les 5 STL dans `out/`.

## Crédit

Modèle redessiné par code à partir de « Mini Tomato » de fifindr (Printables) — usage personnel.
