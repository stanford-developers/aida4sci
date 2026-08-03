"""Page mastheads for the AI + Data for Science site.

Art direction
-------------
Ground:  night by default — every page opens with a dark strip, against which
         the paper-white content below reads as a hard, deliberate contrast.
         The same geometry re-inks onto paper via set_theme(DAY).
Ink:     cardinal at three weights (hairline / structure / emphasis) plus one
         warm ember accent, used sparingly.
Form:    ONE dominant subject per masthead, generated from real mathematics
         (projected 3D backbones, Descartes circle packings, marching-squares
         level sets, sampled embeddings) — never assembled from clip-art motifs.
Layout:  the left 44% is deliberately quiet — that is where the page title
         lands. The subject weights right and bleeds off the edge, so each
         reads as a detail cropped from something larger.

The artwork carries no captions or numbering: a visitor sees a masthead, not
a plate in a catalogue, and anything they cannot decode is just noise.
"""
import math
import random

W, H = 1920, 460
TITLE_ZONE = 0.44  # left fraction kept quiet for page titles

# Two grounds, one drawing. The plates are inked on night by default — the
# site opens every page with a dark strip — and the same geometry re-inks onto
# paper for anywhere a light plate is wanted.
NIGHT = dict(PAPER="#171310", WASH="#241C17", CARDINAL="#C4443C", INK="#E8E2D9",
             GREY="#9A9086", HAIR="#3C332C", SAND="#E9A03E")
DAY = dict(PAPER="#FBFAF8", WASH="#F2EEE7", CARDINAL="#8C1515", INK="#2E2D29",
           GREY="#6E6A63", HAIR="#CFC9C0", SAND="#C9B896")

PAPER = WASH = CARDINAL = INK = GREY = HAIR = SAND = None


def set_theme(theme):
    global PAPER, WASH, CARDINAL, INK, GREY, HAIR, SAND
    PAPER, WASH = theme["PAPER"], theme["WASH"]
    CARDINAL, INK = theme["CARDINAL"], theme["INK"]
    GREY, HAIR, SAND = theme["GREY"], theme["HAIR"], theme["SAND"]


set_theme(NIGHT)


# ----------------------------------------------------------------- helpers
def head():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">\n'
            f'<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
            f'<defs><radialGradient id="wash" cx="0.72" cy="0.5" r="0.62">'
            f'<stop offset="0" stop-color="{WASH}" stop-opacity="0.95"/>'
            f'<stop offset="1" stop-color="{WASH}" stop-opacity="0"/>'
            f'</radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#wash)"/>\n')


def path_of(pts, close=False):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def mix_hex(a, b, t):
    """Blend two #rrggbb colors; t=0 gives a, t=1 gives b."""
    def rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    ca, cb = rgb(a), rgb(b)
    return "#%02X%02X%02X" % tuple(
        max(0, min(255, round(ca[k] + (cb[k] - ca[k]) * t))) for k in range(3))


def stipple(rng, n, region, density, color=None, rmin=0.7, rmax=2.0,
            omin=0.10, omax=0.34):
    """Jittered points, kept with probability `density(x, y)`; the quiet-left
    rule is applied by every caller's density function."""
    # resolved at call time, not definition time, so a theme switch is honored
    color = color or CARDINAL
    x0, y0, x1, y1 = region
    out = [f'<g fill="{color}">']
    tries = 0
    kept = 0
    while kept < n and tries < n * 40:
        tries += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if rng.random() > density(x, y):
            continue
        kept += 1
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(rmin, rmax):.1f}" '
                   f'opacity="{rng.uniform(omin, omax):.2f}"/>')
    out.append('</g>')
    return "\n".join(out)


def quiet_left(x, hard=TITLE_ZONE, soft=0.16):
    """Multiplier that fades everything out across the reserved title zone."""
    t = x / W
    if t > hard + soft:
        return 1.0
    if t < hard - soft:
        return 0.06
    return 0.06 + 0.94 * (t - (hard - soft)) / (2 * soft)


