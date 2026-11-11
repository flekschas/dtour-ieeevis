# /// script
# dependencies = [
#     "anywidget==0.11.0",
#     "dtour==0.5.2",
#     "marimo",
#     "numpy==2.5.4",
#     "polars==2.1.0",
#     "pyarrow==26.0.0",
#     "traitlets==5.16.1",
# ]
# requires-python = ">=3.14"
#
# [tool.marimo.display]
# theme = "dark"
#
# [tool.uv]
# # dtour is ours: take new releases right away despite the global `exclude-newer` cutoff
# exclude-newer-package = { dtour = false }
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="IEEE VIS 2026",
    layout_file="layouts/ieee-vis-2026.slides.json",
    css_file="custom.css",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## dtour @ IEEE VIS 2026 — talk draft (9 min)

    | # | Slide | Target |
    |---|---|---|
    | 1 | Title | 0:30 |
    | 2 | Problem: one 2D projection is not enough | 0:45 |
    | 3 | Many projections on the freedom-of-traversal axis → dtour unifies them (builds) | 1:30 |
    | 4 | Live: the interface on two linked rings in 4D (full-bleed dtour.dev) | 2:15 |
    | 5 | Smooth by design | 0:30 |
    | 6 | Two tour families: hyperdimensional & sequential | 0:30 |
    | 7 | Live · Validating non-linear DR outputs (brain atlas) | 1:15 |
    | 8 | Live · Gradually revealing structure (Fashion MNIST) | 1:15 |
    | 9 | Thanks + honorable mention | 0:20 |
    |   | **Total** | **~8:50** |

    Talking points live in the slides' speaker notes.
    Dashed boxes marked **VISUAL** are placeholders for media still to be made.
    Mark this cell as *skip* in the slides layout.
    """)
    return


@app.cell
def _(ASSETS, background, kicker, mo, row, slide, title):
    slide(
        background(mo.video(ASSETS / "gaussian-blobs.mov", controls=False, muted=True, autoplay=True, loop=True)),
        kicker("IEEE VIS 2026"),
        '<div style="flex:1"></div>',
        title('dtour: A Steerable <i>Tour de Vis</i><br>Through High-Dimensional Data', xl=True),
        row(
            *(
                f'<div><div style="font-size:2cqw; font-weight:800">{name}</div>'
                f'<div style="font-size:1.4cqw">{position}</div>'
                f'<div class="dt-muted" style="font-size:1.4cqw">{affiliation}</div></div>'
                for name, position, affiliation in [
                    ("Fritz Lekschas", "Founding Research Engineer", "Ridge AI"),
                    (
                        "Nezar Abdennur",
                        "Assistant Professor of Genomics and Computational Biology",
                        "UMass Chan Medical School",
                    ),
                ]
            ),
            gap="4cqw",
            style="flex:0 0 auto; margin-top:2.4cqw",
        ),
        '<div class="dt-muted" style="font-size:1.4cqw; margin-top:1.6cqw">dtour.dev&ensp;·&ensp;github.com/flekschas/dtour</div>',
    )
    return


@app.cell
def _(img, kicker, slide, title):
    slide(
        kicker("The problem"),
        title("Understanding high-dimensional data is hard."),
        '<div style="font-size:1.9cqw">Fashion MNIST: 70K images × 784 pixels, five 2D projections. Which one is <b>faithful</b>?<br>'
        '<span class="dt-y">Each one hides or distorts some information.</span></div>',
        '<div style="flex:1"></div>',
        img("fmnist-strip-dark.png", "width:100%"),
        '<div class="dt-muted" style="display:grid; grid-template-columns:repeat(5,1fr); text-align:center; font-size:1.2cqw">'
        "<span>PCA</span><span>LE-like</span><span>ForceAtlas2-like</span><span>UMAP-like</span><span>t-SNE-like</span></div>",
        # The punchline fades in on click (reveal.js fragment)
        '<div class="dt-h1 dt-y fragment" data-fragment-index="1" style="text-align:center; margin-top:1.2cqw">'
        "One 2D projection is not enough.</div>",
        '<div style="flex:1"></div>',
    )
    return


@app.cell
def _(ASSETS, data_uri, kicker, mo, play_on_fragments, slide):
    import re as _re

    # Build steps (reveal.js fragments): 1 play the guided tour · 2 play the manual tour (guided tour stops)
    # · 3 cognitive load · 4 dtour unifies the modes · 5 mantra · 6 takeaway
    def _step(i, effect="", cls=""):
        classes = " ".join(c for c in ("fragment", effect, cls) if c)
        return f'class="{classes}" data-fragment-index="{i}"'


    _Y = "#FEC10E"
    _modes = [
        (230, "Scatter plot matrix", "static grid · compare at a glance", "Overview", "keyframe gallery"),
        (800, "Guided tour", "a movie along a fixed path", "Zoom &amp; filter", "scrub, select &amp; color"),
        (1370, "Manual tour", "drag axes · full control", "Details on demand", "manual &amp; grand tour"),
    ]
    # Each box shows its classic tool, cropped to fill the box. When dtour takes over (step 4), the
    # tools fade out and dtour's take on each mode fades in. Videos start and stop with the build steps.
    def _src(element):
        """The URL marimo serves an asset under, so large media isn't inlined as a data URI."""
        return _re.search(r"src=['\"]([^'\"]+)", element.text)[1]


    def _fill(x, inner, step):
        """`inner` (an <img> or <video>) fills the box at `x`, like `background-size: cover`."""
        return (
            f'<g {step}><foreignObject x="{x - 199}" y="63" width="398" height="216">'
            '<div xmlns="http://www.w3.org/1999/xhtml" style="width:100%; height:100%; border-radius:13px; overflow:hidden; background:#fff">'
            f"{inner}</div></foreignObject></g>"
        )


    _COVER = 'style="display:block; width:100%; height:100%; object-fit:cover"'


    def _img(name):
        return f'<img src="{_src(mo.image(ASSETS / name))}" {_COVER}/>'


    def _video(name, start, until=None):
        until_attr = f' data-play-until="{until}"' if until else ""
        return (
            f'<video src="{_src(mo.video(ASSETS / name))}" muted="" loop="" playsinline="" preload="auto"'
            f' data-play-from="{start}"{until_attr} {_COVER}></video>'
        )


    _tools = [
        _img("scatter-plot-matrix-original.gif"),  # transparent, on the white box background
        _video("ggobi - tour - short.mov", start="dt-play-1", until="dt-play-2"),
        _video("manual-tour-distill.mov", start="dt-play-2", until="dt-play-dtour"),
    ]
    _dtour = [
        _img("dtour-overview.png"),
        _video("dtour-guided.mov", start="dt-play-dtour"),
        _video("dtour-manual.mov", start="dt-play-dtour"),
    ]
    _credits = ["John Hartigan", "Wickham &amp; Cook", "Li, Zhao, Scheidegger"]

    # Boxes 62–280, captions below them. The mantra pills fade in over the boxes' lower part, and the
    # dtour outline ends 24 below the credits, matching the gap above the mode names.
    _boxes = "".join(
        f'<text x="{x}" y="46" class="dt-d-name">{name}</text>'
        f'<rect x="{x - 200}" y="62" width="400" height="218" rx="14" {_step(4, "fade-out", "dt-d-box")}/>'
        f'<rect x="{x - 200}" y="62" width="400" height="218" rx="14" {_step(4, cls="dt-d-box dt-d-dashed")}/>'
        + _fill(x, tool, _step(4, "fade-out"))
        + _fill(x, dtour, _step(4))
        + f'<text x="{x}" y="308" class="dt-d-sub">{sub}</text>'
        f'<text x="{x}" y="330" {_step(4, "fade-out", "dt-d-credit")}>{credit}</text>'
        f'<g {_step(5, "fade-up")}><rect x="{x - 200}" y="216" width="400" height="64" rx="14" class="dt-d-mantra"/>'
        f'<text x="{x}" y="244" class="dt-d-mantra-name">{mantra}</text><text x="{x}" y="270" class="dt-d-mantra-sub">{mantra_sub}</text></g>'
        for (x, name, sub, mantra, mantra_sub), tool, dtour, credit in zip(_modes, _tools, _dtour, _credits)
    )
    _arrows = "".join(
        f'<line x1="{x}" y1="171" x2="{x + 140}" y2="171" class="dt-d-arrow" marker-start="url(#dt-d-head)" marker-end="url(#dt-d-head)"/>'
        for x in (445, 1015)
    )
    # Hand-sketched curves (assets/cognitive-load-*.png): illustrative, not data. The dtour sketch keeps a
    # faint ghost of the "before" curve, so cross-fading the two reads as the old curve stepping back.
    _CURVE = 'x="0" y="440" width="1600" height="112" preserveAspectRatio="none"'

    _diagram = f"""<svg viewBox="0 -45 1600 640" style="width:100%; flex:none; overflow:visible" font-family="inherit">
    <style>
      .dt-d-name {{ fill: #fff; font-size: 30px; font-weight: 800; text-anchor: middle; }}
      .dt-d-sub {{ fill: #A9A9A9; font-size: 22px; text-anchor: middle; }}
      .dt-d-box {{ fill: #161616; stroke: #555; stroke-width: 2; }}
      .dt-d-dashed {{ fill: none; stroke: #888; stroke-dasharray: 10 8; }}
      .dt-d-arrow {{ stroke: #888; stroke-width: 2.5; }}
      .dt-d-dtour {{ fill: none; stroke: {_Y}; stroke-width: 3; }}
      .dt-d-mantra {{ fill: #2a2410; stroke: {_Y}; stroke-width: 1.5; }}
      .dt-d-mantra-name {{ fill: {_Y}; font-size: 22px; font-weight: 800; text-anchor: middle; }}
      .dt-d-mantra-sub {{ fill: #ccc; font-size: 18px; text-anchor: middle; }}
      .dt-d-axis {{ stroke: #bbb; stroke-width: 3; }}
      .dt-d-label {{ fill: #fff; font-size: 26px; }}
      .dt-d-credit {{ fill: #777; font-size: 15px; text-anchor: middle; }}
      .dt-d-note {{ fill: #A9A9A9; font-size: 20px; font-style: italic; }}
    </style>
    <defs>
      <marker id="dt-d-head" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#888"/></marker>
      <marker id="dt-d-axis-head" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#bbb"/></marker>
    </defs>
    <g {_step(4)}><rect x="1.5" y="0" width="1597" height="354" rx="20" class="dt-d-dtour"/>
      <text x="0" y="-12" fill="{_Y}" font-size="30" font-weight="800">dtour</text></g>
    <g {_step(1, cls="dt-play-1")}></g><g {_step(2, cls="dt-play-2")}></g><g {_step(4, cls="dt-play-dtour")}></g>
    {_boxes}
    <g {_step(4, "fade-out")}>{_arrows}</g>
    <line x1="0" y1="389" x2="1590" y2="389" class="dt-d-axis" marker-end="url(#dt-d-axis-head)"/>
    <text x="0" y="422" class="dt-d-label">None</text>
    <text x="800" y="422" class="dt-d-label" text-anchor="middle" font-weight="800">Freedom of traversal</text>
    <text x="1600" y="422" class="dt-d-label" text-anchor="end">Complete</text>
    <g {_step(3)}>
      <g {_step(4, "fade-out")}><image href="{data_uri("cognitive-load-before.png")}" {_CURVE}/>
        <text x="305" y="520" class="dt-d-note" text-anchor="end">switch tools</text><text x="945" y="479" class="dt-d-note" text-anchor="end">switch tools</text></g>
      <g {_step(4)}><image href="{data_uri("cognitive-load-dtour.png")}" {_CURVE}/></g>
      <text x="0" y="585" class="dt-d-label">Low</text>
      <text x="800" y="585" class="dt-d-label" text-anchor="middle" font-weight="800">Cognitive load</text>
      <text x="1600" y="585" class="dt-d-label" text-anchor="end">High</text>
    </g>
    </svg>"""

    slide(
        play_on_fragments(),
        kicker("Touring many projections"),
        '<div style="display:grid">'
        f'<div style="grid-area:1/1" {_step(4, "fade-out", "dt-h1")}>Use <span class="dt-y">many</span> projections! But how?</div>'
        f'<div style="grid-area:1/1" {_step(4, cls="dt-h1")}>dtour: <span class="dt-y">one</span> interface across all modes</div>'
        "</div>",
        _diagram,
        '<div style="flex:1"></div>',
        f'<div style="font-size:1.7cqw" {_step(6)}>Every mode shift is animated, so you never lose track of your points '
        '<span class="dt-muted">(object constancy)</span>. <span class="dt-y">Move freely between modes.</span></div>',
    )
    return


