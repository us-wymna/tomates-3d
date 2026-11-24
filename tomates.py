"""Tomates 3D modulaires - modele parametrique (build123d 0.13).

Modules : corps creux (10 aimants) + tige a baionnette (3 aimants)
         + arbre en segments (2 aimants par branche).
Aimants : disques neodyme N52, 6.00 mm de diametre x 2.00 mm (+/-0.1).
Toutes les dimensions sont en mm. L'axe Z est vertical, Z=0 = plateau.
"""

import math
import os

from build123d import *

# ---------------- Parametres ----------------
MAG_D = 6.0
MAG_T = 2.0
POCKET_D = 6.35            # diametre des logements (jeu 0.35)
POCKET_CLEAR = 0.25        # jeu en profondeur

BODY_R = 16.5              # rayon max du fruit (~33 mm de large, x2 du modele)
BODY_ZC = 16.0
BODY_A = 17.0
WALL = 3.2                 # epaisseur de paroi du corps
NECK_R = 9.5               # rayon exterieur du col
BORE_R = 7.2               # rayon de l'alesage du col
NECK_TOP = 34.0
N_MAG_BODY = 10

PLUG_R = 6.9
FLANGE_R = 10.0
LUG_R_OUT = 8.5            # bout des ergots (saillie 1.6 depuis le plot)
LUG_W = 3.0
LUG_H = 3.0
SLOT_W = 3.4
SLOT_H = 3.4
SLOT_R_IN = 7.2
SLOT_R_OUT = 8.8
SLOT_Z0 = 27.0
SLOT_Z1 = 30.4
SLOT_ARC = 75.0            # rainure plus large que l'ergot (22 deg) pour le verrouillage a 60 deg

CUP_R = 5.0

OUT_DIR = os.path.expanduser("~/workspace/tomates3d/out")
os.makedirs(OUT_DIR, exist_ok=True)


def ellipse_r(z):
    v = 1.0 - ((z - BODY_ZC) / BODY_A) ** 2
    return BODY_R * math.sqrt(max(0.0, v))


def build_slot_sector():
    """Secteur courbe de la rainure baionnette (angles 0..60 deg)."""
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with Locations(
                Location(((SLOT_R_IN + SLOT_R_OUT) / 2, (SLOT_Z0 + SLOT_Z1) / 2, 0))
            ):
                Rectangle(SLOT_R_OUT - SLOT_R_IN, SLOT_Z1 - SLOT_Z0)
        revolve(revolution_arc=SLOT_ARC)
    return bp.part


def build_body():
    zs = list(range(0, 31, 2))
    outer_pts = [(ellipse_r(z), float(z)) for z in zs]
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Spline(*outer_pts)
                Line(outer_pts[-1], (NECK_R, 29.0))
                Line((NECK_R, 29.0), (NECK_R, NECK_TOP))
                Line((NECK_R, NECK_TOP), (0.0, NECK_TOP))
                Line((0.0, NECK_TOP), (0.0, 0.0))
                Line((0.0, 0.0), outer_pts[0])
            make_face()
        revolve(revolution_arc=360)
    outer = bp.part

    # Cavite interieure : paroi 3.2, puis cone vers l'alesage du col (r 7.2 des z=25).
    inner_pts = [(ellipse_r(z) - WALL, float(z)) for z in range(2, 21, 2)]
    with BuildPart() as bp2:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Spline(*inner_pts)
                Line(inner_pts[-1], (BORE_R, 25.0))
                Line((BORE_R, 25.0), (BORE_R, NECK_TOP + 0.5))
                Line((BORE_R, NECK_TOP + 0.5), (0.0, NECK_TOP + 0.5))
                Line((0.0, NECK_TOP + 0.5), (0.0, WALL))
                Line((0.0, WALL), inner_pts[0])
            make_face()
        revolve(revolution_arc=360)
    body = outer - bp2.part

    # 10 logements d'aimants, radiaux, a l'equateur (z=16), fond a 0.9 mm de la surface.
    for k in range(N_MAG_BODY):
        adeg = 36.0 * k
        a = math.radians(adeg)
        cx, cy = 11.8 * math.cos(a), 11.8 * math.sin(a)
        pocket = (
            Pos(cx, cy, 16.0)
            * Rot(0, 0, adeg)
            * Rot(0, 90, 0)
            * Cylinder(POCKET_D / 2, 7.6)
        )
        body = body - pocket

    # Rainures baionnette : 2 secteurs courbes + 2 entrees verticales (ouvertes au bord).
    sector = build_slot_sector()
    body = body - sector
    body = body - (Rot(0, 0, 180) * sector)
    for sx in (8.0, -8.0):
        entry = Pos(sx, 0, 30.55) * Box(1.6, SLOT_W, 7.5)
        body = body - entry
    return body


