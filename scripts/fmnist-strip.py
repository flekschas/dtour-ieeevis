# /// script
# dependencies = ["matplotlib", "numpy", "pyarrow", "scikit-learn"]
# requires-python = ">=3.12"
# ///
"""Render the dark Fashion MNIST strip for the problem slide: PCA, then the attraction-repulsion spectrum.

The spectrum embeddings (LE-like → t-SNE-like) come from the same parquet as the live Fashion MNIST
slide. PCA uses the raw OpenML pixels, which are in the same row order (checked via the labels).

    uv run scripts/fmnist-strip.py
"""

import io
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA

OUT = Path(__file__).parent.parent / "assets" / "fmnist-strip-dark.png"
TOUR_URL = "https://data.dtour.dev/fashion-mnist-attraction-repulsion-tour.pq"
NAMES = ["T-shirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Boot"]
# dtour.build_color_map(sorted(labels), theme="dark"), as on the live Fashion MNIST slide
COLORS = {
    "Bag": "#0072b2", "Boot": "#e69f00", "Coat": "#009e73", "Dress": "#cc79a7", "Pullover": "#56b4e9",
    "Sandal": "#d55e00", "Shirt": "#f0e442", "Sneaker": "#d70000", "T-shirt": "#009700", "Trouser": "#0000ff",
}  # fmt: skip

request = urllib.request.Request(TOUR_URL, headers={"User-Agent": "dtour"})
tour = pq.read_table(io.BytesIO(urllib.request.urlopen(request).read())).to_pydict()
labels = np.array(tour["label"])

pixels = fetch_openml("Fashion-MNIST", version=1, as_frame=False, parser="liac-arff")
assert (np.array(NAMES)[pixels.target.astype(int)] == labels).all(), "row order differs from the tour parquet"
pca = PCA(n_components=2).fit_transform(pixels.data.astype(np.float32))

panels = [pca] + [np.column_stack([tour[f"sp_{2 * i}"], tour[f"sp_{2 * i + 1}"]]) for i in range(4)]
colors = np.array([COLORS[label] for label in labels])
order = np.random.default_rng(0).permutation(len(labels))  # no class is always drawn on top

fig, axes = plt.subplots(1, len(panels), figsize=(5 * len(panels), 5), facecolor="#000")
for ax, xy in zip(axes, panels):
    ax.scatter(*xy[order].T, c=colors[order], s=0.6, alpha=0.5, linewidths=0, rasterized=True)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_facecolor("#000")
    ax.axis("off")
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98, wspace=0.08)
fig.savefig(OUT, dpi=160, facecolor="#000")
print(f"wrote {OUT}")