@app.cell
def _(slide):
    slide(
        '<iframe src="https://dtour.dev/?dataset=linked-rings" '
        'style="flex:1; width:100%; border:0; background:#000" allow="fullscreen"></iframe>',
        full=True,
    )
    return


@app.cell(expand_output=True)
def _(kicker, slide, title):
    import math as _math


    def _catmull_rom(pts, steps=24):
        # Uniform Catmull–Rom through all points (ends duplicated)
        ext = [pts[0], *pts, pts[-1]]
        out = []
        for i in range(1, len(ext) - 2):
            p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
            for s in range(steps):
                t = s / steps
                out.append(tuple(
                    0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t**2 + (-a + 3 * b - 3 * c + d) * t**3)
                    for a, b, c, d in zip(p0, p1, p2, p3)
                ))
        return [*out, pts[-1]]


    # Keyframes deliberately unevenly spaced. One bullet at a time along the bottom; build steps (reveal.js fragments):
    # 0 the C⁰ path (straight segments) in the center · 1 the segments bend into the Catmull–Rom spline
    # · 2 the spline bends into the slider ring (keyframes at their arc length; the tour loops, so a
    # closing segment grows out of the last keyframe) · 3 space keyframes equally, so each segment's width
    # shows how much it was squeezed · 4 a marker plays the tour: constant speed in projection space, so it
    # lingers on wide segments · 5 the marker scrubs instead: constant speed around the slider
    _STEPS, _LAP = 24, 8  # _LAP: seconds per loop of the marker
    _CENTER, _RADIUS = (240, 90), 78
    _AT = (138, 20)  # where the keyframe path sits, centered on the ring
    _keyframes = [(x, 1.4 * y) for x, y in [(12, 72), (24, 50), (130, 78), (142, 22), (192, 60)]]  # stretched to fill the height
    _k = len(_keyframes)


    def _at(points, offset):
        return [(x + offset[0], y + offset[1]) for x, y in points]


    _spline = _at(_catmull_rom(_keyframes, _STEPS), _AT)
    _segments = [_spline[i * _STEPS : (i + 1) * _STEPS + 1] for i in range(_k - 1)]
    # Closing segment (last → first keyframe), with the tangents of a closed Catmull–Rom loop
    _p0, _p1, _p2, _p3 = (_keyframes[i] for i in (-2, -1, 0, 1))
    _segments.append(_at([
        tuple(
            0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t**2 + (-a + 3 * b - 3 * c + d) * t**3)
            for a, b, c, d in zip(_p0, _p1, _p2, _p3)
        )
        for t in (s / _STEPS for s in range(_STEPS + 1))
    ], _AT))
    _lengths = [sum(_math.dist(a, b) for a, b in zip(seg, seg[1:])) for seg in _segments]
    _total = sum(_lengths)


    def _on_ring(fraction):
        angle = 2 * _math.pi * fraction - _math.pi / 2  # clockwise from the top, like the slider
        return _CENTER[0] + _RADIUS * _math.cos(angle), _CENTER[1] + _RADIUS * _math.sin(angle)


    def _seg_states(i):
        seg, start = _segments[i], sum(_lengths[:i])
        walked = [0.0]
        for a, b in zip(seg, seg[1:]):
            walked.append(walked[-1] + _math.dist(a, b))
        # The open path has no closing segment yet: it starts collapsed onto the last keyframe
        if i == _k - 1:
            c0 = path = [seg[0]] * len(seg)
        else:
            (x0, y0), (x1, y1) = seg[0], seg[-1]
            c0 = [(x0 + (x1 - x0) * s / _STEPS, y0 + (y1 - y0) * s / _STEPS) for s in range(_STEPS + 1)]  # straight
            path = seg
        ring = [_on_ring((start + s) / _total) for s in walked]  # arc-length spacing
        equal = [_on_ring((i + s / _lengths[i]) / _k) for s in walked]  # equal spacing
        return c0, path, ring, equal


    def _d(points):
        return 'path("M' + " L".join(f"{x:.2f},{y:.2f}" for x, y in points) + '")'


    _dot_states = [
        _at(_keyframes, _AT),
        _at(_keyframes, _AT),
        [_on_ring(sum(_lengths[:j]) / _total) for j in range(_k)],
        [_on_ring(j / _k) for j in range(_k)],
    ]
    _css = [
        ".dt-k-seg { fill: none; stroke: #fff; stroke-width: 2.2; transition: d 1.2s ease-in-out, stroke-width 1.2s ease-in-out; }",
        ".dt-k-dot { fill: #FEC10E; transition: cx 1.2s ease-in-out, cy 1.2s ease-in-out; }",
        # The ring-width bullet waits for the equal spacing to settle
        ".reveal .slides section .fragment.dt-k-width.current-fragment { transition-delay: 1.2s; }",
        # Position marker, rotated about the ring center (it sits at the top of the ring)
        f".dt-k-marker {{ opacity: 0; transform-origin: {_CENTER[0]}px {_CENTER[1]}px; transition: opacity 0.4s; }}",
        f".dt-slide:has(.dt-k-play.visible) .dt-k-marker {{ opacity: 1; animation: dt-k-play {_LAP}s linear infinite; }}",
        f".dt-slide:has(.dt-k-scrub.visible) .dt-k-marker {{ animation: dt-k-scrub {_LAP}s linear infinite; }}",
        # Playback: each segment takes time proportional to its length but gets an equal 1/k of the ring
        "@keyframes dt-k-play { "
        + " ".join(f"{100 * sum(_lengths[:j]) / _total:.2f}% {{ transform: rotate({360 * j / _k:.2f}deg); }}" for j in range(_k + 1))
        + " }",
        "@keyframes dt-k-scrub { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }",
        # Play / hand icon in the ring's center, shown with the matching marker animation
        ".dt-k-icon { opacity: 0; transition: opacity 0.4s; }",
        ".dt-slide:has(.dt-k-play.visible) .dt-k-icon-play { opacity: 1; }",
        ".dt-slide:has(.dt-k-scrub.visible) .dt-k-icon-play { opacity: 0; }",
        ".dt-slide:has(.dt-k-scrub.visible) .dt-k-icon-scrub { opacity: 1; }",
    ]
    _states = ["", "svg:has(.dt-k-cr.visible) ", "svg:has(.dt-k-ring.visible) ", "svg:has(.dt-k-equal.visible) "]
    for _state, _marker in enumerate(_states):
        for _i in range(_k):
            # Equal spacing squeezes long segments (thicker) and stretches short ones (thinner),
            # with width proportional to length like dtour's slider ring
            _width = f" stroke-width: {max(0.5, 2.4 * _lengths[_i] * _k / _total):.2f};" if _state == 3 else ""
            _css.append(f"{_marker}.dt-k-seg-{_i} {{ d: {_d(_seg_states(_i)[_state])};{_width} }}")
        for _j, (_x, _y) in enumerate(_dot_states[_state]):
            _css.append(f"{_marker}.dt-k-dot-{_j} {{ cx: {_x:.2f}px; cy: {_y:.2f}px; }}")


    def _step(i, effect="", cls=""):
        classes = " ".join(c for c in ("fragment", effect, cls) if c)
        return f'class="{classes}" data-fragment-index="{i}"'


    def _caption(text, x, *attrs):
        return f'<text x="{x}" y="155" fill="#A9A9A9" font-size="8" text-anchor="middle" {" ".join(attrs)}>{text}</text>'


    def _heading(text, x):
        return f'<text x="{x}" y="34" fill="#fff" font-size="9" font-weight="600" text-anchor="middle">{text}</text>'


    # 24×24 icons (Lucide, ISC license), drawn at _ICON units in the ring's center
    _ICON = 34
    _HAND = (
        '<path d="M18 11V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/>'
        '<path d="M14 10V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2"/>'
        '<path d="M10 10.5V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2v8"/>'
        '<path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83L7 15"/>'
    )


    def _icon(cls, shapes):
        x, y, s = _CENTER[0] - _ICON / 2, _CENTER[1] - _ICON / 2, _ICON / 24
        return (
            f'<g class="dt-k-icon {cls}" transform="translate({x} {y}) scale({s})" fill="none" stroke="#fff" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{shapes}</g>'
        )


    _figure = f"""<svg viewBox="0 0 480 180" style="width:100%; flex:1; min-height:0" font-family="inherit">
    <style>{chr(10).join(_css)}</style>
    <g {_step(1, cls="dt-k-cr")}></g><g {_step(2, cls="dt-k-ring")}></g><g {_step(3, cls="dt-k-equal")}></g>
    <g {_step(1, "fade-out")}>
      {_heading("Piecewise geodesic: C⁰", _CENTER[0])}
      {_caption("jumps abruptly at every keyframe", _CENTER[0])}
    </g>
    {"".join(f'<path class="dt-k-seg dt-k-seg-{i}"/>' for i in range(_k))}
    {"".join(f'<circle class="dt-k-dot dt-k-dot-{j}" r="3.2"/>' for j in range(_k))}
    {_icon("dt-k-icon-play", '<path d="M6 3 L20 12 L6 21 Z"/>')}
    {_icon("dt-k-icon-scrub", _HAND)}
    <circle class="dt-k-marker" cx="{_CENTER[0]}" cy="{_CENTER[1] - _RADIUS}" r="5" fill="#fff" stroke="#111" stroke-width="1.5"/>
    <g {_step(1, "fade-in-then-out")}>
      {_heading("Catmull–Rom interpolation + Gram–Schmidt: C¹", _CENTER[0])}
      {_caption("visits every keyframe smoothly", _CENTER[0])}
    </g>
    </svg>"""

    # One bullet per build step, stacked in the same grid cell: (step, fragment effect and classes, text)
    _bullets = [
        (1, "fade-in-then-out", "<span class='dt-y'><b>Catmull–Rom</b></span> through the keyframe bases, re-orthonormalized → no direction jumps"),
        (2, "fade-in-then-out", "<span class='dt-y'><b>Closed loop:</b></span> the guided path wraps from the last keyframe back to the first"),
        (3, "fade-in-then-out dt-k-width", "<span class='dt-y'><b>Slider ring:</b></span> arc width encodes the geodesic distance between keyframes"),
        (4, "fade-in-then-out dt-k-play", "<span class='dt-y'><b>Playback</b></span> is paced by geodesic distance: it travels through projection space at constant speed"),
        (5, "dt-k-scrub", "<span class='dt-y'><b>Scrubbing</b></span> gives each keyframe equal share: it travels faster when keyframes are far apart"),
    ]
    _bullet_row = (
        '<div style="display:grid; text-align:center; min-height:2.8em; align-items:center; padding:0 6cqw">'
        + "".join(f'<div style="grid-area:1/1" {_step(_i, _effect)}>{_text}</div>' for _i, _effect, _text in _bullets)
        + "</div>"
    )

    slide(
        kicker("Smooth by design"),
        title('Traversal should feel <span class="dt-y"><i>continuous</i></span>'),
        '<div class="dt-muted" style="font-size:1.2cqw; display:flex; align-items:center; gap:0.5em">'
        '<span style="width:0.7em; height:0.7em; border-radius:50%; background:#FEC10E"></span>keyframe projection</div>',
        _figure,
        _bullet_row,
    )

    return


