"""Generate six AIDa4Sci logo concept marks as SVG + PNG previews."""
import math
import resvg_py
from PIL import Image, ImageDraw

CARDINAL = "#8C1515"
GOLD = "#E98300"
GREY = "#53565A"

# dark-mode palette swap for preview panels
DARK_MAP = {CARDINAL: "#E06C6C", GOLD: "#F5A952", GREY: "#C9C4BD", "#ffffff": "#1B1917"}


def wrap(body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" '
            f'viewBox="0 0 200 200" role="img" aria-label="{label}">\n{body}\n</svg>\n')


def concept_spark():
    """Data points flow along trajectories and converge into a burst of discovery."""
    b = []
    b.append(f'<g fill="none" stroke="{CARDINAL}" stroke-width="2.5" opacity="0.5" stroke-linecap="round">')
    b.append('<path d="M30 58 Q85 70 124 94"/>')
    b.append('<path d="M24 100 Q80 100 122 100"/>')
    b.append('<path d="M34 146 Q85 132 124 106"/>')
    b.append('</g>')
    dots = [(28,52,3.5,.6),(42,66,2.5,.4),(56,63,3,.5),(22,94,3,.55),(38,104,2.5,.35),
            (54,97,3.5,.5),(30,140,3,.5),(46,150,2.5,.35),(60,136,3.5,.55),(72,80,2.5,.4),
            (74,118,2.5,.4),(88,92,3,.45),(90,110,2.5,.4),(104,99,3,.5)]
    b.append(f'<g fill="{CARDINAL}">')
    for x, y, r, o in dots:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" opacity="{o}"/>')
    b.append('</g>')
    # burst
    b.append(f'<g stroke="{GOLD}" stroke-width="4" stroke-linecap="round">')
    for i in range(8):
        a = math.radians(i * 45)
        r0, r1 = 13, (30 if i % 2 == 0 else 21)
        x0, y0 = 132 + r0 * math.cos(a), 100 + r0 * math.sin(a)
        x1, y1 = 132 + r1 * math.cos(a), 100 + r1 * math.sin(a)
        b.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    b.append('</g>')
    b.append(f'<circle cx="132" cy="100" r="7" fill="{CARDINAL}"/>')
    return wrap("\n".join(b), "Convergence spark")


def concept_iris():
    """An eye/iris whose web is a radial neural network — seeing science through AI."""
    b = [f'<circle cx="100" cy="100" r="80" fill="none" stroke="{CARDINAL}" stroke-width="4"/>']
    nodes = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        nodes.append((100 + 52 * math.cos(a), 100 + 52 * math.sin(a)))
    # chords (octagon)
    b.append(f'<g stroke="{CARDINAL}" stroke-width="2" opacity="0.45" fill="none">')
    for i in range(8):
        x1, y1 = nodes[i]
        x2, y2 = nodes[(i + 1) % 8]
        b.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    b.append('</g>')
    # spokes
    b.append(f'<g stroke="{CARDINAL}" stroke-width="3" opacity="0.8" fill="none">')
    for x, y in nodes:
        b.append(f'<line x1="100" y1="100" x2="{x:.1f}" y2="{y:.1f}"/>')
    b.append('</g>')
    # scatter between web and rim
    b.append(f'<g fill="{CARDINAL}" opacity="0.3">')
    for i in range(10):
        a = math.radians(i * 36 + 18)
        r = 66
        b.append(f'<circle cx="{100 + r * math.cos(a):.1f}" cy="{100 + r * math.sin(a):.1f}" '
                 f'r="{2.5 if i % 2 else 3.5}"/>')
    b.append('</g>')
    b.append(f'<g fill="{CARDINAL}">')
    for x, y in nodes:
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5"/>')
    b.append('</g>')
    b.append(f'<circle cx="100" cy="100" r="15" fill="{CARDINAL}"/>')
    b.append('<circle cx="95" cy="95" r="4" fill="#ffffff" opacity="0.85"/>')
    return wrap("\n".join(b), "Iris network")


