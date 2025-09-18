from typing import Optional, Sequence, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import linregress

def add_trendline_r2(ax: plt.Axes, x: np.ndarray, y: np.ndarray, *, label_in_legend: bool=True) -> Tuple[float,float,float]:
    res = linregress(x, y)
    m, b, r2 = res.slope, res.intercept, res.rvalue**2
    xs = np.linspace(np.min(x), np.max(x), 200)
    label = f"Trend: y={m:.2f}x+{b:.2f} (R²={r2:.4f})" if label_in_legend else None
    ax.plot(xs, m*xs + b, color="grey", lw=2, label=label, zorder=2)
    return m, b, r2

def scatter_by_category(df, xcol, ycol, category_col: Optional[str]=None, categories_order: Optional[Sequence[str]]=None,
                        ax: Optional[plt.Axes]=None, palette: str="tab20", s: int=40,
                        add_y_eq_x: bool=True, add_axes_cross: bool=True, add_trend: bool=True,
                        trend_label_in_legend: bool=True, legend_loc: str="best"):
    ax = ax or plt.gca()
    data = df[[xcol, ycol] + ([category_col] if category_col else [])].dropna()
    x = data[xcol].to_numpy(); y = data[ycol].to_numpy()
    if category_col:
        cats = categories_order or data[category_col].dropna().unique()
        cmap = getattr(cm, palette); colors = cmap(np.linspace(0, 1, len(cats)))
        for cat, color in zip(cats, colors):
            d = data[data[category_col] == cat]
            ax.scatter(d[xcol], d[ycol], s=s, color=color, label=str(cat), zorder=1)
    else:
        ax.scatter(x, y, s=s, color="black", label="Data", zorder=1)
    if add_trend:
        add_trendline_r2(ax, x, y, label_in_legend=trend_label_in_legend)
    if add_y_eq_x:
        ax.axline((0,0), slope=1, linestyle="--", linewidth=1)
    if add_axes_cross:
        ax.axhline(0, color="black", linewidth=2.0, zorder=0)
        ax.axvline(0, color="black", linewidth=2.0, zorder=0)
    ax.grid(True); ax.legend(loc=legend_loc)
    return ax

def annotate_extremes(ax, df, xcol, ycol, label_col, N: int=3, metric: str="distance",
                      top_color: str="red", bottom_color: str="green"):
    data = df[[xcol, ycol, label_col]].dropna().copy()
    if metric == "distance":
        data["_metric"] = np.sqrt(data[xcol]**2 + data[ycol]**2)
    elif metric in data.columns:
        data["_metric"] = data[metric]
    elif metric == "y":
        data["_metric"] = data[ycol]
    else:
        raise ValueError("Unsupported metric.")
    topN = data.nlargest(N, "_metric"); botN = data.nsmallest(N, "_metric")
    ax.scatter(topN[xcol], topN[ycol], color=top_color, s=100, label=f"Top {N}", zorder=3)
    ax.scatter(botN[xcol], botN[ycol], color=bottom_color, s=100, label=f"Bottom {N}", zorder=3)
    for i, (_, r) in enumerate(topN.iterrows()):
        offset = (0, 20) if i % 3 == 0 else (0, 10)
        ax.annotate(str(r[label_col]), (r[xcol], r[ycol]), textcoords="offset points", xytext=offset,
                    ha="center", fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
    for i, (_, r) in enumerate(botN.iterrows()):
        offset = (0,10) if i % 2 == 0 else (0, -15)
        ax.annotate(str(r[label_col]), (r[xcol], r[ycol]), textcoords="offset points", xytext=offset,
                    ha="center", fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
    return topN, botN

def add_inset_zoom(ax, xlim, ylim, width: str="35%", height: str="35%", loc: str="upper left"):
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
    axins = inset_axes(ax, width=width, height=height, loc=loc, borderpad=1.2)
    axins.set_xlim(*xlim); axins.set_ylim(*ylim); axins.grid(True)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    return axins
