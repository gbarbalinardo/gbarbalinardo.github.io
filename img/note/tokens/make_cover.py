import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle


WIDTH = 1200
HEIGHT = 630
DPI = 100

GROUND = "#fbfaf7"
INK = "#22252b"
ACCENT = "#3f5bd6"


def line(ax, start, end, *, color=INK, width=1.6, alpha=1.0, zorder=2):
    ax.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        color=color,
        linewidth=width,
        alpha=alpha,
        solid_capstyle="butt",
        solid_joinstyle="miter",
        zorder=zorder,
    )


def letterspaced_text(
    ax,
    fig,
    x,
    y,
    text,
    *,
    size,
    color=INK,
    tracking=0.9,
    alpha=1.0,
    weight="normal",
    word_spacing=0.0,
    align="left",
):
    """Add tracking only between letters inside a word."""
    font = FontProperties(family="DejaVu Sans", size=size, weight=weight)
    renderer = fig.canvas.get_renderer()
    advances = []

    for index, character in enumerate(text):
        advance = renderer.get_text_width_height_descent(
            character, font, ismath=False
        )[0]
        if character.isspace():
            advance += word_spacing
        if (
            index + 1 < len(text)
            and character.isalpha()
            and text[index + 1].isalpha()
        ):
            advance += tracking
        advances.append(advance)

    total_width = sum(advances)
    cursor = x - total_width if align == "right" else x

    for character, advance in zip(text, advances):
        if not character.isspace():
            ax.text(
                cursor,
                y,
                character,
                fontproperties=font,
                color=color,
                alpha=alpha,
                ha="left",
                va="baseline",
                clip_on=False,
            )
        cursor += advance

    return total_width


def hatched_abutment(ax, center_x, *, top=138, width=54, height=40):
    left = center_x - width / 2
    right = center_x + width / 2
    bottom = top - height

    ax.add_patch(
        Rectangle(
            (left, bottom),
            width,
            height,
            facecolor=GROUND,
            edgecolor="none",
            zorder=1,
        )
    )

    # Fine, clipped 45-degree hatch lines.
    spacing = 8
    offset = -height
    while offset <= width:
        if offset < 0:
            start_x = left
            start_y = bottom - offset
        else:
            start_x = left + offset
            start_y = bottom
        run = min(right - start_x, top - start_y)
        if run > 0:
            line(
                ax,
                (start_x, start_y),
                (start_x + run, start_y + run),
                width=0.6,
                alpha=0.55,
                zorder=2,
            )
        offset += spacing

    ax.add_patch(
        Rectangle(
            (left, bottom),
            width,
            height,
            facecolor="none",
            edgecolor=INK,
            linewidth=1.35,
            zorder=3,
        )
    )
    line(
        ax,
        (left - 30, bottom),
        (right + 30, bottom),
        width=1.35,
        zorder=4,
    )


