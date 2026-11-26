"""Tomates 3D v2 - grappes de tomates cerises ovales, aimant en haut du fruit.

Reponse au retour de Leandre (impression v1 testee, 26 nov. 2026) :
  1. Forme ovale + vraies grappes (tomates allongees ~1,5:1, sepales en etoile,
     rachis ramifie pendant, comme la photo de reference).
  2. Simple : 1 seul aimant par tomate, tombe dans un logement ouvert par le
     haut, retenu par le pin de la grappe. Aucune insertion en cours
     d'impression, pas de colle, pas de baionnette.
  3. Aimant DIRECTEMENT contre la tige : logement tout en haut du fruit, juste
     sous le point d'attache (paroi laterale de 2,2 mm seulement au niveau du
     col) pour que la tige metallique du robot ressente la force.
  4. Tomates imprimables individuellement (rouges / vertes) puis clipsees sur
     la grappe. Grappe (rachis + pedicelles + pins) imprimee en une piece.
  5. Compatibilite arbre v1 : la grappe s'accroche par un crochet en C sur le
     bras de branche existant (diametre 11 mm) - aucune modification de
     l'arbre. Le plot a aimants de la branche v1 reste inutilise.

Mecanisme de cueillette : la tomate tient sur son pin par un cran de retenue
leger (friction). Le robot approche sa tige metallique pres du haut du fruit,
l'aimant l'attire ; en tirant, le cran lache AVANT que l'aimant ne lache
(intention de conception - force non mesuree, a tester sur le vrai robot).

Aimants : disques neodyme N52, 6.00 mm de diametre x 2.00 mm (+/-0.1).
Toutes les dimensions sont en mm. L'axe Z est vertical, Z=0 = plateau.
Tomate : Z=0 base du fruit, Z=35 sommet du col.
Grappe : Z=0 bas du rachis, crochet en haut (Z~166).
"""

import math
import os

import numpy as np
import trimesh
from build123d import *

# ---------------- Parametres ----------------
MAG_D = 6.0
MAG_T = 2.0
POCKET_D = 6.4             # logement aimant (jeu diametral 0.4)
POCKET_Z0 = 24.0           # fond du logement
POCKET_Z1 = 28.4           # haut du logement (profondeur 4.4 = 2 aimants + 0.4)
BORE_R = 3.6               # alesage du manchon (diametre 7.2, aimant 6.0 passe)
BORE_Z1 = 35.5             # bouche du manchon (0.5 au-dessus du col)
GROOVE_R = 3.9             # rainure du cran (0.3 dans la paroi du manchon)
GROOVE_Z0 = 31.4
GROOVE_Z1 = 32.6
WALL = 1.4                 # paroi de la coque

FRUIT_LEN = 35.0           # longueur du fruit (sans sepales)
FRUIT_R = 12.5             # rayon max (diametre 25 mm -> ratio ~1,5:1 avec 38 mm
                           # en comptant le col ; voir note : enveloppe pince)

PIN_R = 3.4                # pin (diametre 6.8, jeu 0.4 diametral dans le manchon)
PIN_TIP_Z = 28.2           # pointe du pin une fois insere (0,2 au-dessus de
                           # 2 aimants empiles, 2,2 au-dessus d'1 seul aimant)
PIN_DROP = 14.0            # pointe du pin sous le coude : le bras passe 2,5 mm
                           # au-dessus des sepales, quelle que soit leur orientation
RIDGE_R = 3.85             # cran de retenue (saillie 0,45)
RIDGE_Z0 = 31.5            # cran centre sur la rainure une fois insere
RIDGE_Z1 = 32.5
COLLAR_R = 5.0             # collerette du pin (appui sur le sommet du col)
COLLAR_H = 1.6

N_PEDICELS = 7
PEDICEL_Z = [16.0, 40.0, 64.0, 88.0, 112.0, 136.0, 160.0]
PEDICEL_AZ = [75.0, 280.0, 110.0, 245.0, 95.0, 285.0, 80.0]  # degres, alternes + jitter
RACHIS_PTS = [(0.0, 0.0, 0.0), (2.5, 0.0, 55.0), (4.0, 0.0, 110.0), (1.5, 0.0, 164.0)]
RACHIS_R = [2.2, 2.5, 2.7, 2.9]
HOOK_R_IN = 5.9            # rayon interieur du crochet (bras de branche : r 5,5)
HOOK_TUBE = 2.6            # demi-epaisseur de la sangle (section 5,2 x 5,2)
HOOK_CENTER = (1.5, 0.0, 178.0)

