#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colormaps
import numpy as np

plt.rcParams['svg.fonttype'] = 'none'

def fancy_list(elements: list, n_rows: int = 1,  colormap = colormaps["Set3"]):
    """
    Plots a grid like list of elements using different colors for each.

    Parameters
    ----------
    elements : list
        Each of the elements that will be plotted.
    n_rows : int, optional
        Number of rows of the grid. Default = 1.
    colormap : matplotlib.colors.Colormap
        Colormap used for list elements. Default = matplotlib.colormaps["Set3"]
    """
    ax = plt.axes()
    ax.axis("off")

    n_cols = int(np.ceil(len(elements)/n_rows))
    h_sep = 1/n_cols
    v_sep = 1/n_rows
    pad = .22*min(h_sep, v_sep)/2
    width = .98*h_sep - pad*2
    height = .98*v_sep - pad*2


    style = patches.BoxStyle.Round(pad=pad)

    # Plot patches
    for i, text in enumerate(elements):
        y_i = int(i/n_cols)
        x_i = i%n_cols
        x = h_sep*x_i + pad
        y = 1 - (v_sep*y_i) - (height + pad)
        ax.add_patch(patches.FancyBboxPatch((x, y), width, height, boxstyle=style, color=colormap(i/len(elements))))
        ax.annotate(text, (x+width/2,y+height/2), color="w", ha="center", fontsize=20)
    plt.show()
