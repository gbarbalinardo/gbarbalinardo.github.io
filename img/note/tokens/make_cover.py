"""Cover image for "The Best Token for a Bridge".

Four tokens, left to right: brick, pose, quantity, theorem.
The visual argument: the enclosure (the constraint) tightens as you move
right. The brick floats free, the pose gets a dotted frame, the quantity a
solid hairline, and the theorem a solid accent frame. The only saturated
color on the page is the theorem, so the eye lands there last.

1200x630 px at dpi 100. Matplotlib only, DejaVu fonts.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

# dejavusans mathtext draws kappa as a near-Latin italic K;
# the serif set gives a proper Greek kappa
plt.rcParams["mathtext.fontset"] = "dejavuserif"

# ---------------------------------------------------------------- palette
BG = "#fbfaf7"
INK = "#22252b"
ACCENT = "#3f5bd6"
GRAY_MID = "#5a5e66"   # secondary text (units)
GRAY_SOFT = "#8a8e96"  # hairline frame
GRAY_FAINT = "#b9bcc2" # dotted frame, chevrons

SERIF = "DejaVu Serif"

# ---------------------------------------------------------------- canvas
fig = plt.figure(figsize=(12.0, 6.3), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1200)
ax.set_ylim(0, 630)
ax.set_facecolor(BG)
ax.axis("off")

# ---------------------------------------------------------------- layout
CY = 368          # vertical center of the token row
TILE = 192        # tile side
HALF = TILE / 2
CENTERS = [196, 466, 736, 1006]
LABEL_Y = CY - HALF - 44
CAPTION_Y = 96

# ---------------------------------------------------------------- frames
def rounded_frame(cx, cy, edge, lw, ls="solid"):
    box = FancyBboxPatch(
        (cx - HALF, cy - HALF), TILE, TILE,
        boxstyle="round,pad=0,rounding_size=18",
        facecolor="none", edgecolor=edge,
        linewidth=lw, linestyle=ls,
    )
    ax.add_patch(box)

# tile 1: no frame (the brick knows its own shape and nothing else)
rounded_frame(CENTERS[1], CY, GRAY_FAINT, 1.2, (0, (1.5, 3.2)))
rounded_frame(CENTERS[2], CY, GRAY_SOFT, 1.3)
rounded_frame(CENTERS[3], CY, ACCENT, 2.6)

# ---------------------------------------------------------------- glyphs

# --- brick: three courses in running bond, loose on the field -----------
def brick_wall(cx, cy):
    bw, bh, gap = 46, 21, 7
    rows = [
        [(-bw - gap / 2, 1), (gap / 2, 1)],                    # top: 2 bricks
        [(-1.5 * bw - gap, 0), (-bw / 2, 0), (bw / 2 + gap, 0)],  # middle: 3
        [(-bw - gap / 2, -1), (gap / 2, -1)],                  # bottom: 2
    ]
    y0 = cy + bh / 2 + gap / 2
    for row in rows:
        for x, level in row:
            r = Rectangle(
                (cx + x, y0 + level * (bh + gap) - bh / 2), bw, bh,
                facecolor="none", edgecolor=INK, linewidth=1.5,
            )
            ax.add_patch(r)

brick_wall(CENTERS[0], CY + 4)

# --- pose: a squat, drawn as a pose-estimation skeleton -----------------
def squat_pose(cx, cy):
    # side view, facing right; coordinates relative to (cx, cy)
    toe = (46, -60)
    ankle = (16, -56)
    knee = (32, -12)
    hip = (-20, 0)
    shoulder = (6, 48)
    elbow = (36, 47)
    wrist = (64, 46)
    head_c = (14, 72)
    head_r = 12
    neck = (11, 60)

    bones = [
        (toe, ankle), (ankle, knee), (knee, hip),
        (hip, shoulder), (shoulder, neck),
        (shoulder, elbow), (elbow, wrist),
    ]
    for (x1, y1), (x2, y2) in bones:
        ax.plot(
            [cx + x1, cx + x2], [cy + y1, cy + y2],
            color=INK, linewidth=2.2, solid_capstyle="round", zorder=3,
        )
    ax.add_patch(Circle(
        (cx + head_c[0], cy + head_c[1]), head_r,
        facecolor=BG, edgecolor=INK, linewidth=2.2, zorder=4,
    ))
    # joint markers: the token carries its joint angles
    for jx, jy in (ankle, knee, hip, shoulder, elbow, wrist):
        ax.add_patch(Circle(
            (cx + jx, cy + jy), 4.4,
            facecolor=BG, edgecolor=INK, linewidth=1.8, zorder=5,
        ))

squat_pose(CENTERS[1], CY - 4)

# --- quantity: a value that carries its dimension ------------------------
# "300 K" is verbatim from the essay; a number with a unit reads as a
# physical quantity at any size, unlike a lone kappa (DejaVu's kappa is
# indistinguishable from a Latin K)
ax.text(
    CENTERS[2], CY + 2, "300 K",
    ha="center", va="center", fontsize=40,
    family=SERIF, color=INK,
)

# --- theorem: the turnstile, the only saturated mark ---------------------
def turnstile(cx, cy):
    ax.plot(
        [cx - 34, cx - 34], [cy - 40, cy + 40],
        color=ACCENT, linewidth=7, solid_capstyle="round", zorder=3,
    )
    ax.plot(
        [cx - 34, cx + 40], [cy, cy],
        color=ACCENT, linewidth=7, solid_capstyle="round", zorder=3,
    )

turnstile(CENTERS[3], CY)

# ---------------------------------------------------------------- chevrons
def chevron(x, y):
    ax.plot(
        [x - 6, x + 6, x - 6], [y + 9, y, y - 9],
        color=GRAY_FAINT, linewidth=2.0,
        solid_capstyle="round", solid_joinstyle="round",
    )

for left, right in zip(CENTERS[:-1], CENTERS[1:]):
    chevron((left + right) / 2, CY)

# ---------------------------------------------------------------- labels
labels = ["brick", "pose", "quantity", "theorem"]
for cx, word in zip(CENTERS, labels):
    color = ACCENT if word == "theorem" else INK
    ax.text(
        cx, LABEL_Y, word,
        ha="center", va="center", fontsize=19,
        family=SERIF, color=color,
    )

# ---------------------------------------------------------------- caption
ax.text(
    600, CAPTION_Y, "the smallest unit that cannot lie",
    ha="center", va="center", fontsize=19,
    family=SERIF, style="italic", color=GRAY_MID,
)

fig.savefig(
    "/Users/juicy/Development/science/lean-compatibility/"
    "gbarbalinardo.github.io/img/note/tokens/tokens_v2.png",
    dpi=100, facecolor=BG,
)
print("wrote tokens_v2.png")
