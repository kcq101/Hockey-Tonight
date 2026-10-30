#!/usr/bin/env python3
"""Build the player sprite atlas from the key-color source sheets in art/src.

Source art uses key colors so one atlas serves every team:
  magenta #FF00FF = jersey + socks, cyan #00FFFF = stripes, lime #00FF00 = helmet/gloves/pants.
The game recolors the atlas for the two teams in each match (see buildKit in index.html).

Output: img/sk/atlas.webp + img/sk/atlas.json
  frames: name -> [x, y, w, h, ax, bx, by]   (ax = foot anchor x; feet on the bottom edge; bx,by = puck point on the blade)
  h0: height in px of a normal standing skater (the renderer scales from this)

Run:  python3 tools/build_sprites.py
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'art', 'src')
OUT = os.path.join(ROOT, 'img', 'sk')
H0 = 100        # px height of a standing skater in the atlas (~1.2x on-screen size at dpr 2)
HG = 104        # px height of the goalie in his ready stance

def load(name): return np.array(Image.open(os.path.join(SRC, name + '.webp')).convert('RGBA'))

def row_frames(im, rows=1):
    """Figures laid out in rows: join each figure's bits (stick, skates), then read left-to-right."""
    lab, n = ndimage.label(ndimage.binary_dilation(im[..., 3] > 170, iterations=6))
    H = im.shape[0]; out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if (lab[sl] == i + 1).sum() < 3000: continue
        sub = im.copy(); sub[..., 3] = np.where(lab == i + 1, im[..., 3], 0)
        out.append(((sl[0].start + sl[0].stop) / 2, (sl[1].start + sl[1].stop) / 2, sub))
    rs = [[] for _ in range(rows)]
    for t in out: rs[min(rows - 1, int(t[0] / H * rows))].append(t)
    return [[t[2] for t in sorted(r, key=lambda t: t[1])] for r in rs]

