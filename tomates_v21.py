"""Tomates 3D v2.1 - pedoncule FIXE, tomate detachable par aimants.

Decision FINALE de Leandre (26 nov. 2026, 13 h 05, relayee par Joseph).
La version « pedoncule detachable qui s'arrache avec la tomate »
(breif de 12 h 51) est ABANDONNEE et n'a pas ete construite ici.

Mecanisme final :
  - Le PEDONCULE est FIXE sur l'arbre/grappe (comme en v2 : rachis +
    pedicelles en une seule piece verte). Pas de piece separee, pas
    d'arrachement, pas d'emmanchement pedoncule/pin.
  - C'est la TOMATE qui est DETACHABLE du pedoncule.
  - 1 aimant dans la tomate (logement v2 inchange : ouvert par le haut,
    D 6,4 x 4,4 mm, plancher de 2 mm - SANS plancher l'aimant tomberait
    dans la coque creuse, bogue v2 corrige ici aussi) + 1 aimant dans
    le bout du PEDONCULE (NOUVEAU logement, face a celui de la tomate) :
    les deux aimants SE COLLENT et c'est cette attraction qui tient la
    tomate sur l'arbre.
  - PAS de cran mecanique de retenue : juste un centrage leger (le
    doigt glisse librement dans le manchon, sans retention) pour que
    les deux faces d'aimants se rencontrent bien face a face. Les
    faces d'aimants sont accessibles et affleurantes.
  - Le PIN v2 n'a plus de role separe : le bout du pedoncule porte
    l'aimant. Le crochet en C et l'arbre v1 sont inchanges. La tomate
    garde ses 5 sepales.
  - « On pourra mettre du tape pour les separer » (Leandre) : du ruban
    adhesif peut etre pose sur une face d'aimant comme separateur/cale
    pour regler la separation (voir la note de conception).
  - Polarite : l'aimant du pedoncule doit ATTIRER celui de la tomate ;
    verifier a l'assemblage (si ca repousse, retourner l'aimant du
    pedoncule) et marquer la face exterieure.

Geometrie :
  - Tomate : INCHANGEE v2 (ovale 35 x D 25 mm, 5 sepales, logement
    ouvert par le haut, plancher de 2 mm, paroi 2,2 mm au col).
  - Doigt (bout du pedoncule, partie de la grappe) : doigt lisse
    r 3,5 qui descend dans le manchon (jeu 0,2), pastille r 4,5 posee
    sur le sommet du col, tige r 2,6 jusqu'a la sphere du coude.
    Logement d'aimant presse dans le bas du doigt (D 6,0, profondeur
    1,2, aimant depasse de 0,8 sous le doigt, face a l'aimant de la
    tomate, distance 2,2 mm avec 1 aimant dans la tomate ; un 2e
    aimant empile dans la tomate est le repli documente si la tenue
    est trop faible - distance 0,2 mm).
  - Grappe : rachis courbe + 7 doigts (partie de la piece verte en une
    piece), crochet en C inchange sur bras v1 D 11 mm, arbre v1
    inchange. Pas 24 mm entre pedicelles (comme v2). Azimuts
    re-espaces (>= 55 degres entre pedicelles du meme cote) car
    l'unite pend plus bas qu'en v2 : avec les azimuts v2, le ventre
    du fruit avalait le coude du pedicelle deux crans plus bas.

Aimants : disques neodyme N52, 6.00 mm de diametre x 2.00 mm (+/-0.1).
Toutes les dimensions sont en mm. L'axe Z est vertical, Z=0 = plateau
(pour la tomate : Z=0 = base du fruit, Z=35 = sommet du col).
"""

import math
import os

import numpy as np
import trimesh
from build123d import *

# ---------------- Parametres (tomate : identiques v2) ----------------
MAG_D = 6.0
MAG_T = 2.0
POCKET_D = 6.4             # logement aimant tomate (jeu diametral 0.4)
POCKET_Z0 = 24.0           # fond du logement tomate
POCKET_Z1 = 28.4           # haut du logement tomate (2 aimants + 0.4)
BORE_R = 3.6               # alesage du manchon tomate (diametre 7.2)
BORE_Z1 = 35.5             # bouche du manchon
GROOVE_R = 3.9             # rainure v2 du manchon (inutilisee en v2.1, conservee)
GROOVE_Z0 = 31.4
GROOVE_Z1 = 32.6
WALL = 1.4                 # paroi de la coque tomate

FRUIT_LEN = 35.0
FRUIT_R = 12.5             # diametre 25 mm

