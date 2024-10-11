import logging
from contextlib import _GeneratorContextManager
from typing import Optional

import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mltraq.utils.plotting import plot_ctx as mltraq_plot_ctx

from cumulative.opts import options

log = logging.getLogger(__name__)


def default_subplots() -> tuple[Figure, Axes]:
    """
    Create subplots with a given figsize config via options.
    """
    fig, ax = plt.subplots(figsize=options().get("plot.ctx.default.figsize"))
    return fig, ax


def plot_ctx(template_name: Optional[str] = None, **params) -> _GeneratorContextManager:
    """
    Return a context manager generator with options pulled
    from a template name `template_name`, and custom ones via `params`.
    """
    if not template_name:
        template_name = "plot.ctx.default"
    params = options().get(template_name) | params
    return mltraq_plot_ctx(**params)


class Plot:
    """
    This class provides an interface to a curated set of visualization routines.
    """

    def __init__(self, c):
        """
        Initializes the plotting interface for the `c` Cumulative instance.
        """
        self.c = c

    def xrays(
        self,
        src: str | None = None,
        ax: mpl.axes.Axes | None = None,
        alpha: float = 1,
        ms: float = 1,
        lw: float = 1,
        k: int = 20,
        style: str = "-",
        color=None,
    ):
        """
        Interpolate series on `k` points and render them as monochrome points/curves.
        """

        src = options().get("transforms.src", prefer=src)
        tmp = options().get("transforms.tmp") + ".plot"

        with options().ctx({"transforms.src": tmp, "transforms.dst": tmp}):

            self.c.copy(src=src)
            self.c.interpolate(method="pchipp", k=k, num=k)
            self.c.plot.draw(ax=ax, alpha=alpha, ms=ms, lw=lw, style=style, color=color)
            self.c.drop()
            return self

    def draw(
        self,
        src: str | None = None,
        ax: mpl.axes.Axes | None = None,
        style: str = ".",
        ms: float = 2,
        lw: float = 1,
        score: str | None = None,
        alpha: str | None = 0.5,
        only_changes: bool = False,
        color=None,
        colormap=None,
    ):
        """
        Basic visualization of a collection of series.
        """

        if not ax:
            _, ax = default_subplots()
            force_show = True
        else:
            force_show = False

        src = options().get("transforms.src", prefer=src)

        color = options().get("plot.color", prefer=color)
        cmap = mpl.colormaps[options().get("plot.colormap", prefer=colormap)]

        for _, row in self.c.df.iterrows():
            row_color = cmap(row[score]) if isinstance(score, str) else color
            row_alpha = row[alpha] if isinstance(alpha, str) else alpha

            if only_changes:
                # If activated, only the first occurrence of a repeated value is retained
                # and the subsequent ones are set to nan (lossless compression, provided
                # there are no missing values in the original series.)
                a = row[f"{src}.y"].copy()
                a = np.where(np.insert(np.diff(a), 0, 1) != 0, a, np.nan)
            else:
                a = row[f"{src}.y"]

            pd.Series(a, index=row[f"{src}.x"]).plot(
                style=style,
                lw=lw,
                ms=ms,
                color=row_color,
                alpha=row_alpha,
                ax=ax,
            )

        if force_show:
            # If the axis is the default one, we force the rendering of the plot
            # before returning (otherwise, it remains in the queue of plots to display.)
            plt.show()

        return self

    def fingerprint(
        self, src: str | None = None, ax: mpl.axes.Axes | None = None, score: str = "base.z", style="-", alpha=0.5
    ):
        """
        Sample and interpolate series on max 100 series, 100 points each, and use the ".z" suffix to select the
        color from the default colormap. This visualization is robust to large datasets, as it samples and
        simplifies the curves.
        """

        src = options().get("transforms.src", prefer=src)
        tmp = options().get("transforms.tmp") + ".plot"

        with options().ctx({"transforms.src": tmp, "transforms.dst": tmp}):

            # Copy from src to tmp, and then work only on tmp (the default src/dst)
            self.c.copy(src=src)
            self.c.sample(m=100)
            self.c.interpolate(method="pchipp", k=100, num=100)
            # Transform .interpolate cleans the tmp prefix, this is why we must create the score column afterwards.
            self.c.score(src=score, dst=f"{tmp}.score", method="value")
            # The highest value ir rendered last, increasing odds it is visible.
            self.c.sort(by=f"{tmp}.score.value")

            self.draw(src=src, ax=ax, style=style, ms=1, alpha=alpha, score=f"{tmp}.score.value", only_changes=True)
            # Transform .drop removes all columns with tmp prefix
            self.c.drop()
            return self
