from math import cos, pi, sin

BASE = 760


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
        f'<circle cx="{x}"  cy="{y}" r="100" />',
        f'<circle cx="{x}"  cy="{y}" r="{inner_radius}" />',
        *wheel_lines,
    ]


def wheel_well(x, y):
    well_height = 125
    well_width = 248
    well_slope = 69

    y_top = y - well_height
    x_left = x - (well_width // 2)
    x_right = x + (well_width // 2)

    return [
        f'<path d="M {x_left} {y} C {x_left} {y_top} {x_left} {y_top} {x_left + well_slope} {y_top}" />',
        f'<path d="M {x_left + well_slope} {y_top} {x_right - well_slope} {y_top}" />',
        f'<path d="M {x_right} {y} C {x_right} {y_top} {x_right} {y_top} {x_right - well_slope} {y_top}" />',
    ]


def make_group(name, lines):
    s = f'<g id="{name}" class="ink">\n'
    for line in lines:
        s += line
        s += "\n"
    s += "</g>\n"
    return s


STYLE = """<style>
.ink   {stroke: #111; }
.thin  {stroke - width: 4; }
.thick {stroke - width: 9; }
.fill-red    {fill: #e8908c; stroke: none; }
.fill-yellow {fill: #efe6a8; stroke: none; }
.fill-grey   {fill: #b8b5b2; stroke: none; }
.fill-ink    {fill: #111;    stroke: none; }
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

BODY_LINES = """<g id="body" class="ink">
<path d="M 250 10 1380 10 "/>
<path d="M 1380 10 C 1463 23 1574 205 1840 460"/>
<path d="M 250 10 C 134 54 106 480 85 660"/>
<path d="M 85 660 C 52 660 52 660 52 760"/>
<path d="M 1885 760 C 1920 760 1920 670 1885 670" />
<path d="M 1885 670 1840 460" />

<path d="M 53 760 331 760"/>
<path d="M 579 760 1316 760" />
<path d="M 1564 760 1885 760" />
</g>
"""


GENERATED = (
    make_group("left_well", wheel_well(455, BASE))
    + make_group("left_wheel", wheel(455, BASE))
    + make_group("right_well", wheel_well(1440, BASE))
    + make_group("right_wheel", wheel(1440, BASE))
)


BODY = f"""{SVG_HEADER}

{STYLE}

{BODY_LINES}

{GENERATED}

</svg>
"""

if __name__ == "__main__":
    with open("static/bessie_ventures.svg", "w") as f:
        f.write(BODY)