def concept_helix():
    """Double helix: one strand is a fitted model curve, the other is data points."""
    y0, y1 = 22, 178
    amp, cx = 30, 100

    def xa(y):
        t = (y - y0) / (y1 - y0)
        return cx + amp * math.sin(3 * math.pi * t - math.pi / 2)

    def xb(y):
        return 2 * cx - xa(y)

    pts = [(xa(y), y) for y in [y0 + i * (y1 - y0) / 96 for i in range(97)]]
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    b = []
    # rungs where strands are far apart
    b.append(f'<g stroke="{GREY}" stroke-width="2.5" opacity="0.55">')
    for i in range(1, 12):
        y = y0 + i * (y1 - y0) / 12
        x_a, x_b = xa(y), xb(y)
        if abs(x_a - x_b) > 34:
            b.append(f'<line x1="{x_a:.1f}" y1="{y:.1f}" x2="{x_b:.1f}" y2="{y:.1f}"/>')
    b.append('</g>')
    b.append(f'<path d="{path}" fill="none" stroke="{CARDINAL}" stroke-width="5" stroke-linecap="round"/>')
    # data-dot strand
    b.append(f'<g fill="{CARDINAL}" opacity="0.55">')
    for i in range(21):
        y = y0 + i * (y1 - y0) / 20
        b.append(f'<circle cx="{xb(y):.1f}" cy="{y:.1f}" r="3.6"/>')
    b.append('</g>')
    # terminal emphasis
    b.append(f'<circle cx="{xa(y1):.1f}" cy="{y1}" r="7" fill="{CARDINAL}"/>')
    b.append(f'<circle cx="{xb(y0):.1f}" cy="{y0}" r="7" fill="{GOLD}"/>')
    return wrap("\n".join(b), "Data helix")


def concept_molecule():
    """Molecule ring fused with circuit traces — wet lab meets silicon."""
    cxh, cyh, r = 84, 100, 40
    verts = []
    for i in range(6):
        a = math.radians(30 + i * 60)
        verts.append((cxh + r * math.cos(a), cyh + r * math.sin(a)))
    ring = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in verts) + " Z"
    b = [f'<path d="{ring}" fill="none" stroke="{CARDINAL}" stroke-width="5" stroke-linejoin="round"/>']
    # inner double-bond hints on alternating edges
    b.append(f'<g stroke="{CARDINAL}" stroke-width="2.5" opacity="0.5">')
    for i in (0, 2, 4):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % 6]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        f = 0.72
        b.append(f'<line x1="{cxh + (x1 - cxh) * f:.1f}" y1="{cyh + (y1 - cyh) * f:.1f}" '
                 f'x2="{cxh + (x2 - cxh) * f:.1f}" y2="{cyh + (y2 - cyh) * f:.1f}"/>')
    b.append('</g>')
    # circuit traces from the two right vertices
    vtr, vbr = verts[5], verts[0]  # top-right (330 deg), bottom-right (30 deg)
    b.append(f'<g stroke="{GREY}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">')
    b.append(f'<path d="M{vtr[0]:.1f} {vtr[1]:.1f} H150 V46"/>')
    b.append(f'<path d="M{vbr[0]:.1f} {vbr[1]:.1f} H142 V154"/>')
    b.append('</g>')
    b.append(f'<rect x="143" y="32" width="14" height="14" rx="3" fill="{GOLD}"/>')
    b.append(f'<rect x="135" y="154" width="14" height="14" rx="3" fill="{GOLD}"/>')
    # atoms
    b.append(f'<g fill="{CARDINAL}">')
    for x, y in verts:
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6"/>')
    b.append('</g>')
    return wrap("\n".join(b), "Molecule circuit")