@app.cell
def _(col, kicker, row, slide, title):
    slide(
        kicker("Tour strategies"),
        title("dtour supports two tour families"),
        row(
            col(
                '<div class="dt-family-name">Hyperdimensional tours</div>',
                '<div style="font-size:1.6cqw; font-weight:400">Keyframes are 2D projections of <b>one</b> high-dimensional space. '
                "Every in-between frame is a valid projection too.</div>",
                '<div class="dt-muted" style="font-size:1.5cqw; font-style:italic; font-weight:400; padding-top:1em; margin-bottom:-0.5em">What does the manifold look like from different angles?</div>',
                "<ul class='dt-scaled' style='font-size:1.5cqw; color:#A9A9A9; padding-left:0'>"
                "<li>E.g., little tour over PCs, Laplacian Eigenmaps tour, grand &amp; manual tours</li>"
                "<li>Use for: exploring a space, validating a 2D embedding against its input (e.g., PCs vs. UMAP)</li>"
                "</ul>",
                style="flex:1",
            ),
            col(
                '<div class="dt-family-name">Sequential tours</div>',
                '<div style="font-size:1.6cqw; font-weight:400">Keyframes are <b>aligned</b> 2D embeddings of the same points. '
                "Only keyframes are real; in-betweens just track points.</div>",
                '<div class="dt-muted" style="font-size:1.5cqw; font-style:italic; font-weight:400; padding-top:1em; margin-bottom:-0.5em">How does the manifold look across lenses?</div>',
                "<ul class='dt-scaled' style='font-size:1.5cqw; color:#A9A9A9; padding-left:0'>"
                "<li>E.g., hyperparameter sweeps (attraction–repulsion), DR methods, embedding models</li>"
                "<li>Use for: telling genuine structure from method artifacts, comparing embedding models</li>"
                "</ul>",
                style="flex:1",
            ),
            gap="2cqw",
        ),
        '<div style="font-size:1.8cqw"><span class="dt-y">Generic</span>: dtour supports any tour or sequence of 2D projections '
        "that fits the two families!</div>",
    )
    return


