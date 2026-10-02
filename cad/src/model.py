"""SwapCell parametric model (build123d), TRL 3, constructable design (SWC-DDR-003).

Run from the repo root:  python cad/src/model.py          exports STEP and STL, prints the checks
                         python cad/src/model.py --check  prints the constructability checks only

Every component is modelled as it is made or bought, with its fixings, so that the build plan
pictures (cad/src/build_plan_media.py) and the drawings come from one source. Interface v0.3
dimensions are parameters. Not fabrication detail: no tolerances before TRL 4.

Axes: X across the pack width, Y out of the wall (the wall is at +Y; the pack back face and
latch face +Y, the lid -Y), Z up along the insertion axis. The pack is shown docked,
connector end down. Dimensions in mm.
"""
import sys
from collections import namedtuple
from pathlib import Path

from build123d import Box, Compound, Cylinder, Pos, Rot, export_step, export_stl

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Interface envelope (SWC-PRC-001 v0.3, R6)
    "pack_w": 90.0, "pack_d": 80.0, "pack_l": 340.0,
    "tray_t": 1.5,            # folded aluminium tray wall
    "lid_t": 3.0,             # flame-retardant lid on the front (-Y) face
    "gasket_t": 1.0,          # flat gasket between the lid and the tray flanges, compressed
    "flange_w": 8.0,          # inward flange round the open front of the tray (DDR-003 P2)
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0,
    "plug_offset_y": 8.0,     # connector toward the back face from the depth centre line
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0, "grip_clear": 25.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 6.0, "latch_h": 24.0,
    "latch_travel": 5.0,      # pawl retracts this far when the thumb button is pressed (DDR-003 P4)
    "guide_clear": 1.0,       # receiver guide clearance per side
    "wake_d": 12.0,           # manual wake button on the lid (interface v0.3)
    # Cells (13S2P 21700)
    "cell_d": 21.0, "cell_l": 70.0, "cell_pitch": 22.0, "series": 13, "parallel": 2,
    "cell_rows_y": (13.0, -9.0),   # moved 8 mm toward the lid to make room for the latch (DDR-003 P4)
    "holder_t": 6.0,          # printed cell holder frames, one at each end of the cells
    # BMS board
    "bms_t": 10.0, "bms_h": 58.0, "bms_l": 230.0,
    # Dock
    "z0": 60.0,               # underside of the docked pack above the dock datum
    "plate_w": 150.0, "plate_t": 12.0, "plate_h": 580.0, "plate_gap": 10.0,
    "plate_z": (-170.0, 410.0),    # back plate bottom and top edge
    "shelf_w": 120.0, "shelf_d": 110.0, "shelf_h": 45.0,
    "guide_t": 12.0, "guide_d": 70.0, "guide_h": 180.0, "guide_lead": 10.0,
    "catch": (50.0, 8.0, 12.0),    # steel catch: width, reach from the plate, height
    "charger_w": 150.0, "charger_d": 64.0, "charger_h": 110.0,
    "float": 3.0,             # receptacle float each way in its cavity (R10)
}

Comp = namedtuple("Comp", "name shape bom kind group")
COLOURS = {1: "#6B7280", 2: "#C2410C", 3: "#0F766E", 4: "#D1D5DB", 5: "#D4A017", 6: "#111827",
           7: "#B45309", 8: "#9CA3AF", 9: "#D4A017", 10: "#374151", 11: "#0F766E"}


