#!/usr/bin/env python3
"""Render the second machinist-fit cover."""

import math
import os
import tempfile
from pathlib import Path


os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-make-c2")
)

import matplotlib


matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch, Polygon
from matplotlib.path import Path as MplPath
from matplotlib.textpath import TextToPath


WIDTH = 1200
HEIGHT = 630
DPI = 100

GROUND = "#fbfaf7"
INK = "#22252b"
ACCENT = "#3f5bd6"


def gray(alpha):
    return mcolors.to_rgba(INK, alpha)


def add_line(ax, points, *, color, width, zorder=8):
    line = Line2D(
        *zip(*points),
        color=color,
        linewidth=width,
        solid_capstyle="butt",
        solid_joinstyle="miter",
        zorder=zorder,
    )
    ax.add_line(line)
    return line


def add_hatching(ax, clip_patch, bounds, *, alpha, width, spacing=6.0):
    """Draw evenly spaced 45 degree section lines in a clip path."""
    xmin, xmax, ymin, ymax = bounds
    step = spacing * math.sqrt(2.0)
    intercept = ymin - xmax - step
    intercept_max = ymax - xmin + step
    reach = (ymax - ymin) + 80
    x0 = xmin - reach
    x1 = xmax + reach

    while intercept <= intercept_max:
        line = Line2D(
            [x0, x1],
            [x0 + intercept, x1 + intercept],
            color=gray(alpha),
            linewidth=width,
            solid_capstyle="butt",
            zorder=4,
        )
        line.set_clip_path(clip_patch)
        ax.add_line(line)
        intercept += step


