"""Génère les illustrations SVG du site (style flat, palette du site).

Usage : python3 scripts/illustrations.py public/images/illustrations
"""
import math
import random
import sys

OUT = sys.argv[1]

# Palette du site
R, RD, O, Y = "#c0262d", "#9e1d23", "#f08a24", "#f7b733"
CR, CR2, CR3 = "#fff6ee", "#fbe9da", "#f4d9c2"
PK, PR, NV = "#f6c9cf", "#a3284f", "#1f2a44"
BL, LB, GR, GRD = "#3d6fb6", "#dbe8f6", "#6cbf84", "#3f9a5c"
W, BR = "#ffffff", "#8a5a3b"
SKIN = ["#f6d2b3", "#e2a97f", "#bf7f55", "#7d4b2f"]
HAIR = ["#2b2240", "#6b3e26", "#d39a3a", "#1c1c1c", "#9a3f28"]


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f"{body}</svg>\n")


# ---------- formes de base ----------

def blob(cx, cy, r, seed=1, n=9, var=0.1, fill=CR2):
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + rnd.uniform(-var, var))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    # Catmull-Rom fermé -> Bézier
    d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return f'<path d="{d}Z" fill="{fill}"/>'


def heart(cx, cy, size, fill, rot=0):
    d = ("M0,0.42 C-0.6,0.02 -0.58,-0.46 -0.26,-0.46 C-0.1,-0.46 0,-0.36 0,-0.24 "
         "C0,-0.36 0.1,-0.46 0.26,-0.46 C0.58,-0.46 0.6,0.02 0,0.42Z")
    return (f'<path d="{d}" fill="{fill}" '
            f'transform="translate({f(cx)} {f(cy)}) rotate({rot}) scale({f(size)})"/>')


def sparkle(cx, cy, r, fill):
    d = "M0,-1 Q0.14,-0.14 1,0 Q0.14,0.14 0,1 Q-0.14,0.14 -1,0 Q-0.14,-0.14 0,-1Z"
    return f'<path d="{d}" fill="{fill}" transform="translate({f(cx)} {f(cy)}) scale({f(r)})"/>'


def star(cx, cy, r, fill, rot=0):
    pts = []
    for i in range(10):
        a = math.radians(-90 + 36 * i + rot)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{f(cx + rr * math.cos(a))},{f(cy + rr * math.sin(a))}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{fill}" stroke-width="{f(r*0.12)}" stroke-linejoin="round"/>'


def cloud(cx, cy, s, fill=W):
    return (f'<g fill="{fill}"><circle cx="{f(cx-18*s)}" cy="{f(cy+4*s)}" r="{f(14*s)}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy-6*s)}" r="{f(20*s)}"/>'
            f'<circle cx="{f(cx+20*s)}" cy="{f(cy+3*s)}" r="{f(15*s)}"/>'
            f'<rect x="{f(cx-32*s)}" y="{f(cy+2*s)}" width="{f(66*s)}" height="{f(16*s)}" rx="{f(8*s)}"/></g>')


def tree(cx, base, s, crown, crown2):
    return (f'<rect x="{f(cx-5*s)}" y="{f(base-60*s)}" width="{f(10*s)}" height="{f(60*s)}" rx="{f(4*s)}" fill="{BR}"/>'
            f'<path d="M{f(cx)},{f(base-38*s)} l{f(-14*s)},{f(-14*s)}" stroke="{BR}" stroke-width="{f(5*s)}" stroke-linecap="round"/>'
            f'<circle cx="{f(cx)}" cy="{f(base-88*s)}" r="{f(36*s)}" fill="{crown}"/>'
            f'<circle cx="{f(cx-22*s)}" cy="{f(base-66*s)}" r="{f(22*s)}" fill="{crown}"/>'
            f'<circle cx="{f(cx+24*s)}" cy="{f(base-70*s)}" r="{f(24*s)}" fill="{crown}"/>'
            f'<circle cx="{f(cx+10*s)}" cy="{f(base-104*s)}" r="{f(16*s)}" fill="{crown2}" opacity="0.55"/>')


def shadow(cx, cy, rx, ry, fill=CR3):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"/>'


# ---------- personnages ----------

