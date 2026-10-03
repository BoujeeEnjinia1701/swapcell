"""SwapCell general arrangement drawing SWC-DWG-002 (Rev P4).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SWC-DWG-002.svg, .pdf and .png from the parametric model.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views, _t, INK, MUTED  # noqa: E402
from model import PARAMS as P, assemblies, derived  # noqa: E402

pack, dock, asm = assemblies()
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="SwapCell", title="General arrangement, pack in wall dock", dwg_no="SWC-DWG-002",
          rev="P4", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Pack: 1.5 mm 5052 Al tray, 3 mm UL 94 V-0 PC sheet lid; dock: 12 mm Al plate, printed shelf and guides. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA, interface v0.3 (SWC-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Notes: connector family, R3 derating (SWC-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Constructable design: latch, fixings, dock (SWC-DDR-003)", "2026-10-01", "AC"),
                     ("P4", "Interface v0.4: handle zone 84 x 43, catch geometry details", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 40, 140, 62, label="Isometric view", sublabel="Not to scale")
s.add_notes("Interface v0.4 key dimensions (mm)", [
    f"Pack body {P['pack_l']:.0f} x {P['pack_w']:.0f} x {P['pack_d']:.0f}, tolerance +0 / -1.5",
    f"Overall length {P['pack_l'] + P['handle_h'] + P['plug_h']:.0f} (handle {P['handle_h']:.0f}, plug {P['plug_h']:.0f})",
    "Datum A: connector face; insertion along Z, connector first",
    f"Plug centred in width, {P['plug_offset_y']:.0f} toward back face from depth centre",
    f"Guide faces 340 x 80, {P['pack_w']:.0f} apart; receiver clearance {P['guide_clear']:.0f} per side",
    f"Latch pawl {P['latch_w']:.0f} wide, {P['latch_from_top']:.0f} below top end, back face",
    f"Catch: face 1 above pawl, reach {P['catch'][1]:.0f}, engagement 4 (detail B)",
    f"Handle zone {P['handle_zone'][0]:.0f} x {P['handle_zone'][1]:.0f} to back face, {P['handle_h']:.0f} high (detail A)",
    "Latch class V1: proof 1.72 kN along insertion axis",
    "Vehicle receiver preload 330 N via over-centre lever",
    "Contacts: P1 PACK+, P2 PACK-, S1 SGND, S2/S3 CAN,",
    "  S4 WAKE, S5 AUX, S6 INTERLOCK (10 kOhm coded)",
    "Connector: custom keyed shroud, commercial contacts",
    "R3: 20 A open-air mount; derate 50 to 60 C cell temp",
    "Flush wake button on lid face",
    "Pack mass about 3.0 kg; 13S2P, 46.8 V, 468 Wh",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=114, width=140)

# ---- interface v0.4 details: A, handle zone on the top end (1:2); B, catch geometry (2:1)
D = derived(P)
L = s._layers


def rect(x, y, w, h, dash=False, fill="none", lw=0.35, col=INK):
    d = ' stroke-dasharray="2 1"' if dash else ""
    L.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{col}" stroke-width="{lw}"{d}/>')


def line(x1, y1, x2, y2, dash=False, lw=0.35):
    d = ' stroke-dasharray="1.5 1"' if dash else ""
    L.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="{lw}"{d}/>')


ACC = "#0F766E"
# Detail A: plan of the top end, looking down; back face (wall side) at the top
k, ox, oy = 0.5, 80.0, 222.0
X = lambda x: ox + x * k  # noqa: E731
Y = lambda y: oy - y * k  # noqa: E731
W_, D_ = P["pack_w"], P["pack_d"]
rect(X(-W_ / 2), Y(D_ / 2), W_ * k, D_ * k)
zw, zd = P["handle_zone"]
rect(X(-zw / 2), Y(D_ / 2), zw * k, zd * k, dash=True, col=ACC, lw=0.45)
py, hd = P["plug_offset_y"], P["handle_d"]
rect(X(-P["handle_w"] / 2), Y(py + hd / 2), P["handle_w"] * k, hd * k, fill="#E5E7EB", lw=0.25)
rect(X(-15), Y(38), 30 * k, 16 * k, fill="#CCFBF1", lw=0.25)
s._dim(X(-zw / 2), Y(D_ / 2), X(zw / 2), Y(D_ / 2), f"{zw:.0f}", "above", off=5)
s._dim(X(zw / 2), Y(D_ / 2), X(zw / 2), Y(D_ / 2 - zd), f"{zd:.0f}", "right", off=6)
L.append(_t(X(0), Y(D_ / 2) - 9.5, "BACK FACE (WALL SIDE)", 1.9, 500, MUTED, "middle"))
L.append(_t(X(0), Y(-D_ / 2) + 4.5, "LID FACE", 1.9, 500, MUTED, "middle"))
L.append(_t(ox - 60, oy - 14, "Handle zone (dashed):", 2.2, 600, ACC))
L.append(_t(ox - 60, oy - 10, "receivers keep it clear", 2.2, 400, INK))
L.append(_t(ox - 60, oy - 4, "Grey: handle", 2.2, 400, INK))
L.append(_t(ox - 60, oy, "Teal: thumb button", 2.2, 400, INK))
L.append(_t(X(0), oy + 33, "DETAIL A: HANDLE ZONE", 2.8, 600, INK, "middle"))
L.append(_t(X(0), oy + 37, "Scale 1:2; top end, looking down (along -Z)", 2.2, 400, MUTED, "middle"))

# Detail B: section through the latch, looking at the right side; Y (out of the wall) to the right
k, ox, oy = 2.0, 142.0, 222.0
yb = D["yback"]; yp = D["yplate"]; pt = D["zlatch"] + P["latch_h"] / 2
Yb = lambda y: ox + (y - yb) * k  # noqa: E731
Zb = lambda z: oy - (z - pt) * k  # noqa: E731
pr, trv, cr, ch = P["latch_proud"], P["latch_travel"], P["catch"][1], P["catch"][2]
rect(Yb(yb - P["tray_t"]), Zb(pt + 13), P["tray_t"] * k, 22 * k, fill="#D1D5DB", lw=0.25)     # back wall
rect(Yb(yb - 4), Zb(pt), (pr + 4) * k, 8 * k, fill="#FED7AA", lw=0.35)                       # pawl tooth
line(Yb(yb + pr - trv), Zb(pt), Yb(yb + pr - trv), Zb(pt - 8), dash=True)                      # retracted tooth face
rect(Yb(yp - cr), Zb(pt + 1 + ch), cr * k, ch * k, fill="#A5F3FC", lw=0.35)                   # catch
rect(Yb(yp), Zb(pt + 13), 2.5 * k, 22 * k, fill="#E7E5E4", lw=0.25)                           # plate
s._dim(Yb(yp - cr), Zb(pt + 1 + ch), Yb(yp), Zb(pt + 1 + ch), f"Reach {cr:.0f}", "above", off=4)
s._dim(Yb(yb), Zb(pt - 8), Yb(yb + pr), Zb(pt - 8), f"Pawl {pr:.0f}", "below", off=4)
s._dim(Yb(yb + pr - trv), Zb(pt - 8), Yb(yb + pr), Zb(pt - 8), f"Travel {trv:.0f}", "below", off=10)
s._dim(Yb(yp - cr), Zb(pt + 1 + ch), Yb(yb + pr), Zb(pt + 1 + ch), "Engage 4", "above", off=10)
L.append(_t(Yb(yp) + 7, Zb(pt + 0.5) + 1, "1 gap: latching face", 2.2, 400, INK))
L.append(_t(Yb(yp) + 7, Zb(pt + 0.5) + 4.5, "above the pawl top", 2.2, 400, INK))
L.append(_t(Yb(yp) + 7, Zb(pt - 7) + 1, "Engage: tooth under catch", 2.2, 400, INK))
L.append(_t(Yb(yp) + 7, Zb(pt - 7) + 4.5, "Dashed: retracted", 2.2, 400, INK))
L.append(_t(Yb(yb - P["tray_t"]) - 1.5, Zb(pt + 10), "Back wall", 2.0, 400, MUTED, "end"))
L.append(_t(Yb(yp) + 6, Zb(pt + 10), "Plate", 2.0, 400, MUTED))
L.append(_t(Yb(yb + 10), oy + 33, "DETAIL B: CATCH GEOMETRY", 2.8, 600, INK, "middle"))
L.append(_t(Yb(yb + 10), oy + 37, "Scale 2:1; section, looking at the right side (along -X)", 2.2, 400, MUTED, "middle"))
s.save(ROOT / "cad/drawings/SWC-DWG-002")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SWC-DWG-002.svg, .pdf, .png")