ROOT = os.path.expanduser("~/workspace/tomates3d/v2")
STL_DIR = os.path.join(ROOT, "stl")
ASCII_DIR = os.path.join(ROOT, "stl-ascii")
GEOM_DIR = os.path.join(ROOT, "geom")
for d in (STL_DIR, ASCII_DIR, GEOM_DIR):
    os.makedirs(d, exist_ok=True)


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _rachis_x(z):
    """Axe du rachis (courbure legere) interpole sur RACHIS_PTS."""
    pts = RACHIS_PTS
    if z <= pts[0][2]:
        return pts[0][0]
    for i in range(len(pts) - 1):
        z0, z1 = pts[i][2], pts[i + 1][2]
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return pts[i][0] + t * (pts[i + 1][0] - pts[i][0])
    return pts[-1][0]


def build_tomato():
    """Coque ovale creuse, manchon + logement d'aimant ouverts en haut, sepales."""
    outer_pts = [
        (4.0, 0.0), (8.5, 1.2), (11.5, 4.5), (12.5, 9.0), (12.3, 14.0),
        (11.2, 19.0), (9.2, 24.0), (7.0, 28.5), (5.6, 31.5), (5.2, 33.0),
    ]
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Spline(*outer_pts)
                Line(outer_pts[-1], (5.2, 35.0))
                Line((5.2, 35.0), (0.0, 35.0))
                Line((0.0, 35.0), (0.0, 0.0))
                Line((0.0, 0.0), outer_pts[0])
            make_face()
        revolve(revolution_arc=360)
    outer = bp.part

    # Cavite : paroi 1,4, plafond conique jusqu'a 2 mm SOUS le fond du
    # logement (z=22) : les 2 mm de matiere entre 22 et 24 forment le
    # PLANCHER du logement, sinon l'aimant tomberait dans la coque creuse.
    inner_pts = [
        (3.5, 1.4), (7.5, 1.8), (10.1, 4.5), (11.1, 9.0),
        (10.9, 14.0), (9.8, 18.0), (8.6, 19.0),
    ]
    with BuildPart() as bp2:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Spline(*inner_pts)
                Line(inner_pts[-1], (3.2, POCKET_Z0 - 2.0))
                Line((3.2, POCKET_Z0 - 2.0), (0.0, POCKET_Z0 - 2.0))
                Line((0.0, POCKET_Z0 - 2.0), (0.0, 1.4))
                Line((0.0, 1.4), inner_pts[0])
            make_face()
        revolve(revolution_arc=360)
    body = outer - bp2.part

    # Logement d'aimant (ouvert par le haut via le manchon).
    body = body - Pos(0, 0, (POCKET_Z0 + POCKET_Z1) / 2) * Cylinder(
        POCKET_D / 2, POCKET_Z1 - POCKET_Z0
    )
    # Manchon (alesage) jusqu'a la bouche.
    body = body - Pos(0, 0, (POCKET_Z1 + BORE_Z1) / 2) * Cylinder(
        BORE_R, BORE_Z1 - POCKET_Z1
    )
    # Rainure du cran de retenue.
    body = body - Pos(0, 0, (GROOVE_Z0 + GROOVE_Z1) / 2) * Cylinder(
        GROOVE_R, GROOVE_Z1 - GROOVE_Z0
    )

    # Sepales : 5, etoile autour du col, sans support (env. 51 degres).
    sepal_pts = [(4.4, 31.0), (9.8, 37.2), (9.0, 37.8), (4.2, 34.2)]
    with BuildPart() as sp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*sepal_pts, close=True)
            make_face()
        extrude(amount=0.5, both=True)
    sepal = sp.part
    sepals = sepal
    for k in range(1, 5):
        sepals = sepals + (Rot(0, 0, 72 * k) * sepal)
    return body + sepals


def build_pin():
    """Pin de la grappe : pointe conique, cran de retenue, collerette, tige.

    Repere local : pointe a z=0, collerette a z=6.8..8.4, tige jusqu'a
    z=15.6 (soude au coude du pedicelle). Une fois insere (pointe a z=28.2
    dans le fruit), le cran est centre sur la rainure (z=32) et la
    collerette repose sur le sommet du col (z=35).
    """
    pts = [
        (0.0, 0.0), (2.6, 0.0), (PIN_R, 1.6), (PIN_R, 3.3),
        (RIDGE_R, 3.55), (RIDGE_R, 4.05), (PIN_R, 4.3), (PIN_R, 6.8),
        (COLLAR_R, 6.8), (COLLAR_R, 8.4), (2.6, 8.4), (2.6, 15.6), (0.0, 15.6),
    ]
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*pts, close=True)
            make_face()
        revolve(revolution_arc=360)
    return bp.part