def concept_ascent():
    """A cloud of measurements, a fitted curve rising through it to a summit."""
    dots = [(30,158,3),(42,150,2.5),(52,160,3.5),(60,142,2.5),(70,148,3),(78,128,3.5),
            (88,136,2.5),(96,118,3),(106,124,3.5),(112,104,2.5),(122,110,3),(128,92,3.5),
            (136,98,2.5),(142,80,3),(150,64,2.5),(148,86,3)]
    curve = "M24 166 C70 162 105 132 132 100 C145 84 152 66 158 48"
    b = []
    # residual whiskers from a few points toward the curve
    b.append(f'<g stroke="{CARDINAL}" stroke-width="1.5" opacity="0.25">')
    for x, y, dy in [(52,160,-8),(78,128,10),(106,124,-9),(128,92,9),(148,86,-10)]:
        b.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + dy}"/>')
    b.append('</g>')
    b.append(f'<g fill="{CARDINAL}" opacity="0.45">')
    for x, y, r in dots:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
    b.append('</g>')
    b.append(f'<path d="{curve}" fill="none" stroke="{CARDINAL}" stroke-width="5" stroke-linecap="round"/>')
    b.append(f'<g stroke="{GOLD}" stroke-width="3.5" stroke-linecap="round">')
    for adeg, ln in [(-20, 16), (-65, 20), (-110, 16), (-155, 14)]:
        a = math.radians(adeg)
        x0, y0 = 158 + 12 * math.cos(a), 48 + 12 * math.sin(a)
        x1, y1 = 158 + (12 + ln) * math.cos(a), 48 + (12 + ln) * math.sin(a)
        b.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    b.append('</g>')
    b.append(f'<circle cx="158" cy="48" r="8" fill="{CARDINAL}"/>')
    return wrap("\n".join(b), "Ascent")


def concept_four():
    """The '4' of AIDa4Sci drawn as a network of nodes and edges."""
    apex, elbow, rend, bottom, cross = (118, 38), (62, 122), (152, 122), (118, 166), (118, 122)
    b = []
    b.append(f'<g stroke="{CARDINAL}" stroke-width="10" stroke-linecap="round">')
    for (x1, y1), (x2, y2) in [(apex, elbow), (elbow, rend), (apex, bottom)]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    b.append('</g>')
    # faint constellation context
    b.append(f'<g fill="{CARDINAL}" opacity="0.28">')
    for x, y, r in [(44,52,3),(160,60,2.5),(38,164,2.5),(168,158,3),(88,74,2.5),(150,92,2.5)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
    b.append('</g>')
    b.append(f'<g fill="{CARDINAL}">')
    for (x, y), r in [(apex, 9), (elbow, 9), (rend, 9), (cross, 7)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
    b.append('</g>')
    b.append(f'<circle cx="{bottom[0]}" cy="{bottom[1]}" r="11" fill="{GOLD}"/>')
    return wrap("\n".join(b), "Network four")


CONCEPTS = {
    "spark": concept_spark,
    "iris": concept_iris,
    "helix": concept_helix,
    "molecule": concept_molecule,
    "ascent": concept_ascent,
    "four": concept_four,
}


def main():
    names = []
    for name, fn in CONCEPTS.items():
        svg = fn()
        with open(f"{name}.svg", "w") as f:
            f.write(svg)
        dark = svg
        for old, new in DARK_MAP.items():
            dark = dark.replace(old, new)
        with open(f"{name}-dark.svg", "w") as f:
            f.write(dark)
        for src, dst, bg in [(f"{name}.svg", f"{name}.png", "#ffffff"),
                             (f"{name}-dark.svg", f"{name}-dark.png", "#1B1917")]:
            png = resvg_py.svg_to_bytes(svg_path=src, width=420, background=bg)
            open(dst, "wb").write(bytes(png))
        names.append(name)

    # contact sheets
    for suffix, sheet in [("", "contact-light.png"), ("-dark", "contact-dark.png")]:
        tiles = [Image.open(f"{n}{suffix}.png") for n in names]
        w, h = tiles[0].size
        pad, label_h = 20, 40
        img = Image.new("RGB", (3 * w + 4 * pad, 2 * (h + label_h) + 3 * pad),
                        "#ffffff" if not suffix else "#1B1917")
        d = ImageDraw.Draw(img)
        for i, (t, n) in enumerate(zip(tiles, names)):
            r, c = divmod(i, 3)
            x, y = pad + c * (w + pad), pad + r * (h + label_h + pad)
            img.paste(t, (x, y))
            d.text((x + w // 2 - 5 * len(n), y + h + 8), n.upper(),
                   fill="#53565A" if not suffix else "#C9C4BD")
        img.save(sheet)
    print("generated:", ", ".join(names))


if __name__ == "__main__":
    main()