def hair_back(cx, hy, r, style, color):
    if style == "long":
        return f'<rect x="{f(cx-r*1.15)}" y="{f(hy-r*0.9)}" width="{f(r*2.3)}" height="{f(r*2.9)}" rx="{f(r)}" fill="{color}"/>'
    if style == "pony":
        return f'<ellipse cx="{f(cx+r*1.05)}" cy="{f(hy+r*0.35)}" rx="{f(r*0.42)}" ry="{f(r*0.85)}" fill="{color}" transform="rotate(-18 {f(cx+r*1.05)} {f(hy+r*0.35)})"/>'
    if style == "bun":
        return f'<circle cx="{f(cx)}" cy="{f(hy-r*1.08)}" r="{f(r*0.45)}" fill="{color}"/>'
    if style == "curly":
        out = ""
        for a in range(-200, 21, 22):
            ar = math.radians(a)
            out += f'<circle cx="{f(cx+r*1.0*math.cos(ar))}" cy="{f(hy+r*1.0*math.sin(ar))}" r="{f(r*0.36)}" fill="{color}"/>'
        return out
    return ""


def hair_front(cx, hy, r, style, color):
    if style == "bald":
        return ""
    k = 1.38 if style != "short" else 1.3
    d = (f"M{f(cx-r*1.02)},{f(hy+r*0.1)} C{f(cx-r*1.02)},{f(hy-r*k)} {f(cx+r*1.02)},{f(hy-r*k)} {f(cx+r*1.02)},{f(hy+r*0.1)} "
         f"C{f(cx+r*0.7)},{f(hy-r*0.3)} {f(cx+r*0.1)},{f(hy-r*0.52)} {f(cx-r*0.35)},{f(hy-r*0.42)} "
         f"C{f(cx-r*0.7)},{f(hy-r*0.3)} {f(cx-r*0.9)},{f(hy-r*0.1)} {f(cx-r*1.02)},{f(hy+r*0.1)}Z")
    return f'<path d="{d}" fill="{color}"/>'


def face(cx, hy, r):
    """Visage minimal : deux yeux et un sourire."""
    return (f'<circle cx="{f(cx-r*0.36)}" cy="{f(hy+r*0.12)}" r="{f(r*0.09)}" fill="{NV}"/>'
            f'<circle cx="{f(cx+r*0.36)}" cy="{f(hy+r*0.12)}" r="{f(r*0.09)}" fill="{NV}"/>'
            f'<path d="M{f(cx-r*0.3)},{f(hy+r*0.42)} Q{f(cx)},{f(hy+r*0.68)} {f(cx+r*0.3)},{f(hy+r*0.42)}" '
            f'stroke="{NV}" stroke-width="{f(r*0.09)}" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{f(cx-r*0.6)}" cy="{f(hy+r*0.42)}" r="{f(r*0.14)}" fill="{PK}" opacity="0.8"/>'
            f'<circle cx="{f(cx+r*0.6)}" cy="{f(hy+r*0.42)}" r="{f(r*0.14)}" fill="{PK}" opacity="0.8"/>')


def arm(x, y, length, angle, width, sleeve, skin):
    """angle en degrés : 0 = vers le bas, 90 = vers l'extérieur droit, -90 = gauche, ±180 = vers le haut."""
    a = math.radians(angle)
    ex, ey = x + length * math.sin(a), y + length * math.cos(a)
    mx, my = x + length * 0.45 * math.sin(a), y + length * 0.45 * math.cos(a)
    return (f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(ex)}" y2="{f(ey)}" stroke="{skin}" stroke-width="{f(width)}" stroke-linecap="round"/>'
            f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(mx)}" y2="{f(my)}" stroke="{sleeve}" stroke-width="{f(width*1.25)}" stroke-linecap="round"/>')