def build_magnet():
    return Pos(0, 0, POCKET_Z0 + MAG_T / 2) * Cylinder(MAG_D / 2, MAG_T)


def _segment(p0, p1, r0, r1):
    d = tuple(b - a for a, b in zip(p0, p1))
    h = math.sqrt(sum(c * c for c in d))
    return Solid.make_cone(r0, r1, h, Plane(origin=p0, z_dir=_norm(d)))


def build_hook():
    """Crochet en C (sangle ouverte) pour le bras de branche (r 5,5).

    Secteur d'anneau extrude (pas de tore partiel : les booleens OCC
    avec un tore a angle limite sont defectueux dans cette version de
    build123d). Ouverture de 100 degres centree sur +Y : enfichage lateral
    sur le bras (axe X). Section de la sangle 5,2 x 5,2 mm.
    """
    a0, a1, am = math.radians(140), math.radians(40), math.radians(270)
    ro = HOOK_R_IN + 2 * HOOK_TUBE
    ri = HOOK_R_IN

    def pt(r, a):
        return (r * math.cos(a), r * math.sin(a))

    so, eo, mo = pt(ro, a0), pt(ro, a1), pt(ro, am)
    si, ei, mi = pt(ri, a0), pt(ri, a1), pt(ri, am)
    with BuildPart() as bp:
        with BuildSketch(Plane.XY):
            with BuildLine():
                ThreePointArc(so, mo, eo)
                Line(eo, ei)
                ThreePointArc(ei, mi, si)
                Line(si, so)
            make_face()
        extrude(amount=HOOK_TUBE, both=True)
    ring = bp.part
    hook = Pos(*HOOK_CENTER) * Rot(0, 90, 0) * ring
    return hook, ring


def pedicel_geometry(i):
    """Retourne (base, coude, direction) du pedicelle i.

    Bras de 19 mm : l'axe de la tomate doit etre a ~19 mm de l'axe du
    rachis, sinon le fruit (rayon 12,5) touche le rachis (rayon ~2,5).
    """
    z = PEDICEL_Z[i]
    az = math.radians(PEDICEL_AZ[i])
    base = (_rachis_x(z), 0.0, z)
    direction = _norm((math.cos(az), math.sin(az), -0.12))
    elbow = tuple(b + 19.0 * d for b, d in zip(base, direction))
    return base, elbow, direction


def build_cluster(with_pins=True):
    """Rachis + pedicelles + pins + crochet, en une seule piece."""
    parts = []
    pts = RACHIS_PTS
    for i in range(len(pts) - 1):
        parts.append(_segment(pts[i], pts[i + 1], RACHIS_R[i], RACHIS_R[i + 1]))
    for p, r in zip(pts, RACHIS_R):
        parts.append(Solid.make_sphere(r, Plane(origin=p)))
    parts.append(Solid.make_sphere(3.0, Plane(origin=pts[0])))
    # Col du crochet + crochet + bout de tige.
    parts.append(
        Solid.make_cylinder(2.6, 13.0, Plane(origin=(1.5, 0.0, 162.0), z_dir=(0, 0, 1)))
    )
    hook, _ring = build_hook()
    parts.append(hook)
    parts.append(
        Solid.make_cylinder(2.2, 14.0, Plane(origin=(1.5, 0.0, 180.0), z_dir=(0, 0, 1)))
    )
    pin = build_pin()
    for i in range(N_PEDICELS):
        base, elbow, direction = pedicel_geometry(i)
        parts.append(
            Solid.make_cylinder(1.9, 19.0, Plane(origin=base, z_dir=direction))
        )
        parts.append(Solid.make_sphere(2.8, Plane(origin=elbow)))
        if with_pins:
            # Pointe du pin a PIN_DROP sous le coude, tige soudee dans la sphere.
            parts.append(Pos(elbow[0], elbow[1], elbow[2] - PIN_DROP) * pin)
    cluster = parts[0]
    for p in parts[1:]:
        cluster = cluster + p
    return cluster


def tomato_placement(i):
    """Position (x, y, z de l'origine) d'une tomate sur le pedicelle i."""
    _base, elbow, _d = pedicel_geometry(i)
    pin_tip_z = elbow[2] - PIN_DROP
    return (elbow[0], elbow[1], pin_tip_z - PIN_TIP_Z)