def build_leaf():
    pts = [(2.5, 11.5), (14.5, 8.8), (15.5, 9.6), (3.5, 13.0)]
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*pts, close=True)
            make_face()
        extrude(amount=1.6, both=True)
    return bp.part


def build_stem():
    plug = Pos(0, 0, 4.5) * Cylinder(PLUG_R, 9.0)
    lug1 = Pos(7.7, 0, 3.5) * Box(LUG_R_OUT - PLUG_R, LUG_W, LUG_H)
    lug2 = Pos(-7.7, 0, 3.5) * Box(LUG_R_OUT - PLUG_R, LUG_W, LUG_H)
    flange = Pos(0, 0, 10.0) * Cylinder(FLANGE_R, 2.0)
    stem_cyl = Pos(0, 0, 14.0) * Cylinder(3.5, 6.0)
    cup = Pos(0, 0, 21.0) * Cylinder(CUP_R, 8.0)
    leaf = build_leaf()
    leaves = leaf
    for k in range(1, 6):
        leaves = leaves + (Rot(0, 0, 60 * k) * leaf)
    stem = plug + lug1 + lug2 + flange + stem_cyl + cup + leaves
    # Logement des 3 aimants de la tige (empiles), ouvert en haut.
    pocket = Pos(0, 0, 21.95) * Cylinder(POCKET_D / 2, 6.5)
    return stem - pocket


def build_base():
    base = Pos(0, 0, 4) * Cylinder(60, 8) + Pos(0, 0, 10) * Cylinder(14, 4)
    sock = Pos(0, 0, 7) * Cylinder(9.5, 10)
    return base - sock


def build_trunk():
    seg = Pos(0, 0, 36) * Cylinder(8.5, 72) + Pos(0, 0, -4) * Cylinder(7.2, 8)
    seg = seg - Pos(0, 0, 68) * Cylinder(7.5, 8)
    for adeg in (0.0, 180.0):
        a = math.radians(adeg)
        hole = (
            Pos(4 * math.cos(a), 4 * math.sin(a), 60)
            * Rot(0, 0, adeg)
            * Rot(0, 90, 0)
            * Cylinder(6.0, 12)
        )
        seg = seg - hole
    return seg


def build_branch():
    arm = Pos(30, 0, 0) * Rot(0, 90, 0) * Cylinder(5.5, 60)
    plug = Pos(-6, 0, 0) * Rot(0, 90, 0) * Cylinder(5.7, 12)
    neck = Pos(60, 0, -2.5) * Cylinder(5.0, 5.0)
    pad = Pos(60, 0, -7.5) * Cylinder(9.0, 5.0)
    br = arm + plug + neck + pad
    # Logement des 2 aimants de la branche (empiles), ouvert vers le bas.
    pocket = Pos(60, 0, -7.85) * Cylinder(POCKET_D / 2, 4.3)
    return br - pocket


def check(name, part):
    bb = part.bounding_box()
    print(
        f"{name}: valid={part.is_valid} vol={part.volume:.1f} mm3 "
        f"bbox=({bb.min.X:.1f},{bb.min.Y:.1f},{bb.min.Z:.1f}).."
        f"({bb.max.X:.1f},{bb.max.Y:.1f},{bb.max.Z:.1f})"
    )
    return part


def main():
    body = check("corps", build_body())
    stem = check("tige", build_stem())
    base = check("arbre-base", build_base())
    trunk = check("arbre-tronc", build_trunk())
    branch = check("arbre-branche", build_branch())

    # Assemblage : la tige inseree dans le corps, 3 positions de rotation.
    for label, rot in (("entree", 0), ("mi-course", 30), ("verrouillee", 60)):
        placed = Pos(0, 0, 25) * Rot(0, 0, rot) * stem
        inter = body & placed
        print(f"assemblage {label}: intersection={inter.volume:.3f} mm3")
        assert inter.volume < 2.0, f"collision en position {label}"

    # Dimensions des logements vs aimants.
    assert abs(POCKET_D - MAG_D) >= 0.3
    print(
        f"logements: corps profondeur 2.3 (aimant {MAG_T}), "
        f"tige {3 * MAG_T + 0.3}, branche {2 * MAG_T + 0.3}"
    )

    export_stl(body, os.path.join(OUT_DIR, "tomate-corps.stl"))
    export_stl(stem, os.path.join(OUT_DIR, "tomate-tige.stl"))
    export_stl(base, os.path.join(OUT_DIR, "arbre-base.stl"))
    export_stl(trunk, os.path.join(OUT_DIR, "arbre-tronc-segment.stl"))
    export_stl(branch, os.path.join(OUT_DIR, "arbre-branche.stl"))
    print("STL ecrits dans", OUT_DIR)


if __name__ == "__main__":
    main()
