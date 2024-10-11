import argparse
import textwrap
import io
from collections.abc import Callable, Sequence
from functools import partial
from pathlib import Path
from typing import Literal, Optional, cast

import matplotlib.font_manager as fm
import matplotlib.image as mpimage
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.text import Annotation
from matplotlib.transforms import Bbox
from tqdm import tqdm


from ithappens.card import Card
from ithappens.utils import slugify


def text_with_wrap_autofit(
    ax: plt.Axes,
    txt: str,
    xy_size: tuple[float, float],
    width: float,
    height: float,
    *,
    min_font_size=None,
    bleed: Optional[float] = None,
    pad: Optional[float] = None,
    show_rect: bool = False,
    **kwargs,
):
    """Automatically fits the text to some axes.

    Args:
        ax: axes to put the text on.
        txt: text to display.
        xy: location to place the text.
        width: width of the text box in fractions.
        height: height of the text box in fractions.
        min_font_size: minimum acceptable font size.
        bleed: bleed of the figure.
        pad: padding of the box.
        **kwargs: keyword arguments passed to Axes.annotate.

    Returns:
        text artist.
    """

    #  Different alignments give different bottom left and top right anchors.
    x, y = xy_size
    if bleed is None:
        bleed = 0
    if pad:
        bleed += pad
        x -= 2 * pad
        y -= 2 * pad

    if show_rect:
        alpha = 0.3
    else:
        alpha = 0

    rect = Rectangle(
        (bleed + (1 - width) * x, bleed + (1 - height) * y),
        width * x,
        height * y,
        alpha=alpha,
    )
    ax.add_patch(rect)

    # Get transformation to go from display to data-coordinates.
    inv_data = ax.transData.inverted()

    fig: Figure = ax.get_figure()
    dpi = fig.dpi
    rect_height_inch = rect.get_height() / dpi

    # Initial fontsize according to the height of boxes
    fontsize = rect_height_inch * 72

    wrap_lines = 1
    xy = (bleed + 0.5 * x, bleed + 0.95 * y)
    while True:
        wrapped_txt = "\n".join(
            textwrap.wrap(txt, width=len(txt) // wrap_lines, break_long_words=False)
        )

        # For dramatic effect, place text after ellipsis on newline.
        wrapped_txt = wrapped_txt.replace("... ", "...\n")
        wrapped_txt = wrapped_txt.replace("… ", "...\n")
        text: Annotation = ax.annotate(wrapped_txt, xy, **kwargs)
        text.set_fontsize(fontsize)

        # Adjust the fontsize according to the box size.
        bbox: Bbox = text.get_window_extent()
        inv_text_bbox = inv_data.transform(bbox)
        width_text = inv_text_bbox[1][0] - inv_text_bbox[0][0]
        adjusted_size = fontsize * rect.get_width() / width_text
        if min_font_size is None or adjusted_size >= min_font_size:
            break
        text.remove()
        wrap_lines += 1
    text.set_fontsize(adjusted_size)

    return text


class ithappensArgs(argparse.Namespace):
    input_dir: str
    name: str
    merge: bool
    rank: bool
    side: Literal["front", "back", "both"]
    format: Literal["pdf", "png"]
    workers: int
    chunks: int


def parse_input_file(
    input_path: Path,
) -> pd.DataFrame:
    """Parse an input file.

    It must have two colums: descriptions along with their misery index.

    Args:
        intput_path: path of the input file (.csv or .xlsx)

    Returns:
        Pandas DataFrame with index, description, and misery index.
    """
    usecols = ["misery index", "situation"]
    try:
        df = pd.read_excel(input_path)
        df = df[usecols]
    except ValueError:
        pass
    except KeyError:
        print(f"Make sure {input_path} has two columns named {usecols}.")
        exit()
    else:
        return df

    try:
        df = pd.read_csv(input_path)
        df = df[usecols]
    except UnicodeDecodeError:
        print(f"{input_path} is not a valid .csv or .xlsx file.")
        exit()
    except KeyError:
        print(f"Make sure {input_path} has two columns named {usecols}.")
        exit()
    else:
        return df


def plot_crop_marks(ax: Axes, bleed: float, factor: float = 0.6):
    """Plots crop marks on the given axis.
    The crop marks will mark the bleed. The crop mark size is adjustable with the factor.
    """
    crop_mark_len = factor * bleed
    fig = ax.get_figure()
    bbox: Bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    x_size, y_size = bbox.width, bbox.height

    # h, v - horizontal, vertical
    # u, d - up, down
    # l, r - left, right
    hul = (y_size - bleed, 0, crop_mark_len)
    hdl = (bleed, 0, crop_mark_len)
    hur = (y_size - bleed, x_size - crop_mark_len, x_size)
    hdr = (bleed, x_size - crop_mark_len, x_size)
    vul = (bleed, y_size - crop_mark_len, y_size)
    vdl = (bleed, 0, crop_mark_len)
    vur = (x_size - bleed, y_size - crop_mark_len, y_size)
    vdr = (x_size - bleed, 0, crop_mark_len)

    cropmarkstyle = {"color": "white", "linewidth": 1}

    for horizontal_mark in [hul, hdl, hur, hdr]:
        ax.hlines(*horizontal_mark, **cropmarkstyle)
    for vertical_mark in [vul, vdl, vur, vdr]:
        ax.vlines(*vertical_mark, **cropmarkstyle)


def plot_card_front(card: Card) -> Figure:
    # To be able to convert between centimeters and inches.
    cm_per_inch = 2.54

    # 62x88 mm for typical playing cards.
    x_size = 6.2 / cm_per_inch  # cm front and back
    y_size = 8.8 / cm_per_inch  # cm top to bottom

    # Add margin on all sides.
    bleed = 0.5 / cm_per_inch  # cm
    pad = 0.3 / cm_per_inch

    x_total = x_size + 2 * bleed
    y_total = y_size + 2 * bleed
    xy_size = (x_total, y_total)

    plt.style.use("ithappens")
    fig, ax = plt.subplots()

    fig.set_size_inches(*xy_size)
    fig.set_facecolor("black")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.axis("off")

    ax.set_xlim(0, x_total)
    ax.set_ylim(0, y_total)

    prop = fm.FontProperties(weight="extra bold")

    text_kwargs = dict(wrap=True, horizontalalignment="center", fontproperties=prop)

    # Front.
    text_with_wrap_autofit(
        ax,
        card.desc.upper(),
        (x_size, y_size),
        1,
        0.4,
        **text_kwargs,
        bleed=bleed,
        pad=pad,
        min_font_size=11,
        va="top",
        weight="extra bold",
        color="yellow",
    )

    mi_desc = "misery index"
    ax.text(
        x_total / 2,
        1.3 * y_size / 8 + bleed,
        mi_desc.upper(),
        **text_kwargs,
        color="yellow",
        fontsize=13,
        weight="extra bold",
        verticalalignment="center",
    )

    ax.text(
        x_total / 2,
        0.05 * y_size + bleed,
        card.misery_index if ".5" in str(card.misery_index) else int(card.misery_index),
        **text_kwargs,
        color="black",
        fontsize=23,
        weight="extra bold",
        verticalalignment="center",
    )

    mi_block = Rectangle(
        (bleed + x_size / 4, 0), x_size / 2, y_size / 8 + bleed, fc="yellow"
    )
    ax.add_patch(mi_block)

    plot_crop_marks(ax, bleed)

    plt.close(fig)

    return fig


def plot_card_back(card: Card, expansion_logo_path: Path | None = None) -> Figure:
    # To be able to convert between centimeters and inches.
    cm_per_inch = 2.54

    # 62x88 mm for typical playing cards.
    x_size = 6.2 / cm_per_inch  # cm front and back
    y_size = 8.8 / cm_per_inch  # cm top to bottom

    # Add margin on all sides.
    bleed = 0.5 / cm_per_inch  # cm

    x_total = x_size + 2 * bleed
    y_total = y_size + 2 * bleed
    xy_size = (x_total, y_total)

    plt.style.use("ithappens")
    fig, ax = plt.subplots()

    fig.set_size_inches(*xy_size)
    fig.set_facecolor("black")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.axis("off")

    prop_regular = fm.FontProperties(weight="regular")

    text_kwargs = dict(
        wrap=True, horizontalalignment="center", fontproperties=prop_regular
    )

    game_name = "It Happens"
    expansion_text = "edition"
    expansion_text_full = card.expansion_name + " " + expansion_text

    ax.text(
        x_size / 2 + bleed,
        0.9 * y_size + bleed,
        game_name.upper(),
        **text_kwargs,
        color="yellow",
        fontsize=20,
        weight="regular",
        verticalalignment="center",
    )

    prop_light = fm.FontProperties(weight="regular")

    text_kwargs = dict(
        wrap=True, horizontalalignment="center", fontproperties=prop_light
    )

    ax.text(
        x_size / 2 + bleed,
        0.83 * y_size + bleed,
        expansion_text_full.upper(),
        **text_kwargs,
        color="yellow",
        fontsize=14,
        fontstyle="italic",
        weight="ultralight",
        verticalalignment="center",
    )

    # Expansion logo
    if expansion_logo_path is None:
        parent_dir = Path(__file__).parent.resolve()
        expansion_logo_path = parent_dir / Path("images/expansion-logo.png")

    expansion_logo = mpimage.imread(str(expansion_logo_path))

    expansion_logoax = fig.add_axes([0.2, 0.1, 0.6, 0.6])
    expansion_logoax.imshow(
        expansion_logo,
    )
    expansion_logoax.axis("off")

    plot_crop_marks(ax, bleed)

    ax.set_xlim(0, x_total)
    ax.set_ylim(0, y_total)

    plt.close(fig)

    return fig


def save_card(
    card: Card,
    output_dir: Path,
    side: Literal["front", "back"],
    dpi: int = 300,
    format: str = "pdf",
) -> None:
    side_fn = "front" if side == "front" else "back"

    output_dir = output_dir / side_fn

    output_dir.mkdir(parents=True, exist_ok=True)

    fn = f"{card.misery_index}-{card.desc}"
    fn = slugify(fn)
    save_fn = (output_dir / fn).with_suffix("." + format)

    if side == "front":
        card.fig_front.savefig(
            str(save_fn),
            format=save_fn.suffix[1:],
            pad_inches=0,
            dpi=dpi,
            transparent=False,
        )
    elif side == "back":
        card.fig_back.savefig(
            str(save_fn),
            format=save_fn.suffix[1:],
            pad_inches=0,
            dpi=dpi,
            transparent=False,
        )


def create_card(
    row,
    expansion_name,
    expansion_logo_path,
    output_dir,
    side,
    ext: Literal["pdf", "png"],
) -> Card:
    card = Card(row[1]["situation"], row[1]["misery index"], expansion_name)

    if side == "front" or side == "both":
        card.fig_front = plot_card_front(card)
        save_card(card, output_dir, "front", format=ext)

    if side == "back" or side == "both":
        card.fig_back = plot_card_back(card, expansion_logo_path)
        save_card(card, output_dir, "back", format=ext)

    return card


def create_cards(
    df: pd.DataFrame,
    expansion_name: str,
    expansion_logo_path: Path,
    output_dir: Path,
    merge: bool,
    side: Literal["front", "back", "both"],
    ext: Literal["pdf", "png"],
    workers: int,
    callbacks: Sequence[Callable] | None = None,
) -> None:
    nmax = df.shape[0]
    create_card_par = partial(
        create_card,
        expansion_name=expansion_name,
        expansion_logo_path=expansion_logo_path,
        output_dir=output_dir,
        side=side,
        ext=ext,
    )
    desc = "Plotting cards"
    from concurrent.futures import ProcessPoolExecutor, as_completed

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(create_card_par, row) for row in df.iterrows()]
        cards = []
        for future in tqdm(as_completed(futures), total=nmax, desc=desc):
            card = future.result()
            cards.append(card)
            for callback in callbacks:
                callback()

    if merge:
        with PdfPages(output_dir / "front" / "merged.pdf") as pdf:
            for card in cards:
                pdf.savefig(card.fig_front)
        with PdfPages(output_dir / "back" / "merged.pdf") as pdf:
            for card in cards:
                pdf.savefig(card.fig_back)


def main(**args) -> None:
    input_file = args["input_file"]
    output_dir = Path(args["output_dir"])
    expansion_logo_path = (
        Path(args["expansion_logo_path"]) if args["expansion_logo_path"] else None
    )

    if args["name"]:
        expansion_name = args["name"]
    else:
        try:
            expansion_name = Path(input_file).stem
        except TypeError:  # In streamlit, the input_file is a file object.
            input_file = cast(io.BytesIO, input_file)
            expansion_name = Path(input_file.name).stem
        print(
            "Argument -n/--name not given. "
            f"Expansion name inferred to be {expansion_name}."
        )

    df = parse_input_file(input_file)

    callbacks = args.get("callbacks", None)

    create_cards(
        df,
        expansion_name,
        expansion_logo_path,
        output_dir,
        args["merge"],
        args["side"],
        args["format"],
        args["workers"],
        callbacks,
    )


def main_cli(**kwargs):
    try:
        main(**kwargs)
    except KeyboardInterrupt:
        print("Interrupted.")


if __name__ == "__main__":
    main()