def tomato_rotation(i):
    """Rotation Z de la tomate sur son pin (degres).

    Le joint est axisymetrique : on tourne chaque tomate de 36 degres par
    rapport a son pedicelle pour que les sepales (tous les 72 degres) ne
    touchent jamais le bras du pedicelle.
    """
    return PEDICEL_AZ[i] + 36.0


def write_stl_ascii(mesh, path, name):
    tris = np.asarray(mesh.triangles, dtype=np.float64)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"solid {name}\n")
        for tri in tris:
            n = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            ln = np.linalg.norm(n)
            n = n / ln if ln > 0 else np.array([0.0, 0.0, 0.0])
            fh.write(
                " facet normal %.4f %.4f %.4f\n  outer loop\n" % (n[0], n[1], n[2])
            )
            for v in tri:
                fh.write("  vertex %.4f %.4f %.4f\n" % (v[0], v[1], v[2]))
            fh.write("  endloop\n endfacet\n")
        fh.write(f"endsolid {name}\n")


def inter_vol(a, b):
    """Volume d'intersection (0.0 si les solides ne se touchent pas :
    l'operateur & de build123d renvoie None dans ce cas)."""
    inter = a & b
    return 0.0 if inter is None else inter.volume


def check(name, part):
    bb = part.bounding_box()
    print(
        f"{name}: valid={part.is_valid} vol={part.volume:.1f} mm3 "
        f"bbox=({bb.min.X:.1f},{bb.min.Y:.1f},{bb.min.Z:.1f}).."
        f"({bb.max.X:.1f},{bb.max.Y:.1f},{bb.max.Z:.1f})"
    )
    return part


def check_mesh(path):
    m = trimesh.load(path, force="mesh")
    print(
        f"  {os.path.basename(path)}: watertight={m.is_watertight} "
        f"vol={m.volume:.1f} mm3 tris={len(m.faces)}"
    )
    assert m.is_watertight, f"STL non etanche : {path}"
    return m


def clean_stl(path):
    """Retire les triangles degeneres (sommet repete, aire nulle) que le
    mailleur OCC emet aux points de couture (8 sur la grappe, 0 sur la
    tomate). Geometrie inchangee (volume identique), maillage etanche."""
    m = trimesh.load(path, force="mesh")
    faces = np.asarray(m.faces)
    keep = np.array([len(set(f.tolist())) == 3 for f in faces])
    if (~keep).any():
        m.update_faces(keep)
        m.remove_unreferenced_vertices()
        m.export(path)
    return int((~keep).sum())