def marching_squares(f, level, bounds, nx=220, ny=90):
    """Level set of a scalar field as line segments (linear interpolation)."""
    x0, y0, x1, y1 = bounds
    dx, dy = (x1 - x0) / nx, (y1 - y0) / ny
    grid = [[f(x0 + i * dx, y0 + j * dy) for j in range(ny + 1)] for i in range(nx + 1)]
    segs = []

    def interp(pa, va, pb, vb):
        t = 0.5 if va == vb else (level - va) / (vb - va)
        return (pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t)

    for i in range(nx):
        for j in range(ny):
            px, py = x0 + i * dx, y0 + j * dy
            corners = [((px, py), grid[i][j]), ((px + dx, py), grid[i + 1][j]),
                       ((px + dx, py + dy), grid[i + 1][j + 1]), ((px, py + dy), grid[i][j + 1])]
            crossings = []
            for k in range(4):
                (pa, va), (pb, vb) = corners[k], corners[(k + 1) % 4]
                if (va < level) != (vb < level):
                    crossings.append(interp(pa, va, pb, vb))
            if len(crossings) == 2:
                segs.append((crossings[0], crossings[1]))
    return segs


def segs_to_svg(segs, color, width, opacity):
    if not segs:
        return ""
    d = " ".join(f"M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}" for a, b in segs)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" opacity="{opacity}"/>\n')