def bust(cx, sy, s, skin, hair, shirt, style="short", raise_arm=None, collar=W):
    """Buste (épaules en sy)."""
    r = 22 * s
    hy = sy - 36 * s
    out = hair_back(cx, hy, r, style, hair)
    if raise_arm:
        sgn = 1 if raise_arm == "right" else -1
        sx, sy0, L, ang = cx + sgn * 30 * s, sy + 16 * s, 60 * s, sgn * 172
        out += arm(sx, sy0, L, ang, 13 * s, shirt, skin)
        a = math.radians(ang)
        out += f'<circle cx="{f(sx + L*math.sin(a))}" cy="{f(sy0 + L*math.cos(a))}" r="{f(9*s)}" fill="{skin}"/>'
    out += f'<rect x="{f(cx-8*s)}" y="{f(hy+10*s)}" width="{f(16*s)}" height="{f(sy-hy)}" rx="{f(6*s)}" fill="{skin}"/>'
    out += (f'<path d="M{f(cx-44*s)},{f(sy+90*s)} L{f(cx-44*s)},{f(sy+22*s)} Q{f(cx-44*s)},{f(sy)} {f(cx-22*s)},{f(sy)} '
            f'L{f(cx+22*s)},{f(sy)} Q{f(cx+44*s)},{f(sy)} {f(cx+44*s)},{f(sy+22*s)} L{f(cx+44*s)},{f(sy+90*s)}Z" fill="{shirt}"/>')
    out += f'<path d="M{f(cx-10*s)},{f(sy)} L{f(cx)},{f(sy+11*s)} L{f(cx+10*s)},{f(sy)}Z" fill="{skin}"/>'
    out += f'<circle cx="{f(cx)}" cy="{f(hy)}" r="{f(r)}" fill="{skin}"/>'
    out += hair_front(cx, hy, r, style, hair)
    out += face(cx, hy, r)
    return out


def kid(cx, fy, s, skin, hair, shirt, pants, style="short", arms=(-25, 25), spread=6, backpack=None):
    r = 17 * s
    hip = fy - 30 * s
    sh = hip - 34 * s
    hy = sh - 20 * s
    out = ""
    if backpack:
        out += f'<rect x="{f(cx-20*s)}" y="{f(sh+2*s)}" width="{f(40*s)}" height="{f(30*s)}" rx="{f(8*s)}" fill="{backpack}"/>'
    for side, sgn in ((arms[0], -1), (arms[1], 1)):
        out += arm(cx + sgn * 13 * s, sh + 6 * s, 30 * s, side, 7.5 * s, shirt, skin)
    for sgn in (-1, 1):
        x1 = cx + sgn * 7 * s
        x2 = x1 + sgn * spread * s
        out += f'<line x1="{f(x1)}" y1="{f(hip)}" x2="{f(x2)}" y2="{f(fy-5*s)}" stroke="{pants}" stroke-width="{f(10*s)}" stroke-linecap="round"/>'
        out += f'<ellipse cx="{f(x2+sgn*3*s)}" cy="{f(fy-2*s)}" rx="{f(8*s)}" ry="{f(4.5*s)}" fill="{NV}"/>'
    out += f'<rect x="{f(cx-17*s)}" y="{f(sh)}" width="{f(34*s)}" height="{f(40*s)}" rx="{f(12*s)}" fill="{shirt}"/>'
    if backpack:
        out += f'<line x1="{f(cx-10*s)}" y1="{f(sh+2*s)}" x2="{f(cx-10*s)}" y2="{f(sh+26*s)}" stroke="{backpack}" stroke-width="{f(4*s)}" stroke-linecap="round"/>'
        out += f'<line x1="{f(cx+10*s)}" y1="{f(sh+2*s)}" x2="{f(cx+10*s)}" y2="{f(sh+26*s)}" stroke="{backpack}" stroke-width="{f(4*s)}" stroke-linecap="round"/>'
    out += hair_back(cx, hy, r, style, hair)
    out += f'<circle cx="{f(cx)}" cy="{f(hy)}" r="{f(r)}" fill="{skin}"/>'
    out += hair_front(cx, hy, r, style, hair)
    out += face(cx, hy, r)
    return out


# ---------- bâtiments ----------

def house(cx, base, s):
    return (f'<path d="M{f(cx-38*s)},{f(base-50*s)} L{f(cx)},{f(base-84*s)} L{f(cx+38*s)},{f(base-50*s)}Z" fill="{R}" stroke="{R}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>'
            f'<rect x="{f(cx-30*s)}" y="{f(base-52*s)}" width="{f(60*s)}" height="{f(52*s)}" rx="{f(3*s)}" fill="#ffe2b8"/>'
            f'<rect x="{f(cx+8*s)}" y="{f(base-30*s)}" width="{f(14*s)}" height="{f(30*s)}" rx="{f(3*s)}" fill="{RD}"/>'
            + heart(cx - 10 * s, base - 30 * s, 20 * s, R))