def rectangles_path(rectangles):
    """Return one compound clipping path made from axis-aligned rectangles."""
    vertices = []
    codes = []
    for x0, x1, y0, y1 in rectangles:
        vertices.extend(
            [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        )
        codes.extend(
            [
                MplPath.MOVETO,
                MplPath.LINETO,
                MplPath.LINETO,
                MplPath.LINETO,
                MplPath.CLOSEPOLY,
            ]
        )
    return MplPath(vertices, codes)


def text_width(text, prop):
    width, _, _ = TextToPath().get_text_width_height_descent(
        text, prop, ismath=False
    )
    return width * DPI / 72.0


def add_label(ax, x, baseline, text, *, size, color):
    prop = FontProperties(family="DejaVu Sans", size=size, weight="normal")
    ax.text(
        x,
        baseline,
        text,
        fontproperties=prop,
        color=color,
        ha="left",
        va="baseline",
        zorder=10,
    )
    return x + text_width(text, prop)


def add_letterspaced_text(
    ax, x, baseline, text, *, size, tracking, color
):
    prop = FontProperties(family="DejaVu Sans", size=size, weight="normal")
    cursor = x
    metrics = TextToPath()
    for glyph in text:
        ax.text(
            cursor,
            baseline,
            glyph,
            fontproperties=prop,
            color=color,
            ha="left",
            va="baseline",
            zorder=10,
        )
        advance, _, _ = metrics.get_text_width_height_descent(
            glyph, prop, ismath=False
        )
        cursor += advance * DPI / 72.0 + tracking


def render():
    matplotlib.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.sans-serif": ["DejaVu Sans"],
            "font.serif": ["DejaVu Serif"],
        }
    )

    fig = plt.figure(figsize=(12, 6.3), dpi=DPI, facecolor=GROUND)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=GROUND)
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(HEIGHT, 0)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    # Headline and its short hairline rule.
    headline = FontProperties(family="DejaVu Serif", size=26, weight="normal")
    ax.text(
        300,
        76,
        "A theorem is a token",
        fontproperties=headline,
        color=INK,
        ha="left",
        va="baseline",
        zorder=10,
    )
    ax.text(
        300,
        116,
        "that cannot lie.",
        fontproperties=headline,
        color=INK,
        ha="left",
        va="baseline",
        zorder=10,
    )
    add_line(ax, [(300, 150), (480, 150)], color=INK, width=0.7)

    # Statement wall. The edge remains open at both ends.
    wall_profile = [
        (830, 285),
        (885, 285),
        (885, 329),
        (920, 329),
        (920, 377),
        (872, 377),
        (872, 430),
        (830, 430),
    ]

    # Section hatching: one continuous, even-density band over the whole
    # material silhouette (the wall minus the socket void), so the section
    # reads as a single piece of stock.
    material_vertices = [
        (830, 175), (954, 175), (954, 555), (830, 555),
        (830, 430), (872, 430), (872, 377), (920, 377),
        (920, 329), (885, 329), (885, 285), (830, 285),
    ]
    material_clip = Polygon(
        material_vertices,
        closed=True,
        facecolor="none",
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(material_clip)
    add_hatching(
        ax,
        material_clip,
        (830, 954, 175, 555),
        alpha=0.50,
        width=0.4,
        spacing=6.0,
    )
    add_line(ax, [(830, 175), (830, 285)], color=INK, width=1.0)
    add_line(ax, wall_profile, color=ACCENT, width=1.4, zorder=9)
    add_line(ax, [(830, 430), (830, 555)], color=INK, width=1.0)

    # The term carries the same profile 12 px to the left.
    term_profile = [(x - 12, y) for x, y in wall_profile]
    term_vertices = [(568, 285), *term_profile, (568, 430)]
    term_clip = Polygon(
        term_vertices,
        closed=True,
        facecolor=GROUND,
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(term_clip)
    add_hatching(
        ax,
        term_clip,
        (568, 908, 285, 430),
        alpha=0.55,
        width=0.45,
        spacing=6.0,
    )
    add_line(
        ax,
        [(568, 285), term_profile[0]],
        color=INK,
        width=0.9,
    )
    add_line(ax, term_profile, color=ACCENT, width=1.4, zorder=9)
    add_line(
        ax,
        [term_profile[-1], (568, 430), (568, 285)],
        color=INK,
        width=0.9,
    )

    # Labels with compact orthogonal leaders.
    proof_end = add_label(
        ax,
        520,
        239,
        "THE PROOF IS A TERM OF THAT TYPE",
        size=7.5,
        color=ACCENT,
    )
    add_line(
        ax,
        [(proof_end + 8, 236), (760, 236), (760, 285)],
        color=ACCENT,
        width=0.5,
    )

    statement_end = add_label(
        ax,
        650,
        510,
        "THE STATEMENT IS A TYPE",
        size=7.5,
        color=gray(0.45),
    )
    add_line(
        ax,
        [(statement_end + 8, 507), (810, 507), (810, 480), (830, 480)],
        color=gray(0.45),
        width=0.5,
    )

    # Rejected candidate, scaled down with an intentionally over-deep last step.
    rejected_vertices = [
        (78, 445),
        (215.5, 445),
        (245.75, 445),
        (245.75, 469.2),
        (265.0, 469.2),
        (265.0, 495.6),
        (255.1, 495.6),
        (255.1, 524.75),
        (215.5, 524.75),
        (78, 524.75),
    ]
    rejected_clip = Polygon(
        rejected_vertices,
        closed=True,
        facecolor=GROUND,
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(rejected_clip)
    add_hatching(
        ax,
        rejected_clip,
        (78, 265, 445, 525),
        alpha=0.30,
        width=0.4,
        spacing=6.0,
    )
    rejected_outline = Polygon(
        rejected_vertices,
        closed=True,
        fill=False,
        edgecolor=gray(0.50),
        linewidth=0.7,
        joinstyle="miter",
        zorder=7,
    )
    ax.add_patch(rejected_outline)
    add_line(
        ax,
        [(84, 519), (259, 451)],
        color=INK,
        width=0.7,
        zorder=9,
    )

    add_label(
        ax,
        62,
        432,
        "THE KERNEL CHECKS THE TERM OR REJECTS IT",
        size=7.0,
        color=gray(0.50),
    )
    ax.text(
        78,
        551,
        "no such thing as a plausible proof",
        fontproperties=FontProperties(
            family="DejaVu Serif", size=9.5, style="italic"
        ),
        color=gray(0.50),
        ha="left",
        va="baseline",
        zorder=10,
    )

    add_letterspaced_text(
        ax,
        48,
        607,
        "THE TYPE SYSTEM MAKES THE LIE INEXPRESSIBLE",
        size=6.2,
        tracking=0.9,
        color=gray(0.45),
    )

    output = Path(__file__).resolve().with_name("c3.png")
    fig.savefig(
        output,
        dpi=DPI,
        facecolor=GROUND,
        edgecolor=GROUND,
        bbox_inches=None,
        pad_inches=0,
    )
    plt.close(fig)

    rendered = plt.imread(output)
    if rendered.shape[:2] != (HEIGHT, WIDTH):
        raise RuntimeError(
            f"Expected {WIDTH}x{HEIGHT}, got "
            f"{rendered.shape[1]}x{rendered.shape[0]}"
        )


if __name__ == "__main__":
    render()

