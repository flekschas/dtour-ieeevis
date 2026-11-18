"""Turn the marimo export `deck.html` into the static web deck `site/index.html`.

    MARIMO_OUTPUT_MAX_BYTES=500000000 uvx marimo export html --sandbox ieee-vis-2026.py -o deck.html
    python3 scripts/build_web_deck.py

The export inlines every image and video as a data URI and its live dtour widgets need Python. This
swaps the media for the web encodings in `assets/web/`, the dtour widgets for iframes of the dtour
webapp in `site/app/` (same origin, so linked selections work), and the Fashion MNIST image widget for
the standalone `<fm-images>` element (`site/fm-images.js`). The live notebook stays untouched.

Note: `marimo.toml` overrides MARIMO_OUTPUT_MAX_BYTES, so leave `output_max_bytes` out of it.
"""

import base64
import json
import re
import shutil
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
WEB = ASSETS / "web"
SITE = ROOT / "site"

# The notebook's color maps: dtour.build_color_map(sorted labels, theme="dark")
FMNIST_COLORS = {
    "Bag": "#0072b2", "Boot": "#e69f00", "Coat": "#009e73", "Dress": "#cc79a7", "Pullover": "#56b4e9",
    "Sandal": "#d55e00", "Shirt": "#0000ff", "Sneaker": "#d70000", "T-shirt": "#009700",
    "Trouser": "#f0e442",
}  # fmt: skip
BRAIN_COLORS = {
    "Blood": "#0072b2", "Choroid plexus": "#e69f00", "Ectoderm": "#009e73", "Endoderm": "#cc79a7",
    "Ependymal": "#56b4e9", "Fibroblast": "#d55e00", "Gastrulation": "#f0e442", "Glioblast": "#d70000",
    "Immune": "#009700", "Mesenchyme": "#0000ff", "Mesoderm": "#ffba00", "Neural crest": "#00d0ff",
    "Neural tube": "#ff00ba", "Neuroblast": "#8f5a00", "Neuron": "#00ff97",
    "Olfactory ensheathing cell": "#a900ff", "Oligodendrocyte": "#818181", "Pineal gland": "#ff8161",
    "Radial glia": "#006b4f", "Schwann cell": "#6d6dff", "Subcommissural organ": "#ff0039",
    "Vascular": "#89ab00",
}  # fmt: skip

BRAIN = {"themeMode": "dark", "pointColorBy": "Class", "pointOpacity": 0.5, "pointColorMap": BRAIN_COLORS, "link": "brain"}
BRAIN_VIEWS = [
    {**BRAIN, "tourDimensions": [f"PC{i}" for i in range(1, 9)], "previewSize": "small",
     "previewCount": 8, "showLegend": False},
    {**BRAIN, "tourDimensions": ["UMAP1", "UMAP2"]},
]  # fmt: skip
FMNIST_VIEWS = [
    {"themeMode": "dark", "pointColorBy": "label", "pointColorMap": FMNIST_COLORS, "tooltipColumns": ["image", "label"],
     "cameraZoom": 0.5, "previewCount": 4, "previewSize": "medium", "link": "fmnist"},
]  # fmt: skip


def app_url(params):
    """The bundled dtour webapp. Its relative URLs, e.g., data files, resolve against `app/`."""
    query = "&".join(f"{k}={quote(v if isinstance(v, str) else json.dumps(v), safe='')}" for k, v in params)
    return f"app/?{query}"


# marimo wraps every <iframe> of an output in an unstyled <div>, so the frame stretches that wrapper too
FRAME_CSS = (
    "<style>.dt-frame { display:flex; min-width:0; min-height:0; }"
    " .dt-frame > div { display:flex; flex:1; min-width:0; min-height:0; }"
    " .dt-frame iframe { flex:1; width:100%; height:100%; min-height:0; border:0; background:#000; }</style>"
)


def iframe(src, flex=1):
    return f'<div class="dt-frame" style="flex:{flex}"><iframe src="{escape(src)}" allow="fullscreen"></iframe></div>'


WIDGET_ROW = re.compile(r'<div class="dt-row dt-measure".*?</marimo-ui-element></div></div>', re.S)
SLIDES = {
    # Brain atlas: a little tour over PC1-8 linked to the 2D UMAP of the same file
    "Validating non-linear DR outputs": FRAME_CSS
    + iframe(
        app_url([("url", "../data/lamanno2021-pca-umap.pq"), ("views", BRAIN_VIEWS)])
    ),
    # Fashion MNIST: the attraction-repulsion tour next to the images of the selected points
    "Gradually revealing structure": (
        FRAME_CSS
        + '<div class="dt-row" style="gap:1cqw">'
        + iframe(
            app_url(
                [
                    ("url", "../data/fashion-mnist-attraction-repulsion-tour.pq"),
                    ("views", FMNIST_VIEWS),
                ]
            ),
            flex=4,
        )
        + '<div class="dt-col" style="flex:1">'
        + f"<fm-images link=\"fmnist\" rows=\"70000\" colors='{escape(json.dumps(FMNIST_COLORS))}'></fm-images>"
        + "</div></div>"
    ),
}


