"""SwapCell concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

The pack is shown seated in the wall dock, connector end down. Axes: X across the pack
width, Y out of the wall (the wall is at +Y), Z up. Dimensions in mm.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

# Geometry comes from the parametric model (cad/src/model.py), so the media match the STEP files.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import PARAMS, build_parts

PACK_W, PACK_D, PACK_L = PARAMS["pack_w"], PARAMS["pack_d"], PARAMS["pack_l"]
Z0 = PARAMS["z0"]
PLATE_Y0 = PACK_D / 2 + PARAMS["plate_gap"]
parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]

# Context for scale: the wall behind the dock and a hand holding the carry handle
wall = Pos(0, PLATE_Y0 + 12 + 10, 150) * Box(320.0, 20.0, 700.0)
top = Z0 + PACK_L + 35
hand = (Pos(0, 8, top - 2) * Box(96.0, 44.0, 26.0)                        # fingers wrapped over the grip
        + Pos(0, -6, top + 36) * Rot(20, 0, 0) * Box(92.0, 34.0, 70.0)   # palm and back of hand
        + Pos(0, -40, top + 150) * Rot(20, 0, 0) * Cylinder(32.0, 170.0))  # wrist and forearm
context = [Part("Wall and adult hand", wall + hand, "#C8CDD3")]

render_all(
    parts, project="SwapCell", title="Pack and wall dock concept", dwg_no="SWC-DWG-001", date="2026-10-01",
    key_figures=["13S2P 21700: 46.8 V nominal, 10 Ah, about 468 Wh",
                 "Pack body 340 x 90 x 80 mm, about 3.0 kg (SWC-CAL-001)",
                 "20 A continuous, 35 A peak for 10 s",
                 "Interface v0.3: 2 power + 6 signal, CAN 250 kbit/s",
                 "Dock 5 A: about 2.3 h full charge (estimate)"],
    scale_figure=False, context=context, cut_exclude=("Pack lid and wake button",),
    flow={"title": "energy per full cycle, grid or solar to wheel (estimates)", "unit": "Wh (est.)",
          "stages": [("Grid or solar in", 547), ("Dock charger out", 493), ("Stored in pack", 468),
                     ("Pack output", 457), ("At the wheel", 366)],
          "losses": [(1, "Charger", 54), (2, "Cell charge", 25),
                     (3, "Pack resistance", 11), (4, "Motor and controller", 91)]},
)
