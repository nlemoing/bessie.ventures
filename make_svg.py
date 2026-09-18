from math import cos, pi, sin

WHEEL_WIDTH = 248
WHEEL_BASE = 760
WHEEL_LEFT_X = 455
WHEEL_RIGHT_X = 1440

STYLE = """<style>
.ink   {stroke: #111; }
.thin  {stroke - width: 4; }
.thick {stroke - width: 9; }
.fill-white {fill: #ffffff; }
.fill-grey   {fill: #b8b5b2; }
</style>
"""

SVG_HEADER = """<svg xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 2000 982"
width="2000" height="982"
fill="none"
stroke="#111"
stroke-width="6"
stroke-linecap="round"
stroke-linejoin="round">"""


def point_on_circle(theta, x, y, r):
    return x + r * cos(theta), y + r * sin(theta)


def wheel(x: int, y: int):
    inner_radius = 70
    inner_spoke_radius = 20
    inner_skew = 0.55
    base_angles = [i * 2 * pi / 5 for i in range(5)]

    wheel_lines = [
        f'<line x1="{p1[0]}" x2="{p2[0]}" y1="{p1[1]}" y2="{p2[1]}" />\n'
        + f'<line x1="{p1[0]}" x2="{p3[0]}" y1="{p1[1]}" y2="{p3[1]}" />'
        for theta in base_angles
        if (p1 := point_on_circle(theta, x, y, inner_spoke_radius))
        and (p2 := point_on_circle(theta - inner_skew, x, y, inner_radius))
        and (p3 := point_on_circle(theta + inner_skew, x, y, inner_radius))
    ]
    return [
        f'<circle cx="{x}"  cy="{y}" r="100" class="fill-grey" />',
        f'<circle cx="{x}"  cy="{y}" r="{inner_radius}" class="fill-white" />',
        *wheel_lines,
    ]


def wheel_well(x, y):
    well_height = 125
    well_slope = 69

    y_top = y - well_height
    x_left = x - (WHEEL_WIDTH // 2)
    x_right = x + (WHEEL_WIDTH // 2)

    return (
        f"C {x_left} {y_top} {x_left} {y_top} {x_left + well_slope} {y_top} "
        + f"L {x_right - well_slope} {y_top} "
        + f"C {x_right} {y_top} {x_right} {y_top} {x_right} {y}"
    )


def make_group(name, lines):
    s = f'<g id="{name}" class="ink">\n'
    for line in lines:
        s += line
        s += "\n"
    s += "</g>\n"
    return s


BODY_LINES = f"""<g id="body" class="ink fill-white">
<path d="M 250 10 C 134 54 106 480 85 660 C 52 660 52 660 52 {WHEEL_BASE}
    L {WHEEL_LEFT_X - (WHEEL_WIDTH // 2)} {WHEEL_BASE}
    {wheel_well(WHEEL_LEFT_X, WHEEL_BASE)}
    L {WHEEL_RIGHT_X - (WHEEL_WIDTH // 2)} {WHEEL_BASE}
    {wheel_well(WHEEL_RIGHT_X, WHEEL_BASE)}
    L 1885 {WHEEL_BASE}
    C 1920 760 1920 670 1885 670 L 1840 460 C 1574 205 1463 23 1380 10 Z
    "/>
</g>
"""

DETAIL_LINES = """<g id="window" class="ink fill-grey">
<path d="M 1280 100 C 1484 102 1442 103 1650 314 L 1280 314 Z" />
</g>

<g id="handle" class="ink fill-grey">
<rect x="1320" y="397" width="100" height="20" rx="5" />
</g>

<g id="bullbar" class="ink fill-grey">
<rect x="1911" y="700" width="25" height="10" />
<rect x="1911" y="730" width="25" height="10" />
<rect x="1937" y="675" width="20" height="100" rx="10" />
</g>

<g id="tailpipe" class="ink fill-grey">
<rect x="10" y="720" width="42" height="30" rx="5" />
</g>

<g id="rear-light" class="ink fill-grey">
<path d="M 111 430 C 166 430 157 469 140 600 L 93 600 Z" />
</g>

<g id="front-light" class="ink fill-grey">
<path d="M 1835 665 C 1839 618 1837 591 1867 590 L 1884 665 Z" />
</g>
"""


GENERATED = make_group("left_wheel", wheel(WHEEL_LEFT_X, WHEEL_BASE)) + make_group(
    "right_wheel", wheel(WHEEL_RIGHT_X, WHEEL_BASE)
)


BODY = f"""{SVG_HEADER}

{STYLE}

{BODY_LINES}

{DETAIL_LINES}

{GENERATED}

</svg>
"""

if __name__ == "__main__":
    with open("static/bessie_ventures.svg", "w") as f:
        f.write(BODY)