def ribbon(pts, widths, color, opacity=1.0):
    """Variable-width band around a polyline — a proper tapered ribbon."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        xa, ya = pts[max(0, i - 1)]
        xb, yb = pts[min(len(pts) - 1, i + 1)]
        tx, ty = xb - xa, yb - ya
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = widths[i]
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    outline = left + right[::-1]
    return (f'<path d="{path_of(outline, close=True)}" fill="{color}" '
            f'opacity="{opacity}"/>\n')


# ------------------------------------------------------------ I · THE FOLD
def plate_fold():
    """A protein backbone: real 3D helices and loops, projected and inked.

    Alpha helices are true parametric coils; the strand between them is a
    smooth interpolated loop. Confidence contours (a scalar field peaked on
    the fold) sit behind it, the way a predicted structure carries its own
    uncertainty.
    """
    rng = random.Random(21)
    s = head()

    def norm(v):
        L = math.sqrt(sum(c * c for c in v)) or 1
        return tuple(c / L for c in v)

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def helix(A, B, turns, radius, samples=150):
        """A true alpha helix: a coil of `turns` wound about the axis A→B."""
        axis = norm(tuple(B[k] - A[k] for k in range(3)))
        ref = (0, 0, 1) if abs(axis[2]) < 0.85 else (1, 0, 0)
        u = norm(cross(axis, ref))
        v = norm(cross(axis, u))
        span = math.dist(A, B)
        pts = []
        for i in range(samples):
            t = i / (samples - 1)
            a = 2 * math.pi * turns * t
            d = span * t
            pts.append(tuple(A[k] + axis[k] * d + radius * (u[k] * math.cos(a) + v[k] * math.sin(a))
                             for k in range(3)))
        return pts

    def catmull(p0, p1, p2, p3, n):
        out = []
        for i in range(n):
            t = i / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t +
                       (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 +
                       (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3)
                for k in range(3)))
        return out

    def strand(A, B, samples=34):
        """A beta strand: an almost-straight run with a slight natural twist."""
        pts = []
        for i in range(samples):
            t = i / (samples - 1)
            wob = math.sin(t * math.pi * 1.6) * 9
            pts.append((A[0] + (B[0] - A[0]) * t,
                        A[1] + (B[1] - A[1]) * t + wob,
                        A[2] + (B[2] - A[2]) * t + wob * 0.5))
        return pts

    # Backbone built in a local space, then rotated into a three-quarter view.
    # Secondary structure varies — two helices of different pitch and radius,
    # a beta strand, and irregular connecting loops — because a real fold is
    # not one motif repeated.
    # Local x is chosen so the fold starts clear of the title zone and its last
    # helix runs off the right edge — a crop of something larger.
    HELIX, LOOP, SHEET = "helix", "loop", "sheet"
    segments = [
        (helix((-390, 96, -62), (-215, -26, 50), 3.5, 33, 84), HELIX),
        (None, LOOP),
        (helix((-95, -84, 62), (95, 46, -52), 3.5, 29, 84), HELIX),
        (None, LOOP),
        (helix((175, -44, 46), (350, 62, -40), 3.0, 30, 76), HELIX),
        (None, LOOP),
        # the strand ends the chain, so its arrowhead runs off the right edge
        (strand((420, 22, -26), (580, -28, 24), 26), SHEET),
    ]

    chain, kinds = [], []
    for i, (pts, kind) in enumerate(segments):
        if kind == LOOP:
            a = segments[i - 1][0]
            b = segments[i + 1][0]
            pts = catmull(a[-2], a[-1], b[0], b[1], 24)
        chain += pts
        kinds += [kind] * len(pts)

    # three-quarter view
    YAW, PITCH = math.radians(19), math.radians(-13)
    CXP, CYP = 1370, 232

    SCALE = 1.2

    def place(p):
        x, y, z = p
        rx = x * math.cos(YAW) + z * math.sin(YAW)
        rz = -x * math.sin(YAW) + z * math.cos(YAW)
        ry = y * math.cos(PITCH) - rz * math.sin(PITCH)
        rz = y * math.sin(PITCH) + rz * math.cos(PITCH)
        return (CXP + rx * SCALE, CYP + ry * SCALE, rz)

    placed = [place(p) for p in chain]
    pts2 = [(p[0], p[1]) for p in placed]
    zs = [p[2] for p in placed]
    zmin, zmax = min(zs), max(zs)

    WIDTH = {HELIX: 17.0, SHEET: 19.0, LOOP: 6.5}

    # the density envelope behind the fold
    centers = [pts2[i] for i in range(0, len(pts2), 14)]

    def field(x, y):
        v = 0.0
        for cx, cy in centers:
            v += math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 26000)
        return v * quiet_left(x)

    for lv, op in ((0.30, 0.15), (0.62, 0.12), (1.05, 0.09)):
        s += segs_to_svg(marching_squares(field, lv, (760, 10, W, H - 20), 240, 100),
                         CARDINAL, 1.0, op)
    s += stipple(rng, 380, (700, 20, W, H - 30),
                 lambda x, y: 0.5 * quiet_left(x), rmax=1.8, omax=0.20)

    # Painter's algorithm, at the granularity of a *run*: the chain is cut
    # wherever it reverses in depth, so each run is one half-turn of a coil.
    # Runs are drawn far to near as single bands behind a ground-colored halo,
    # which makes near coils genuinely occlude far ones. (Haloing every small
    # quad instead would rib the ribbon like a caterpillar.)
    cuts = [0]
    for i in range(1, len(zs) - 1):
        if (zs[i + 1] - zs[i]) * (zs[i] - zs[i - 1]) < 0:
            cuts.append(i)
    cuts.append(len(zs) - 1)

    def normal_at(i):
        a = pts2[max(0, i - 1)]
        b = pts2[min(len(pts2) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        return (-dy / L, dx / L)

    runs = []
    for k in range(len(cuts) - 1):
        # overlap neighbours by a point so consecutive runs leave no gap
        lo = max(0, cuts[k] - 1)
        hi = min(len(pts2) - 1, cuts[k + 1] + 1)
        idx = list(range(lo, hi + 1))
        if len(idx) < 2:
            continue
        left, right = [], []
        for i in idx:
            nx, ny = normal_at(i)
            w = WIDTH[kinds[i]] / 2
            left.append((pts2[i][0] + nx * w, pts2[i][1] + ny * w))
            right.append((pts2[i][0] - nx * w, pts2[i][1] - ny * w))
        outline = left + right[::-1]
        runs.append((sum(zs[i] for i in idx) / len(idx), outline))

    halo = mix_hex(PAPER, CARDINAL, 0.14)
    for z, outline in sorted(runs, key=lambda r: r[0]):
        depth = (z - zmin) / (zmax - zmin or 1)
        # A far half-turn still has to read: it darkens toward the ground but
        # never sinks into it. Near ones warm toward the ember.
        if depth < 0.5:
            fill = mix_hex(PAPER, CARDINAL, 0.60 + 0.80 * depth)
        else:
            fill = mix_hex(CARDINAL, SAND, (depth - 0.5) * 0.6)
        d = path_of(outline, close=True)
        # a narrow halo separates overlapping turns without eating them
        s += (f'<path d="{d}" fill="{halo}" stroke="{halo}" stroke-width="4" '
              f'stroke-linejoin="round"/>\n')
        s += f'<path d="{d}" fill="{fill}"/>\n'

    # the strand's arrowhead, drawn at its own depth
    si = max(i for i, k in enumerate(kinds) if k == SHEET)
    (ax, ay), (bx, by) = pts2[si - 1], pts2[si]
    L = math.hypot(bx - ax, by - ay) or 1
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = -uy, ux
    head_w, head_l = 21.0, 38.0
    tip = (bx + ux * head_l, by + uy * head_l)
    arrow = [(bx + nx * head_w, by + ny * head_w), tip,
             (bx - nx * head_w, by - ny * head_w)]
    dep = (zs[si] - zmin) / (zmax - zmin or 1)
    s += (f'<path d="{path_of(arrow, close=True)}" fill="{halo}" stroke="{halo}" '
          f'stroke-width="4" stroke-linejoin="round"/>\n')
    s += (f'<path d="{path_of(arrow, close=True)}" '
          f'fill="{mix_hex(CARDINAL, SAND, max(0, dep - 0.5) * 0.62)}"/>\n')

    return s + "</svg>"


# ----------------------------------------------------------- II · THE PROOF
def plate_proof():
    """An Apollonian gasket built by Descartes' circle theorem, with three
    lines of Lean set as manuscript marginalia. A real theorem, drawn — not
    a soup of famous equations."""
    rng = random.Random(4)
    s = head()

    # Apollonian gasket by the Descartes reflection formula, in the complex
    # plane: given four mutually tangent circles, replacing one gives
    #   k' = 2(k1+k2+k3) - k4,  z' = (2(k1z1+k2z2+k3z3) - k4z4) / k'
    R = 214
    CX, CY = 1480, 206
    MIN_R = 2.2

    def circ(k, z, depth):
        return (k, z, depth)

    outer = circ(-1 / R, complex(CX, CY), 0)
    r_in = R * (2 * math.sqrt(3) - 3)
    inner = []
    for i in range(3):
        a = math.radians(90 + i * 120)
        d = R - r_in
        inner.append(circ(1 / r_in, complex(CX + d * math.cos(a), CY - d * math.sin(a)), 1))

    circles = [outer] + inner

    def recurse(c1, c2, c3, c4, depth):
        if depth > 9:
            return
        k1, z1, _ = c1
        k2, z2, _ = c2
        k3, z3, _ = c3
        k4, z4, _ = c4
        k = 2 * (k1 + k2 + k3) - k4
        if k <= 0 or 1 / k < MIN_R:
            return
        z = (2 * (k1 * z1 + k2 * z2 + k3 * z3) - k4 * z4) / k
        new = circ(k, z, depth)
        circles.append(new)
        recurse(c1, c2, new, c3, depth + 1)
        recurse(c1, c3, new, c2, depth + 1)
        recurse(c2, c3, new, c1, depth + 1)

    # (outer, in1, in2, in3) is already a Descartes quadruple — every circle
    # of the gasket follows from reflecting each member in turn
    base = [outer] + inner
    for i in range(4):
        others = [base[j] for j in range(4) if j != i]
        recurse(others[0], others[1], others[2], base[i], 2)

    # ink the gasket: outer ring heavy, interior lightening with depth
    for k, z, depth in circles:
        r = abs(1 / k)
        if depth == 0:
            s += (f'<circle cx="{z.real:.1f}" cy="{z.imag:.1f}" r="{r:.1f}" fill="none" '
                  f'stroke="{CARDINAL}" stroke-width="2.6" opacity="0.9"/>\n')
        else:
            op = max(0.14, 0.60 - depth * 0.055)
            wd = max(0.55, 1.8 - depth * 0.16)
            s += (f'<circle cx="{z.real:.1f}" cy="{z.imag:.1f}" r="{r:.1f}" fill="none" '
                  f'stroke="{CARDINAL}" stroke-width="{wd:.2f}" opacity="{op:.2f}"/>\n')
    # one circle picked out — the object of the proof
    bz = inner[0][1]
    s += (f'<circle cx="{bz.real:.1f}" cy="{bz.imag:.1f}" r="{r_in:.1f}" fill="{SAND}" '
          f'opacity="0.13"/>\n')

    # marginalia: Lean, set like a gloss with a hairline bracket
    mono = "'SF Mono', Menlo, Consolas, monospace"
    mx, my = 900, 250
    s += (f'<path d="M{mx-18} {my-24} L{mx-30} {my-24} L{mx-30} {my+72} L{mx-18} {my+72}" '
          f'fill="none" stroke="{HAIR}" stroke-width="1.2"/>\n')
    for i, line in enumerate([
            "theorem descartes (k&#8321; k&#8322; k&#8323; k&#8324; : &#8477;)",
            "  (h : tangent k&#8321; k&#8322; k&#8323; k&#8324;) :",
            "  (k&#8321;+k&#8322;+k&#8323;+k&#8324;)^2 =",
            "    2*(k&#8321;^2+k&#8322;^2+k&#8323;^2+k&#8324;^2) := by",
            "  field_simp [h, sq]; ring"]):
        s += (f'<text x="{mx}" y="{my + i * 26}" font-family="{mono}" font-size="16" '
              f'fill="{GREY}" opacity="{0.58 - i * 0.07:.2f}" xml:space="preserve">{line}</text>\n')

    s += stipple(rng, 260, (720, 40, W, H - 80),
                 lambda x, y: 0.34 * quiet_left(x), rmax=1.6, omax=0.16)
    return s + "</svg>"


# ------------------------------------------------------------ III · THE CELL
def plate_cell():
    """A single-cell embedding: sampled clusters as stipple, level-set hulls
    around them, one population picked out — the shape of a cell atlas."""
    rng = random.Random(9)
    s = head()

    clusters = [
        (1080, 268, 150, 88, 620, 0.30),
        (1400, 138, 118, 66, 430, 0.24),
        (1610, 318, 132, 78, 560, 0.26),
        (1880, 186, 104, 62, 340, 0.22),
        (1300, 372, 86, 46, 240, 0.20),
    ]
    # gaussian point clouds
    for i, (cx, cy, sx, sy, n, op) in enumerate(clusters):
        highlight = (i == 2)
        color = CARDINAL if highlight else GREY
        pts = []
        for _ in range(n):
            x = rng.gauss(cx, sx * 0.5)
            y = rng.gauss(cy, sy * 0.5)
            if quiet_left(x) < rng.random():
                continue
            pts.append((x, y))
        s += f'<g fill="{color}">'
        for x, y in pts:
            r = rng.uniform(1.8, 3.6) if highlight else rng.uniform(1.4, 2.8)
            o = rng.uniform(0.38, 0.78) if highlight else rng.uniform(0.20, 0.42)
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" opacity="{o:.2f}"/>'
        s += '</g>\n'

    # density hulls via marching squares over the mixture
    def field(x, y):
        v = 0.0
        for cx, cy, sx, sy, n, _ in clusters:
            v += n / 560 * math.exp(-(((x - cx) / (sx * 0.8)) ** 2 + ((y - cy) / (sy * 0.8)) ** 2))
        return v * quiet_left(x)

    s += segs_to_svg(marching_squares(field, 0.34, (700, 20, W, H - 60), 250, 105),
                     CARDINAL, 1.4, 0.34)
    s += segs_to_svg(marching_squares(field, 0.70, (700, 20, W, H - 60), 250, 105),
                     CARDINAL, 1.0, 0.20)

    # a trajectory through the manifold — pseudotime
    traj = [(1010, 300), (1180, 240), (1380, 176), (1520, 250), (1630, 322), (1800, 246), (1930, 196)]
    sm = []
    for i in range(len(traj) - 1):
        (x1, y1), (x2, y2) = traj[i], traj[i + 1]
        for t in [k / 12 for k in range(12)]:
            sm.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t - 16 * math.sin(math.pi * t)))
    s += (f'<path d="{path_of(sm)}" fill="none" stroke="{INK}" stroke-width="2" '
          f'opacity="0.5" stroke-dasharray="1 7" stroke-linecap="round"/>\n')
    s += (f'<circle cx="{traj[-1][0]}" cy="{traj[-1][1]}" r="6" fill="{INK}" opacity="0.75"/>\n')

    return s + "</svg>"


# ----------------------------------------------------------- IV · THE FIELD
def plate_field():
    """Level sets of a potential warped by three masses — read it as a lensed
    spacetime or a loss surface; both are what these machines search."""
    s = head()
    rng = random.Random(31)
    masses = [(1290, 232, 1.35), (1620, 150, 0.85), (1720, 350, 0.62)]

    def pot(x, y):
        v = 0.0
        for mx, my, m in masses:
            d = math.hypot(x - mx, y - my) + 26
            v += m * 9000 / d
        return v * quiet_left(x)

    lv = 14
    for i in range(lv):
        level = 26 + i * 15
        op = 0.42 - i * 0.021
        wd = 1.9 - i * 0.075
        s += segs_to_svg(marching_squares(pot, level, (700, 10, W, H - 50), 300, 120),
                         CARDINAL, max(0.6, wd), max(0.09, op))

    # geodesics bending through the field
    for y0 in (70, 130, 196, 268, 340, 404):
        pts = []
        x, y = 700.0, float(y0)
        vx, vy = 1.0, 0.0
        while x < W + 10:
            gx = (pot(x + 3, y) - pot(x - 3, y)) / 6
            gy = (pot(x, y + 3) - pot(x, y - 3)) / 6
            vx += -gx * 0.0016
            vy += -gy * 0.0016
            L = math.hypot(vx, vy) or 1
            vx, vy = vx / L, vy / L
            x += vx * 7
            y += vy * 7
            pts.append((x, y))
        s += (f'<path d="{path_of(pts)}" fill="none" stroke="{INK}" stroke-width="1.2" '
              f'opacity="0.28"/>\n')

    for mx, my, m in masses:
        s += (f'<circle cx="{mx}" cy="{my}" r="{7 + 7 * m:.0f}" fill="{PAPER}" opacity="0.9"/>'
              f'<circle cx="{mx}" cy="{my}" r="{4 + 5 * m:.0f}" fill="{CARDINAL}" opacity="0.92"/>\n')

    s += stipple(rng, 200, (700, 20, W, H - 60),
                 lambda x, y: 0.3 * quiet_left(x), color=INK, rmax=1.5, omax=0.14)
    return s + "</svg>"


# ------------------------------------------------------- V · THE ATTENTION
def plate_attention():
    """An attention matrix as a halftone grid, with the arcs it induces drawn
    beneath — the mechanism itself, rendered as an engraving."""
    rng = random.Random(17)
    s = head()

    n = 24
    cell = 14.0
    gx0, gy0 = 1400, 58

    # causal attention with a few strong heads
    heads = [(3, 0.9), (7, 0.55), (12, 0.4)]
    strength = {}
    for i in range(n):
        for j in range(i + 1):
            v = 0.10 + 0.55 * math.exp(-(i - j) / 4.5)
            for off, amp in heads:
                if i - j == off:
                    v += amp
            v *= 0.75 + 0.5 * rng.random()
            strength[(i, j)] = min(1.0, v)

    s += f'<g>'
    for (i, j), v in strength.items():
        x = gx0 + j * cell
        y = gy0 + i * cell
        r = 1.1 + 4.6 * v ** 1.7
        op = 0.16 + 0.7 * v ** 1.5
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{CARDINAL}" opacity="{op:.2f}"/>'
    s += '</g>\n'
    # grid frame
    s += (f'<rect x="{gx0 - cell/2:.1f}" y="{gy0 - cell/2:.1f}" width="{n*cell:.1f}" '
          f'height="{n*cell:.1f}" fill="none" stroke="{HAIR}" stroke-width="1.2"/>\n')

    # the arcs those weights induce, over a token axis
    ax0, ax1, ay = 860, 1900, 396
    s += f'<line x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}" stroke="{HAIR}" stroke-width="1.2"/>\n'
    xs = [ax0 + (ax1 - ax0) * k / (n - 1) for k in range(n)]
    # keep only the strongest, long-range arcs — a few decisive spans rather
    # than every weight, which would collapse into a moire of equal semicircles
    # deliberately span a RANGE of dependency lengths — taking the globally
    # strongest weights would return one offset over and over and collapse
    # the diagram into a chain of identical semicircles
    arcs = []
    for lo, hi, take in ((3, 4, 3), (5, 8, 4), (9, 13, 4), (14, 23, 4)):
        band = [((i, j), v) for (i, j), v in strength.items() if lo <= i - j <= hi]
        arcs += sorted(band, key=lambda kv: -kv[1])[:take]
    for (i, j), v in arcs:
        x1, x2 = xs[j], xs[i]
        span = abs(x2 - x1)
        h = 34 + span * 0.42        # taller for longer dependencies
        mid = (x1 + x2) / 2
        d = f"M{x1:.0f} {ay} C{x1 + span*0.22:.0f} {ay - h:.0f} {x2 - span*0.22:.0f} {ay - h:.0f} {x2:.0f} {ay}"
        op = (0.16 + 0.46 * v) * quiet_left(mid)
        s += (f'<path d="{d}" fill="none" stroke="{CARDINAL}" stroke-width="{0.9 + 2.4*v:.1f}" '
              f'opacity="{op:.2f}"/>\n')
    s += '<g>'
    for k, x in enumerate(xs):
        o = 0.55 * quiet_left(x)
        s += f'<circle cx="{x:.0f}" cy="{ay}" r="3" fill="{INK}" opacity="{o:.2f}"/>'
    s += '</g>\n'

    return s + "</svg>"


# ------------------------------------------------- FRONTISPIECE (home hero)
def plate_hero():
    """The home hero carries a centered lockup, so its plate is symmetric and
    pitched far quieter than the five — level sets of a wide, gentle field
    opening from the middle, with the center left clear for the wordmark."""
    rng = random.Random(41)
    global H
    H_save = H
    H = 620
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">\n'
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>\n')

    masses = [(300, 180, 1.0), (250, 470, 0.75), (1620, 165, 0.95),
              (1700, 470, 0.7), (960, 640, 0.9)]

    def pot(x, y):
        v = 0.0
        for mx, my, m in masses:
            v += m * 9000 / (math.hypot(x - mx, y - my) + 30)
        # fade out across the middle where the lockup sits
        c = 1 - 0.92 * math.exp(-(((x - 960) / 470) ** 2 + ((y - 250) / 200) ** 2))
        return v * c

    for i in range(16):
        s += segs_to_svg(marching_squares(pot, 24 + i * 13, (-20, -20, W + 20, H + 20), 300, 140),
                         CARDINAL, max(0.55, 1.5 - i * 0.06), max(0.05, 0.20 - i * 0.010))

    s += stipple(rng, 300, (0, 0, W, H),
                 lambda x, y: 0.5 * (1 - math.exp(-(((x - 960) / 500) ** 2 + ((y - 250) / 220) ** 2))),
                 rmax=1.7, omax=0.16)
    H = H_save
    return s + "</svg>"


PLATES = {
    "hero": plate_hero,
    "fold": plate_fold,
    "proof": plate_proof,
    "cell": plate_cell,
    "field": plate_field,
    "attention": plate_attention,
}


def main():
    import resvg_py
    from PIL import Image, ImageDraw
    names = list(PLATES)
    for label, theme, suffix, sheet_bg, text in (
            ("night", NIGHT, "", "#0E0B09", "#8A8079"),
            ("day", DAY, "-day", "#E9E5DE", "#555555")):
        set_theme(theme)
        for name, fn in PLATES.items():
            svg = fn()
            open(f"plate-{name}{suffix}.svg", "w").write(svg)
            open(f"plate-{name}{suffix}.png", "wb").write(
                bytes(resvg_py.svg_to_bytes(svg_string=svg, width=1100)))
        tiles = [Image.open(f"plate-{n}{suffix}.png") for n in names]
        w, h = tiles[0].size
        pad, lab = 14, 30
        img = Image.new("RGB", (w + 2 * pad, len(tiles) * (h + lab) + 2 * pad), sheet_bg)
        d = ImageDraw.Draw(img)
        for i, (t, nm) in enumerate(zip(tiles, names)):
            y = pad + i * (h + lab)
            img.paste(t, (pad, y))
            d.text((pad + 4, y + h + 6), nm.upper(), fill=text)
        img.save(f"plates-contact{suffix or '-night'}.png")
        print(f"generated {label}:", ", ".join(names))
    set_theme(NIGHT)


if __name__ == "__main__":
    main()
