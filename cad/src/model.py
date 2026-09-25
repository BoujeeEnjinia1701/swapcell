"""SwapCell parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Massing-plus detail: correct interface features and main dimensions of the pack
(SwapCell interface v0.3) and the wall dock; not fabrication detail.

Axes: X across the pack width, Y out of the wall (the wall is at +Y, the pack back
face and latch face +Y), Z up along the insertion axis. The pack is shown docked,
connector end down. Dimensions in mm.
"""
from pathlib import Path

from build123d import Box, Compound, Cylinder, Pos, Rot, export_step, export_stl

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Interface envelope (SWC-PRC-001 v0.3, R6)
    "pack_w": 90.0, "pack_d": 80.0, "pack_l": 340.0,
    "tray_t": 1.5,            # folded aluminium tray wall
    "lid_t": 3.0,             # printed lid on the front (-Y) face
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0,
    "plug_offset_y": 8.0,     # connector toward the back face from the depth centre line
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0, "grip_clear": 25.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    "guide_clear": 1.0,       # receiver guide clearance per side
    "wake_d": 12.0,           # manual wake button on the lid (interface v0.3)
    # Cells (13S2P 21700)
    "cell_d": 21.0, "cell_l": 70.0, "cell_pitch": 22.0, "series": 13, "parallel": 2,
    # BMS board
    "bms_t": 10.0, "bms_h": 58.0, "bms_l": 230.0,
    # Dock
    "z0": 60.0,               # underside of the docked pack above the dock datum
    "plate_w": 150.0, "plate_t": 12.0, "plate_h": 520.0, "plate_gap": 10.0,
    "shelf_w": 120.0, "shelf_d": 110.0, "shelf_h": 45.0,
    "guide_t": 12.0, "guide_d": 60.0, "guide_h": 180.0,
    "charger_w": 150.0, "charger_d": 64.0, "charger_h": 110.0,
}


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    W, D, L, t = p["pack_w"], p["pack_d"], p["pack_l"], p["tray_t"]
    z0 = p["z0"]; zc = z0 + L / 2
    lid_t = p["lid_t"]

    # Cell block: axes along X, 13 groups along Z, 2 deep in Y
    cx = -W / 2 + t + 2.5 + p["cell_l"] / 2
    ys = (21.0, -1.0)
    cells = None
    for iz in range(p["series"]):
        for y in ys[: p["parallel"]]:
            c = Pos(cx, y, zc + (iz - (p["series"] - 1) / 2) * p["cell_pitch"]) * Rot(0, 90, 0) * \
                Cylinder(p["cell_d"] / 2, p["cell_l"])
            cells = c if cells is None else cells + c

    # Folded tray, open to the front (-Y); lid closes the front face
    tray_d = D - lid_t
    tray = Pos(0, lid_t / 2, zc) * Box(W, tray_d, L)
    pocket = Pos(0, lid_t / 2 - t / 2 - 1, zc) * Box(W - 2 * t, tray_d - t + 2, L - 2 * t)
    housing = tray - pocket
    lid = Pos(0, -D / 2 + lid_t / 2, zc) * Box(W, lid_t, L)
    # Flush manual wake button: shown as a ring groove in the lid face (no protrusion past the envelope)
    wz = z0 + L - 70
    lid -= Pos(0, -D / 2 + 0.75, wz) * Rot(90, 0, 0) * (Cylinder(p["wake_d"] / 2 + 1.0, 1.5) - Cylinder(p["wake_d"] / 2, 1.5))

    bms = Pos(W / 2 - t - 1 - p["bms_t"] / 2, 7, zc) * Box(p["bms_t"], p["bms_h"], p["bms_l"])

    # Pack-side plug: keyed shroud with 2 power and 6 signal contact bores
    py = p["plug_offset_y"]
    plug = Pos(0, py, z0 - p["plug_h"] / 2) * Box(p["plug_w"], p["plug_d"], p["plug_h"])
    plug -= Pos(p["plug_w"] / 2 - 4, py + p["plug_d"] / 2 - 4, z0 - p["plug_h"] / 2) * Box(10, 10, p["plug_h"] + 1)  # key
    for x in (-15.0, 15.0):
        plug -= Pos(x, py - 5, z0 - p["plug_h"] + 6) * Cylinder(4.5, 12.0)
    for i in range(6):
        plug -= Pos(-17.5 + 7 * i, py + 9, z0 - p["plug_h"] + 5) * Cylinder(1.5, 10.0)

    # Handle over the top end, clear of the latch
    hz = z0 + L + p["handle_h"] / 2
    handle = Pos(0, py, hz) * (Box(p["handle_w"], p["handle_d"], p["handle_h"])
                               - Pos(0, 0, -(p["handle_h"] - p["grip_clear"]) / 2 - 1)
                               * Box(p["handle_w"] - 22, p["handle_d"] + 8, p["grip_clear"] + 1))
    latch = Pos(0, D / 2 + p["latch_proud"] / 2, z0 + L - p["latch_from_top"]) * \
        Box(p["latch_w"], p["latch_proud"], p["latch_h"])

    # Wall dock
    plate_y0 = D / 2 + p["plate_gap"]
    plate = Pos(0, plate_y0 + p["plate_t"] / 2, 110) * Box(p["plate_w"], p["plate_t"], p["plate_h"])
    shelf = Pos(0, -5, z0 - 22.5) * Box(p["shelf_w"], p["shelf_d"], p["shelf_h"]) \
        - Pos(0, py, z0 - 8) * Box(p["plug_w"] + 4, p["plug_d"] + 4, 20.0)
    gx = W / 2 + p["guide_clear"] + p["guide_t"] / 2
    guides = (Pos(-gx, 10, z0 + 90) * Box(p["guide_t"], p["guide_d"], p["guide_h"])
              + Pos(gx, 10, z0 + 90) * Box(p["guide_t"], p["guide_d"], p["guide_h"]))
    catch = Pos(0, plate_y0 - 4, z0 + L - p["latch_from_top"] - 20) * Box(50.0, 8.0, 12.0)
    cradle = plate + shelf + guides + catch
    receptacle = Pos(0, py, z0 - 24) * Box(p["plug_w"] + 2, p["plug_d"] + 2, 12.0)
    charger = Pos(0, plate_y0 - p["charger_d"] / 2, -85) * Box(p["charger_w"], p["charger_d"], p["charger_h"])
    controller = Pos(85, 15, 25) * Box(50.0, 50.0, 30.0)

    ex = 300.0
    return [
        ("Pack housing tray", housing, "#6B7280", 1, (0, 0, ex)),
        ("Cell block, 13S2P 21700", cells, "#C2410C", 2, (-280, 0, ex + 60)),
        ("BMS board with CAN", bms, "#0F766E", 3, (170, -40, ex + 40)),
        ("Pack lid and wake button", lid, "#D1D5DB", 4, (-60, -200, ex - 170)),
        ("Blind-mate plug, pack side", plug, "#D4A017", 5, (150, -60, ex - 40)),
        ("Carry handle", handle, "#111827", 6, (0, 0, ex + 70)),
        ("Latch pawl", latch, "#B45309", 7, (0, 40, ex)),
        ("Wall dock cradle", cradle, "#9CA3AF", 8, (0, 0, 0)),
        ("Blind-mate receptacle, dock side", receptacle, "#D4A017", 9, (0, 0, 60)),
        ("Dock charger, 54.6 V 5 A", charger, "#374151", 10, (0, -120, 0)),
        ("Dock controller (ESP32, CAN)", controller, "#0F766E", 11, (120, 0, 0)),
    ]


PACK_ITEMS = {1, 2, 3, 4, 5, 6, 7}


def assemblies(parts=None):
    parts = parts or build_parts()
    pack = Compound([s for _, s, _, b, _ in parts if b in PACK_ITEMS])
    dock = Compound([s for _, s, _, b, _ in parts if b not in PACK_ITEMS])
    return pack, dock, Compound([s for _, s, _, _, _ in parts])


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    pack, dock, asm = assemblies(parts)
    for name, shape in (("swapcell-pack", pack), ("swapcell-dock", dock), ("swapcell-assembly", asm)):
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:20s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    body = Compound([s for n, s, _, b, _ in parts if b in (1, 4)]).bounding_box()
    print(f"pack body (tray + lid, incl. wake button) {body.size.X:.1f} x {body.size.Y:.1f} x {body.size.Z:.1f} mm")