def school(cx, base, s, roof=O):
    out = (f'<rect x="{f(cx-44*s)}" y="{f(base-54*s)}" width="{f(88*s)}" height="{f(54*s)}" rx="{f(3*s)}" fill="#fde2c3"/>'
           f'<path d="M{f(cx-50*s)},{f(base-52*s)} L{f(cx)},{f(base-86*s)} L{f(cx+50*s)},{f(base-52*s)}Z" fill="{roof}" stroke="{roof}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>'
           f'<circle cx="{f(cx)}" cy="{f(base-64*s)}" r="{f(9*s)}" fill="{W}"/>'
           f'<path d="M{f(cx)},{f(base-70*s)} V{f(base-64*s)} H{f(cx+5*s)}" stroke="{NV}" stroke-width="{f(2*s)}" fill="none" stroke-linecap="round"/>'
           f'<line x1="{f(cx)}" y1="{f(base-86*s)}" x2="{f(cx)}" y2="{f(base-106*s)}" stroke="{NV}" stroke-width="{f(2.5*s)}" stroke-linecap="round"/>'
           f'<path d="M{f(cx)},{f(base-106*s)} h{f(14*s)} l{f(-4*s)},{f(5*s)} l{f(4*s)},{f(5*s)} h{f(-14*s)}Z" fill="{R}"/>'
           f'<path d="M{f(cx-9*s)},{f(base)} V{f(base-18*s)} a{f(9*s)},{f(9*s)} 0 0 1 {f(18*s)},0 V{f(base)}Z" fill="{R}"/>')
    for x in (-34, -20, 12, 26):
        for y in (-44, -26):
            out += f'<rect x="{f(cx+x*s)}" y="{f(base+y*s)}" width="{f(9*s)}" height="{f(11*s)}" rx="{f(1.5*s)}" fill="{LB}"/>'
    return out


def mairie(cx, base, s):
    out = (f'<rect x="{f(cx-46*s)}" y="{f(base-8*s)}" width="{f(92*s)}" height="{f(8*s)}" rx="{f(2*s)}" fill="{NV}"/>'
           f'<rect x="{f(cx-40*s)}" y="{f(base-50*s)}" width="{f(80*s)}" height="{f(42*s)}" fill="#f7dcc0"/>'
           f'<path d="M{f(cx-48*s)},{f(base-50*s)} L{f(cx)},{f(base-76*s)} L{f(cx+48*s)},{f(base-50*s)}Z" fill="{NV}" stroke="{NV}" stroke-width="{f(4*s)}" stroke-linejoin="round"/>'
           f'<circle cx="{f(cx)}" cy="{f(base-60*s)}" r="{f(5*s)}" fill="{Y}"/>')
    for x in (-32, -16, 8, 24):
        out += f'<rect x="{f(cx+x*s)}" y="{f(base-48*s)}" width="{f(8*s)}" height="{f(40*s)}" fill="{W}"/>'
    out += (f'<line x1="{f(cx)}" y1="{f(base-76*s)}" x2="{f(cx)}" y2="{f(base-98*s)}" stroke="{NV}" stroke-width="{f(2.5*s)}" stroke-linecap="round"/>'
            f'<rect x="{f(cx)}" y="{f(base-98*s)}" width="{f(6*s)}" height="{f(11*s)}" fill="{BL}"/>'
            f'<rect x="{f(cx+6*s)}" y="{f(base-98*s)}" width="{f(6*s)}" height="{f(11*s)}" fill="{W}"/>'
            f'<rect x="{f(cx+12*s)}" y="{f(base-98*s)}" width="{f(6*s)}" height="{f(11*s)}" fill="{R}"/>')
    return out