def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def xcyl(x0, x1, y, z, r):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def ycyl(x, y0, y1, z, r):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def zcyl(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def derived(p=PARAMS):
    W, D, L, t = p["pack_w"], p["pack_d"], p["pack_l"], p["tray_t"]
    z0 = p["z0"]
    d = dict(W=W, D=D, L=L, t=t, z0=z0, ztop=z0 + L, zc=z0 + L / 2,
             yback=D / 2, yfront=-D / 2,
             ytray_f=-D / 2 + p["lid_t"] + p["gasket_t"],   # open front edge of the tray
             zlatch=z0 + L - p["latch_from_top"],             # pawl centre height
             yplate=D / 2 + p["plate_gap"],                   # front face of the dock back plate
             wake_z=z0 + L - 70.0)
    d["xin"] = W / 2 - t
    d["yin_b"] = D / 2 - t
    hw = p["latch_w"] / 2
    d["pawl_x"] = hw
    d["hous_x"] = hw + 2.0            # housing outside half-width: pawl, 0.5 gap, 1.5 wall
    d["hous_y0"] = 26.0               # housing front wall outside face
    d["hous_z0"] = d["zlatch"] - p["latch_h"] / 2 - 1.5
    d["catch_z"] = (d["zlatch"] + p["latch_h"] / 2 + 1.0, d["zlatch"] + p["latch_h"] / 2 + 1.0 + p["catch"][2])
    return d


# ------------------------------------------------------------------ pack hole positions (x, z or y)
LID_SCREWS_Z = (90.0, 185.0, 275.0, 370.0)
PLUG_SCREWS = ((-25.0, -5.0), (25.0, -5.0), (-25.0, 21.0), (9.0, 22.0))   # (x, y) on the connector face
HOLDER_SCREWS_Z = (120.0, 300.0)
BMS_POS = ((-18.0, 140.0), (32.0, 140.0), (-18.0, 320.0), (32.0, 320.0))  # (y, z) on the right side wall
HANDLE_X = 36.5
RIVETS_Z = (350.0, 370.0, 390.0)
# dock
SHELF_SCREWS = ((-45.0, 25.0), (45.0, 25.0), (-45.0, 50.0), (45.0, 50.0))   # (x, z) through the plate
GUIDE_SCREWS_Z = (100.0, 200.0)
WALL_HOLES = ((-30.0, -160.0), (30.0, -160.0), (-62.0, 398.0), (62.0, 398.0))
RET_SCREWS = ((-40.0, -21.0), (40.0, -21.0), (-40.0, 37.0), (40.0, 37.0))  # (x, y) under the shelf
STRAP_X = 62.0


def build_components(p=PARAMS):
    """Every component as a Comp(name, shape, bom, kind, group), keyed by a short name.
    kind is 'made', 'bought' or 'fixing'; group is the BOM-level part it belongs to."""
    D = derived(p)
    W, Dp, L, t = D["W"], D["D"], D["L"], D["t"]
    z0, zt, zc = D["z0"], D["ztop"], D["zc"]
    yb, yf = D["yback"], D["ytray_f"]
    xin, yinb = D["xin"], D["yin_b"]
    fw = p["flange_w"]
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    # ---------------- 1 tray: back, two sides, two ends folded from one blank, inward front flanges
    outer = bx(-W / 2, W / 2, yf, yb, z0, zt)
    inner = bx(-xin, xin, yf - 1, yinb, z0 + t, zt - t)
    tray = outer - inner
    tray += bx(-xin, -xin + fw, yf, yf + t, z0 + t, zt - t) + bx(xin - fw, xin, yf, yf + t, z0 + t, zt - t)
    tray += bx(-xin + fw, xin - fw, yf, yf + t, z0 + t, z0 + t + fw) + bx(-xin + fw, xin - fw, yf, yf + t, zt - t - fw, zt - t)
    zl = D["zlatch"]; lh = p["latch_h"]; hw = D["pawl_x"]
    tray -= bx(-hw - 0.5, hw + 0.5, yinb - 1, yb + 1, zl - lh / 2 - 0.5, zl + lh / 2 + 0.5)       # pawl slot
    for sx in (-1, 1):
        for z in RIVETS_Z:
            tray -= ycyl(sx * (D["hous_x"] + 5.0), yinb - 1, yb + 1, z, 2.05)
    for x in (25.0, -37.0):
        for z in HOLDER_SCREWS_Z:
            tray -= ycyl(x, yinb - 1, yb + 1, z, 1.35)
    tray -= bx(-15.5, 15.5, yinb - p["latch_travel"] - 0.5, yinb, zt - t - 1, zt + 1)           # release slider slot
    for sx in (-1, 1):
        tray -= zcyl(sx * HANDLE_X, p["plug_offset_y"], zt - t - 1, zt + 1, 2.75)
    tray -= bx(-21.0, 21.0, -3.0, 19.0, z0 - 1, z0 + t + 1)                                   # plug lead opening
    for x, y in PLUG_SCREWS:
        tray -= zcyl(x, y, z0 - 1, z0 + t + 1, 1.7)
    for y, z in BMS_POS:
        tray -= xcyl(xin - 1, W / 2 + 1, y, z, 1.35)
    for sx in (-1, 1):
        for z in LID_SCREWS_Z:
            tray -= ycyl(sx * (xin - fw / 2), yf - 1, yf + t + 1, z, 2.1)
    add("tray", "Pack tray", tray, 1, "made", "tray")
    pn = fuse([ycyl(sx * (xin - fw / 2), yf + t, yf + t + 3.0, z, 3.0) - ycyl(sx * (xin - fw / 2), yf + t - 1, yf + t + 4, z, 1.5)
               for sx in (-1, 1) for z in LID_SCREWS_Z])
    add("pnuts", "M3 press-in nuts (8)", pn, 13, "fixing", "tray")

    # ---------------- 2 cells and holder frames
    cx0, cx1 = -41.0, -41.0 + p["cell_l"]
    cells = []
    zs = [zc + (iz - (p["series"] - 1) / 2) * p["cell_pitch"] for iz in range(p["series"])]
    for z in zs:
        for y in p["cell_rows_y"][: p["parallel"]]:
            cells.append(xcyl(cx0, cx1, y, z, p["cell_d"] / 2))
    add("cells", "Cells, 13S2P 21700", fuse(cells), 2, "bought", "cells")
    ht = p["holder_t"]
    hz0, hz1 = zs[0] - 18.0, zs[-1] + 18.0
    hy0 = min(p["cell_rows_y"]) - p["cell_d"] / 2 - 1.5
    holders = {}
    for key, x0 in (("holder_l", cx0 + 1.0), ("holder_r", cx1 - 1.0 - ht)):
        h = bx(x0, x0 + ht, hy0, yinb, hz0, hz1)
        for z in zs:
            for y in p["cell_rows_y"]:
                h -= xcyl(x0 - 1, x0 + ht + 1, y, z, p["cell_d"] / 2)
        for z in HOLDER_SCREWS_Z:
            h -= ycyl(x0 + ht / 2, yinb - 10.0, yinb + 1, z, 1.3)
        if key == "holder_r":
            h -= bx(x0 - 1, x0 + ht + 1, 32.0, yinb + 1, D["hous_z0"] - 6.0, hz1 + 1)          # notch for the latch housing
        holders[key] = h
    add("holder_l", "Cell holder frame, left", holders["holder_l"], 16, "made", "cells")
    add("holder_r", "Cell holder frame, right", holders["holder_r"], 16, "made", "cells")

    # ---------------- 3 BMS on four short standoffs on the right side wall
    bx0 = xin - 2.0 - p["bms_t"]
    bms = bx(bx0, bx0 + p["bms_t"], -22.0, 36.0, 115.0, 345.0)
    add("bms", "BMS board with CAN", bms, 3, "bought", "bms")
    so = fuse([xcyl(bx0 + p["bms_t"], xin, y, z, 2.5) for y, z in BMS_POS])
    add("bms_so", "BMS standoffs (4)", so, 13, "fixing", "bms")

    # ---------------- 4 lid, gasket and wake button
    ylf = D["yfront"]
    lid = bx(-W / 2, W / 2, ylf, ylf + p["lid_t"], z0, zt)
    wz = D["wake_z"]
    lid -= ycyl(0, ylf - 1, ylf + p["lid_t"] + 1, wz, p["wake_d"] / 2 + 0.5)
    for sx in (-1, 1):
        for z in LID_SCREWS_Z:
            lid -= ycyl(sx * (xin - fw / 2), ylf - 1, ylf + p["lid_t"] + 1, z, 1.7)
            lid -= ycyl(sx * (xin - fw / 2), ylf - 1, ylf + 1.65, z, 2.8)          # countersink, heads flush
    add("lid", "Pack lid", lid, 4, "made", "lid")
    gy0 = ylf + p["lid_t"]
    gk = bx(-W / 2 + 0.5, W / 2 - 0.5, gy0, gy0 + p["gasket_t"], z0 + 0.5, zt - 0.5) - \
        bx(-xin + fw, xin - fw, gy0 - 1, gy0 + p["gasket_t"] + 1, z0 + t + fw, zt - t - fw)
    for sx in (-1, 1):
        for z in LID_SCREWS_Z:
            gk -= ycyl(sx * (xin - fw / 2), gy0 - 1, gy0 + 2, z, 2.0)
    add("gasket", "Lid gasket", gk, 13, "bought", "lid")
    wake = ycyl(0, ylf, ylf + p["lid_t"], wz, p["wake_d"] / 2) + ycyl(0, ylf + p["lid_t"], ylf + p["lid_t"] + 3, wz, 9.0) + \
        ycyl(0, ylf + p["lid_t"] + 3, ylf + p["lid_t"] + 15, wz, 7.5)
    add("wake", "Wake button (sealed switch)", wake, 14, "bought", "lid")
    ls = fuse([ycyl(sx * (xin - fw / 2), ylf, ylf + 1.65, z, 2.75) + ycyl(sx * (xin - fw / 2), ylf + 1.65, yf + t + 3.0, z, 1.5)
               for sx in (-1, 1) for z in LID_SCREWS_Z])
    add("lid_screws", "M3 lid screws (8)", ls, 13, "fixing", "lid")

    # ---------------- 5 plug: printed keyed shroud, contacts through it, four M3 screws from inside
    py = p["plug_offset_y"]
    pw, pd, ph = p["plug_w"], p["plug_d"], p["plug_h"]
    plug = bx(-pw / 2, pw / 2, py - pd / 2, py + pd / 2, z0 - ph, z0)
    plug -= bx(pw / 2 - 8, pw / 2 + 1, py + pd / 2 - 8, py + pd / 2 + 1, z0 - ph - 1, z0 + 1)          # key notch
    for x in (-15.0, 15.0):
        plug -= zcyl(x, py - 5, z0 - ph - 1, z0 + 1, 4.5)
    for i in range(6):
        plug -= zcyl(-17.5 + 7 * i, py + 9, z0 - ph - 1, z0 + 1, 1.5)
    for x, y in PLUG_SCREWS:
        plug -= zcyl(x, y, z0 - 9, z0 + 1, 2.0)
    add("plug", "Plug shroud with contacts", plug, 5, "made", "plug")
    pc = fuse([zcyl(x, py - 5, z0 - ph + 4, z0 + 6, 4.0) - zcyl(x, py - 5, z0 - ph + 3, z0 + 7, 3.2) for x in (-15.0, 15.0)] +
              [zcyl(-17.5 + 7 * i, py + 9, z0 - ph + 4, z0 + 4, 1.4) - zcyl(-17.5 + 7 * i, py + 9, z0 - ph + 3, z0 + 5, 1.15) for i in range(6)])
    add("plug_contacts", "Plug contacts (2 power, 6 signal)", pc, 5, "bought", "plug")
    ps = fuse([zcyl(x, y, z0 - 8, z0 + t, 1.5) + zcyl(x, y, z0 + t, z0 + t + 1.8, 2.75) for x, y in PLUG_SCREWS])
    add("plug_screws", "M3 plug screws (4)", ps, 13, "fixing", "plug")

    # ---------------- 6 carry handle, two M5 screws from inside the tray
    hh, hd, hwid, gc = p["handle_h"], p["handle_d"], p["handle_w"], p["grip_clear"]
    handle = bx(-hwid / 2, hwid / 2, py - hd / 2, py + hd / 2, zt, zt + hh) - \
        bx(-hwid / 2 + 11, hwid / 2 - 11, py - hd / 2 - 1, py + hd / 2 + 1, zt - 1, zt + gc)
    for sx in (-1, 1):
        handle -= zcyl(sx * HANDLE_X, py, zt - 1, zt + 12, 2.5)
    add("handle", "Carry handle", handle, 6, "made", "handle")
    hs = fuse([zcyl(sx * HANDLE_X, py, zt - t - 3.0, zt - t, 4.25) + zcyl(sx * HANDLE_X, py, zt - t, zt + 10, 2.5) for sx in (-1, 1)])
    add("handle_screws", "M5 handle screws (2)", hs, 13, "fixing", "handle")

    # ---------------- 7 latch: pawl, housing (the doubler), release slider and thumb button
    # The pawl slides in and out through a slot in the back wall. Above the slot it has a shoulder
    # that rests on the inside of the back wall (the out stop); the shoulder's top back edge is a
    # 45 degree ramp. The release slider runs down the inside of the back wall; its ramped lower end
    # wedges between the wall and the shoulder, so pressing the thumb button 5 mm pulls the pawl in
    # 5 mm. Two springs in the pawl push it back out, which lifts the slider and button.
    pr, trv = p["latch_proud"], p["latch_travel"]
    pz0, pz1 = zl - lh / 2, zl + lh / 2
    py0 = yb + pr - 12.5                                   # pawl inside face with the pawl out
    sh_top = pz1 + 10.0                                    # top of the shoulder
    pawl = bx(-hw, hw, py0, yb + pr, pz0, pz1) + bx(-hw, hw, py0, yinb, pz1, sh_top)
    pawl -= Pos(0, yb + pr, pz0) * Rot(45, 0, 0) * Box(2 * hw + 2, 4 * 2 ** 0.5, 4 * 2 ** 0.5)                    # lead-in under the tooth
    pawl -= Pos(0, yinb, sh_top) * Rot(45, 0, 0) * Box(2 * hw + 2, trv * 2 ** 0.5, trv * 2 ** 0.5)       # release ramp
    for x in (-10.0, 10.0):
        pawl -= ycyl(x, py0 - 1, py0 + 8.0, zl, 3.0)                                                 # spring bores
    add("pawl", "Latch pawl", pawl, 7, "made", "latch")
    hx, hy0, hz0 = D["hous_x"], D["hous_y0"], D["hous_z0"]
    hzt = zt - t
    hous = bx(-hx, hx, hy0, yinb, hz0, hzt) - bx(-hx + 1.5, hx - 1.5, hy0 + 1.5, yinb + 1, hz0 + 1.5, hzt + 1)
    for sx in (-1, 1):
        fl = bx(min(sx * hx, sx * (hx + 10)), max(sx * hx, sx * (hx + 10)), yinb - 1.5, yinb, hz0, hzt)
        for z in RIVETS_Z:
            fl -= ycyl(sx * (hx + 5.0), yinb - 2, yinb + 1, z, 2.05)
        hous += fl
    add("housing", "Latch housing", hous, 15, "made", "latch")
    sl = bx(-17.0, 17.0, yinb - trv, yinb, sh_top - trv, zt - t - 1.0) + bx(-15.0, 15.0, yinb - trv, yinb, zt - t - 1.0, zt + 8.0)
    sl -= Pos(0, yinb - trv, sh_top - trv) * Rot(45, 0, 0) * Box(36.0, trv * 2 ** 0.5, trv * 2 ** 0.5)          # ramp, matches the shoulder
    add("slider", "Release slider", sl, 15, "made", "latch")
    thumb = bx(-15.0, 15.0, 22.0, 38.0, zt + 8.0, zt + 16.0)
    add("thumb", "Thumb button", thumb, 15, "made", "latch")
    springs = fuse([ycyl(x, hy0 + 1.5, py0 + 8.0, zl, 2.5) for x in (-10.0, 10.0)])
    add("springs", "Pawl springs (2)", springs, 15, "bought", "latch")
    rv = fuse([ycyl(sx * (hx + 5.0), yinb - 1.5, yb, z, 2.0) + ycyl(sx * (hx + 5.0), yinb - 3.5, yinb - 1.5, z, 2.75)
               for sx in (-1, 1) for z in RIVETS_Z])
    add("rivets", "4 mm countersunk blind rivets (6)", rv, 13, "fixing", "latch")
    hsc = fuse([ycyl(x, 30.0, yb, z, 1.25) for x in (25.0, -37.0) for z in HOLDER_SCREWS_Z])
    add("holder_screws", "M2.5 holder screws (4)", hsc, 13, "fixing", "cells")

    # ---------------- dock
    yp = D["yplate"]
    pz_lo, pz_hi = p["plate_z"]
    plate = bx(-p["plate_w"] / 2, p["plate_w"] / 2, yp, yp + p["plate_t"], pz_lo, pz_hi)
    for x, z in WALL_HOLES:
        plate -= ycyl(x, yp - 1, yp + p["plate_t"] + 1, z, 3.25)
    for x, z in SHELF_SCREWS:
        plate -= ycyl(x, yp - 1, yp + p["plate_t"] + 1, z, 2.75)
    gx = W / 2 + p["guide_clear"] + p["guide_t"] / 2
    for sx in (-1, 1):
        for z in GUIDE_SCREWS_Z:
            plate -= ycyl(sx * gx, yp - 1, yp + p["plate_t"] + 1, z, 2.75)
    for x in (-16.0, 16.0):
        plate -= ycyl(x, yp - 1, yp + p["plate_t"] + 1, sum(D["catch_z"]) / 2, 2.75)
    for sx in (-1, 1):
        for z in (-19.0, -151.0):
            plate -= ycyl(sx * STRAP_X, yp - 1, yp + 10.0, z, 2.1)          # M5 tapped, charger straps
        plate -= ycyl(sx * 15.0, yp - 1, yp + 10.0, -10.0, 1.65)             # M4 tapped, controller box
    add("plate", "Dock back plate", plate, 8, "made", "cradle")

    sw, sd, sh = p["shelf_w"], p["shelf_d"], p["shelf_h"]
    sz0 = z0 - sh
    shelf = bx(-sw / 2, sw / 2, yp - sd, yp, sz0, z0)
    shelf -= bx(-pw / 2 - 2, pw / 2 + 2, py - pd / 2 - 2, py + pd / 2 + 2, z0 - ph, z0 + 1)               # plug pocket
    fl_ = p["float"]
    rcx, rcy = pw / 2 + 5, pd / 2 + 5                                                                      # receptacle flange half sizes
    shelf -= bx(-rcx - fl_, rcx + fl_, py - rcy - fl_, py + rcy + fl_, sz0 - 1, z0 - ph)                    # receptacle cavity
    for x, z in SHELF_SCREWS:
        shelf -= ycyl(x, yp - 12, yp + 1, z, 2.0)
    for x, y in RET_SCREWS:
        shelf -= zcyl(x, y, sz0 - 1, sz0 + 8, 1.6)
    add("shelf", "Cradle shelf", shelf, 8, "made", "cradle")

    gl = p["guide_lead"]
    for key, sx in (("guide_l", -1), ("guide_r", 1)):
        g = bx(sx * gx - p["guide_t"] / 2, sx * gx + p["guide_t"] / 2, yp - p["guide_d"], yp, z0, z0 + p["guide_h"])
        g -= Pos(sx * (W / 2 + p["guide_clear"]), (2 * yp - p["guide_d"]) / 2, z0 + p["guide_h"]) * Rot(0, 45, 0) * \
            Box(gl * 1.414, p["guide_d"] + 2, gl * 1.414)
        for z in GUIDE_SCREWS_Z:
            g -= ycyl(sx * gx, yp - 12, yp + 1, z, 2.0)
        add(key, f"Side guide, {'left' if sx < 0 else 'right'}", g, 8, "made", "cradle")

    cw, cr, chh = p["catch"]
    cz = D["catch_z"]
    catch = bx(-cw / 2, cw / 2, yp - cr, yp, cz[0], cz[1])
    for x in (-16.0, 16.0):
        catch -= ycyl(x, yp - 7, yp + 1, (cz[0] + cz[1]) / 2, 2.1)
    add("catch", "Latch catch", catch, 8, "made", "cradle")

    # 9 receptacle: printed body with a top flange that the pocket ledge captures, key post, pins
    rz1 = z0 - ph
    rec = bx(-pw / 2 - 1, pw / 2 + 1, py - pd / 2 - 1, py + pd / 2 + 1, rz1 - 12.0, rz1) + \
        bx(-rcx, rcx, py - rcy, py + rcy, rz1 - 3.0, rz1)
    rec += bx(pw / 2 - 7.5, pw / 2 - 0.5, py + pd / 2 - 7.5, py + pd / 2 - 0.5, rz1, rz1 + ph - 2.0)          # key post
    for x in (-15.0, 15.0):
        rec -= zcyl(x, py - 5, rz1 - 13.0, rz1 + 1, 3.0)
    for i in range(6):
        rec -= zcyl(-17.5 + 7 * i, py + 9, rz1 - 13.0, rz1 + 1, 1.0)
    add("receptacle", "Receptacle shroud", rec, 9, "made", "receptacle")
    pins = fuse([zcyl(x, py - 5, rz1, rz1 + (11.0 if x < 0 else 10.0), 3.0) for x in (-15.0, 15.0)] +
                [zcyl(-17.5 + 7 * i, py + 9, rz1, rz1 + (5.0 if i == 5 else 8.0), 1.0) for i in range(6)])
    add("rec_pins", "Receptacle pins (2 power, 6 signal)", pins, 9, "bought", "receptacle")
    foam = bx(-rcx, rcx, py - rcy, py + rcy, sz0, rz1 - 12.0)
    add("foam", "Foam pad", foam, 17, "bought", "receptacle")
    ret = bx(-44.0, 44.0, -25.0, 41.0, sz0 - 3.0, sz0)
    ret -= zcyl(0, py, sz0 - 4, sz0 + 1, 8.0)
    for x, y in RET_SCREWS:
        ret -= zcyl(x, y, sz0 - 4, sz0 + 1, 2.2)
    add("retainer", "Receptacle retainer plate", ret, 17, "made", "receptacle")

    # 10 charger and its two straps; 11 controller box
    cy0 = yp - p["charger_d"]
    ch_top = -30.0
    charger = bx(-p["charger_w"] / 2, p["charger_w"] / 2, cy0, yp, ch_top - p["charger_h"], ch_top)
    add("charger", "Dock charger (certified, bought)", charger, 10, "bought", "charger")
    straps = None
    for sx in (-1, 1):
        x0, x1 = sx * STRAP_X - 10, sx * STRAP_X + 10
        s = bx(x0, x1, cy0 - 1.5, cy0, ch_top - p["charger_h"] - 1.5, ch_top + 1.5)
        s += bx(x0, x1, cy0 - 1.5, yp - 1.5, ch_top, ch_top + 1.5)
        s += bx(x0, x1, cy0 - 1.5, yp - 1.5, ch_top - p["charger_h"] - 1.5, ch_top - p["charger_h"])
        s += bx(x0, x1, yp - 1.5, yp, ch_top, ch_top + 20.0)
        s += bx(x0, x1, yp - 1.5, yp, ch_top - p["charger_h"] - 20.0, ch_top - p["charger_h"])
        for z in (ch_top + 11.0, ch_top - p["charger_h"] - 11.0):
            s -= ycyl(sx * STRAP_X, yp - 2, yp + 1, z, 2.75)
        straps = s if straps is None else straps + s
    add("straps", "Charger straps (2)", straps, 17, "made", "charger")
    ctrl = bx(-25.0, 25.0, yp - 50.0, yp, -25.0, 5.0)
    add("controller", "Dock controller box", ctrl, 11, "bought", "controller")

    # dock fixings: countersunk M5 screws from behind the plate (heads flush with its back face)
    yb2 = yp + p["plate_t"]
    df = [ycyl(x, yp - 10, yb2, z, 2.5) for x, z in SHELF_SCREWS]
    df += [ycyl(sx * gx, yp - 10, yb2, z, 2.5) for sx in (-1, 1) for z in GUIDE_SCREWS_Z]
    df += [ycyl(x, yp - 6, yb2, (cz[0] + cz[1]) / 2, 2.5) for x in (-16.0, 16.0)]
    df += [zcyl(x, y, sz0 - 5.0, sz0 + 6.0, 1.5) for x, y in RET_SCREWS]
    df += [ycyl(sx * STRAP_X, yp - 1.5, yp + 8.0, z, 2.0) + ycyl(sx * STRAP_X, yp - 4.5, yp - 1.5, z, 4.25)
           for sx in (-1, 1) for z in (-19.0, -151.0)]
    add("dock_screws", "Dock screws", fuse(df), 17, "fixing", "cradle")
    return C


# ------------------------------------------------------------------ legacy interface for the media
GROUPS = [  # (group, BOM item, label, explode offset)
    ("tray", 1, "Pack housing tray", (0, 0, 300)),
    ("cells", 2, "Cell block, 13S2P 21700", (-280, 0, 360)),
    ("bms", 3, "BMS board with CAN", (170, -40, 340)),
    ("lid", 4, "Pack lid and wake button", (-60, -200, 130)),
    ("plug", 5, "Blind-mate plug, pack side", (150, -60, 260)),
    ("handle", 6, "Carry handle", (0, 0, 370)),
    ("latch", 7, "Latch pawl and release", (0, 40, 300)),
    ("cradle", 8, "Wall dock cradle", (0, 0, 0)),
    ("receptacle", 9, "Blind-mate receptacle, dock side", (0, 0, 60)),
    ("charger", 10, "Dock charger, 54.6 V 5 A", (0, -120, 0)),
    ("controller", 11, "Dock controller (ESP32, CAN)", (120, -40, 0)),
]
PACK_ITEMS = {1, 2, 3, 4, 5, 6, 7}


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset), one per BOM-level group."""
    C = build_components(p)
    out = []
    for g, bom, label, ex in GROUPS:
        shapes = [c.shape for c in C.values() if c.group == g]
        out.append((label, Compound(shapes), COLOURS[bom], bom, ex))
    return out


def assemblies(parts=None):
    parts = parts or build_parts()
    pack = Compound([s for _, s, _, b, _ in parts if b in PACK_ITEMS])
    dock = Compound([s for _, s, _, b, _ in parts if b not in PACK_ITEMS])
    return pack, dock, Compound([s for _, s, _, _, _ in parts])


def wall_context(p=PARAMS):
    D = derived(p)
    y = D["yplate"] + p["plate_t"]
    return bx(-200, 200, y, y + 20, -260, 520)


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs of parts with what must hold between them: 'touch' (no overlap, gap 0) or a minimum
    clearance in mm. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    D = derived(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.1 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # pack
    chk("Cells clear of the tray", S("cells"), S("tray"), 1.5)
    chk("Cells clear of the latch housing", S("cells"), S("housing"), 1.5)
    chk("Cells clear of the BMS", S("cells"), S("bms"), 1.0)
    chk("Cells clear of the lid fixings", S("cells"), S("pnuts") + S("lid_screws"), 3.0)
    chk("Cells clear of the wake button", S("cells"), S("wake"), 1.5)
    chk("Cells clear of the handle and plug screws", S("cells"), S("handle_screws") + S("plug_screws"), 3.0)
    for k in ("holder_l", "holder_r"):
        chk(f"{C[k].name} on the cells", S(k), S("cells"), "touch")
        chk(f"{C[k].name} on the tray back wall", S(k), S("tray"), "touch")
        chk(f"{C[k].name} clear of the latch housing and rivets", S(k), S("housing") + S("rivets"), 0.4)
        chk(f"{C[k].name} clear of the BMS", S(k), S("bms"), 1.0)
        chk(f"{C[k].name} clear of the handle and plug screws", S(k), S("handle_screws") + S("plug_screws"), 1.0)
    chk("Holder screws in the holder frames", S("holder_screws"), S("holder_l") + S("holder_r"), "touch")
    chk("BMS on its standoffs", S("bms"), S("bms_so"), "touch")
    chk("BMS standoffs on the side wall", S("bms_so"), S("tray"), "touch")
    chk("BMS clear of the latch housing", S("bms"), S("housing"), 1.0)
    chk("Gasket on the tray flanges", S("gasket"), S("tray"), "touch")
    chk("Lid on the gasket", S("lid"), S("gasket"), "touch")
    chk("Lid clear of the tray (gasket between)", S("lid"), S("tray"), 0.9)
    chk("Press-in nuts in the flanges", S("pnuts"), S("tray"), "touch")
    chk("Wake button in the lid", S("wake"), S("lid"), "touch")
    chk("Plug on the connector face", S("plug"), S("tray"), "touch")
    chk("Handle on the top end", S("handle"), S("tray"), "touch")
    chk("Handle clear of the thumb button", S("handle"), S("thumb"), 2.0)
    chk("Latch housing on the back wall", S("housing"), S("tray"), "touch")
    chk("Pawl on the housing floor", S("pawl"), S("housing"), "touch")
    chk("Pawl shoulder on the back wall (out stop)", S("pawl"), S("tray"), "touch")
    chk("Release slider ramp on the pawl ramp", S("slider"), S("pawl"), "touch")
    chk("Release slider sliding on the back wall", S("slider"), S("tray"), "touch")
    chk("Release slider clear of the housing", S("slider"), S("housing"), 1.0)
    chk("Springs between the pawl and the housing", S("springs"), S("housing"), "touch")
    chk("Thumb button on the slider", S("thumb"), S("slider"), "touch")
    sbb = S("slider").bounding_box()
    rows.append(("Slider wider than its slot in the tray top (keeps it in)", 0.0, sbb.size.X - 31.0, 2.0, sbb.size.X - 31.0 >= 2.0))
    chk("Thumb button travel above the tray top", S("thumb"), S("tray"), p["latch_travel"] + 1.0)
    chk("Rivets through the housing flanges", S("rivets"), S("housing"), "touch")
    # dock
    chk("Shelf on the back plate", S("shelf"), S("plate"), "touch")
    for k in ("guide_l", "guide_r"):
        chk(f"{C[k].name} on the back plate", S(k), S("plate"), "touch")
        chk(f"{C[k].name} on the shelf", S(k), S("shelf"), "touch")
    chk("Catch on the back plate", S("catch"), S("plate"), "touch")
    chk("Receptacle captured under the pocket ledge", S("receptacle"), S("shelf"), "touch")
    chk("Receptacle on its foam pad", S("receptacle"), S("foam"), "touch")
    chk("Foam pad on the retainer", S("foam"), S("retainer"), "touch")
    chk("Retainer under the shelf", S("retainer"), S("shelf"), "touch")
    chk("Charger on the back plate", S("charger"), S("plate"), "touch")
    chk("Charger straps on the charger", S("straps"), S("charger"), "touch")
    chk("Charger straps on the back plate", S("straps"), S("plate"), "touch")
    chk("Controller box on the back plate", S("controller"), S("plate"), "touch")
    chk("Controller clear of the shelf retainer", S("controller"), S("retainer"), 3.0)
    chk("Controller clear of the charger and straps", S("controller"), S("charger") + S("straps"), 3.0)
    chk("Controller inside the plate width", S("controller"), bx(-200, -75, -200, 200, -400, 600) + bx(75, 200, -200, 200, -400, 600), 1.0)
    # pack in the dock
    pack_body = S("tray") + S("lid")
    chk("Pack seated on the shelf", pack_body, S("shelf"), "touch")
    chk("Plug in the pocket (2 mm each side)", S("plug"), S("shelf"), 1.9)
    chk("Plug face on the receptacle", S("plug"), S("receptacle"), "touch")
    chk("Receptacle pins inside the plug contacts", S("rec_pins"), S("plug_contacts"), 0.1)
    chk("Pack clear of the guides (1 mm each side)", pack_body, S("guide_l") + S("guide_r"), 0.9)
    chk("Pack clear of the back plate", pack_body, S("plate"), 9.0)
    chk("Pack clear of the catch", pack_body + S("rivets"), S("catch"), 1.5)
    chk("Pawl under the catch (1 mm)", S("pawl"), S("catch"), 0.9)
    chk("Pawl clear of the back plate", S("pawl"), S("plate"), 3.0)
    chk("Pack clear of the receptacle retainer", pack_body, S("retainer"), 10.0)
    # the pawl overlaps the catch in depth (it hooks under it) and clears it when retracted
    pr = p["latch_proud"]; cr = p["catch"][1]
    engage = pr - (p["plate_gap"] - cr)
    rows.append(("Pawl tooth under the catch, depth of engagement", 0.0, engage, 4.0, engage >= 4.0 - 1e-6))
    clear = (p["plate_gap"] - cr) - (pr - p["latch_travel"])
    rows.append(("Retracted pawl clear of the catch", 0.0, clear, 1.0, clear >= 1.0 - 1e-6))
    # envelope
    body = (S("tray") + S("lid") + S("gasket")).bounding_box()
    for ax, want in (("X", p["pack_w"]), ("Y", p["pack_d"]), ("Z", p["pack_l"])):
        got = getattr(body.size, ax)
        rows.append((f"Pack body {ax} within the envelope", 0.0, want - got, 0.0, -1e-6 <= want - got <= 1.5))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    pack, dock, asm = assemblies(parts)
    for name, shape in (("swapcell-pack", pack), ("swapcell-dock", dock), ("swapcell-assembly", asm)):
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name:20s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    C = build_components()
    body = (C["tray"].shape + C["lid"].shape + C["gasket"].shape).bounding_box()
    print(f"pack body (tray, gasket, lid) {body.size.X:.1f} x {body.size.Y:.1f} x {body.size.Z:.1f} mm")
    print_checks()