@app.cell
def _(brain_tour, brain_umap, col, slide, widget_row):
    slide(
        '<div class="dt-h2">Usage scenario: <span class="dt-y">Validating non-linear DR outputs</span></div>',
        widget_row(col(brain_tour), col(brain_umap)),
        padding="2.5cqw 3cqw",
    )
    return


@app.cell
def _(col, fmnist_images, fmnist_tour, slide, widget_row):
    slide(
        '<div class="dt-h2">Usage scenario: <span class="dt-y">Gradually revealing structure in high-dimensional data</span></div>',
        widget_row(col(fmnist_tour, style="flex:4"), col(fmnist_images, style="flex:1")),
        padding="2.5cqw 3cqw",
    )
    return


@app.cell
def _(kicker, slide):
    slide(
        kicker("Thank you"),
        '<div style="flex:1"></div>',
        # Smaller than a regular title (3.8cqw), so the tagline fits on one line
        '<div class="dt-h1" style="font-size:2.75cqw">Take a tour. Enjoy the view!</div>',
        '<div style="font-size:2.4cqw; line-height:1.6; margin-top:2.4cqw">'
        '<b class="dt-y">dtour.dev</b>&ensp;·&ensp;github.com/flekschas/dtour<br>'
        '<span class="dt-muted">pip install dtour · Jupyter, marimo, React</span></div>',
        '<div class="dt-badge">🏆 Best Short Paper Honorable Mention</div>',
        '<div class="dt-muted" style="font-size:1.3cqw; margin-top:1.6cqw">Fritz Lekschas · Nezar Abdennur</div>',
    )
    return