def paper(x, y, w, h, rot=0, lines=3, check=False):
    out = f'<g transform="rotate({rot} {f(x+w/2)} {f(y+h/2)})"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="4" fill="{W}"/>'
    for i in range(lines):
        ly = y + 12 + i * (h - 20) / max(1, lines - 1) if lines > 1 else y + h / 2
        if check:
            out += (f'<path d="M{f(x+8)},{f(ly)} l4,4 l7,-8" stroke="{GRD}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<line x1="{f(x+26)}" y1="{f(ly)}" x2="{f(x+w-8)}" y2="{f(ly)}" stroke="{CR3}" stroke-width="4" stroke-linecap="round"/>')
        else:
            out += f'<line x1="{f(x+8)}" y1="{f(ly)}" x2="{f(x+w-8-(i%2)*10)}" y2="{f(ly)}" stroke="{CR3}" stroke-width="4" stroke-linecap="round"/>'
    return out + "</g>"


def bubble(x, y, w, h, fill, tail="left", content=""):
    tx = x + 18 if tail == "left" else x + w - 18
    d = tail == "left" and -1 or 1
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2.4)}" fill="{fill}"/>'
            f'<path d="M{f(tx-8)},{f(y+h-2)} L{f(tx+d*6)},{f(y+h+14)} L{f(tx+8)},{f(y+h-2)}Z" fill="{fill}"/>' + content)


def dots(cx, cy, fill, gap=12, r=4):
    return "".join(f'<circle cx="{f(cx+i*gap)}" cy="{f(cy)}" r="{r}" fill="{fill}"/>' for i in (-1, 0, 1))


# ---------- illustrations ----------

def bien_etre():
    b = blob(200, 206, 168, seed=3)
    b += f'<circle cx="318" cy="88" r="30" fill="{Y}"/><circle cx="318" cy="88" r="42" fill="{Y}" opacity="0.25"/>'
    b += heart(200, 212, 300, PK)
    b += shadow(200, 344, 110, 14)
    b += kid(200, 342, 2.55, SKIN[0], HAIR[2], R, NV, "pony", arms=(-150, 150), spread=10)
    b += heart(112, 128, 44, R, -12) + heart(292, 176, 30, O, 14)
    b += sparkle(92, 222, 11, Y) + sparkle(322, 262, 9, O) + sparkle(150, 66, 8, Y) + sparkle(250, 60, 6, R)
    return svg(400, 400, b)


def lien():
    b = blob(200, 206, 170, seed=7)
    A, B, C = (110, 132), (290, 132), (200, 296)
    dash = f'stroke="{O}" stroke-width="5" stroke-dasharray="1 13" stroke-linecap="round" fill="none"'
    b += f'<path d="M{A[0]},{A[1]} Q200,92 {B[0]},{B[1]}" {dash}/>'
    b += f'<path d="M{B[0]},{B[1]} Q282,230 {C[0]},{C[1]}" {dash}/>'
    b += f'<path d="M{C[0]},{C[1]} Q118,230 {A[0]},{A[1]}" {dash}/>'
    for (x, y) in (A, B, C):
        b += f'<circle cx="{x}" cy="{y+5}" r="60" fill="{CR3}"/><circle cx="{x}" cy="{y}" r="60" fill="{W}"/>'
    b += house(A[0], A[1] + 32, 0.95) + school(B[0], B[1] + 34, 0.72) + mairie(C[0], C[1] + 34, 0.8)
    b += bubble(168, 178, 64, 40, R, "left", dots(200, 198, W, 13, 4.5))
    b += heart(200, 100, 22, R) + heart(300, 222, 18, O, 20) + heart(100, 222, 18, O, -20)
    return svg(400, 400, b)


def conseils():
    b = blob(200, 206, 170, seed=11)
    b += bubble(62, 64, 98, 50, O, "right",
                f'<line x1="80" y1="82" x2="140" y2="82" stroke="{W}" stroke-width="5" stroke-linecap="round"/>'
                f'<line x1="80" y1="97" x2="124" y2="97" stroke="{W}" stroke-width="5" stroke-linecap="round"/>')
    b += bubble(250, 52, 82, 46, LB, "left", dots(291, 75, NV, 14, 4.5))
    b += bust(104, 256, 1.15, SKIN[1], HAIR[0], BL, "curly")
    b += bust(296, 256, 1.15, SKIN[3], HAIR[3], O, "short")
    b += bust(200, 240, 1.25, SKIN[0], HAIR[4], R, "long", raise_arm="right")
    b += f'<rect x="36" y="284" width="328" height="24" rx="12" fill="{NV}"/>'
    b += f'<rect x="58" y="304" width="284" height="70" rx="10" fill="{RD}"/>'
    b += star(200, 340, 18, Y)
    b += paper(80, 262, 54, 30, -6, 2) + paper(250, 256, 60, 36, 5, 2, check=True)
    b += f'<rect x="170" y="268" width="36" height="20" rx="4" fill="{W}"/><rect x="176" y="274" width="24" height="3" rx="1.5" fill="{CR3}"/>'
    return svg(400, 400, b)