def grid_frames(im, rows, cols):
    """Figures in a grid: each cell keeps the pieces centred in it; a piece bridging two cells is split at the edge."""
    H, W = im.shape[:2]; cw, ch = W / cols, H / rows
    lab, n = ndimage.label(im[..., 3] > 60)
    yy, xx = np.mgrid[0:H, 0:W]; cell = (yy // ch).astype(int) * cols + (xx // cw).astype(int)
    own = np.full((H, W), -1)
    for i, sl in enumerate(ndimage.find_objects(lab)):
        m = lab == i + 1
        if m.sum() < 40: continue
        if sl[1].stop - sl[1].start > 1.7 * cw: own[m] = cell[m]
        else:
            cy, cx = ndimage.center_of_mass(m); own[m] = int(cy // ch) * cols + int(cx // cw)
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            sub = im.copy(); sub[..., 3] = np.where(own == r * cols + c, im[..., 3], 0); row.append(sub)
        out.append(row)
    return out

def trim(sub):
    ys, xs = np.nonzero(sub[..., 3] > 40)
    return sub[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def height(sub): return trim(sub).shape[0]

def blade(sub, ax):
    """Where the puck sits on the stick: the largest bright-white tape blob that isn't skate steel.
    Skate blades are the white bits low down near the feet, so those are skipped."""
    h, w = sub.shape[:2]; rgb = sub[..., :3].astype(float); mx = rgb.max(-1); mn = rgb.min(-1)
    white = (mx > 215) & ((mx - mn) < .14 * mx) & (sub[..., 3] > 200); white[:int(h * .45)] = False
    lab, n = ndimage.label(ndimage.binary_closing(white, iterations=2)); best = None
    for i in range(n):
        ys, xs = np.nonzero(lab == i + 1)
        if len(ys) < 30: continue
        cy, cx = ys.mean() / h, xs.mean() / w
        if cy > .78 and abs(cx - ax) < .3: continue          # skate steel under the feet
        if best is None or len(ys) > best[0]: best = (len(ys), cx, cy)
    return (best[1], best[2]) if best else None

def fit(sub, scale):
    """Trim, scale, find the foot anchor (centre of the skates in the lowest 12%) and the puck point on the blade."""
    sub = trim(sub); h, w = sub.shape[:2]
    low = sub[int(h * .88):, :, 3] > 40; fx = np.nonzero(low.any(0))[0]; ax = (fx.min() + fx.max()) / 2 / w
    im = Image.fromarray(sub).resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    return im, ax, blade(sub, ax)

def ref_height(frames, n=None):
    """Upright reference height for a sheet: median of its shortest figures (ignores raised sticks)."""
    hs = sorted(height(f) for f in frames)
    return float(np.median(hs[:n or len(hs)]))

frames = {}
def put(name, sub, scale):
    frames[name] = fit(sub, scale)

# idle poses, 5 directions (S, SE, E, NE, N); the game mirrors these for SW, W, NW
turn = row_frames(load('turnaround'))[0]
s = H0 / ref_height(turn)
for d, f in zip(['S', 'SE', 'E', 'NE', 'N'], turn): put(f'idle_{d}', f, s)

# stride cycles: push(left side of image), glide, push(right side), glide
for d in ['S', 'SE', 'E', 'N']:
    fr = row_frames(load('stride-' + d))[0]; s = H0 / ref_height(fr)
    for i, f in enumerate(fr): put(f'run_{d}_{i}', f, s)
ne = row_frames(load('stride-NE'))[0]
rp = load('stride-NE-rpush')                     # hand-built right-side push (frame 3), same pixel scale as the sheet
s = H0 / ref_height(ne)
for i, f in enumerate([ne[0], ne[1], rp, ne[3]]): put(f'run_NE_{i}', f, s)

# actions: front (facing camera), side (3/4 to the right), back (facing away)
ACT = ['windup', 'slap', 'wrist', 'pass', 'poke', 'check', 'stop', 'accel']
side = grid_frames(load('actions-side'), 3, 4)
s = H0 / ref_height(side[0])                    # row 1 of this sheet is upright skating
for i, a in enumerate(ACT): put(f'{a}_E', side[1 + i // 4][i % 4], s)
for key, name in [('S', 'actions-front'), ('N', 'actions-back')]:
    g = grid_frames(load(name), 2, 4); flat = [f for r in g for f in r]
    s = H0 / ref_height(flat, 5)
    for i, a in enumerate(ACT): put(f'{a}_{key}', flat[i], s)

# goalie: row 1 facing camera, row 2 facing away: ready, butterfly, glove save, blocker save
gk = row_frames(load('goalie'), rows=2)
s = HG / ref_height(gk[0][:1])
for key, row in [('S', gk[0]), ('N', gk[1])]:
    for a, f in zip(['g_ready', 'g_fly', 'g_glove', 'g_block'], row): put(f'{a}_{key}', f, s)

# shelf-pack into one atlas
items = sorted(frames.items(), key=lambda kv: -kv[1][0].height)
W = 1024; x = y = shelf = 0; place = {}
for name, (im, ax, bl) in items:
    if x + im.width + 2 > W: x = 0; y += shelf + 2; shelf = 0
    place[name] = (x, y); x += im.width + 2; shelf = max(shelf, im.height)
H = y + shelf
atlas = Image.new('RGBA', (W, H))
meta = {'h0': H0, 'hg': HG, 'frames': {}}
for name, (im, ax, bl) in frames.items():
    px, py = place[name]; atlas.alpha_composite(im, (px, py))
    # [x, y, w, h, foot-x, blade-x, blade-y]  (blade point in frame px; -1 when no blade is on the ice)
    b = [round(bl[0] * im.width, 1), round(bl[1] * im.height, 1)] if bl else [-1, -1]
    meta['frames'][name] = [px, py, im.width, im.height, round(ax * im.width, 1)] + b
os.makedirs(OUT, exist_ok=True)
# a 256-colour palette keeps every key hue intact (checked: recoloured output is indistinguishable) at ~1/4 the size
atlas = atlas.quantize(colors=256, method=Image.Quantize.FASTOCTREE).convert('RGBA')
atlas.save(os.path.join(OUT, 'atlas.webp'), lossless=True, method=6)
json.dump(meta, open(os.path.join(OUT, 'atlas.json'), 'w'), separators=(',', ':'))
print(f'{len(frames)} frames, atlas {W}x{H}, {os.path.getsize(os.path.join(OUT, "atlas.webp")) // 1024} KB')