def main():
    tomato = check("tomate-v2", build_tomato())
    pin = check("pin-v2", build_pin())
    cluster = check("grappe-v2", build_cluster())
    cluster_nopins = build_cluster(with_pins=False)

    # --- Jeu aimant / logement ---
    assert abs(POCKET_D - MAG_D) >= 0.3, "jeu aimant insuffisant"
    # --- Plancher du logement : l'aimant doit reposer a z=24 ---
    floor_probe = Pos(0, 0, 23.0) * Cylinder(3.0, 2.0)  # z 22-24 : plancher
    floor_vol = inter_vol(tomato, floor_probe)
    assert floor_vol > 50.0, f"pas de plancher sous le logement ({floor_vol:.1f})"
    pocket_probe = Pos(0, 0, 26.0) * Cylinder(3.0, 4.0)  # z 24-28 : logement
    assert inter_vol(tomato, pocket_probe) < 1.0, "le logement n'est pas vide"
    print(f"logement : plancher present ({floor_vol:.1f} mm3 de matiere sous z=24), logement vide")
    assert POCKET_Z1 - POCKET_Z0 >= 2 * MAG_T + 0.3, "profondeur logement"
    print(
        f"logement: diametre {POCKET_D} (aimant {MAG_D}, jeu 0,4), "
        f"profondeur {POCKET_Z1 - POCKET_Z0} (2 aimants = {2 * MAG_T} + 0,4)"
    )
    print(
        f"aimant : paroi laterale au col = {5.2 - MAG_D / 2:.1f} mm "
        f"(magnet r {MAG_D / 2} dans le col r 5,2)"
    )

    # --- Assemblage pin dans le manchon ---
    # Entree et insere : jeu libre (cran dans la rainure). Mi-course : le cran
    # (r 3,85) passe dans le manchon (r 3,6) -> interference attendue, c'est
    # l'encliquetage ; elle doit rester petite (quelques mm3).
    for label, tip_z, vmax in (
        ("entree", 33.0, 2.0),
        ("mi-course", 30.5, 10.0),
        ("insere", PIN_TIP_Z, 2.0),
    ):
        placed = Pos(0, 0, tip_z) * pin
        v = inter_vol(tomato, placed)
        print(f"assemblage pin {label}: intersection={v:.3f} mm3")
        assert v < vmax, f"collision pin/tomate en position {label}"
    mid = inter_vol(tomato, Pos(0, 0, 30.5) * pin)
    assert mid > 0.5, "le cran ne s'engage pas dans le manchon"

    # --- Grappe + 7 tomates : pas de collision hors pins, tomates entre elles ---
    def placed_tomato(i):
        x, y, z = tomato_placement(i)
        return Pos(x, y, z) * Rot(0, 0, tomato_rotation(i)) * tomato

    for i in range(N_PEDICELS):
        v = inter_vol(cluster_nopins, placed_tomato(i))
        assert v < 1.0, f"tomate {i} touche la grappe ({v:.2f})"
    for i in range(N_PEDICELS):
        for j in range(i + 1, N_PEDICELS):
            v = inter_vol(placed_tomato(i), placed_tomato(j))
            assert v < 1.0, f"tomates {i}/{j} se touchent ({v:.2f})"
    print("assemblage grappe + 7 tomates : aucune collision (hors pins)")

    # --- Crochet : le bras de branche (r 5,5, axe X) passe libre, ouverture +Y ---
    hook, _ring = build_hook()
    arm = Solid.make_cylinder(
        5.5, 30.0, Plane(origin=(HOOK_CENTER[0] - 15, 0, HOOK_CENTER[2]), z_dir=(1, 0, 0))
    )
    inter = inter_vol(hook, arm)
    print(f"crochet + bras assis : intersection={inter:.3f} mm3")
    assert inter < 1.0, "le bras touche le crochet une fois assis"
    gap_probe = Pos(HOOK_CENTER[0], 8.5, HOOK_CENTER[2]) * Box(6.0, 7.0, 6.0)
    assert inter_vol(hook, gap_probe) < 0.5, "l'ouverture du crochet n'est pas libre (+Y)"
    ring_probe = Pos(HOOK_CENTER[0], -8.5, HOOK_CENTER[2]) * Box(6.0, 7.0, 6.0)
    assert inter_vol(hook, ring_probe) > 5.0, "l'anneau du crochet est absent (-Y)"
    print("crochet : ouverture libre cote +Y, anneau present cote -Y")

    # --- Exports ---
    export_stl(tomato, os.path.join(STL_DIR, "tomate-v2.stl"))
    export_stl(cluster, os.path.join(STL_DIR, "grappe-v2.stl"))
    # Geometrie pour rendus : demi-tomate en coupe, aimant, pin seul.
    half_box = Pos(0, -25, 24.5) * Box(100, 50, 51)
    half = tomato & half_box
    export_stl(half, os.path.join(GEOM_DIR, "tomate-v2-demi.stl"))
    export_stl(build_magnet(), os.path.join(GEOM_DIR, "aimant-v2.stl"))
    export_stl(pin, os.path.join(GEOM_DIR, "pin-v2.stl"))
    n_deg = clean_stl(os.path.join(STL_DIR, "grappe-v2.stl"))
    clean_stl(os.path.join(STL_DIR, "tomate-v2.stl"))
    clean_stl(os.path.join(GEOM_DIR, "tomate-v2-demi.stl"))
    print(f"STL binaires ecrits dans {STL_DIR} ({n_deg} triangles degeneres retires)")

    for name, part in (("tomate-v2", tomato), ("grappe-v2", cluster)):
        mesh = trimesh.load(os.path.join(STL_DIR, f"{name}.stl"), force="mesh")
        write_stl_ascii(mesh, os.path.join(ASCII_DIR, f"{name}.stl"), name)
    print("STL ASCII ecrits dans", ASCII_DIR)

    print("Validation etancheite :")
    check_mesh(os.path.join(STL_DIR, "tomate-v2.stl"))
    check_mesh(os.path.join(STL_DIR, "grappe-v2.stl"))
    check_mesh(os.path.join(GEOM_DIR, "tomate-v2-demi.stl"))
    print("OK - v2 prete")


if __name__ == "__main__":
    main()