def evenements():
    b = blob(200, 210, 170, seed=5)
    b += f'<path d="M24,74 Q200,120 376,74" stroke="{NV}" stroke-width="2.5" fill="none"/>'
    cols = [R, O, Y, LB, R, O, Y, LB, R]
    for i, c in enumerate(cols):
        t = (i + 0.5) / len(cols)
        x = 24 + 352 * t
        y = (1 - t) ** 2 * 74 + 2 * (1 - t) * t * 120 + t * t * 74
        b += f'<path d="M{f(x-14)},{f(y-1)} L{f(x+14)},{f(y-1)} L{f(x)},{f(y+24)}Z" fill="{c}" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>'
    # poteaux et auvent
    b += f'<rect x="76" y="140" width="8" height="200" rx="4" fill="{NV}"/><rect x="316" y="140" width="8" height="200" rx="4" fill="{NV}"/>'
    b += f'<rect x="62" y="130" width="276" height="30" rx="8" fill="{R}"/>'
    for i in range(10):
        x = 62 + 13.8 + i * 27.6
        b += f'<path d="M{f(x-13.8)},159 A13.8,13.8 0 0 0 {f(x+13.8)},159Z" fill="{R if i % 2 == 0 else W}"/>'
    # ballons
    for (x, y, c) in ((52, 176, R), (36, 206, O), (64, 214, LB)):
        b += f'<path d="M{x},{y+22} Q{x+8},{y+60} 80,{y+86}" stroke="{NV}" stroke-width="1.5" fill="none"/>'
        b += f'<ellipse cx="{x}" cy="{y}" rx="17" ry="21" fill="{c}"/><ellipse cx="{x-6}" cy="{y-7}" rx="4" ry="6" fill="{W}" opacity="0.5"/>'
    # bénévoles
    b += bust(160, 250, 1.12, SKIN[2], HAIR[1], O, "bun")
    b += bust(246, 248, 1.12, SKIN[0], HAIR[0], LB, "short")
    b += f'<rect x="232" y="262" width="28" height="26" rx="8" fill="{W}"/>'
    # comptoir
    b += f'<rect x="62" y="266" width="276" height="16" rx="8" fill="{RD}"/>'
    b += f'<rect x="72" y="280" width="256" height="70" rx="6" fill="{R}"/>'
    for i in range(1, 16, 2):
        b += f'<rect x="{72 + i*16}" y="280" width="16" height="70" fill="{W}"/>'
    b += f'<rect x="72" y="280" width="256" height="70" rx="6" fill="none" stroke="{RD}" stroke-width="2"/>'
    b += f'<circle cx="200" cy="315" r="25" fill="{W}" stroke="{RD}" stroke-width="3"/>' + star(200, 315, 13, R)
    # crêpes et gâteau
    b += f'<ellipse cx="116" cy="264" rx="30" ry="6" fill="{W}"/>'
    for i, c in enumerate((O, Y, O, Y)):
        b += f'<ellipse cx="116" cy="{260-i*5}" rx="24" ry="5" fill="{c}"/>'
    b += f'<rect x="292" y="244" width="30" height="22" rx="4" fill="{PK}"/><rect x="292" y="244" width="30" height="7" rx="3" fill="{W}"/>'
    b += f'<circle cx="307" cy="240" r="4" fill="{R}"/>'
    b += shadow(200, 356, 150, 10)
    return svg(400, 400, b)


