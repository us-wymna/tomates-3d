# Tomates 3D modulaires — entraînement du robot à cueillir

Tomate creuse en 2 modules (corps + tige) qui s'assemblent par baïonnette, et arbre imprimé en segments. Le robot tire la tomate : elle se détache à l'arbre grâce aux aimants, jamais au milieu.

Ouvre `index.html` (ou le site déployé) pour voir le modèle en 360° et télécharger les fichiers.

## Fichiers

| Fichier | Quantité | Rôle |
|---|---|---|
| `stl/tomate-corps.stl` | ×40 (20 rouges + 20 vertes) | Corps creux, 10 logements d'aimants |
| `stl/tomate-tige.stl` | ×40 | Tige + calice, baïonnette, logement de 3 aimants |
| `stl/arbre-base.stl` | ×1 | Base Ø 120 mm |
| `stl/arbre-tronc-segment.stl` | ×3 | Tronçon de tronc (2 trous de branche chacun) |
| `stl/arbre-branche.stl` | ×6 | Branche + plot à 2 aimants |
| `tomates.py` | — | Script paramétrique (build123d) qui régénère les STL |
| `index.html` | — | Visionneuse 360° + téléchargements |

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
- Tailles : tomate ~33 mm de large, ~50 mm de haut assemblée. Arbre ~24 cm de haut, base 12 cm de diamètre. Environ 400 g de PLA avec 25 % de remplissage.

## Modifier le modèle

Toutes les dimensions sont en haut de `tomates.py` (build123d) :

```sh
python tomates.py
```

Ça régénère les 5 STL dans `out/`.

## Crédit

Modèle redessiné par code à partir de « Mini Tomato » de fifindr (Printables) — usage personnel.