@app.cell(hide_code=True)
def _():
    import base64
    import urllib.request
    from functools import cache

    import dtour
    import marimo as mo
    import numpy as np
    import polars as pl
    import pyarrow as pa
    import pyarrow.parquet as pq
    from anywidget import AnyWidget
    from traitlets import Int, List

    return (
        AnyWidget,
        Int,
        List,
        base64,
        cache,
        dtour,
        mo,
        np,
        pa,
        pl,
        pq,
        urllib,
    )


@app.cell(hide_code=True)
def _(base64, cache, mo, np, pl):
    ASSETS = mo.notebook_dir() / "assets"
    DATA_URL = "https://data.dtour.dev"

    SLIDE_CSS = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,800;1,300;1,400;1,800&display=swap');
    .dt-wrap { container-type: inline-size; width: 100%; }
    .dt-slide {
      aspect-ratio: 16 / 9; box-sizing: border-box; overflow: hidden;
      display: flex; flex-direction: column; gap: 1.6cqw;
      padding: 3.6cqw 4.5cqw; border-radius: 4px;
      background: #000; color: #fff;
      font-family: 'Open Sans', 'Helvetica Neue', sans-serif;
      font-size: 1.8cqw; font-weight: 300; line-height: 1.4;
    }
    .dt-slide { position: relative; }
    .dt-slide > * { position: relative; z-index: 1; }
    .dt-slide > .dt-bg {
      /* --bleed-* is the slide's distance to the reveal.js viewport edges, set by background() */
      position: absolute; z-index: 0;
      top: calc(-1 * var(--bleed-top, 0px)); bottom: calc(-1 * var(--bleed-bottom, 0px));
      right: calc(-1 * var(--bleed-right, 0px)); width: calc(60% + var(--bleed-right, 0px));
      -webkit-mask-image: linear-gradient(to right, transparent, #000 45%);
      mask-image: linear-gradient(to right, transparent, #000 45%);
    }
    .dt-slide:has(> .dt-bg), .reveal .overflow-auto:has(.dt-bg) { overflow: visible !important; }
    /* marimo's slide thumbnails lay outputs out in a row, where a size-contained .dt-wrap collapses */
    .output:has(> .dt-wrap) { width: 100%; min-width: 0; }
    /* marimo wraps iframes in a <div>; let it fill the slide */
    .dt-slide > :has(> iframe) { flex: 1; display: flex; }
    /* The bleeding background is not scrollable content */
    .reveal section:has(.dt-bg) [data-testid="slide-scroll-hint"] { display: none !important; }
    .dt-bg > video { display: block; width: 100%; height: 100%; object-fit: cover; }
    .dt-fade-in { opacity: 0; animation: dt-fade-in 2.5s ease-out 0.5s forwards; }
    @keyframes dt-fade-in { to { opacity: 0.85; } }
    .dt-slide b, .dt-slide strong { font-weight: 600; }
    .dt-h1 { font-weight: 800; font-size: 3.8cqw; line-height: 1.1; letter-spacing: -0.01em; }
    .dt-kicker { color: #A9A9A9; font-weight: 600; font-size: 1.2cqw; letter-spacing: 0.1em; text-transform: uppercase; }
    .dt-h1.dt-xl { font-size: 5.2cqw; }
    .dt-muted { color: #A9A9A9; }
    .dt-y { color: #FEC10E; }
    .dt-row { display: flex; flex: 1; min-height: 0; }
    .dt-col { display: flex; flex-direction: column; gap: 1.2cqw; flex: 1; min-width: 0; min-height: 0; }
    .dt-slide ul { margin: 0; padding-left: 1.2em; }
    .dt-slide li { margin: 0.3em 0; }
    /* marimo gives <li> a fixed px size; .dt-scaled lists follow their own (cqw) size instead */
    .dt-slide .dt-scaled li { font-size: inherit; }
    .dt-slide img { display: block; max-width: 100%; max-height: 100%; object-fit: contain; }
    .dt-todo {
      flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;
      gap: 0.6cqw; padding: 1.5cqw; text-align: center;
      border: 0.15cqw dashed #555; border-radius: 0.8cqw;
      color: #A9A9A9; font-size: 1.3cqw; line-height: 1.35;
    }
    .dt-todo > b { color: #FEC10E; font-size: 0.9cqw; letter-spacing: 0.15em; }
    .dt-badge {
      align-self: flex-start; background: #FEC10E; color: #000;
      font-weight: 800; font-size: 1.4cqw; padding: 0.4cqw 1.1cqw; border-radius: 99cqw;
    }
    .dt-spectrum { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1cqw; }
    .dt-mode { border: 0.12cqw solid #444; border-radius: 0.6cqw; padding: 0.9cqw 1.2cqw; }
    .dt-mode-name { font-weight: 800; font-size: 1.6cqw; }
    .dt-mode-sub { color: #A9A9A9; font-size: 1.15cqw; }
    .dt-spectrum.dtour .dt-mode { border-color: #FEC10E; }
    .dt-axis {
      display: flex; justify-content: space-between; margin-top: 0.6cqw; padding-top: 0.4cqw;
      border-top: 0.12cqw solid #A9A9A9; color: #A9A9A9; font-size: 1.1cqw;
    }
    .dt-span {
      margin-bottom: 0.6cqw; padding: 0.3cqw; border-radius: 0.6cqw;
      background: #FEC10E; color: #000; font-weight: 800; font-size: 1.5cqw; text-align: center;
    }
    .dt-h2 { font-weight: 800; font-size: 2.4cqw; line-height: 1.1; }
    .dt-family { border: 0.12cqw solid #444; border-radius: 0.6cqw; padding: 1.4cqw 1.6cqw; }
    .dt-family-name { font-weight: 800; font-size: 2.2cqw; color: #FEC10E; }
    .dt-family .dt-muted { font-size: 1.4cqw; }
    .dt-slide .dt-family ul { font-size: 1.5cqw; }
    /* Slides view: black canvas around the 16:9 slide and no extra padding, also in fullscreen */
    .reveal-viewport:has(.dt-slide), .reveal-viewport:has(.dt-slide):fullscreen { background-color: #000 !important; border-color: #000 !important; }
    .reveal-viewport:has(.dt-slide) .mo-slide-content { padding: 0 !important; }
    /* reveal.js scales slides with a transform, which offsets pointer input in live widgets (e.g., the lasso) */
    .reveal-viewport:has(.dt-slide) .slides { transform: translate(-50%, -50%) !important; }
    .reveal-viewport:has(.dt-slide) .controls, .reveal-viewport:has(.dt-slide) .progress { color: #FEC10E; }
    </style>"""


    @cache
    def data_uri(name):
        """An image from `assets/` as a data URI, so slides export self-contained."""
        import mimetypes

        mime = mimetypes.guess_type(name)[0]
        return f"data:{mime};base64,{base64.b64encode((ASSETS / name).read_bytes()).decode()}"


    def img(name, style=""):
        return f'<img src="{data_uri(name)}" style="{style}">'


    def kicker(text):
        return f'<div class="dt-kicker">{text}</div>'


    def title(text, xl=False):
        return f'<div class="dt-h1{" dt-xl" if xl else ""}">{text}</div>'


    def row(*cols, gap="2.5cqw", style=""):
        return f'<div class="dt-row" style="gap:{gap};{style}">{"".join(map(html, cols))}</div>'


    def col(*parts, style=""):
        return f'<div class="dt-col" style="{style}">{"".join(map(html, parts))}</div>'


    def todo(what, style=""):
        """Placeholder for a visual that still needs to be made."""
        return f'<div class="dt-todo" style="{style}"><b>VISUAL</b><div>{what}</div></div>'


    def spectrum(dtour=False):
        """The traversal-freedom spectrum from the paper's intro."""
        modes = [
            ("Static grids", "scatter plot matrices · small multiples"),
            ("Animated tours", "guided · grand (GGobi, tourr)"),
            ("Manual tours", "drag individual axes"),
        ]
        cells = "".join(
            f'<div class="dt-mode"><div class="dt-mode-name">{name}</div>'
            f'<div class="dt-mode-sub">{sub}</div></div>'
            for name, sub in modes
        )
        span = '<div class="dt-span">dtour — one interface, move freely between modes</div>' if dtour else ""
        return (
            f'<div>{span}<div class="dt-spectrum{" dtour" if dtour else ""}">{cells}</div>'
            '<div class="dt-axis"><span>&larr; comparable at a glance, but fixed</span>'
            "<span>freedom of traversal &amp; steerability &rarr;</span></div></div>"
        )


    def html(part):
        """Slide parts are HTML strings or marimo-renderable objects, e.g., widgets."""
        return part if isinstance(part, str) else mo.as_html(part).text


    def slide(*parts, full=False, padding=None):
        """Render a 16:9 slide. `full=True` drops the padding for full-bleed content."""
        style = ' style="padding:0; gap:0"' if full else f' style="padding:{padding}"' if padding else ""
        return mo.Html(
            f'{SLIDE_CSS}<div class="dt-wrap"><div class="dt-slide"{style}>{"".join(map(html, parts))}</div></div>'
        )


    def selected_rows(widget, df, column):
        """Rows selected in a dtour *widget*, by lasso or by clicking labels of *column*."""
        if widget.selected_labels:
            return np.flatnonzero(df[column].cast(pl.String).is_in(widget.selected_labels).to_numpy())
        return np.asarray(widget.selected_indices, dtype=int)

    return (
        ASSETS,
        DATA_URL,
        col,
        data_uri,
        html,
        img,
        kicker,
        row,
        selected_rows,
        slide,
        title,
    )


@app.cell(hide_code=True)
def _(AnyWidget, Int, html, mo):
    class RowHeight(AnyWidget):
        """Reports the pixel height of the enclosing `.dt-measure` row of a slide shown in reveal.js."""

        _esm = """
        function findRow(node) {
          while (node) {
            if (node.nodeType === 1 && node.classList.contains("dt-measure")) return node;
            node = node.parentNode ?? node.host;
          }
        }
        function render({ model, el }) {
          let observer, timer, frame;
          const attach = () => {
            const row = findRow(el);
            if (!row || !row.closest(".reveal")) { frame = requestAnimationFrame(attach); return; }
            observer = new ResizeObserver(() => {
              clearTimeout(timer);
              timer = setTimeout(() => {
                const height = Math.floor(row.clientHeight);
                if (height > 100 && Math.abs(height - model.get("height")) > 8) {
                  model.set("height", height);
                  model.save_changes();
                }
              }, 400);
            });
            observer.observe(row);
          };
          attach();
          return () => { cancelAnimationFrame(frame); clearTimeout(timer); observer?.disconnect(); };
        }
        export default { render };
        """
        height = Int(560).tag(sync=True)


    # Live widgets take the height of the slide row they sit in, re-measured, e.g., when entering fullscreen
    slide_row = mo.ui.anywidget(RowHeight())


    def widget_row(*cols, gap="1cqw"):
        """A slide row that fills the remaining height and measures it for the live widgets."""
        measure = f'<div style="position:absolute; width:0; height:0; overflow:hidden">{mo.as_html(slide_row).text}</div>'
        return f'<div class="dt-row dt-measure" style="gap:{gap}; position:relative">{measure}{"".join(map(html, cols))}</div>'

    class SlideBleed(AnyWidget):
        """Sets `--bleed-*` on the enclosing slide to its distance from the edges of the reveal.js viewport."""

        _esm = """
        function findSlide(node) {
          while (node) {
            if (node.nodeType === 1 && node.classList.contains("dt-slide")) return node;
            node = node.parentNode ?? node.host;
          }
        }
        function render({ el }) {
          let observer, frame, timer;
          const attach = () => {
            const slide = findSlide(el);
            const viewport = slide?.closest(".reveal-viewport");
            if (!viewport) { frame = requestAnimationFrame(attach); return; }
            const update = () => {
              const s = slide.getBoundingClientRect();
              const v = viewport.getBoundingClientRect();
              if (!s.width) return;
              const scale = s.width / slide.offsetWidth;  // reveal.js scales the slides
              for (const [side, px] of [["top", s.top - v.top], ["right", v.right - s.right], ["bottom", v.bottom - s.bottom]]) {
                slide.style.setProperty(`--bleed-${side}`, `${Math.max(0, px / scale)}px`);
              }
            };
            // Re-measure once slide transitions and fullscreen changes have settled
            const schedule = () => { update(); clearTimeout(timer); timer = setTimeout(update, 800); };
            observer = new ResizeObserver(schedule);
            observer.observe(viewport);
            observer.observe(slide);
            schedule();
          };
          attach();
          return () => { cancelAnimationFrame(frame); clearTimeout(timer); observer?.disconnect(); };
        }
        export default { render };
        """


    slide_bleed = mo.ui.anywidget(SlideBleed())


    def background(content):
        """A faded-in slide background, right-aligned and spanning the full height of the reveal.js viewport."""
        measure = f'<div style="position:absolute; width:0; height:0; overflow:hidden">{mo.as_html(slide_bleed).text}</div>'
        return f'{measure}<div class="dt-bg dt-fade-in">{html(content)}</div>'

    class FragmentPlayer(AnyWidget):
        """Plays the slide's `<video data-play-from="a" data-play-until="b">` while the fragment with class `a` is shown and `b` is not.

        Classes, not fragment indices: reveal.js renumbers the indices from 0.
        """

        _esm = """
        function findSlide(node) {
          while (node) {
            if (node.nodeType === 1 && node.classList.contains("dt-slide")) return node;
            node = node.parentNode ?? node.host;
          }
        }
        function render({ el }) {
          let observer, frame;
          const attach = () => {
            const slide = findSlide(el);
            const section = slide?.closest(".reveal section");  // thumbnails are not in reveal.js
            if (!section) { frame = requestAnimationFrame(attach); return; }
            const shown = (cls) => cls != null && !!slide.querySelector(`.fragment.visible.${cls}`);
            const update = () => {
              for (const video of slide.querySelectorAll("video[data-play-from]")) {
                const play = section.classList.contains("present")
                  && shown(video.dataset.playFrom) && !shown(video.dataset.playUntil);
                if (play && video.paused) video.play().catch(() => {});
                if (!play && !video.paused) video.pause();
              }
            };
            observer = new MutationObserver(update);
            observer.observe(section, { attributes: true, attributeFilter: ["class"], subtree: true });
            update();
          };
          attach();
          return () => { cancelAnimationFrame(frame); observer?.disconnect(); };
        }
        export default { render };
        """


    fragment_player = mo.ui.anywidget(FragmentPlayer())


    def play_on_fragments():
        """Include once in a slide whose videos should start and stop with its fragments."""
        return f'<div style="position:absolute; width:0; height:0; overflow:hidden">{mo.as_html(fragment_player).text}</div>'


    return background, play_on_fragments, slide_row, widget_row


@app.cell
def _(DATA_URL, dtour, pl):
    # Developing mouse brain (La Manno et al. 2021): a little tour over PC1-8, linked to a 2D UMAP of the same PCs
    brain = pl.read_parquet(f"{DATA_URL}/notebooks/lamanno2021-pca-umap.pq")
    brain_pcs = [f"PC{i}" for i in range(1, 9)]
    brain_colors = dtour.build_color_map(sorted(brain["Class"].unique()), theme="dark")
    brain_little_tour = dtour.little_tour(brain.select(brain_pcs))
    return brain, brain_colors, brain_little_tour, brain_pcs


@app.cell
def _(brain, brain_colors, brain_little_tour, brain_pcs, dtour):
    brain_tour = dtour.Widget(
        data=brain.select(*brain_pcs, "Age", "Class", "Subclass"),
        tour=brain_little_tour,
        tour_dimensions=brain_pcs,
        point_color_by="Class",
        point_opacity=0.5,
        color_map=brain_colors,
        preview_size="small",
        preview_count=8,
        show_legend=False,  # the UMAP next to it shows the legend
        theme_mode="dark",
    )
    # A static dtour scatter of the 2D UMAP of the same PCs
    brain_umap = dtour.Widget(
        data=brain.select("UMAP1", "UMAP2", "Class", "Subclass"),
        tour_dimensions=["UMAP1", "UMAP2"],
        point_color_by="Class",
        point_opacity=0.5,
        color_map=brain_colors,
        theme_mode="dark",
    )
    # Keep lasso and legend selections in sync, in the browser
    _unlink = dtour.link(brain_tour, brain_umap)
    return brain_tour, brain_umap


@app.cell(hide_code=True)
def _(AnyWidget, Int, List):
    class FashionImages(AnyWidget):
        """Thumbnails of the selected Fashion MNIST images, as [url, color] pairs."""

        _esm = """
        function render({ model, el }) {
          el.classList.add("fm-images");
          const show = () => {
            const images = model.get("images");
            el.style.height = `${model.get("height")}px`;
            el.replaceChildren();
            const head = el.appendChild(document.createElement("div"));
            head.className = "fm-images-title";
            head.textContent = images.length
              ? `${images.length.toLocaleString()} selected`
              : "Select points to see their images";
            const grid = el.appendChild(document.createElement("div"));
            grid.className = "fm-images-grid";
            for (const [url, color] of images.slice(0, model.get("max"))) {
              const tile = grid.appendChild(document.createElement("div"));
              tile.style.border = `2px solid ${color}`;
              tile.style.backgroundImage = `url(${url})`;
            }
          };
          model.on("change:images", show);
          model.on("change:height", show);
          show();
        }
        export default { render };
        """
        _css = """
        .fm-images { display: flex; flex-direction: column; gap: 6px; overflow: hidden; color: #A9A9A9; }
        .fm-images-title { font-size: 0.8rem; font-weight: 600; }
        .fm-images-grid {
          display: grid; grid-template-columns: repeat(auto-fill, minmax(32px, 1fr)); gap: 3px;
          align-content: start; overflow: auto;
        }
        .fm-images-grid div {
          aspect-ratio: 1; box-sizing: border-box; border-radius: 2px; background-size: contain; background-repeat: no-repeat; background-position: center;
        }
        """
        images = List().tag(sync=True)
        height = Int(400).tag(sync=True)
        max = Int(300).tag(sync=True)

    return (FashionImages,)


@app.cell
def _(DATA_URL, dtour, pa, pl, pq, urllib):
    # Fashion MNIST (70K images): a sequential tour along the attraction-repulsion spectrum, LE-like -> t-SNE
    _request = urllib.request.Request(
        f"{DATA_URL}/fashion-mnist-attraction-repulsion-tour.pq", headers={"User-Agent": "dtour"}
    )
    _table = pq.read_table(pa.BufferReader(urllib.request.urlopen(_request).read()))
    fmnist = pl.from_arrow(_table)
    fmnist_dims = [c for c in fmnist.columns if c.startswith("sp_")]
    fmnist_colors = dtour.build_color_map(sorted(fmnist["label"].unique()), theme="dark")
    fmnist_spectrum_tour = dtour.TourResult.from_parquet(_table)
    fmnist_spectrum_tour.feature_names = fmnist_dims
    return fmnist, fmnist_colors, fmnist_dims, fmnist_spectrum_tour


@app.cell
def _(
    FashionImages,
    dtour,
    fmnist,
    fmnist_colors,
    fmnist_dims,
    fmnist_spectrum_tour,
    selected_rows,
):
    fmnist_tour = dtour.Widget(
        data=fmnist,
        tour=fmnist_spectrum_tour,
        tour_dimensions=fmnist_dims,
        point_color_by="label",
        color_map=fmnist_colors,
        tooltip_columns=["image", "label"],
        camera_zoom=0.5,
        preview_count=4,
        preview_size="medium",
        theme_mode="dark",
    )
    fmnist_images = FashionImages()


    def _show_images(_):
        rows = fmnist[selected_rows(fmnist_tour, fmnist, "label")]
        fmnist_images.images = [
            [url, fmnist_colors.get(label, "#888")] for url, label in rows.select("image", "label").iter_rows()
        ]


    fmnist_tour.observe(_show_images, names=["selected_indices", "selected_labels"])
    return fmnist_images, fmnist_tour


@app.cell(hide_code=True)
def _(brain_tour, brain_umap, fmnist_images, fmnist_tour, slide_row):
    # Fit the live widgets to the measured slide row, e.g., after entering fullscreen. All of them resize
    # in place, so selections and the tour position survive (dtour >= 0.5.2).
    live_height = slide_row.value["height"]
    for _widget in (brain_tour, brain_umap, fmnist_tour, fmnist_images):
        _widget.height = live_height
    return


if __name__ == "__main__":
    app.run()