def association():
    b = blob(200, 210, 170, seed=9)
    b += heart(200, 108, 96, R) + sparkle(138, 86, 10, Y) + sparkle(268, 74, 12, O) + sparkle(252, 140, 7, Y)
    b += bust(166, 250, 1.18, SKIN[3], HAIR[3], Y, "curly")
    b += bust(236, 252, 1.18, SKIN[0], HAIR[2], BL, "bun")
    b += bust(104, 276, 1.25, SKIN[1], HAIR[0], R, "long")
    b += bust(298, 276, 1.25, SKIN[2], HAIR[1], O, "short")
    for (x, y, c, r) in ((60, 150, O, 20), (340, 140, LB, -25), (86, 210, Y, 35), (326, 214, R, -10), (40, 250, R, 15), (360, 262, Y, 40)):
        b += f'<rect x="{x-5}" y="{y-9}" width="10" height="18" rx="3" fill="{c}" transform="rotate({r} {x} {y})"/>'
    return svg(400, 400, b)


def enfants():
    b = ""
    b += cloud(130, 64, 1.2) + cloud(360, 44, 0.9) + f'<circle cx="662" cy="44" r="24" fill="{Y}" opacity="0.9"/>'
    b += f'<path d="M30,298 C160,268 330,286 470,279 C570,273 640,280 676,284 C704,290 704,344 672,352 L40,354 C4,348 0,306 30,298Z" fill="{CR2}"/>'
    # école
    b += f'<rect x="456" y="150" width="210" height="140" rx="4" fill="#fde2c3"/>'
    b += f'<path d="M446,154 L561,86 L676,154Z" fill="{R}" stroke="{R}" stroke-width="8" stroke-linejoin="round"/>'
    b += f'<circle cx="561" cy="128" r="15" fill="{W}"/><path d="M561,118 V128 H569" stroke="{NV}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    b += f'<line x1="561" y1="86" x2="561" y2="52" stroke="{NV}" stroke-width="3" stroke-linecap="round"/>'
    b += f'<rect x="561" y="52" width="9" height="14" fill="{BL}"/><rect x="570" y="52" width="9" height="14" fill="{W}"/><rect x="579" y="52" width="9" height="14" fill="{R}"/>'
    for x in (474, 506, 596, 628):
        for y in (172, 222):
            b += f'<rect x="{x}" y="{y}" width="22" height="30" rx="3" fill="{LB}"/><line x1="{x+11}" y1="{y}" x2="{x+11}" y2="{y+30}" stroke="{W}" stroke-width="2.5"/>'
    b += f'<path d="M543,290 V246 a18,18 0 0 1 36,0 V290Z" fill="{R}"/><circle cx="571" cy="270" r="2.5" fill="{Y}"/>'
    b += f'<rect x="446" y="286" width="230" height="8" rx="4" fill="{CR3}"/>'
    # arbres
    b += tree(74, 300, 1.25, O, Y) + tree(402, 292, 0.9, Y, W) + tree(672, 294, 0.62, R, PK)
    # marelle
    b += f'<g stroke="{W}" stroke-width="3" fill="none" stroke-linejoin="round">' \
         f'<path d="M150,346 l40,0 l-6,-10 l-40,0Z"/><path d="M144,336 l40,0 l-5,-9 l-40,0Z"/><path d="M139,327 l20,0 l-4,-8 l-20,0Z M159,327 l20,0 l-4,-8 l-20,0Z"/></g>'
    # enfants et ballon
    b += shadow(250, 332, 34, 6, CR3) + shadow(350, 334, 34, 6, CR3) + shadow(130, 322, 30, 5, CR3)
    b += kid(250, 330, 1.45, SKIN[2], HAIR[0], R, NV, "curly", arms=(-120, 70), spread=10)
    b += kid(350, 332, 1.45, SKIN[0], HAIR[2], Y, BL, "pony", arms=(-150, 150), spread=7)
    b += kid(130, 320, 1.2, SKIN[1], HAIR[1], LB, NV, "short", arms=(-20, 135), spread=5, backpack=O)
    b += f'<circle cx="302" cy="170" r="17" fill="{W}"/><circle cx="302" cy="170" r="17" fill="none" stroke="{NV}" stroke-width="3"/>'
    b += f'<path d="M302,153 L306,166 L319,168 M306,166 L298,176 L304,186 M298,176 L286,172" stroke="{NV}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    b += f'<path d="M270,196 q10,-14 20,-18" stroke="{O}" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="1 8"/>'
    b += sparkle(205, 150, 9, Y) + sparkle(420, 110, 7, O) + heart(40, 120, 26, PK, -10)
    return svg(700, 360, b)