# Build steps the web deck skips: (HTML of a fragment, the same HTML without the fragment)
FRAGMENTS = [
    # Two tour strategies: show "Hyperdimensional tours" with the slide; "Sequential tours" stays a click
    (
        '<div class="dt-col fragment" data-fragment-index="1" style="flex:1">'
        '<div class="dt-family-name" style="text-align:center">Hyperdimensional tours</div>',
        '<div class="dt-col" style="flex:1">'
        '<div class="dt-family-name" style="text-align:center">Hyperdimensional tours</div>',
    ),
]


def web_name(name):
    stem, suffix = name.rsplit(".", 1)
    return f"{stem}.{ {'png': 'webp', 'mov': 'webm'}.get(suffix, suffix) }"


def read_object(text, marker):
    """The JSON value following the regex `marker` in `text`, and its span."""
    start = re.search(marker, text).end()
    value, end = json.JSONDecoder().raw_decode(text, start)
    return value, start, end


def to_js(value):
    """JSON that is safe inside a <script>, escaped like marimo's export."""
    text = json.dumps(value)
    return text.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")


def main():
    deck = (ROOT / "deck.html").read_text(encoding="utf-8")

    # Every asset by the start of its base64, to recognize it in the data URIs
    by_prefix = {
        base64.b64encode(path.read_bytes()[:3000]).decode(): path.name
        for path in ASSETS.iterdir()
        if path.is_file() and not path.name.startswith(".")
    }
    used = set()

    def swap_media(match):
        name = by_prefix.get(match[2][:4000])
        if name is None:
            sys.exit(f"An inlined {match[1]} matches no file in assets/")
        if not (WEB / web_name(name)).exists():
            sys.exit(f"Missing the web encoding of {name}: assets/web/{web_name(name)}")
        used.add(web_name(name))
        return f"assets/web/{quote(web_name(name))}"

    config, start, end = read_object(deck, r'"__MARIMO_MOUNT_CONFIG__",\s*\{\s*value:\s*Object\.freeze\(')
    removed_models = set()
    found_fragments = set()
    for cell in config["session"]["cells"]:
        for output in cell.get("outputs", []):
            html = output.get("data", {}).get("text/html")
            if html is None:
                continue
            html = re.sub(r"data:([a-z]+/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)", swap_media, html)
            html = html.replace("https://dtour.dev/?dataset=", "app/?dataset=")
            for title, replacement in SLIDES.items():
                if title in html:
                    row = WIDGET_ROW.search(html)
                    removed_models |= set(re.findall(r"data-model-id='&quot;([0-9a-f]+)&quot;'", row[0]))
                    html = html[: row.start()] + replacement + html[row.end() :]
            for i, (fragment, shown) in enumerate(FRAGMENTS):
                if fragment in html:
                    html = html.replace(fragment, shown)
                    found_fragments.add(i)
            output["data"]["text/html"] = html
    if missing := [FRAGMENTS[i][0] for i in range(len(FRAGMENTS)) if i not in found_fragments]:
        sys.exit(f"Fragments not found, did the slides change? {missing}")
    outputs = json.dumps(config["session"])
    removed_models = {m for m in removed_models if m not in outputs}
    deck = deck[:start] + to_js(config) + deck[end:]

    # Drop the widget models no slide shows anymore, with their layouts
    models, start, end = read_object(deck, r"modelNotifications:\s*Object\.freeze\(")
    layouts = {
        n["message"]["state"].get("layout", "").removeprefix("IPY_MODEL_")
        for n in models
        if n["model_id"] in removed_models and isinstance(n["message"].get("state"), dict)
    }
    models = [n for n in models if n["model_id"] not in removed_models | layouts]
    deck = deck[:start] + to_js(models) + deck[end:]

    head, body, tail = deck.rpartition("</body>")
    deck = head + '<script type="module" src="fm-images.js"></script>\n' + body + tail

    (SITE / "assets" / "web").mkdir(parents=True, exist_ok=True)
    for name in used:
        shutil.copy2(WEB / name, SITE / "assets" / "web" / name)
    (SITE / "index.html").write_text(deck, encoding="utf-8")
    (SITE / ".nojekyll").touch()
    print(f"site/index.html: {len(deck.encode()) / 1e6:.1f} MB, {len(used)} media files, "
          f"{len(removed_models)} widgets replaced")  # fmt: skip


if __name__ == "__main__":
    main()