# ---------------- Parametres (doigt : bout du pedoncule, repere tomate) ----------------
FINGER_R = 3.5             # doigt lisse (diametre 7.0, jeu 0.2 dans le manchon)
FINGER_Z0 = 29.0           # bas du doigt (0,6 au-dessus du haut du logement)
FINGER_Z1 = 35.0           # haut du doigt = dessous de la pastille
FINGER_POCKET_R = 3.0      # logement aimant pedoncule (D 6.0, presse legere :
                           # les trous FDM sortent ~0,1-0,2 plus petits ; si
                           # l'aimant est lache, une pointe de colle ; voir note)
FINGER_POCKET_Z0 = 29.0    # ouverture du logement (bas du doigt)
FINGER_POCKET_Z1 = 30.2    # haut du logement (profondeur 1.2, aimant depasse
                           # de 0.8 sous le doigt, face a l'aimant tomate)
PAD_R = 4.5                # pastille posee sur le sommet du col
PAD_Z0 = 35.0
PAD_Z1 = 37.0
STEM_R = 2.6               # tige jusqu'a la sphere du coude
STEM_Z1 = 55.0             # sommet de la tige (dans la sphere du coude)
UNIT_DROP = 54.0           # origine tomate = coude - 54 (doigt : coude -> z=29)

N_PEDICELS = 7
PEDICEL_Z = [16.0, 40.0, 64.0, 88.0, 112.0, 136.0, 160.0]
# Azimuts re-espaces : >= 55 degres entre pedicelles du meme cote.
PEDICEL_AZ = [60.0, 240.0, 120.0, 300.0, 65.0, 245.0, 125.0]
RACHIS_PTS = [(0.0, 0.0, 0.0), (2.5, 0.0, 55.0), (4.0, 0.0, 110.0), (1.5, 0.0, 164.0)]
RACHIS_R = [2.2, 2.5, 2.7, 2.9]
HOOK_R_IN = 5.9
HOOK_TUBE = 2.6
HOOK_CENTER = (1.5, 0.0, 178.0)

ROOT = os.path.expanduser("~/workspace/tomates3d/v2.1")
STL_DIR = os.path.join(ROOT, "stl")
ASCII_DIR = os.path.join(ROOT, "stl-ascii")
GEOM_DIR = os.path.join(ROOT, "geom")
for d in (STL_DIR, ASCII_DIR, GEOM_DIR):
    os.makedirs(d, exist_ok=True)


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _rachis_x(z):
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
    """Coque ovale creuse v2, inchangee (plancher de 2 mm sous le logement)."""
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

    body = body - Pos(0, 0, (POCKET_Z0 + POCKET_Z1) / 2) * Cylinder(
        POCKET_D / 2, POCKET_Z1 - POCKET_Z0
    )
    body = body - Pos(0, 0, (POCKET_Z1 + BORE_Z1) / 2) * Cylinder(
        BORE_R, BORE_Z1 - POCKET_Z1
    )
    body = body - Pos(0, 0, (GROOVE_Z0 + GROOVE_Z1) / 2) * Cylinder(
        GROOVE_R, GROOVE_Z1 - GROOVE_Z0
    )

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


def build_finger():
    """Doigt (bout du pedoncule), repere tomate. Lisse, SANS cran : le
    centrage seul guide la tomate, seuls les aimants la retiennent.

    Le doigt ne descend JAMAIS dans le logement de la tomate : il
    s'arrete a z=29.0, au-dessus du haut du logement (28.4) ; seul
    l'aimant depasse dans le haut du logement.
    """
    finger = Pos(0, 0, (FINGER_Z0 + FINGER_Z1) / 2) * Cylinder(
        FINGER_R, FINGER_Z1 - FINGER_Z0
    )
    pad = Pos(0, 0, (PAD_Z0 + PAD_Z1) / 2) * Cylinder(
        PAD_R, PAD_Z1 - PAD_Z0
    )
    stem = Pos(0, 0, (PAD_Z1 + STEM_Z1) / 2) * Cylinder(
        STEM_R, STEM_Z1 - PAD_Z1
    )
    body = finger + pad + stem

    # Logement d'aimant du pedoncule (ouvert par le bas du doigt).
    body = body - Pos(0, 0, (FINGER_POCKET_Z0 + FINGER_POCKET_Z1) / 2) * Cylinder(
        FINGER_POCKET_R, FINGER_POCKET_Z1 - FINGER_POCKET_Z0
    )
    return body