def apple(cx, cy, r, fill, face_on=True, star_on=False, rot=0):
    d = ("M0,-0.74 C0.34,-1.02 1,-0.86 1,-0.1 C1,0.6 0.55,1 0.25,0.95 C0.12,0.93 0.06,0.88 0,0.88 "
         "C-0.06,0.88 -0.12,0.93 -0.25,0.95 C-0.55,1 -1,0.6 -1,-0.1 C-1,-0.86 -0.34,-1.02 0,-0.74Z")
    g = f'<g transform="translate({f(cx)} {f(cy)}) rotate({rot})">'
    g += f'<path d="M0,-0.72 C0.04,-0.9 0.1,-1.04 0.2,-1.12" stroke="{BR}" stroke-width="0.09" fill="none" stroke-linecap="round" transform="scale({f(r)})"/>'
    g += f'<ellipse cx="{f(r*0.42)}" cy="{f(-r*1.02)}" rx="{f(r*0.34)}" ry="{f(r*0.15)}" fill="{GR}" transform="rotate(-24 {f(r*0.42)} {f(-r*1.02)})"/>'
    g += f'<path d="{d}" fill="{fill}" transform="scale({f(r)})"/>'
    g += f'<ellipse cx="{f(-r*0.5)}" cy="{f(-r*0.38)}" rx="{f(r*0.16)}" ry="{f(r*0.28)}" fill="{W}" opacity="0.35" transform="rotate(25 {f(-r*0.5)} {f(-r*0.38)})"/>'
    if face_on:
        g += (f'<path d="M{f(-r*0.34)},{f(r*0.02)} q{f(r*0.1)},{f(-r*0.12)} {f(r*0.2)},0" stroke="{NV}" stroke-width="{f(r*0.07)}" fill="none" stroke-linecap="round"/>'
              f'<path d="M{f(r*0.14)},{f(r*0.02)} q{f(r*0.1)},{f(-r*0.12)} {f(r*0.2)},0" stroke="{NV}" stroke-width="{f(r*0.07)}" fill="none" stroke-linecap="round"/>'
              f'<path d="M{f(-r*0.2)},{f(r*0.24)} q{f(r*0.2)},{f(r*0.2)} {f(r*0.4)},0" stroke="{NV}" stroke-width="{f(r*0.07)}" fill="none" stroke-linecap="round"/>'
              f'<circle cx="{f(-r*0.52)}" cy="{f(r*0.24)}" r="{f(r*0.1)}" fill="{PK}" opacity="0.9"/>'
              f'<circle cx="{f(r*0.52)}" cy="{f(r*0.24)}" r="{f(r*0.1)}" fill="{PK}" opacity="0.9"/>')
    if star_on:
        g += star(r * 0.55, -r * 0.42, r * 0.17, Y)
    return g + "</g>"


def frise():
    b = f'<path d="M30,238 C90,120 160,110 220,196 C270,116 360,78 430,160 C490,90 580,60 640,150" stroke="{NV}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round" fill="none" opacity="0.55"/>'
    b += (f'<g transform="translate(208 150) rotate(-12)"><rect x="-26" y="-18" width="52" height="38" rx="8" fill="{PK}"/>'
          f'<path d="M-12,-18 v-8 a6,6 0 0 1 6,-6 h12 a6,6 0 0 1 6,6 v8" stroke="{PK}" stroke-width="6" fill="none"/>'
          f'<rect x="-26" y="-18" width="52" height="12" rx="6" fill="{R}" opacity="0.35"/><rect x="-5" y="-8" width="10" height="8" rx="2" fill="{Y}"/></g>')
    b += apple(90, 196, 30, PR, rot=-10)
    b += apple(430, 138, 44, R, rot=6)
    b += apple(690, 234, 64, R, star_on=True)
    b += sparkle(330, 70, 9, Y) + sparkle(560, 60, 12, O) + sparkle(150, 96, 7, Y)
    return svg(800, 300, b)


for name, fn in (("bien-etre", bien_etre), ("lien", lien), ("conseils", conseils), ("evenements", evenements),
                 ("association", association), ("enfants", enfants), ("pommes-frise", frise)):
    with open(f"{OUT}/{name}.svg", "w") as fh:
        fh.write(fn())
    print(name)
