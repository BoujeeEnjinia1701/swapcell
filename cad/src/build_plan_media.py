"""SwapCell prototype build plan pictures (SWC-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. A sheet or step number after the word draws just that one
(for example "sheets 103" or "steps 7"), which keeps memory low. Every picture is drawn from
cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SWC-DWG-101 to 115        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, bx, wall_context  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)

COL = {"tray": "#6B7280", "pnuts": "#111827", "cells": "#C2410C", "holder": "#7C3AED", "bms": "#0F766E",
       "lid": "#D1D5DB", "gasket": "#1F2937", "wake": "#0F766E", "plug": "#D4A017", "contacts": "#B45309",
       "handle": "#111827", "pawl": "#B45309", "housing": "#57534E", "slider": "#1D4ED8", "thumb": "#0F766E",
       "springs": "#DC2626", "fix": "#111827", "plate": "#A8A29E", "shelf": "#94A3B8", "guide": "#64748B",
       "catch": "#0E7490", "rec": "#16A34A", "foam": "#FDE68A", "retainer": "#78716C", "charger": "#374151",
       "straps": "#1D4ED8", "ctrl": "#0F766E", "wall": "#E7E5E4"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*keys):
    return _fuse([C[k].shape for k in keys])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def named():
    """The components in build order, with the colours used in every picture."""
    return {
        "tray": part("Pack tray, with press-in nuts", S("tray", "pnuts"), COL["tray"]),
        "housing": part("Latch housing", S("housing"), COL["housing"]),
        "pawl": part("Latch pawl and springs", S("pawl", "springs"), COL["pawl"]),
        "slider": part("Release slider and thumb button", S("slider", "thumb"), COL["slider"]),
        "plug": part("Plug shroud with contacts", S("plug", "plug_contacts"), COL["plug"]),
        "holders": part("Cell holder frames (2)", S("holder_l", "holder_r"), COL["holder"]),
        "cells": part("Cells (26)", S("cells"), COL["cells"]),
        "bms": part("BMS board on standoffs", S("bms", "bms_so"), COL["bms"]),
        "handle": part("Carry handle", S("handle"), COL["handle"]),
        "gasket": part("Lid gasket", S("gasket"), COL["gasket"]),
        "lid": part("Lid and wake button", S("lid", "wake"), COL["lid"]),
        "plate": part("Dock back plate", S("plate"), COL["plate"]),
        "shelf": part("Cradle shelf", S("shelf"), COL["shelf"]),
        "guides": part("Side guides (2)", S("guide_l", "guide_r"), COL["guide"]),
        "catch": part("Latch catch", S("catch"), COL["catch"]),
        "rec": part("Receptacle with pins", S("receptacle", "rec_pins"), COL["rec"]),
        "retainer": part("Foam pad and retainer plate", S("foam", "retainer"), COL["retainer"]),
        "ctrl": part("Controller box", S("controller"), COL["ctrl"]),
        "charger": part("Charger (bought)", S("charger"), COL["charger"]),
        "straps": part("Charger straps (2)", S("straps"), COL["straps"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = named()
    pk = (-330, 0, 170)       # the pack is drawn up and to the left of the dock
    add = lambda a, b: tuple(x + y for x, y in zip(a, b))  # noqa: E731
    off = {"tray": pk, "housing": add(pk, (130, 0, 190)), "pawl": add(pk, (200, 30, 160)),
           "slider": add(pk, (130, 0, 290)), "plug": add(pk, (0, 0, -100)), "holders": add(pk, (-200, 0, 170)),
           "cells": add(pk, (-200, 0, 170)), "bms": add(pk, (140, -40, -30)), "handle": add(pk, (0, 0, 130)),
           "gasket": add(pk, (0, -130, -150)), "lid": add(pk, (0, -240, -270)),
           "plate": (0, 0, 0), "shelf": (0, -120, -10), "guides": (0, -120, 80), "catch": (0, -90, 0),
           "rec": (0, -120, -80), "retainer": (0, -120, -140), "ctrl": (0, -150, -160), "charger": (0, -170, -190),
           "straps": (170, -170, -190)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "SwapCell prototype: every component, pulled apart",
                       subtitle="Numbered in build order: pack (1 to 11) up and to the left, wall dock (12 to 20) on the right. "
                                "Seen from the front right and above",
                       elev=16, azim=-50, size=(11, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = named()
    base = dict(project="SwapCell", date=DATE)
    out = []
    zl, zt, z0 = D["zlatch"], D["ztop"], D["z0"]
    pack_ctx = [M["tray"], M["cells"], M["handle"], M["plug"]]

    def sheet(no, *a, **k):
        if only and no not in only:
            return
        out.append(bv.component_sheet(*a, dwg_no=f"SWC-DWG-{no}", **k, **base))

    sheet(101, Part("Pack tray", C["tray"].shape, COL["tray"]), [M["plate"], M["shelf"], M["guides"]],
          title="SwapCell pack tray: making sketch", material="Aluminium sheet 1.5 mm, 5052-H32",
          view_shape=b.Pos(0, 0, -z0) * C["tray"].shape, inset_view=(20, -55),
          notes=["One blank folded into an open box 90 wide, 76 deep, 340 tall: back,",
                 "  two sides, two ends; 10 mm tabs on the ends rivet to the sides.",
                 "8 mm flanges folded inward round the open front (the lid side).",
                 "Heights from the connector face; left and right seen from the lid.",
                 "Back: pawl slot 37 x 25, 282.5 to 307.5 up; six 4.1 rivet holes at",
                 "  25 each side, 290, 310, 330 up; holder screws 2.7 at 25 right",
                 "  and 37 left, 60 and 240 up. Countersink all from outside.",
                 "Top end: slider slot 31 x 5.5 against the back wall; two 5.5",
                 "  handle holes at 36.5 each side, 32 in from the back face.",
                 "Connector face: lead opening 42 x 22, 21 to 43 in from the back",
                 "  face; four 3.4 plug screw holes (see the build plan).",
                 "Right side: four 2.7 BMS holes, 8 and 58 from the back face,",
                 "  80 and 260 up, countersunk outside so the face stays flat.",
                 "Flanges: eight 4.2 holes for M3 press-in nuts, 5.5 in from each",
                 "  side, 30, 125, 215, 310 up. Seal the corner seams."])

    hs = C["housing"].shape
    sheet(102, Part("Latch housing", hs, COL["housing"]), [M["tray"], M["pawl"], M["slider"]],
          title="SwapCell latch housing: making sketch", material="Steel sheet 1.5 mm, zinc plated",
          view_shape=b.Pos(0, 0, -D["hous_z0"]) * hs, inset_view=(15, 60),
          notes=["An open box 40 wide, 12.5 deep, 57 tall, open on the back (the",
                 "  side against the tray wall) and at the top (the tray top closes it).",
                 "Fold from one blank: front, two sides and a bottom, with a",
                 "  10 mm flange on the back edge of each side, folded outward.",
                 "Drill three 4.1 holes in each flange, 5 from the side wall,",
                 "  8.5, 28.5 and 48.5 up from the bottom.",
                 "Fit: flanges flat on the inside of the back wall, bottom 281.5",
                 "  up from the connector face, centred across. Six countersunk",
                 "  blind rivets from outside. It is the latch doubler: the pawl's",
                 "  lifting load goes into its bottom, then through the rivets.",
                 "Check: the pawl slides in and out freely with 0.5 mm each side."])

    pw = C["pawl"].shape
    sheet(103, Part("Latch pawl", pw, COL["pawl"]), [M["tray"], M["housing"], M["slider"], M["catch"]],
          title="SwapCell latch pawl: making sketch", material="Steel flat bar 40 x 15 mm, 1018 class",
          view_shape=b.Pos(0, -D["yback"], -(zl - P["latch_h"] / 2)) * pw, inset_view=(10, 50),
          notes=["Cut a block 36 wide, 34 tall, 12.5 deep. Square all faces.",
                 "Tooth (lower 24 mm): full depth. Its top face is the latching face:",
                 "  keep it flat and square to the back. File a 4 x 45 degree lead-in",
                 "  along the outer bottom edge.",
                 "Shoulder (top 10 mm): mill or file away the outer 7.5 mm, leaving",
                 "  5 deep, then file its top back edge to a 5 x 45 degree ramp.",
                 "Drill two 6 mm spring holes 8 deep in the inside face, 10 each",
                 "  side of centre, 12 up from the bottom.",
                 "Fit: the tooth passes through the back wall and stands 6 proud;",
                 "  the shoulder rests on the inside of the wall (the out stop).",
                 "  It hooks 4 mm under the dock catch; pressing the thumb button",
                 "  pulls it in 5 mm, 1 mm clear of the catch.",
                 "Check: it slides in its slot without binding at any point."])

    sl = C["slider"].shape + C["thumb"].shape
    sheet(104, Part("Release slider and thumb button", sl, COL["slider"]), [M["tray"], M["pawl"], M["handle"], M["housing"]],
          title="SwapCell release slider and thumb button: making sketch", material="Steel flat bar 35 x 5 mm; printed button",
          view_shape=b.Pos(0, 0, -(zt - 30)) * sl, inset_view=(18, 55),
          notes=["Slider: a steel bar 5 thick, 34 wide for its lower 25.5 mm and",
                 "  30 wide for the 10.5 mm above (file the steps), 36 long in all.",
                 "File the lower end to a 45 degree ramp across the full 5 mm,",
                 "  sloping up toward the lid side, to match the pawl's ramp.",
                 "Drill and tap M3, 6 deep, in the top end.",
                 "Button: print 30 x 16 x 8 in the same plastic as the handle, with",
                 "  a 3.4 hole through, counterbored from the top for the screw.",
                 "Fit: the slider goes up through the tray top from inside, flat",
                 "  against the back wall; the wide part stops under the tray top",
                 "  so it cannot come out. The button screws on top, 8 above it.",
                 "Press: the ramp wedges between the wall and the pawl and pulls",
                 "  the pawl in 5 mm. The pawl springs push it back up.",
                 "Check: 5 mm of button travel retracts the tooth flush."])

    pg = C["plug"].shape
    sheet(105, Part("Plug shroud", pg, COL["plug"]), [M["tray"], M["rec"], M["shelf"]],
          title="SwapCell plug shroud: making sketch", material="Printed flame-retardant PC-ABS or PA, 100 % infill",
          view_shape=b.Pos(0, 0, -(z0 - P["plug_h"])) * pg, inset_view=(-30, -60),
          notes=["Print 56 x 34 x 18 with the key notch, 8 x 8, at the back right corner.",
                 "Power contact holes 9 dia through, 15 each side, 12 in from the",
                 "  front edge; six signal holes 3 dia through at 7 pitch, 26 in.",
                 "Check the hole sizes against the contacts bought before printing.",
                 "Four M3 heat-set inserts in the top face, 8 deep: 25 each side",
                 "  4 in from the front edge; 25 left and 9 right at the back.",
                 "Press in the contacts from the top with their wires fitted; pot",
                 "  the six signal contacts. The INTERLOCK contact is shortest.",
                 "Fit: top face flat on the connector face, centred across, 8 toward",
                 "  the back; four M3 screws from inside the tray; wires up through",
                 "  the lead opening; a bead of sealant round the opening.",
                 "Check: the key notch is at the back right seen from the lid."])

    hr = C["holder_r"].shape
    sheet(106, Part("Cell holder frame", hr, COL["holder"]), [M["cells"], M["tray"], M["housing"]],
          title="SwapCell cell holder frame (make 2): making sketch", material="Printed flame-retardant PC-ABS, 6 mm",
          view_shape=b.Rot(0, 0, 90) * b.Pos(-25, 0, -80) * hr, inset_view=(20, -40),
          notes=["Print two frames 6 thick, 59.5 deep and 300 tall, lying flat.",
                 "26 pockets 21.2 dia through, two rows at 25.5 and 47.5 in from",
                 "  the back edge, 13 pockets per row at 22 pitch, the first 18 up.",
                 "Print one plain (left) and one with a notch 6.5 deep from the",
                 "  back edge over the top 44.5 mm (right), which clears the latch.",
                 "Two M2.5 heat-set inserts in the back edge of each, 40 and 220",
                 "  up from its bottom, on the frame's centre line.",
                 "Fit: one frame 1 mm in from each end of the cells; cells pushed",
                 "  in until 1 mm stands out for the nickel strip. The back edges",
                 "  rest on the tray back wall, held by two M2.5 countersunk",
                 "  screws each from outside the tray.",
                 "Check: the cells sit square and do not turn by hand."])

    hd = C["handle"].shape
    sheet(107, Part("Carry handle", hd, COL["handle"]), [M["tray"], M["slider"]],
          title="SwapCell carry handle: making sketch", material="Printed PETG or PA, 60 % infill",
          view_shape=b.Pos(0, 0, -zt) * hd, inset_view=(25, -50),
          notes=["Print 84 wide, 22 deep, 35 tall, as an arch: a grip bar 10 thick",
                 "  over a 62 x 25 opening, legs 11 wide.",
                 "Round every grip edge to 3 mm.",
                 "M5 heat-set insert in the bottom of each leg, 12 deep, at",
                 "  36.5 each side of centre.",
                 "Fit: legs flat on the tray top end, 8 toward the back from the",
                 "  depth centre; two M5 screws from inside the tray.",
                 "The thumb button sits just behind the grip, 3 mm clear of it.",
                 "Check: a gloved hand fits through the opening."])

    ld = C["lid"].shape
    sheet(108, Part("Pack lid", ld, COL["lid"]), [M["tray"], M["gasket"]],
          title="SwapCell pack lid: making sketch", material="Flame-retardant polymer 3 mm, UL 94 V-0 grade",
          view_shape=b.Pos(0, 0, -z0) * ld, inset_view=(20, -60),
          notes=["A flat plate 90 x 340 x 3 (printed, or cut from V-0 sheet).",
                 "Eight 3.4 holes countersunk on the outside, 39.5 each side of",
                 "  centre, 30, 125, 215 and 310 up from the connector end.",
                 "Wake button hole 13 dia, centred across, 270 up.",
                 "Fit: on a 1 mm flat gasket over the tray flanges, eight M3",
                 "  countersunk screws into the press-in nuts; heads flush.",
                 "Tighten in a cross pattern from the middle out.",
                 "Check: the gasket squeezes evenly with no gap at the corners."])

    pl = C["plate"].shape
    sheet(109, Part("Dock back plate", pl, COL["plate"]), [M["shelf"], M["guides"], M["catch"], M["charger"]],
          title="SwapCell dock back plate: making sketch", material="Aluminium plate 12 mm, 6082 or 6061",
          view_shape=b.Pos(0, 0, 170) * pl, inset_view=(20, -55),
          notes=["Cut 150 x 580 from 12 mm plate; square, deburr, round corners 3.",
                 "Heights from the bottom edge, sideways from the centre line.",
                 "Countersunk from the back (the wall side), 5.5 dia:",
                 "  shelf 45 each side at 195 and 220; guides 52 each side at",
                 "  270 and 370; catch 16 each side at 544.",
                 "Tapped from the front: M5 strap holes 62 each side at 19 and",
                 "  151; M4 controller holes 15 each side at 160.",
                 "Wall holes 6.5: 30 each side at 10, 62 each side at 568.",
                 "Fit: everything else on the dock hangs on its front face; its",
                 "  back goes flat on a non-combustible wall.",
                 "Check: screw heads sit flush or below the back face."])

    sh = C["shelf"].shape
    sheet(110, Part("Cradle shelf", sh, COL["shelf"]), [M["plate"], M["guides"], M["rec"]],
          title="SwapCell cradle shelf: making sketch", material="Printed ASA or PETG, 40 % infill, 4 walls",
          view_shape=b.Pos(0, 0, -15) * sh, inset_view=(35, -60),
          notes=["Print 120 wide, 110 deep, 45 tall.",
                 "Plug pocket 60 x 38, 18 deep from the top, centred across, its back",
                 "  edge 23 from the shelf back face.",
                 "Receptacle cavity 72 x 50 from the bottom up to 27, centred under",
                 "  the pocket; the 6 mm ledge between them holds the receptacle.",
                 "Four M5 heat-set inserts in the back face, 45 each side, 10 and 35",
                 "  up; four M3 inserts in the bottom, 40 each side, 13 and 71",
                 "  from the back face, for the retainer plate.",
                 "Fit: back face flat on the plate, four M5 countersunk screws from",
                 "  behind; top face 60 above the dock datum.",
                 "Check: the plug drops into the pocket with 2 mm all round."])

    gr = C["guide_r"].shape
    sheet(111, Part("Side guide", gr, COL["guide"]), [M["plate"], M["shelf"], M["tray"]],
          title="SwapCell side guide (make 2, a left and a right): making sketch", material="Printed ASA or PETG, 40 % infill",
          view_shape=b.Pos(0, 0, -z0) * gr, inset_view=(25, -60),
          notes=["Print 12 wide, 70 deep, 180 tall, standing up.",
                 "Lead-in: a 10 x 45 degree chamfer along the top inner edge.",
                 "The left guide is a mirror image of the right.",
                 "Two M5 heat-set inserts in the back end, 40 and 140 up.",
                 "Fit: back end flat on the plate, bottom on the shelf top;",
                 "  inner faces 92 apart, 1 mm clear of the pack each side.",
                 "Two M5 countersunk screws each from behind the plate.",
                 "Check: the pack slides between them without rubbing."])

    ct = C["catch"].shape
    sheet(112, Part("Latch catch", ct, COL["catch"]), [M["plate"], M["guides"], M["shelf"]],
          title="SwapCell latch catch: making sketch", material="Steel flat bar 12 x 8 mm, zinc plated",
          view_shape=b.Pos(0, 0, -D["catch_z"][0]) * ct, inset_view=(15, -35),
          notes=["Cut 50 long from 12 x 8 flat bar; square and deburr.",
                 "The bottom face is the latching face: keep it flat and square.",
                 "Two M5 tapped holes 7 deep in the back face, 16 each side of",
                 "  centre, half way up.",
                 "Fit: back face flat on the plate front, centred, 544 up from",
                 "  the plate bottom; two M5 countersunk screws from behind.",
                 "It stands 8 out from the plate and ends 2 from the pack's back.",
                 "With the pack seated, the pawl sits 1 below it, overlapping 4.",
                 "Check: lift the seated pack by its handle: the pawl stops it."])

    rc = C["receptacle"].shape
    sheet(113, Part("Receptacle shroud", rc, COL["rec"]), [M["shelf"], M["plug"], M["retainer"]],
          title="SwapCell receptacle shroud: making sketch", material="Printed flame-retardant PC-ABS or PA, 100 % infill",
          view_shape=b.Pos(0, 0, -(z0 - P["plug_h"] - 12)) * rc, inset_view=(30, -60),
          notes=["Print a body 58 x 36 x 12 with a 3 mm flange 66 x 44 at its top.",
                 "Key post 7 x 7, 16 tall, at the back right corner of the top face.",
                 "Pin holes through, matched to the plug: power 15 each side,",
                 "  13 in from the front of the body; signal at 7 pitch, 27 in.",
                 "Press in the pins: power pins 10 above the face (PACK- 11),",
                 "  signal pins 8, the INTERLOCK pin only 5, so it mates last.",
                 "Solder the 10 kOhm coding resistor from INTERLOCK to SGND.",
                 "Fit: drops into the cavity from below; the flange stops under",
                 "  the pocket ledge with 3 mm to float each way; the foam pad",
                 "  and retainer plate hold it up.",
                 "Check: it moves 3 mm each way by hand and springs back up."])

    rt = C["retainer"].shape
    sheet(114, Part("Receptacle retainer plate", rt, COL["retainer"]), [M["shelf"], M["rec"]],
          title="SwapCell receptacle retainer plate: making sketch", material="Aluminium sheet 3 mm",
          view_shape=b.Pos(0, 0, -12) * rt, inset_view=(-35, -55),
          notes=["Cut 88 x 66 from 3 mm sheet; deburr.",
                 "Four 4.4 holes, 40 each side of centre, 4 and 62 from the front",
                 "  edge; a 16 mm hole for the receptacle wires, centred across,",
                 "  33 from the front edge.",
                 "Fit: flat under the shelf, holding the 15 mm foam pad and the",
                 "  receptacle in the cavity; four M3 screws into the inserts.",
                 "Check: the receptacle flange touches the ledge with the foam",
                 "  lightly squeezed."])

    stp = C["straps"].shape & bx(0, 200, -200, 200, -400, 400)
    sheet(115, Part("Charger strap", stp, COL["straps"]), [M["plate"], M["charger"]],
          title="SwapCell charger strap (make 2): making sketch", material="Aluminium strip 20 x 1.5 mm",
          view_shape=stp, inset_view=(20, -55),
          notes=["Cut 20 wide strip 300 long. Fold to a hat shape that fits the",
                 "  charger: two feet 20 long, two legs 64, a front 113.",
                 "Measure your charger first: legs = its depth, front = its height",
                 "  plus 3.",
                 "Drill a 5.5 hole in each foot, 11 from the fold.",
                 "Fit: the charger's back flat on the plate; each strap over it,",
                 "  62 each side of centre, feet flat on the plate, one M5 screw",
                 "  into each tapped hole.",
                 "Check: the charger does not move when pulled by hand."])
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []
    yb, zt, z0, zl = D["yback"], D["ztop"], D["z0"], D["zlatch"]
    # 01 lid, gasket, flange, press-in nut and screw, cut through a screw
    z = 185.0
    bx_ = (26, 47, -42, -24, z - 14, z)
    out.append(bv.joint([
        part("Lid", win(C["lid"].shape, *bx_), COL["lid"]),
        part("Gasket", win(C["gasket"].shape, *bx_), COL["gasket"]),
        part("Tray side wall and front flange", win(C["tray"].shape, *bx_), COL["tray"]),
        part("M3 press-in nut", win(C["pnuts"].shape, *bx_), "#57534E"),
        part("M3 countersunk screw", win(C["lid_screws"].shape, *bx_), "#1D4ED8")],
        OUT / "joint-01.png", "Joint 1: lid on the tray flange (cut through a screw)",
        subtitle="Cut level with a screw, seen from above. Lid, 1 mm gasket, 8 mm flange; the nut is pressed in from inside",
        elev=62, azim=-75, size=(8, 6)))
    # 02 latch: pawl, housing, slider and tray back wall, cut at the centre
    bx_ = (-22, 2, 20, 50, zl - 22, zt + 18)
    out.append(bv.joint([
        part("Tray back wall and top", win(C["tray"].shape, *bx_), COL["tray"]),
        part("Latch housing", win(C["housing"].shape, *bx_), COL["housing"]),
        part("Pawl (shoulder rests on the wall)", win(C["pawl"].shape, *bx_), COL["pawl"]),
        part("Spring", win(C["springs"].shape, *bx_), COL["springs"]),
        part("Release slider (ramp on the pawl ramp)", win(C["slider"].shape, *bx_), COL["slider"]),
        part("Thumb button", win(C["thumb"].shape, *bx_), COL["thumb"])],
        OUT / "joint-02.png", "Joint 2: the latch, cut through its middle",
        subtitle="Seen from the right. Pressing the button drives the slider ramp down and pulls the pawl in 5 mm",
        elev=6, azim=-4, size=(8, 7)))
    # 03 pawl under the catch, pack seated
    bx_ = (-30, 2, 25, 63, zl - 20, zl + 30)
    out.append(bv.joint([
        part("Pack back wall (thin, grey)", win(C["tray"].shape, *bx_), COL["tray"]),
        part("Pawl (orange)", win(C["pawl"].shape, *bx_), COL["pawl"]),
        part("Latch housing (dark)", win(C["housing"].shape, *bx_), COL["housing"]),
        part("Catch (teal)", win(C["catch"].shape, *bx_), COL["catch"]),
        part("Dock back plate", win(C["plate"].shape, *bx_), COL["plate"])],
        OUT / "joint-03.png", "Joint 3: pawl under the catch, pack seated (cut through the middle)",
        subtitle="Seen from the right. The tooth hooks 4 mm under the catch with 1 mm above it; retracted it clears by 1 mm",
        elev=6, azim=-4, size=(8, 6)))
    # 04 plug on the connector face, cut through the two left screws
    bx_ = (-46, -25, -12, 28, z0 - 20, z0 + 10)
    out.append(bv.joint([
        part("Tray connector face", win(C["tray"].shape, *bx_), COL["tray"]),
        part("Plug shroud", win(C["plug"].shape, *bx_), COL["plug"]),
        part("M3 screw into a heat-set insert", win(C["plug_screws"].shape, *bx_), "#DC2626")],
        OUT / "joint-04.png", "Joint 4: plug shroud on the connector face (cut through the left screws)",
        subtitle="Seen from the right, slightly below. Each M3 screw goes down from inside the tray into a heat-set insert in the shroud",
        elev=-12, azim=-15, size=(8, 6)))
    # 05 plug in the receptacle in the shelf, cut through a power pin
    bx_ = (-40, -15, -20, 52, z0 - 50, z0 + 8)
    out.append(bv.joint([
        part("Cradle shelf", win(C["shelf"].shape, *bx_), COL["shelf"]),
        part("Plug shroud", win(C["plug"].shape, *bx_), COL["plug"]),
        part("Socket contact", win(C["plug_contacts"].shape, *bx_), COL["contacts"]),
        part("Receptacle, green (floats 3 mm)", win(C["receptacle"].shape, *bx_), COL["rec"]),
        part("Pin", win(C["rec_pins"].shape, *bx_), "#111827"),
        part("Foam pad (yellow) on the retainer plate", win(C["foam"].shape + C["retainer"].shape, *bx_), COL["foam"]),
        part("Pack tray", win(C["tray"].shape, *bx_), COL["tray"])],
        OUT / "joint-05.png", "Joint 5: plug in the receptacle (cut through a power contact)",
        subtitle="Seen from the front right. The receptacle flange sits under the pocket ledge on a foam pad, free to float",
        elev=10, azim=-30, size=(8, 6.5)))
    # 06 holder frame on the back wall
    bx_ = (16, 34, -25, 44, 104, 120)
    out.append(bv.joint([
        part("Tray back wall", win(C["tray"].shape, *bx_), COL["tray"]),
        part("Cell holder frame", win(C["holder_r"].shape, *bx_), COL["holder"]),
        part("Cells", win(C["cells"].shape, *bx_), COL["cells"]),
        part("M2.5 countersunk screw", win(C["holder_screws"].shape, *bx_), "#1D4ED8")],
        OUT / "joint-06.png", "Joint 6: cell holder frame on the back wall (right frame)",
        subtitle="Cut level with a screw, seen from above. The frame's back edge rests on the wall; one screw from outside",
        elev=65, azim=-60, size=(8, 6)))
    # 07 handle on the top end
    bx_ = (-50, 50, P["plug_offset_y"], 45, zt - 8, zt + 38)
    out.append(bv.joint([
        part("Tray top end", win(C["tray"].shape, *bx_), COL["tray"]),
        part("Carry handle", win(C["handle"].shape, *bx_), "#4B5563"),
        part("M5 screw from inside", win(C["handle_screws"].shape, *bx_), "#DC2626"),
        part("Thumb button", win(C["thumb"].shape, *bx_), COL["thumb"]),
        part("Release slider", win(C["slider"].shape, *bx_), COL["slider"])],
        OUT / "joint-07.png", "Joint 7: handle and thumb button on the top end",
        subtitle="Cut through both handle screws, seen from the front. The thumb button sits behind the grip, 8 mm above the tray",
        elev=12, azim=-78, size=(8, 6)))
    # 08 shelf and guide on the plate
    bx_ = (20, 52, -30, 66, z0 - 50, z0 + 70)
    out.append(bv.joint([
        part("Dock back plate", win(C["plate"].shape, *bx_), COL["plate"]),
        part("Cradle shelf", win(C["shelf"].shape, *bx_), COL["shelf"]),
        part("Side guide (cut)", win(C["guide_r"].shape, *bx_), COL["guide"]),
        part("M5 countersunk screws from behind", win(C["dock_screws"].shape, *bx_), "#DC2626")],
        OUT / "joint-08.png", "Joint 8: shelf and right guide on the back plate",
        subtitle="Cut through the guide screw, seen from the right. Screws from behind the plate into inserts; the shelf is the same",
        elev=15, azim=-20, size=(8, 6)))
    # 09 charger strap and controller
    bx_ = (-30, 76, -20, 64, -60, 8)
    out.append(bv.joint([
        part("Dock back plate", win(C["plate"].shape, *bx_), COL["plate"]),
        part("Charger", win(C["charger"].shape, *bx_), COL["charger"]),
        part("Charger strap", win(C["straps"].shape, *bx_), COL["straps"]),
        part("Controller box", win(C["controller"].shape, *bx_), COL["ctrl"]),
        part("M5 screw", win(C["dock_screws"].shape, *bx_), "#B45309")],
        OUT / "joint-09.png", "Joint 9: charger strap and controller box on the back plate",
        subtitle="Seen from the front right. The strap's foot takes one M5 screw into the plate; the box takes two M4",
        elev=25, azim=-40, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = named()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    tray = part("Pack tray", S("tray"), COL["tray"])
    st(1, [tray], [mv(part("M3 press-in nuts (8)", S("pnuts"), COL["pnuts"]), (0, 60, 0))],
       "press-in nuts into the tray flanges",
       "Eight nuts from inside, pressed flush in a vice with soft jaws. Seen from the front left (the lid side)",
       elev=20, azim=-130, label_done=False)
    t1 = [M["tray"]]
    st(2, t1, [mv(part("Pawl with its springs", S("pawl", "springs"), COL["pawl"]), (0, -110, 0)),
               mv(part("Release slider", S("slider"), COL["slider"]), (0, -110, -150))],
       "pawl and release slider into the back wall",
       "From inside: pawl through its slot, springs in its holes; slider up through the top slot. Seen from the front right, lid off",
       elev=20, azim=-45, label_done=False)
    t2 = t1 + [part("Pawl and slider", S("pawl", "springs", "slider"), COL["pawl"])]
    st(3, t2, [mv(M["housing"], (0, -110, 0))], "latch housing over them",
       "Flanges flat on the back wall; six countersunk blind rivets from outside. Seen from the front right, lid off",
       elev=20, azim=-45, label_done=False)
    t3 = t2 + [M["housing"]]
    st(4, t3, [mv(part("Thumb button", S("thumb"), COL["thumb"]), (0, 0, 50))], "thumb button onto the slider",
       "One M3 screw into the slider top. Press it: the pawl must pull in flush with the back face",
       elev=25, azim=-40, label_done=False)
    t4 = t3 + [part("Thumb button", S("thumb"), COL["thumb"])]
    st(5, t4, [mv(M["plug"], (0, 0, -70))], "plug shroud onto the connector face",
       "Wires fed up through the opening; four M3 screws from inside; sealant round the opening. Seen from below",
       elev=-25, azim=-50, label_done=False)
    st(6, [M["cells"]], [mv(part("Left holder frame", S("holder_l"), COL["holder"]), (-60, 0, 0)),
                         mv(part("Right holder frame", S("holder_r"), COL["holder"]), (60, 0, 0))],
       "build the cell block",
       "Cells in 13 pairs, ends 1 mm proud of each frame; then nickel strips and fuse wires (see the wiring picture)",
       elev=20, azim=-50, label_done=False)
    t5 = t4 + [M["plug"]]
    st(7, t5, [mv(part("Cell block", S("cells", "holder_l", "holder_r"), COL["cells"]), (0, -140, 0))],
       "cell block into the tray",
       "Frames' back edges on the back wall; four M2.5 countersunk screws from outside. Hold point: S2",
       elev=15, azim=-60, label_done=False)
    t6 = t5 + [part("Cell block", S("cells", "holder_l", "holder_r"), COL["cells"])]
    st(8, t6, [mv(M["bms"], (0, -130, 0))], "BMS board onto the right side wall",
       "Four standoffs and M2.5 countersunk screws from outside; then wire it as the wiring picture. Hold point: S3",
       elev=15, azim=-60, label_done=False)
    t7 = t6 + [M["bms"]]
    st(9, t7, [mv(M["handle"], (0, 0, 70))], "carry handle onto the top end",
       "Two M5 screws up from inside the tray into the inserts in its legs",
       elev=20, azim=-50, label_done=False)
    t8 = t7 + [M["handle"]]
    st(10, t8, [mv(M["gasket"], (0, -80, 0)), mv(M["lid"], (0, -160, 0))], "gasket and lid",
       "Gasket on the flanges; lid on top; eight M3 countersunk screws in a cross pattern. Hold point: S4",
       elev=15, azim=-55, label_done=False)
    pl = M["plate"]
    st(11, [pl], [mv(M["shelf"], (0, -110, 0))], "cradle shelf onto the back plate",
       "Four M5 countersunk screws from behind the plate into the shelf's inserts",
       elev=18, azim=-50, label_done=False)
    d1 = [pl, M["shelf"]]
    st(12, d1, [mv(M["guides"], (0, -110, 0))], "side guides onto the back plate",
       "Each on two M5 countersunk screws from behind; bottom on the shelf, lead-ins at the top inside",
       elev=18, azim=-50, label_done=False)
    d2 = d1 + [M["guides"]]
    st(13, d2, [mv(M["catch"], (0, -90, 0))], "latch catch onto the back plate",
       "Two M5 countersunk screws from behind, centred, 544 mm up the plate",
       elev=18, azim=-50, label_done=False)
    d3 = d2 + [M["catch"]]
    st(14, d3, [mv(M["rec"], (0, 0, -60)), mv(M["retainer"], (0, 0, -120))], "receptacle into the shelf",
       "Up into the cavity from below, then the foam pad and retainer plate on four M3 screws. Seen from below",
       elev=-25, azim=-50, label_done=False)
    d4 = d3 + [M["rec"], M["retainer"]]
    st(15, d4, [mv(M["ctrl"], (0, -100, 0)), mv(M["charger"], (0, -170, 0)), mv(M["straps"], (0, -260, 0))],
       "controller box, charger and straps",
       "Box on two M4 screws; charger back on the plate; each strap on two M5 screws. Wire as the wiring picture",
       elev=15, azim=-55, label_done=False)
    d5 = d4 + [M["ctrl"], M["charger"], M["straps"]]
    wall = part("Wall (non-combustible)", wall_context(P), COL["wall"])
    dock = part("Wall dock", S("plate", "shelf", "guide_l", "guide_r", "catch", "receptacle", "foam", "retainer",
                               "controller", "charger", "straps"), COL["plate"])
    st(16, [], [mv(dock, (0, -150, 0))], "dock onto the wall",
       "Four 6 mm screws into wall anchors; top of the shelf 0.8 to 1.2 m above the floor. Hold point: S5",
       context=[wall], elev=15, azim=-55)
    pack = part("Pack", S("tray", "pnuts", "housing", "pawl", "springs", "slider", "thumb", "plug", "holder_l", "holder_r",
                          "cells", "bms", "handle", "gasket", "lid", "wake"), COL["tray"])
    st(17, d5, [mv(pack, (0, 0, 240))], "pack into the dock",
       "Connector end down between the guides; it drops onto the shelf and the pawl clicks under the catch. Hold point: S6",
       context=[wall], elev=15, azim=-55, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 76); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    RED, BLU, GRY, BLK, ORG = "#B91C1C", "#1D4ED8", "#6B7280", "#111827", "#C2410C"
    ax.text(2, 74, "SwapCell prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 70.6, "Pack (left) and wall dock (right) meet at the plug and receptacle. Stranded silicone copper; "
            "wire sizes shown. No circuit board is laid out at this stage.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/swapcell", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def zone(x, y, w, h, text):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
        ax.text(x + 1.2, y + h - 1.2, text, fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

    zone(2, 8, 57, 58, "Inside the pack")
    zone(68, 8, 50, 58, "On the wall dock")
    blk(4, 44, 15, 15, "Cell block", "13S2P, 26 cells,\nnickel strip, fuse\nwire to each cell", ORG)
    blk(31, 44, 25, 15, "BMS board", "13S, CAN, balancing,\n30 A FETs on PACK+,\npre-charge, INTERLOCK wake", "#0F766E")
    blk(4, 26, 10, 10, "Wake", "sealed button\nin the lid", "#0F766E")
    blk(35, 26, 10, 10, "Fuse", "40 A, in\nPACK+", RED)
    blk(46, 10, 11, 11, "Plug", "P1, P2,\nS1 to S6", "#D4A017")
    blk(70, 10, 13, 11, "Receptacle", "pins, 10 kOhm\nINTERLOCK\nto SGND", "#D4A017")
    blk(90, 24, 25, 15, "Controller box", "ESP32, CAN transceiver\nwith 120 Ohm termination,\nDC relay, current sensor", "#0F766E")
    blk(90, 46, 25, 13, "Charger (certified)", "54.6 V, 5 A CC-CV,\n100 to 240 V AC in", "#374151")
    blk(70, 46, 15, 13, "Mains", "plug-in cord,\nRCD-protected\nsocket", BLK)
    # pack wiring
    wire([(19, 55), (31, 55)], RED); lab(25, 57, "B+ 6 mm²", RED, "center")
    wire([(19, 50), (31, 50)], GRY, 1.2); lab(25, 47.6, "13 sense leads\nand thermistors\n0.25 mm²", GRY, "center")
    wire([(40, 44), (40, 36)], RED); lab(40.6, 40, "PACK+ 6 mm²", RED)
    wire([(40, 26), (40, 18), (46, 18)], RED); lab(39.4, 21.5, "6 mm²", RED, "right")
    wire([(15, 44), (15, 40), (24, 40), (24, 14), (46, 14)], BLK); lab(34, 12.2, "B- to PACK- 6 mm²", BLK, "center")
    wire([(53, 44), (53, 21)], BLU, 1.2); lab(52.4, 30, "CAN, WAKE,\nINTERLOCK,\nSGND\n0.25 mm²", BLU, "right")
    wire([(14, 31), (28, 31), (28, 42), (33, 42), (33, 44)], GRY, 1.2); lab(21, 33, "button\n0.25 mm²", GRY, "center")
    # dock wiring
    wire([(58, 15.5), (70, 15.5)], "#D4A017", 3.0); lab(64, 18, "mates here", "#B45309", "center")
    wire([(83, 18), (95, 18), (95, 24)], RED); lab(89, 20.2, "PACK+, PACK- 2.5 mm²", RED, "center")
    wire([(83, 13), (110, 13), (110, 24)], BLU, 1.2); lab(97, 11.3, "CAN, SGND 0.25 mm², twisted pair", BLU, "center")
    wire([(102, 46), (102, 39)], RED); lab(102.6, 42.5, "54.6 V out, 2.5 mm²", RED)
    wire([(85, 52.5), (90, 52.5)], BLK, 2.4); lab(87.5, 61.5, "mains cord", BLK, "center")
    ax.text(70, 5.2, "Safety: the plug's power contacts stay dead until the BMS sees the coded INTERLOCK loop. "
            "Build the cell block one series group at a time with the BMS unplugged.", fontsize=7.4, color="#B45309", fontweight="bold",
            ha="center")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    i = 0
    while i < len(args):
        w = args[i]; i += 1
        nums = []
        while i < len(args) and args[i].isdigit():
            nums.append(int(args[i])); i += 1
        r = fns[w](set(nums)) if nums else fns[w]()
        print(w, "->", r)
