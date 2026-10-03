"""SwapCell product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: folded aluminium tray with bend radii and rounded
ends, 3 mm polycarbonate sheet lid with a parting line and eight flush countersunk screws, flush wake button, state-of-charge light bar
behind a clear lens, interface label and rating label, carry handle with a ribbed rubber grip,
6 mm latch pawl and the thumb button behind the grip, keyed plug with visible contacts; wall dock
with a brushed 580 mm back plate, cradle shelf with a status light, lead-in guides, steel catch,
receptacle contacts, finned charger held by two straps, its mains cord and a controller box. A compact painted wall section gives the mounting.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, fixing position and interface comes from model.py (PARAMS, derived and the
hole tables), updated 2026-10-02 to the constructable design and interface v0.4. Axes as model.py: X across
the pack width, Y out of the wall (wall at +Y, front of the pack at -Y), Z up along the
insertion axis. For the renders the pack is shown part way through a swap: lifted INSERT_LIFT
above its seated position, still between the dock guides (model.py shows it seated).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build123d import (Align, Axis, Box, Cylinder, Plane, Pos, RectangleRounded, RegularPolygon, Rot,
                       Sphere, Text, extrude, fillet)
from model import (HOLDER_SCREWS_Z, LID_SCREWS_Z, PARAMS, RIVETS_Z, STRAP_X, WALL_HOLES,  # noqa: E402
                   build_components, derived)

TITLE = "SwapCell: swappable e-bike battery pack and wall charging dock"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); the pack is part way "
             "into the wall dock, lid with wake button and charge light facing the viewer, charger below"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): pack tray, lid, cell "
             "block, BMS board, handle, latch and plug above; dock plate, shelf, guides, receptacle, "
             "controller and charger below"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 22, "az": -32,
     "note": "Detail from the front right, slightly above (about 22 deg elevation): pack and dock without "
             "the wall; plug entering the guides above the dock receptacle, shelf status light lit"},
]

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Colours (restrained product palette; kit accent)
C_TRAY = "#4B5563"       # painted aluminium tray
C_LID = "#E5E7EB"
C_HANDLE = "#2B2F36"
C_GRIP = "#15181C"
C_ACCENT = "#0F766E"
C_LIGHT = "#2DD4BF"
C_LIGHT_OFF = "#3A4048"
C_WHITE = "#F3F4F6"
C_INK = "#1F2937"
C_LABEL = "#F4F4F2"
C_METAL = "#B8BEC6"
C_STEEL = "#8E959E"
C_CONTACT = "#C9A227"
C_SHROUD = "#1C1F24"
C_PLATE = "#C3C8CE"
C_DOCK = "#374151"
C_CHARGER = "#2B2F36"
C_BOX = "#E5E7EB"
C_CELL = "#C2410C"
C_NICKEL = "#D1D5DB"
C_PCB = "#166534"
C_CHIP = "#111827"
C_RED = "#B91C1C"
C_WALL = "#ECEAE6"

# Appearance-only sizes and pose (mm)
INSERT_LIFT = 110.0      # pack lifted above its seated position, still between the guides
R_BEND = 6.0             # tray bend radius on the four long edges
FIL_END = 3.0            # fillet on the tray and lid ends
GROOVE = 0.6             # parting-line groove width and depth


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _prism(w, d, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan (w along X, d along Y), from z0 up by h."""
    r = max(min(r, min(w, d) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(w, d, r), amount=h)


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _ends(s):
    f = s.faces().sort_by(Axis.Z)
    return list(f[0].edges()) + list(f[-1].edges())


def _cyl_y(x, y0, y1, z, r):
    """Cylinder along Y from y0 to y1."""
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, abs(y1 - y0))


def _cyl_x(x0, x1, y, z, r):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def _front_plane(x, y, z):
    """Plane on a -Y facing surface: text reads along +X, up is +Z, extrusion toward -Y."""
    return Plane(origin=(x, y, z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))


def _side_plane(x, y, z):
    """Plane on the +X facing surface: text reads along +Y, up is +Z, extrusion toward +X."""
    return Plane(origin=(x, y, z), x_dir=(0, 1, 0), z_dir=(1, 0, 0))


def _text(pl, txt, size, h):
    try:
        return extrude(pl * Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER)),
                       amount=h)
    except Exception:
        return None


