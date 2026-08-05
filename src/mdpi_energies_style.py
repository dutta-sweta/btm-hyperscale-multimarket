"""
mdpi_energies_style.py
----------------------
Shared matplotlib style + export helpers that make every figure in this
project compliant with the MDPI *Energies* Instructions for Authors.

Key Energies rules encoded here
-------------------------------
* Figures should be high quality, preferably >= 600 dpi, in PNG/JPEG/TIFF.
  -> save_fig() writes a 600-dpi PNG (the submission artefact) plus a
     vector PDF (archival source of truth; regenerate, never hand-edit).
* Figures are inserted in the main text after the paragraph of first
  citation, numbered in order of appearance, with captions in the
  manuscript text (short explanatory title + description).
* Use minus signs (not em dashes) and decimal points in numbers.
* Colour figures at no extra cost; palette below is colour-blind safe
  (Okabe-Ito) so figures also survive greyscale printing.

Widths: MDPI Energies lays out single-column pages ~17 cm of text width.
  "narrow" = 90 mm, "medium" = 140 mm, "full" = 170 mm.

Usage
-----
    from mdpi_energies_style import set_style, COLS, OKABE_ITO, save_fig, new_fig
    set_style()
    fig, ax = new_fig(width="medium", height_ratio=0.62)
    ax.plot(...)
    save_fig(fig, "Figure_1")        # writes 600-dpi PNG + vector PDF
"""
from __future__ import annotations
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

# --- Figure widths (inches). MDPI text block is ~170 mm wide --------------
COLS = {
    "narrow": 90 / 25.4,    # 3.543 in
    "medium": 140 / 25.4,   # 5.512 in
    "full":   170 / 25.4,   # 6.693 in
}

# --- Okabe-Ito colour-blind-safe qualitative palette ----------------------
OKABE_ITO = {
    "blue":       "#0072B2",
    "orange":     "#E69F00",
    "green":      "#009E73",
    "vermillion": "#D55E00",
    "skyblue":    "#56B4E9",
    "yellow":     "#F0E442",
    "purple":     "#CC79A7",
    "black":      "#000000",
    "grey":       "#999999",
}
OKABE_ITO_CYCLE = [
    OKABE_ITO["blue"], OKABE_ITO["vermillion"], OKABE_ITO["green"],
    OKABE_ITO["orange"], OKABE_ITO["purple"], OKABE_ITO["skyblue"],
    OKABE_ITO["yellow"], OKABE_ITO["grey"],
]


def set_style() -> None:
    """Apply the shared rcParams. Call once at the top of a figure script."""
    mpl.rcParams.update({
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Helvetica Neue",
                            "Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "figure.titlesize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
        "axes.axisbelow": True,
        "lines.linewidth": 1.3,
        "lines.markersize": 5,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "grid.linewidth": 0.4,
        "grid.color": "#DDDDDD",
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO_CYCLE),
        "figure.dpi": 150,
        "savefig.dpi": 600,            # Energies: preferably >= 600 dpi
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "figure.autolayout": False,
    })


def new_fig(width: str = "medium", height_ratio: float = 0.72):
    """Create a figure sized to the MDPI text block ("narrow"/"medium"/"full")."""
    w = COLS[width]
    fig, ax = plt.subplots(figsize=(w, w * height_ratio))
    return fig, ax


def save_fig(fig, name: str, outdir: str = "figures",
             raster_dpi: int = 600, formats=("png", "pdf")) -> None:
    """Save `outdir/name.<ext>` for each format.

    PNG at >= 600 dpi is the MDPI submission artefact (insert into the Word
    manuscript). The PDF is the vector source of truth for archival; if a
    figure is wrong, fix the script and re-run; never hand-edit outputs.
    """
    os.makedirs(outdir, exist_ok=True)
    for ext in formats:
        path = os.path.join(outdir, f"{name}.{ext}")
        if ext in ("png", "tif", "tiff", "jpg", "jpeg"):
            fig.savefig(path, dpi=raster_dpi)
        else:
            fig.savefig(path)
        print(f"  wrote {path}")


def label_points(ax, xs, ys, labels, offsets=None, fontsize=7):
    """Simple per-point offset labels (fallback when adjustText is absent)."""
    offsets = offsets or {}
    for x, y, lab in zip(xs, ys, labels):
        dx, dy = offsets.get(lab, (4, 4))
        ax.annotate(lab, (x, y), textcoords="offset points",
                    xytext=(dx, dy), fontsize=fontsize,
                    color="#222222", annotation_clip=False)


def city_names(sites, with_state=False):
    """Convert site keys ('SBN_SouthBend_IN') or 'City, ST' to city names."""
    import re
    out = []
    for s in sites:
        s = str(s).strip()
        if "_" in s:
            parts = s.split("_")
            city = parts[1] if len(parts) > 1 else parts[0]
            state = parts[2] if len(parts) > 2 else ""
        elif "," in s:
            city, _, state = (p.strip() for p in s.partition(","))
        else:
            city, state = s, ""
        city = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", city)
        out.append(f"{city}, {state}" if (with_state and state) else city)
    return out


def label_points_repel(ax, xs, ys, labels, fontsize=6.8, seed=0,
                       line_color="#8a8a8a"):
    """Collision-free point labels with thin leader lines (adjustText).

    Deterministic given `seed`; falls back to label_points if adjustText
    is unavailable. Handles near-coincident points (markets that share a
    threshold) that manual offsets cannot.
    """
    try:
        import numpy as np
        from adjustText import adjust_text
    except Exception:                      # pragma: no cover
        return label_points(ax, xs, ys, labels, fontsize=fontsize)

    np.random.seed(seed)
    texts = [ax.text(float(x), float(y), str(lab), fontsize=fontsize,
                     color="#222222", ha="center", va="center")
             for x, y, lab in zip(xs, ys, labels)]
    adjust_text(
        texts, x=list(map(float, xs)), y=list(map(float, ys)), ax=ax,
        arrowprops=dict(arrowstyle="-", color=line_color, lw=0.45,
                        shrinkA=2, shrinkB=3),
        expand=(1.6, 1.9),
        force_text=(0.5, 0.9),
        force_static=(0.3, 0.6),
        min_arrow_len=4,
        time_lim=3,
    )
    return texts