def build_magnet_tomato():
    return Pos(0, 0, POCKET_Z0 + MAG_T / 2) * Cylinder(MAG_D / 2, MAG_T)


def build_magnet_finger():
    # Aimant presse dans le doigt : de 0.8 sous le doigt (28.2) a 30.2.
    return Pos(0, 0, 29.2) * Cylinder(MAG_D / 2, MAG_T)


def _segment(p0, p1, r0, r1):
    d = tuple(b - a for a, b in zip(p0, p1))
    h = math.sqrt(sum(c * c for c in d))
    return Solid.make_cone(r0, r1, h, Plane(origin=p0, z_dir=_norm(d)))


def build_hook():
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
    z = PEDICEL_Z[i]
    az = math.radians(PEDICEL_AZ[i])
    base = (_rachis_x(z), 0.0, z)
    direction = _norm((math.cos(az), math.sin(az), -0.12))
    elbow = tuple(b + 19.0 * d for b, d in zip(base, direction))
    return base, elbow, direction


def build_cluster():
    """Rachis + pedicelles + doigts + crochet, en une seule piece verte."""
    parts = []
    pts = RACHIS_PTS
    for i in range(len(pts) - 1):
        parts.append(_segment(pts[i], pts[i + 1], RACHIS_R[i], RACHIS_R[i + 1]))
    for p, r in zip(pts, RACHIS_R):
        parts.append(Solid.make_sphere(r, Plane(origin=p)))
    parts.append(Solid.make_sphere(3.0, Plane(origin=pts[0])))
    parts.append(
        Solid.make_cylinder(2.6, 13.0, Plane(origin=(1.5, 0.0, 162.0), z_dir=(0, 0, 1)))
    )
    hook, _ring = build_hook()
    parts.append(hook)
    parts.append(
        Solid.make_cylinder(2.2, 14.0, Plane(origin=(1.5, 0.0, 180.0), z_dir=(0, 0, 1)))
    )
    finger = build_finger()
    for i in range(N_PEDICELS):
        base, elbow, direction = pedicel_geometry(i)
        parts.append(
            Solid.make_cylinder(1.9, 19.0, Plane(origin=base, z_dir=direction))
        )
        parts.append(Solid.make_sphere(2.8, Plane(origin=elbow)))
        # Doigt : repere tomate, origine a coude - UNIT_DROP.
        parts.append(Pos(elbow[0], elbow[1], elbow[2] - UNIT_DROP) * finger)
    cluster = parts[0]
    for p in parts[1:]:
        cluster = cluster + p
    return cluster


def tomato_placement(i):
    """Position (x, y, z de l'origine) d'une tomate sur le pedicelle i."""
    _base, elbow, _d = pedicel_geometry(i)
    return (elbow[0], elbow[1], elbow[2] - UNIT_DROP)


def tomato_rotation(i):
    """Rotation Z de la tomate (degres) : les sepales (tous les 72 degres)
    ne touchent jamais le bras du pedicelle."""
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
    m = trimesh.load(path, force="mesh")
    faces = np.asarray(m.faces)
    keep = np.array([len(set(f.tolist())) == 3 for f in faces])
    if (~keep).any():
        m.update_faces(keep)
        m.remove_unreferenced_vertices()
        m.export(path)
    return int((~keep).sum())


