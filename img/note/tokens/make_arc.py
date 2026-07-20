#!/usr/bin/env python3
"""Render the five-step conceptual token chart for Brief B2."""

import os
import tempfile
import unicodedata
from pathlib import Path


# Keep Matplotlib's runtime cache out of the artwork directory.
os.environ.setdefault(
    "MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib-studio-cache")
)

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties


GROUND = "#fbfaf7"
INK = "#22252b"
ACCENT = "#3f5bd6"
DPI = 100
WIDTH = 1200
HEIGHT = 700


def from_top(y):
    """Convert a pixel position measured from the top to plot coordinates."""
    return HEIGHT - y


def _track_pair(left, right):
    """Return true only for a pair inside a word, excluding punctuation."""
    if left.isspace() or right.isspace():
        return False
    return not (
        unicodedata.category(left).startswith("P")
        or unicodedata.category(right).startswith("P")
    )


def tracked_text(
    ax,
    renderer,
    x,
    y,
    text,
    *,
    size=7,
    color=INK,
    alpha=1.0,
    tracking=0.8,
    word_spacing=0.0,
    align="left",
):
    """Draw horizontal text with tracking inside words only."""
    font = FontProperties(family="DejaVu Sans", size=size, weight="normal")
    widths = []
    for char in text:
        width = renderer.get_text_width_height_descent(
            char, font, ismath=False
        )[0]
        if char.isspace():
            width += word_spacing
        widths.append(width)
    extras = [
        tracking if _track_pair(text[index], text[index + 1]) else 0.0
        for index in range(len(text) - 1)
    ]
    total_width = sum(widths) + sum(extras)
    cursor = -total_width / 2 if align == "center" else 0.0

    for index, (char, width) in enumerate(zip(text, widths)):
        if not char.isspace():
            ax.text(
                x + cursor,
                y,
                char,
                color=color,
                alpha=alpha,
                fontproperties=font,
                ha="left",
                va="baseline",
                clip_on=False,
            )
        cursor += width
        if index < len(extras):
            cursor += extras[index]

    return total_width


def main():
    matplotlib.rcParams.update(
        {
            "figure.dpi": DPI,
            "savefig.dpi": DPI,
            "font.family": "DejaVu Sans",
            "font.sans-serif": ["DejaVu Sans"],
            "font.serif": ["DejaVu Serif"],
            "text.color": INK,
            "lines.color": INK,
        }
    )

    fig = plt.figure(figsize=(12, 7), dpi=DPI, facecolor=GROUND)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=GROUND)
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_axis_off()

    # Nudge the staircase up and left while preserving its proportions.
    baseline_y = from_top(590)
    staircase_dx = -35
    staircase_dy = 25
    points = [
        (315 + staircase_dx, from_top(520) + staircase_dy),
        (455 + staircase_dx, from_top(440) + staircase_dy),
        (600 + staircase_dx, from_top(360) + staircase_dy),
        (745 + staircase_dx, from_top(280) + staircase_dy),
        (885 + staircase_dx, from_top(195) + staircase_dy),
    ]

    # The baseline spans exactly from the first riser to the last riser.
    ax.plot(
        [points[0][0], points[-1][0]],
        [baseline_y, baseline_y],
        color=INK,
        linewidth=0.8,
        solid_capstyle="butt",
        zorder=1,
    )

    # Solid treads and dotted risers keep the step construction unambiguous.
    ax.plot(
        [points[0][0], points[0][0]],
        [baseline_y, points[0][1]],
        color=INK,
        alpha=0.35,
        linewidth=0.6,
        linestyle=(0, (1.2, 3.0)),
        dash_capstyle="round",
        zorder=1,
    )
    for left, right in zip(points, points[1:]):
        ax.plot(
            [left[0], right[0]],
            [left[1], left[1]],
            color=INK,
            alpha=0.35,
            linewidth=0.6,
            linestyle="solid",
            solid_capstyle="butt",
            zorder=1,
        )
        ax.plot(
            [right[0], right[0]],
            [left[1], right[1]],
            color=INK,
            alpha=0.35,
            linewidth=0.6,
            linestyle=(0, (1.2, 3.0)),
            dash_capstyle="round",
            zorder=1,
        )

    for x, y in points[:-1]:
        ax.plot(
            x,
            y,
            marker="o",
            markersize=3.5,
            markerfacecolor=INK,
            markeredgecolor=INK,
            markeredgewidth=0,
            linestyle="none",
            zorder=3,
        )

    theorem_x, theorem_y = points[-1]
    ax.plot(
        theorem_x,
        theorem_y,
        marker="o",
        markersize=5,
        markerfacecolor=ACCENT,
        markeredgecolor=ACCENT,
        markeredgewidth=0,
        linestyle="none",
        zorder=3,
    )

    # Draw once so the Agg renderer can supply exact glyph advances.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    tracked_text(
        ax,
        renderer,
        240,
        from_top(140),
        "WHAT PREDICTION BECOMES",
        size=7.5,
        color=INK,
        alpha=0.45,
        tracking=0.35,
        word_spacing=3.0,
    )

    # The lower line sits 12 pixels above its tread at every point.
    annotations = [
        ("word shard", "AUTOCOMPLETE", INK),
        ("pose", "COACHING", INK),
        ("member", "STRUCTURE", INK),
        ("quantity", "SIMULATION", INK),
        ("theorem", "DISCOVERY WITH A REFEREE", ACCENT),
    ]
    for (x, y), (token, outcome, color) in zip(points, annotations):
        ax.text(
            x,
            y + 31,
            token,
            color=color,
            family="DejaVu Serif",
            fontsize=11,
            fontweight="normal",
            ha="left",
            va="baseline",
        )
        tracked_text(
            ax,
            renderer,
            x,
            y + 12,
            outcome,
            size=7,
            color=color,
            alpha=1.0 if color == ACCENT else 0.45,
            tracking=0.3 if outcome in {
                "SIMULATION",
                "DISCOVERY WITH A REFEREE",
            } else 0.8,
            word_spacing=3.0 if outcome == "DISCOVERY WITH A REFEREE" else 0.0,
        )

    tracked_text(
        ax,
        renderer,
        600,
        from_top(625),
        "CONSTRAINTS THE TOKEN CARRIES",
        size=7.5,
        color=INK,
        alpha=0.45,
        tracking=0.85,
        align="center",
    )

    output = Path(__file__).resolve().with_name("b3.png")
    fig.savefig(
        output,
        dpi=DPI,
        facecolor=GROUND,
        edgecolor="none",
        bbox_inches=None,
        pad_inches=0,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
