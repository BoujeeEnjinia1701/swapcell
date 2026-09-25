"""SwapCell concept massing model and media (TRL 2).

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

# Pack body envelope (SWC-PRC-001, interface section)
PACK_W, PACK_D, PACK_L = 90.0, 80.0, 340.0   # X, Y, Z
WALL = 3.0
Z0 = 60.0                                    # underside of the pack body when docked
ZC = Z0 + PACK_L / 2
LID_T = 3.0

# Cell block: 13S2P, 21700 cells (21 x 70 mm) with their axes along X, 13 along Z, 2 deep in Y
CELL_D, CELL_L, PITCH = 21.0, 70.0, 22.0
CELL_X = -PACK_W / 2 + WALL + 1 + CELL_L / 2          # cells sit against the -X wall
cells = None
for iz in range(13):
    for y in (21.0, -1.0):
        c = Pos(CELL_X, y, ZC + (iz - 6) * PITCH) * Rot(0, 90, 0) * Cylinder(CELL_D / 2, CELL_L)
        cells = c if cells is None else cells + c

# Housing tray open to the front (-Y); lid closes the front face
tray_depth = PACK_D - LID_T
tray = Pos(0, LID_T / 2, ZC) * Box(PACK_W, tray_depth, PACK_L)
pocket = Pos(0, LID_T / 2 - WALL / 2 - 1, ZC) * Box(PACK_W - 2 * WALL, tray_depth - WALL + 2, PACK_L - 2 * WALL)
housing = tray - pocket
lid = Pos(0, -PACK_D / 2 + LID_T / 2, ZC) * Box(PACK_W, LID_T, PACK_L)

# BMS board stands in the YZ plane beside the cells (thickness along X)
bms = Pos(PACK_W / 2 - WALL - 6, 7, ZC) * Box(10.0, 58.0, 230.0)

# Pack-side blind-mate plug under the body; carry handle on top; latch pawl on the back face
plug = Pos(0, 8, Z0 - 9) * Box(56.0, 34.0, 18.0)
handle = Pos(0, 8, Z0 + PACK_L + 17.5) * (Box(84.0, 22.0, 35.0) - Pos(0, 0, -6) * Box(62.0, 30.0, 25.0))
latch = Pos(0, PACK_D / 2 + 5, Z0 + PACK_L - 45) * Box(36.0, 10.0, 24.0)

# Wall dock: back plate, cradle shelf with connector pocket, side guides, catch, charger, controller
PLATE_Y0 = PACK_D / 2 + 10                   # front face of the back plate
plate = Pos(0, PLATE_Y0 + 6, 110) * Box(150.0, 12.0, 520.0)
shelf = Pos(0, -5, 37.5) * Box(120.0, 110.0, 45.0) - Pos(0, 8, 52) * Box(60.0, 38.0, 20.0)
guides = (Pos(-PACK_W / 2 - 6, 10, 150) * Box(12.0, 60.0, 180.0)) + (Pos(PACK_W / 2 + 6, 10, 150) * Box(12.0, 60.0, 180.0))
cradle = plate + shelf + guides + Pos(0, PLATE_Y0 - 4, Z0 + PACK_L - 65) * Box(50.0, 8.0, 12.0)
receptacle = Pos(0, 8, 36) * Box(58.0, 36.0, 12.0)
charger = Pos(0, PLATE_Y0 - 32, -85) * Box(150.0, 64.0, 110.0)
controller = Pos(85, 15, 25) * Box(50.0, 50.0, 30.0)

EX = 300.0   # pack lifted out of the dock in the exploded view
parts = [
    Part("Pack housing tray", housing, "#6B7280", 1, (0, 0, EX)),
    Part("Cell block, 13S2P 21700", cells, "#C2410C", 2, (-280, 0, EX + 60)),
    Part("BMS board with CAN", bms, "#0F766E", 3, (170, -40, EX + 40)),
    Part("Pack lid", lid, "#D1D5DB", 4, (-60, -200, EX - 170)),
    Part("Blind-mate plug, pack side", plug, "#D4A017", 5, (150, -60, EX - 40)),
    Part("Carry handle", handle, "#111827", 6, (0, 0, EX + 70)),
    Part("Latch pawl", latch, "#B45309", 7, (0, 40, EX)),
    Part("Wall dock cradle", cradle, "#9CA3AF", 8),
    Part("Blind-mate receptacle, dock side", receptacle, "#D4A017", 9, (0, 0, 60)),
    Part("Dock charger, 54.6 V 5 A", charger, "#374151", 10, (0, -120, 0)),
    Part("Dock controller (ESP32, CAN)", controller, "#0F766E", 11, (120, 0, 0)),
]

# Context for scale: the wall behind the dock and a hand holding the carry handle
wall = Pos(0, PLATE_Y0 + 12 + 10, 150) * Box(320.0, 20.0, 700.0)
top = Z0 + PACK_L + 35
hand = (Pos(0, 8, top - 2) * Box(96.0, 44.0, 26.0)                        # fingers wrapped over the grip
        + Pos(0, -6, top + 36) * Rot(20, 0, 0) * Box(92.0, 34.0, 70.0)   # palm and back of hand
        + Pos(0, -40, top + 150) * Rot(20, 0, 0) * Cylinder(32.0, 170.0))  # wrist and forearm
context = [Part("Wall and adult hand", wall + hand, "#C8CDD3")]

render_all(
    parts, project="SwapCell", title="Pack and wall dock concept", dwg_no="SWC-DWG-001",
    key_figures=["13S2P 21700: 46.8 V nominal, 10 Ah, about 470 Wh",
                 "Pack body 340 x 90 x 80 mm, about 2.8 kg (estimate)",
                 "20 A continuous, 35 A peak for 10 s",
                 "Blind-mate: 2 power + 6 signal, CAN 250 kbit/s",
                 "Dock 5 A: about 2.3 h full charge (estimate)"],
    scale_figure=False, context=context, cut_exclude=("Pack lid",),
    flow={"title": "energy per full cycle, grid or solar to wheel (estimates)", "unit": "Wh (est.)",
          "stages": [("Grid or solar in", 550), ("Dock charger out", 495), ("Stored in pack", 468),
                     ("Pack output", 454), ("At the wheel", 363)],
          "losses": [(1, "Charger", 55), (2, "Cell charge", 27),
                     (3, "Pack resistance", 14), (4, "Motor and controller", 91)]},
)
