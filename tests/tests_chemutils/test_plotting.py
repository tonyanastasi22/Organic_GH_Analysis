import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from chemutils.plotting import scatter_by_category, add_trendline_r2, annotate_extremes
def sample_df():
    x = np.linspace(0, 10, 20)
    y = 2.0 * x + 1.0 + np.random.normal(scale=0.5, size=x.size)
    fam = np.where(x < 5, "A", "B")
    names = [f"P{i}" for i in range(len(x))]
    return pd.DataFrame({"x": x, "y": y, "Family": fam, "Name": names})
def test_scatter_by_category_runs():
    df = sample_df(); fig, ax = plt.subplots(figsize=(4,3))
    ax = scatter_by_category(df, "x", "y", category_col="Family", add_trend=True)
    fig.canvas.draw(); plt.close(fig)
def test_add_trendline_r2_returns_values():
    df = sample_df(); fig, ax = plt.subplots(figsize=(4,3))
    m, b, r2 = add_trendline_r2(ax, df["x"].to_numpy(), df["y"].to_numpy())
    assert np.isfinite(m) and np.isfinite(b) and (0.0 <= r2 <= 1.0)
    plt.close(fig)
def test_annotate_extremes_runs():
    df = sample_df(); fig, ax = plt.subplots(figsize=(4,3))
    ax.scatter(df["x"], df["y"])
    top, bot = annotate_extremes(ax, df, "x", "y", label_col="Name", N=2, metric="distance")
    assert len(top) == 2 and len(bot) == 2
    fig.canvas.draw(); plt.close(fig)