def _screw_y(x, y_face, z, r=2.75, h=1.4):
    """Button-head screw on a -Y facing surface, with a hex socket."""
    head = _cyl_y(x, y_face - h, y_face, z, r)
    head = _fillet_try(head, head.faces().sort_by(Axis.Y)[0].edges(), [0.6, 0.4])
    head -= Pos(x, y_face - h - 0.2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(1.3, 6), amount=-1.0)
    return head


def product_parts(P=PARAMS):
    W, D, L, t, lid_t = P["pack_w"], P["pack_d"], P["pack_l"], P["tray_t"], P["lid_t"]
    z0 = P["z0"]
    zb = z0 + INSERT_LIFT            # pack underside (connector face) in the render pose
    zc = zb + L / 2
    zt = zb + L                      # pack top face
    py = P["plug_offset_y"]
    yf = -D / 2                      # lid front face
    yp = -D / 2 + lid_t              # lid and tray joint
    out = []

    def add(name, shape, color, material, bom, group, explode):
        if shape is None:
            return
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    EX = 360.0                        # pack lift in the exploded view

    # ================================================================ pack body
    outer = _prism(W, D, R_BEND, zb, L)
    outer = _fillet_try(outer, _ends(outer), [FIL_END, 2.0, 1.0])
    groove = _box(-W, W, yp - GROOVE / 2, yp + GROOVE / 2, zb - 5, zt + 5) - \
        _prism(W - 2 * GROOVE, D - 2 * GROOVE, R_BEND - GROOVE, zb + GROOVE, L - 2 * GROOVE)

    # ---- tray (BOM 1): open front, closed ends, bend radii
    tray = (outer & _box(-W, W, yp, D, zb - 5, zt + 5)) - _prism(W - 2 * t, D - 2 * t, R_BEND - t, zb + t, L - 2 * t)
    tray -= groove
    # latch window in the back face (the pawl sits in it) and handle bolt holes are hidden; not modelled
    add("Pack housing tray", tray, C_TRAY, "painted", 1, "shell", (0, 0, EX))

    # blind rivets for the latch doubler, both sides near the back edge
    lz = zt - P["latch_from_top"]
    MD = derived(P)
    dz_ = zb - P["z0"]                              # model.py heights to the render pose
    riv = None
    for sx in (-1, 1):
        for zr in RIVETS_Z:                         # six countersunk blind rivets, flush on the back face
            r = _cyl_y(sx * (MD["hous_x"] + 5.0), D / 2, D / 2 + 0.3, zr + dz_, 3.4)
            riv = r if riv is None else riv + r
    for x in (25.0, -37.0):                         # holder frame screws, countersunk from outside
        for zr in HOLDER_SCREWS_Z:
            riv += _cyl_y(x, D / 2, D / 2 + 0.3, zr + dz_, 2.4)
    add("Latch doubler rivets", riv, C_METAL, "metal", 13, "shell", (0, 0, EX))

    # rating label on the +X side, with printed lines
    lzc = zc - 40.0
    sp = _side_plane(W / 2, 0.0, lzc)
    lab = extrude(sp * RectangleRounded(60.0, 96.0, 3.0), amount=0.25)
    add("Rating label", lab, C_LABEL, "paper", 14, "shell", (0, 0, EX))
    band = extrude(_side_plane(W / 2 + 0.25, 0.0, lzc + 39.0) * RectangleRounded(60.0, 18.0, 3.0), amount=0.1)
    band -= _box(W / 2, W / 2 + 1, -31, 31, lzc + 30.0 - 9.0, lzc + 30.5)
    add("Rating label band", band, C_ACCENT, "paper", 14, "shell", (0, 0, EX))
    ink = _text(_side_plane(W / 2 + 0.35, 0.0, lzc + 39.5), "SWAPCELL", 7.0, 0.12)
    add("Rating label wordmark", ink, C_WHITE, "paper", 14, "shell", (0, 0, EX))
    lines = [("46.8 V  10 Ah  468 Wh", 4.2, 18.0), ("Li-ion 13S2P  21700", 4.2, 9.0),
             ("Interface v0.4", 4.2, 0.0), ("CAN 250 kbit/s", 4.2, -9.0)]
    tl = None
    for txt, size, dz in lines:
        tt = _text(_side_plane(W / 2 + 0.25, 0.0, lzc + dz), txt, size, 0.12)
        if tt is not None:
            tl = tt if tl is None else tl + tt
    bars = None
    for k, dz in enumerate((-24.0, -30.0, -36.0)):
        b = _box(W / 2 + 0.25, W / 2 + 0.37, -24.0, 24.0 - 10 * k, lzc + dz - 1.0, lzc + dz + 1.0)
        bars = b if bars is None else bars + b
    tl = bars if tl is None else tl + bars
    add("Rating label print", tl, C_INK, "paper", 14, "shell", (0, 0, EX))

    # ---- lid (BOM 4): plate with rounded ends, parting groove, wake button hole, charge window
    lid = (outer & _box(-W, W, yf - 1, yp, zb - 5, zt + 5)) - groove
    wz = zt - 70.0                               # wake button height, as model.py
    lid -= _cyl_y(0, yf - 1, yp + 1, wz, P["wake_d"] / 2 + 0.6)
    sz = wz - 22.0                               # charge light window
    win = Pos(0, yf - 1, sz) * extrude(Plane.XZ * RectangleRounded(44.0, 7.0, 3.0), amount=-(lid_t + 2))
    lid -= win
    # eight M3 countersunk screws into press-in nuts in the tray flanges, as model.py
    xs_ = MD["xin"] - P["flange_w"] / 2
    screw_xz = [(sx * xs_, zr + dz_) for sx in (-1, 1) for zr in LID_SCREWS_Z]
    for x, z in screw_xz:
        lid -= _cyl_y(x, yf - 1, yf + 0.3, z, 2.9)
    add("Pack lid (polycarbonate sheet)", lid, C_LID, "plastic", 4, "shell", (0, -170, EX))

    scr = None
    for x, z in screw_xz:
        s = _cyl_y(x, yf + 0.05, yf + 0.3, z, 2.75)                     # flush countersunk head
        s -= Pos(x, yf - 0.2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(1.3, 6), amount=-0.4)
        scr = s if scr is None else scr + s
    add("Lid screws (M3)", scr, C_STEEL, "metal", 13, "shell", (0, -200, EX))

    # interface label panel and wordmark (BOM 14), low on the lid
    pz = zb + 72.0
    panel = extrude(_front_plane(0, yf, pz) * RectangleRounded(62.0, 34.0, 3.0), amount=0.4)
    add("Interface label", panel, C_ACCENT, "painted", 14, "shell", (0, -178, EX))
    mark = _text(_front_plane(0, yf - 0.4, pz + 6.0), "SWAPCELL", 8.0, 0.2)
    sub = _text(_front_plane(0, yf - 0.4, pz - 7.0), "48 V  IF v0.4", 5.0, 0.2)
    if mark is not None and sub is not None:
        mark = mark + sub
    add("Interface label print", mark, C_WHITE, "painted", 14, "shell", (0, -178, EX))

    # wake button: flush sealed cap with a retaining flange behind the lid, and a ring mark
    btn = _cyl_y(0, yf + 0.3, yp, wz, P["wake_d"] / 2)
    btn = _fillet_try(btn, btn.faces().sort_by(Axis.Y)[0].edges(), [0.8, 0.5])
    btn += _cyl_y(0, yp, yp + 1.2, wz, P["wake_d"] / 2 + 2.5)
    add("Wake button", btn, C_ACCENT, "plastic", 14, "shell", (0, -195, EX))
    ring = _cyl_y(0, yf - 0.15, yf, wz, P["wake_d"] / 2 + 3.2) - _cyl_y(0, yf - 1, yf + 1, wz, P["wake_d"] / 2 + 2.2)
    add("Wake button ring mark", ring, C_ACCENT, "painted", 14, "shell", (0, -170, EX))

    # charge light: clear lens in the window, five segments behind (four lit), dark carrier
    lens = Pos(0, yf + 0.2, sz) * extrude(Plane.XZ * RectangleRounded(43.6, 6.6, 2.9), amount=-1.2)
    add("Charge light lens", lens, "#DCEBF5", "clear", 14, "shell", (0, -185, EX))
    lit, dark = None, None
    for i in range(5):
        seg = _box(-20.0 + 8.4 * i, -20.0 + 8.4 * i + 6.8, yf + 1.5, yf + 2.3, sz - 2.2, sz + 2.2)
        if i < 4:
            lit = seg if lit is None else lit + seg
        else:
            dark = seg
    add("Charge light segments (lit)", lit, C_LIGHT, "emissive", 3, "shell", (0, -175, EX))
    add("Charge light segment (off)", dark, C_LIGHT_OFF, "plastic", 3, "shell", (0, -175, EX))
    carrier = _box(-25.0, 25.0, yp, yp + 1.5, sz - 6.0, sz + 6.0)
    add("Charge light carrier", carrier, C_SHROUD, "plastic", 3, "internal", (0, -175, EX))

    # ================================================================ pack internals
    # cells (BOM 2): 13S2P 21700 with axes along X, as model.py
    cx = -41.0 + P["cell_l"] / 2                 # as model.py
    cl, cr = P["cell_l"], P["cell_d"] / 2
    ys = tuple(P["cell_rows_y"])[: P["parallel"]]
    zs = [zc + (iz - (P["series"] - 1) / 2) * P["cell_pitch"] for iz in range(P["series"])]
    wrap, caps = None, None
    for z in zs:
        for y in ys:
            w_ = _cyl_x(cx - cl / 2 + 0.8, cx + cl / 2 - 0.8, y, z, cr)
            wrap = w_ if wrap is None else wrap + w_
            for xe in (cx - cl / 2 + 0.4, cx + cl / 2 - 0.4):
                c_ = _cyl_x(xe - 0.4, xe + 0.4, y, z, cr - 0.8)
                caps = c_ if caps is None else caps + c_
    ex_cells = (-270, -40, EX + 20)
    add("Cells, 13S2P 21700 (wraps)", wrap, C_CELL, "painted", 2, "internal", ex_cells)
    add("Cells, end caps", caps, C_METAL, "metal", 2, "internal", ex_cells)

    # cell holders at both ends and nickel strips (BOM 12)
    hold = None
    for xh in (cx - cl / 2 + 4.0, cx + cl / 2 - 4.0):
        h_ = _box(xh - 3.0, xh + 3.0, min(ys) - cr - 1.5, MD["yin_b"], zs[0] - 18.0, zs[-1] + 18.0)
        for z in zs:
            for y in ys:
                h_ -= _cyl_x(xh - 4, xh + 4, y, z, cr + 0.2)
        h_ = _fillet_try(h_, h_.edges().filter_by(Axis.X), [1.0, 0.5])
        hold = h_ if hold is None else hold + h_
    add("Cell holders", hold, C_SHROUD, "plastic", 12, "internal", ex_cells)
    strips = None
    for xe in (cx - cl / 2 - 0.35, cx + cl / 2 + 0.35):
        for z in zs:
            s_ = _box(xe - 0.3, xe + 0.3, min(ys) - 4.0, max(ys) + 4.0, z - 4.0, z + 4.0)
            strips = s_ if strips is None else strips + s_
    add("Nickel strips", strips, C_NICKEL, "metal", 12, "internal", ex_cells)
    # battery board temperature sensor on the middle cell of the rear row (decision of 2026-10-02)
    ts = build_components(P)["tsense"].shape
    add("Board temperature sensor", Pos(0, 0, dz_) * ts, C_SHROUD, "rubber", 12, "internal", ex_cells)

    # BMS board (BOM 3): board on its long edge beside the cells, components toward +X
    bx0 = MD["xin"] - 2.0 - P["bms_t"]           # envelope from model.py
    bh, bl = P["bms_h"], P["bms_l"]
    pcb = _box(bx0, bx0 + 1.6, 7 - bh / 2, 7 + bh / 2, zc - bl / 2, zc + bl / 2)
    pcb = _fillet_try(pcb, pcb.edges().filter_by(Axis.X), [2.0, 1.0])
    ex_bms = (170, -40, EX + 40)
    add("BMS board", pcb, C_PCB, "plastic", 3, "internal", ex_bms)
    xs = bx0 + 1.6
    comps = None
    for i in range(6):                           # FET row
        c_ = _box(xs, xs + 2.4, -18.0, -10.0, zc - 90 + 14 * i, zc - 80 + 14 * i)
        comps = c_ if comps is None else comps + c_
    for i in range(13):                          # balance resistors
        comps += _box(xs, xs + 1.0, 18.0, 26.0, zc - 104 + 16 * i, zc - 100 + 16 * i)
    comps += _box(xs, xs + 2.0, -4.0, 8.0, zc + 20, zc + 34)       # MCU
    comps += _box(xs, xs + 1.6, -4.0, 4.0, zc + 45, zc + 53)       # CAN transceiver
    comps += _box(xs, xs + 1.6, 10.0, 18.0, zc - 20, zc - 12)      # flash
    add("BMS components", comps, C_CHIP, "plastic", 3, "internal", ex_bms)
    sink = _box(xs + 2.4, xs + 6.4, -20.0, -8.0, zc - 94, zc - 2)
    for i in range(7):
        sink -= _box(xs + 4.0, xs + 7.0, -21.0, -7.0, zc - 90 + 12 * i, zc - 87 + 12 * i)
    add("BMS FET heatsink", sink, C_METAL, "metal", 3, "internal", ex_bms)
    conn = _box(xs, xs + 6.0, -2.0, 16.0, zc + 80, zc + 92)
    add("BMS CAN and balance connectors", conn, C_WHITE, "plastic", 3, "internal", ex_bms)
    caps_e = _cyl_x(xs, xs + 7.0, 26.0, zc + 70, 3.0) + _cyl_x(xs, xs + 7.0, 26.0, zc + 80, 3.0)
    add("BMS capacitors", caps_e, "#1E293B", "metal", 3, "internal", ex_bms)
    fuse = _box(xs, xs + 5.0, 14.0, 30.0, zc - 70, zc - 60)
    add("Main fuse, 40 A", fuse, C_RED, "plastic", 12, "internal", ex_bms)

    # pack power leads (BOM 12) from the cell block down to the plug
    zbot = zs[0] - cr
    lead_p = Pos(15.0, py - 5, (zb + zbot) / 2) * Cylinder(2.8, zbot - zb - 1.0)
    lead_n = Pos(-15.0, py - 5, (zb + zbot) / 2) * Cylinder(2.8, zbot - zb - 1.0)
    add("Pack power lead (+)", lead_p, C_RED, "rubber", 12, "internal", (0, 0, EX))
    add("Pack power lead (-)", lead_n, C_SHROUD, "rubber", 12, "internal", (0, 0, EX))

    # ================================================================ plug, handle, latch
    # plug (BOM 5): keyed shroud, 2 power and 6 signal bores, as model.py, with contacts
    ph, pw, pdp = P["plug_h"], P["plug_w"], P["plug_d"]
    plug = _prism(pw, pdp, 3.0, zb - ph, ph, y=py)
    plug = _fillet_try(plug, plug.faces().sort_by(Axis.Z)[0].edges(), [1.2, 0.8])
    plug -= Pos(pw / 2 - 4, py + pdp / 2 - 4, zb - ph / 2) * Box(10, 10, ph + 1)
    for x in (-15.0, 15.0):
        plug -= Pos(x, py - 5, zb - ph + 6) * Cylinder(4.5, 12.0)
    for i in range(6):
        plug -= Pos(-17.5 + 7 * i, py + 9, zb - ph + 5) * Cylinder(1.5, 10.0)
    ex_plug = (0, 0, EX - 90)
    add("Blind-mate plug shroud", plug, C_SHROUD, "plastic", 5, "shell", ex_plug)
    pins = None
    for x in (-15.0, 15.0):
        c_ = Pos(x, py - 5, zb - 13.5) * Cylinder(2.6, 3.0)
        c_ = (c_ - Pos(x, py - 5, zb - 15.0) * Cylinder(1.6, 1.2))
        pins = c_ if pins is None else pins + c_
    for i in range(6):
        pins += Pos(-17.5 + 7 * i, py + 9, zb - 11.0) * Cylinder(0.8, 6.0)
    add("Plug contacts", pins, C_CONTACT, "metal", 5, "shell", ex_plug)

    # carry handle (BOM 6): model.py loop, rounded, with a ribbed rubber grip on the bar
    hw, hd, hh, gc = P["handle_w"], P["handle_d"], P["handle_h"], P["grip_clear"]
    hz = zt + hh / 2
    handle = Pos(0, py, hz) * Box(hw, hd, hh)
    handle = _fillet_try(handle, handle.edges().filter_by(Axis.Y), [6.0, 4.0, 2.0])
    handle -= Pos(0, py, hz - (hh - gc) / 2 - 1) * Box(hw - 22, hd + 8, gc + 1)
    handle = _fillet_try(handle, handle.faces().sort_by(Axis.Y)[0].edges() + handle.faces().sort_by(Axis.Y)[-1].edges(),
                         [1.5, 1.0, 0.5])
    ex_h = (0, 0, EX + 110)
    add("Carry handle", handle, C_HANDLE, "plastic", 6, "shell", ex_h)
    bar_z0 = hz - (hh - gc) / 2 - 1 + (gc + 1) / 2          # underside of the grip bar
    gl = hw - 22 - 8
    grip = Pos(0, py, (bar_z0 + hz + hh / 2) / 2 + 0.0) * Box(gl, hd + 2.4, (hz + hh / 2 - bar_z0) + 2.4)
    grip = _fillet_try(grip, grip.edges().filter_by(Axis.X), [4.0, 3.0, 1.5])
    grip -= Pos(0, py, (bar_z0 + hz + hh / 2) / 2) * Box(gl + 2, hd, hz + hh / 2 - bar_z0)
    for i in range(9):
        x = -gl / 2 + 5.0 + i * (gl - 10.0) / 8
        grip -= Pos(x, py, hz + hh / 2 + 1.2) * Box(1.4, hd + 6, 1.4)
    add("Handle grip (TPE)", grip, C_GRIP, "rubber", 6, "shell", ex_h)

    # latch pawl (BOM 7) on the back face, and the thumb release behind the handle
    latch = Pos(0, D / 2 + P["latch_proud"] / 2, lz) * Box(P["latch_w"], P["latch_proud"], P["latch_h"])
    latch = _fillet_try(latch, latch.edges().filter_by(Axis.Y), [2.0, 1.0])
    latch -= Pos(0, D / 2 + P["latch_proud"], lz + P["latch_h"] / 2) * Rot(45, 0, 0) * Box(P["latch_w"] + 2, 5.0, 5.0)
    ex_l = (120, 40, EX + 60)
    add("Latch pawl", latch, C_STEEL, "metal", 7, "shell", ex_l)
    # thumb button on the release slider, behind the grip, as model.py (inside the v0.4 handle zone)
    rel = _box(-15.0, 15.0, 22.0, 38.0, zt + 8.0, zt + 16.0)
    rel = _fillet_try(rel, rel.edges().filter_by(Axis.Z) + rel.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.2, 0.6])
    for i in range(4):
        rel -= Pos(-6.0 + 4 * i, 30.0, zt + 16.0) * Box(1.2, 18.0, 1.2)
    rel += _box(-15.0, 15.0, MD["yin_b"] - P["latch_travel"], MD["yin_b"], zt - 0.5, zt + 8.0)      # slider top
    add("Latch thumb release", rel, C_ACCENT, "plastic", 7, "shell", ex_l)

    # ================================================================ wall dock
    plate_y0 = D / 2 + P["plate_gap"]
    pt, ph_, pw_ = P["plate_t"], P["plate_h"], P["plate_w"]
    pz_lo, pz_hi = P["plate_z"]
    plate = Pos(0, plate_y0 + pt / 2, (pz_lo + pz_hi) / 2) * Box(pw_, pt, pz_hi - pz_lo)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [10.0, 6.0, 3.0])
    plate = _fillet_try(plate, plate.faces().sort_by(Axis.Y)[0].edges(), [2.0, 1.0])
    add("Dock back plate", plate, C_PLATE, "metal", 8, "shell", (0, 0, 0))
    wscr = None
    for x, z in WALL_HOLES:
        s = _screw_y(x, plate_y0, z, r=4.5, h=2.0)
        s += _cyl_y(x, plate_y0 - 0.8, plate_y0, z, 6.0)      # washer
        wscr = s if wscr is None else wscr + s
    add("Wall screws and washers", wscr, C_STEEL, "metal", 13, "shell", (0, -40, 0))

    # cradle shelf with the connector pocket, as model.py; status light on the front
    sw, sd, sh = P["shelf_w"], P["shelf_d"], P["shelf_h"]
    shelf = _prism(sw, sd, 8.0, z0 - sh, sh, y=-5)
    shelf = _fillet_try(shelf, shelf.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0, 1.0])
    shelf -= Pos(0, py, z0 - 8) * Box(P["plug_w"] + 4, P["plug_d"] + 4, 20.0)
    ys0 = -5 - sd / 2
    shelf -= _box(-22.0, 22.0, ys0 - 1, ys0 + 1.5, z0 - 26.0, z0 - 22.0)
    add("Dock cradle shelf", shelf, C_DOCK, "plastic", 8, "shell", (0, 0, 0))
    status = _box(-21.5, 21.5, ys0 + 0.3, ys0 + 1.5, z0 - 25.6, z0 - 22.4)
    add("Dock status light", status, C_LIGHT, "emissive", 11, "shell", (0, 0, 0))
    dmark = _text(_front_plane(0, ys0, z0 - 12.0), "SWAPCELL DOCK", 5.5, 0.2)
    add("Dock wordmark", dmark, C_WHITE, "painted", 8, "shell", (0, 0, 0))

    # side guides with lead-in chamfers
    gt, gd, gh = P["guide_t"], P["guide_d"], P["guide_h"]
    gx = W / 2 + P["guide_clear"] + gt / 2
    guides = None
    for sx in (-1, 1):
        gy = plate_y0 - gd / 2                    # back end on the plate, as model.py
        g = Pos(sx * gx, gy, z0 + gh / 2) * Box(gt, gd, gh)
        g = _fillet_try(g, g.edges().filter_by(Axis.Z), [3.0, 2.0])
        g -= Pos(sx * (gx - gt / 2), gy, z0 + gh) * Rot(0, 45, 0) * Box(P["guide_lead"] * 1.414, gd + 2, P["guide_lead"] * 1.414)
        g -= Pos(sx * (gx - gt / 2), gy - gd / 2, z0 + gh / 2) * Rot(0, 0, 45) * Box(5.0, 5.0, gh + 2)
        guides = g if guides is None else guides + g
    add("Dock side guides", guides, C_DOCK, "plastic", 8, "shell", (0, 0, 0))

    # latch catch on the plate (steel), as model.py
    cw_, cr_, ch_ = P["catch"]
    catch = Pos(0, plate_y0 - cr_ / 2, sum(MD["catch_z"]) / 2) * Box(cw_, cr_, ch_)
    catch = _fillet_try(catch, catch.edges().filter_by(Axis.Y), [2.0, 1.0])
    add("Dock latch catch", catch, C_STEEL, "metal", 8, "shell", (0, -30, 0))

    # receptacle (BOM 9), with its mating contacts standing in the pocket
    rec = Pos(0, py, z0 - 24) * Box(P["plug_w"] + 2, P["plug_d"] + 2, 12.0)
    ex_r = (0, -170, 60)
    add("Blind-mate receptacle, dock side", rec, C_SHROUD, "plastic", 9, "shell", ex_r)
    rpins = None
    for x in (-15.0, 15.0):
        c_ = Pos(x, py - 5, z0 - 18 + 3.5) * Cylinder(1.5, 7.0)
        c_ = _fillet_try(c_, c_.faces().sort_by(Axis.Z)[-1].edges(), [0.6, 0.3])
        rpins = c_ if rpins is None else rpins + c_
    for i in range(6):
        rpins += Pos(-17.5 + 7 * i, py + 9, z0 - 18 + 2.5) * Cylinder(0.6, 5.0)
    add("Receptacle contacts", rpins, C_CONTACT, "metal", 9, "shell", ex_r)

    # charger (BOM 10): rounded enclosure with fins, status LED, mains cord
    cw, cd, chh = P["charger_w"], P["charger_d"], P["charger_h"]
    cy, cz = plate_y0 - cd / 2, -85.0
    chg = Pos(0, cy, cz) * Box(cw, cd, chh)
    chg = _fillet_try(chg, chg.edges().filter_by(Axis.Y), [8.0, 5.0, 3.0])
    chg = _fillet_try(chg, chg.faces().sort_by(Axis.Y)[0].edges(), [3.0, 2.0, 1.0])
    for i in range(11):
        x = -cw / 2 + 25.0 + i * (cw - 50.0) / 10
        chg -= Pos(x, cy - cd / 2, cz - 6.0) * Box(3.0, 5.0, chh - 36.0)
    chg -= Pos(cw / 2 - 16.0, cy - cd / 2, cz + chh / 2 - 12.0) * Rot(90, 0, 0) * Cylinder(2.6, 2.0)
    ex_c = (0, -170, -60)
    add("Dock charger, 54.6 V 5 A", chg, C_CHARGER, "painted", 10, "shell", ex_c)
    led = _cyl_y(cw / 2 - 16.0, cy - cd / 2 + 0.2, cy - cd / 2 + 1.2, cz + chh / 2 - 12.0, 2.4)
    add("Charger LED", led, "#22C55E", "emissive", 10, "shell", ex_c)
    straps = build_components(P)["straps"].shape                     # two folded straps, as model.py
    add("Charger straps", straps, C_METAL, "metal", 17, "shell", ex_c)
    clab = _text(_front_plane(-cw / 2 + 36.0, cy - cd / 2, cz + chh / 2 - 12.0), "54.6 V  5 A", 5.0, 0.2)
    add("Charger marking", clab, "#9CA3AF", "painted", 10, "shell", ex_c)
    # mains cord: gland on the underside, down and back to the wall
    cordx = 30.0                     # clear of the right strap
    gl_ = Pos(cordx, cy + 8.0, cz - chh / 2 - 4.0) * Cylinder(6.0, 8.0)
    gl_ = _fillet_try(gl_, gl_.faces().sort_by(Axis.Z)[0].edges(), [1.5, 1.0])
    drop = 26.0
    cord = Pos(cordx, cy + 8.0, cz - chh / 2 - 8.0 - drop / 2) * Cylinder(3.5, drop)
    cord += Pos(cordx, cy + 8.0, cz - chh / 2 - 8.0 - drop) * Sphere(3.5)
    ywall = plate_y0 + pt
    cord += Pos(cordx, (cy + 8.0 + ywall) / 2, cz - chh / 2 - 8.0 - drop) * Rot(90, 0, 0) * Cylinder(3.5, ywall - cy - 8.0)
    add("Charger cable gland", gl_, C_SHROUD, "plastic", 10, "shell", ex_c)
    add("Charger mains cord", cord, C_SHROUD, "rubber", 10, "context", (0, 0, 0))
    grom = _cyl_y(cordx, ywall - 2.0, ywall, cz - chh / 2 - 8.0 - drop, 7.0)
    grom = _fillet_try(grom, grom.faces().sort_by(Axis.Y)[0].edges(), [1.0, 0.5])
    add("Wall cord grommet", grom, C_BOX, "plastic", None, "context", (0, 0, 0))

    # dock controller (BOM 11): small enclosure with a parting line, LED and microSD slot
    # on the plate between the charger and the shelf, as model.py (50 x 50 x 30 box on two M4 screws)
    ky0 = plate_y0 - 50.0
    ctl = _box(-25.0, 25.0, ky0, plate_y0, -25.0, 5.0)
    ctl = _fillet_try(ctl, ctl.edges().filter_by(Axis.Y), [4.0, 2.0])
    ctl = _fillet_try(ctl, ctl.faces().sort_by(Axis.Y)[0].edges(), [2.0, 1.0])
    ctl -= _box(-8.0, 6.0, ky0 - 1.0, ky0 + 2.0, -22.0, -20.0)                       # microSD slot
    ex_k = (130, -60, 0)
    add("Dock controller enclosure", ctl, C_BOX, "plastic", 11, "shell", ex_k)
    kled = _cyl_y(15.0, ky0 - 0.3, ky0 + 1.0, -8.0, 1.8)
    add("Controller status LED", kled, C_LIGHT, "emissive", 11, "shell", ex_k)
    klab = _text(_front_plane(-6.0, ky0, -8.0), "CAN", 5.0, 0.2)
    add("Controller marking", klab, C_ACCENT, "painted", 11, "shell", ex_k)

    # ================================================================ context (not in the BOM)
    wall = _box(-150.0, 190.0, ywall, ywall + 30.0, -215.0, 585.0)
    add("Wall section (painted plaster)", wall, C_WALL, "paper", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:36s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.2f} cm3")