def main():
    tomato = check("tomate-v21", build_tomato())
    finger = check("doigt-v21", build_finger())
    cluster = check("grappe-v21", build_cluster())
    mag_t = build_magnet_tomato()
    mag_f = build_magnet_finger()

    # --- Plancher du logement tomate (bogue v2 : ne pas reintroduire) ---
    floor_probe = Pos(0, 0, 23.0) * Cylinder(3.0, 2.0)
    floor_vol = inter_vol(tomato, floor_probe)
    assert floor_vol > 50.0, f"pas de plancher sous le logement ({floor_vol:.1f})"
    pocket_probe = Pos(0, 0, 26.0) * Cylinder(3.0, 4.0)
    assert inter_vol(tomato, pocket_probe) < 1.0, "le logement tomate n'est pas vide"
    print(f"logement tomate : plancher present ({floor_vol:.1f} mm3), logement vide")

    # --- Logement d'aimant du doigt : vide + anneau de matiere present ---
    fpocket_probe = Pos(0, 0, 29.6) * Cylinder(2.8, 0.8)
    assert inter_vol(finger, fpocket_probe) < 1.0, "logement doigt non vide"
    ring_outer = Pos(0, 0, 29.6) * Cylinder(3.4, 0.8)
    ring_inner = Pos(0, 0, 29.6) * Cylinder(3.1, 0.8)
    ring_vol = inter_vol(finger, ring_outer - ring_inner)
    assert ring_vol > 1.0, f"anneau du logement doigt absent ({ring_vol:.1f})"
    print(f"logement doigt : vide, anneau present ({ring_vol:.1f} mm3)")

    # --- Les 2 aimants face a face : 2,2 mm de distance, sans contact ---
    gap = 28.2 - (POCKET_Z0 + MAG_T)
    print(f"aimants face a face : distance = {gap:.1f} mm")
    assert 2.0 < gap < 2.4, "distance aimants hors plage"
    assert inter_vol(mag_t, mag_f) == 0.0, "les aimants se touchent"
    assert inter_vol(finger, mag_f) < 0.5, "l'aimant depasse dans le doigt"

    # --- Glissement du doigt dans le manchon : sans contact, sans cran ---
    # La tomate monte sur le doigt : entree (10 mm sous la position),
    # mi-course (4 mm sous), en place (0). Aucune retention mecanique :
    # l'intersection doit rester ~0 partout (jeu 0,2 diametral).
    for label, dz in (("entree", -10.0), ("mi-course", -4.0), ("en place", 0.0)):
        placed = Pos(0, 0, dz) * tomato
        v = inter_vol(finger, placed)
        print(f"glissement doigt {label}: intersection={v:.3f} mm3")
        assert v < 1.0, f"contact doigt/tomate en position {label}"
    assert inter_vol(tomato, mag_f) == 0.0, "l'aimant du doigt touche la tomate"

    # --- Grappe + 7 tomates : pas de collision ---
    def placed_tomato(i):
        x, y, z = tomato_placement(i)
        return Pos(x, y, z) * Rot(0, 0, tomato_rotation(i)) * tomato

    for i in range(N_PEDICELS):
        v = inter_vol(cluster, placed_tomato(i))
        assert v < 1.0, f"tomate {i} touche la grappe ({v:.2f})"
    for i in range(N_PEDICELS):
        for j in range(i + 1, N_PEDICELS):
            v = inter_vol(placed_tomato(i), placed_tomato(j))
            assert v < 1.0, f"tomates {i}/{j} se touchent ({v:.2f})"
    print("assemblage grappe + 7 tomates : aucune collision")

    # --- Crochet : bras de branche (r 5,5, axe X), ouverture +Y ---
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
    export_stl(tomato, os.path.join(STL_DIR, "tomate-v21.stl"))
    export_stl(cluster, os.path.join(STL_DIR, "grappe-v21.stl"))
    export_stl(finger, os.path.join(GEOM_DIR, "doigt-v21.stl"))
    half_box = Pos(0, -25, 24.5) * Box(100, 50, 51)
    export_stl(tomato & half_box, os.path.join(GEOM_DIR, "demi-tomate-v21.stl"))
    half_box_tall = Pos(0, -25, 29.5) * Box(100, 50, 61)
    export_stl(finger & half_box_tall, os.path.join(GEOM_DIR, "demi-doigt-v21.stl"))
    export_stl(mag_t, os.path.join(GEOM_DIR, "aimant-v21.stl"))
    n_deg = 0
    for f in ("tomate-v21.stl", "grappe-v21.stl"):
        n_deg += clean_stl(os.path.join(STL_DIR, f))
    clean_stl(os.path.join(GEOM_DIR, "demi-tomate-v21.stl"))
    clean_stl(os.path.join(GEOM_DIR, "demi-doigt-v21.stl"))
    print(f"STL binaires ecrits dans {STL_DIR} ({n_deg} triangles degeneres retires)")

    for name, part in (("tomate-v21", tomato), ("grappe-v21", cluster)):
        mesh = trimesh.load(os.path.join(STL_DIR, f"{name}.stl"), force="mesh")
        write_stl_ascii(mesh, os.path.join(ASCII_DIR, f"{name}.stl"), name)
    print("STL ASCII ecrits dans", ASCII_DIR)

    print("Validation etancheite :")
    check_mesh(os.path.join(STL_DIR, "tomate-v21.stl"))
    check_mesh(os.path.join(STL_DIR, "grappe-v21.stl"))
    check_mesh(os.path.join(GEOM_DIR, "demi-tomate-v21.stl"))
    check_mesh(os.path.join(GEOM_DIR, "demi-doigt-v21.stl"))
    print("OK - v2.1 prete")


if __name__ == "__main__":
    main()