def main():
    fig = plt.figure(
        figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=GROUND
    )
    ax = fig.add_axes([0, 0, 1, 1], facecolor=GROUND)
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.axis("off")

    serif = FontProperties(family="DejaVu Serif", weight="normal")

    # Headline.
    ax.text(
        82,
        550,
        "The token of a bridge is not the brick.",
        fontproperties=serif,
        fontsize=27,
        color=INK,
        ha="left",
        va="baseline",
    )
    ax.text(
        82,
        502,
        "It is the brick plus statics.",
        fontproperties=serif,
        fontsize=16,
        color=INK,
        alpha=0.55,
        ha="left",
        va="baseline",
    )
    line(ax, (82, 474), (402, 474), width=0.7)

    # Eight equal panels, centered at x=652.5.
    bottom_y = 150
    deck_y = bottom_y - 12
    top_y = 395
    panel_width = (1130 - 175) / 8
    nodes = [175 + panel_width * index for index in range(9)]

    # The abutment tops meet the lower deck line.
    hatched_abutment(ax, nodes[0], top=deck_y)
    hatched_abutment(ax, nodes[-1], top=deck_y)

    # Deck line and its panel ticks.
    line(ax, (nodes[0], deck_y), (nodes[-1], deck_y), width=1.2, zorder=4)
    for x in nodes:
        line(ax, (x, deck_y), (x, bottom_y), width=1.2, zorder=4)

    # Chords, end posts, and vertical members.
    line(ax, (nodes[0], bottom_y), (nodes[-1], bottom_y), width=2.7)
    line(ax, (nodes[1], top_y), (nodes[-2], top_y), width=2.7)
    line(ax, (nodes[0], bottom_y), (nodes[1], top_y), width=2.4)
    line(ax, (nodes[-2], top_y), (nodes[-1], bottom_y), width=2.4)
    for x in nodes[1:-1]:
        line(ax, (x, bottom_y), (x, top_y), width=2.4)

    # Pratt diagonals descend toward the exact center from both sides.
    for panel in (2, 3, 4):
        left = panel - 1
        right = panel
        line(ax, (nodes[left], top_y), (nodes[right], bottom_y), width=2.4)
    for panel in (6, 7):
        left = panel - 1
        right = panel
        line(ax, (nodes[right], top_y), (nodes[left], bottom_y), width=2.4)

    accent_lower = (nodes[4], bottom_y)
    accent_upper = (nodes[5], top_y)
    line(
        ax,
        accent_upper,
        accent_lower,
        color=ACCENT,
        width=5.5,
        zorder=6,
    )
    ax.plot(
        [accent_upper[0], accent_lower[0]],
        [accent_upper[1], accent_lower[1]],
        linestyle="none",
        marker="o",
        markersize=3,
        markerfacecolor=ACCENT,
        markeredgecolor=ACCENT,
        markeredgewidth=0,
        zorder=7,
    )

    # Shift the leader bend 80 px left while retaining its vertical rise.
    rise_length = 70
    leader_bend = (
        accent_upper[0] + rise_length * math.cos(math.radians(75)) - 80,
        accent_upper[1] + rise_length * math.sin(math.radians(75)),
    )

    # Machinist title block, inset 26 px from the bottom and right edges.
    title_left = WIDTH - 26 - 205
    title_bottom = 26
    title_width = 205
    title_height = 44
    ax.add_patch(
        Rectangle(
            (title_left, title_bottom),
            title_width,
            title_height,
            facecolor="none",
            edgecolor=INK,
            linewidth=0.7,
            zorder=2,
        )
    )
    line(
        ax,
        (title_left, title_bottom + title_height / 2),
        (title_left + title_width, title_bottom + title_height / 2),
        width=0.7,
    )

    # Prime the renderer before measuring letter advances.
    fig.canvas.draw()
    annotation_right = 908
    first_line_width = letterspaced_text(
        ax,
        fig,
        annotation_right,
        leader_bend[1] + 30,
        "WHAT IT MUST NOT DO:",
        size=12.8,
        tracking=0.8,
        weight="semibold",
        word_spacing=3.0,
        align="right",
    )
    second_line_width = letterspaced_text(
        ax,
        fig,
        annotation_right,
        leader_bend[1] + 12,
        "YIELD, BUCKLE, RESONATE",
        size=12.8,
        tracking=0.8,
        weight="semibold",
        word_spacing=3.0,
        align="right",
    )
    annotation_left = annotation_right - max(
        first_line_width, second_line_width
    )
    # Callout shelf: the text block sits wholly above a full-width shelf,
    # and the diagonal attaches at the shelf end nearest the member.
    shelf_left = (annotation_left - 8, leader_bend[1])
    shelf_right = (annotation_right + 4, leader_bend[1])
    line(ax, accent_upper, shelf_left, width=0.7, zorder=8)
    line(ax, shelf_left, shelf_right, width=0.7, zorder=8)
    ax.plot(
        accent_upper[0],
        accent_upper[1],
        linestyle="none",
        marker="o",
        markersize=4,
        markerfacecolor=INK,
        markeredgecolor=INK,
        markeredgewidth=0,
        zorder=9,
    )
    letterspaced_text(
        ax,
        fig,
        title_left + 10,
        title_bottom + 29,
        "PLATE 001",
        size=7.5,
        tracking=1.0,
    )
    letterspaced_text(
        ax,
        fig,
        title_left + 10,
        title_bottom + 8,
        "MEMBER BY MEMBER",
        size=6.5,
        tracking=0.8,
        alpha=0.45,
    )

    canvas_size = fig.canvas.get_width_height()
    assert canvas_size == (WIDTH, HEIGHT)
    assert math.isclose(nodes[4], (nodes[0] + nodes[-1]) / 2)
    assert 300 <= accent_lower[0] <= 900 and 300 <= accent_upper[0] <= 900

    fig.savefig(
        "a3.png",
        dpi=DPI,
        facecolor=GROUND,
        edgecolor=GROUND,
        bbox_inches=None,
        pad_inches=0,
    )
    print(f"Output: {canvas_size[0]}x{canvas_size[1]}")
    plt.close(fig)


if __name__ == "__main__":
    main()
