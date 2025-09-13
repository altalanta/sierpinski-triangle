import argparse
import math
from pathlib import Path
from typing import List, Tuple

Point = Tuple[float, float]
Triangle = Tuple[Point, Point, Point]


def midpoint(a: Point, b: Point) -> Point:
    return (0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]))


def carve_holes(tri: Triangle, depth: int, holes: List[Triangle]) -> None:
    if depth <= 0:
        return
    a, b, c = tri
    m_ab = midpoint(a, b)
    m_bc = midpoint(b, c)
    m_ca = midpoint(c, a)
    # Central inverted triangle to carve out
    holes.append((m_ab, m_bc, m_ca))
    # Recurse into the three corner triangles
    carve_holes((a, m_ab, m_ca), depth - 1, holes)
    carve_holes((m_ab, b, m_bc), depth - 1, holes)
    carve_holes((m_ca, m_bc, c), depth - 1, holes)


def polygon(points: Triangle, fill: str, stroke: str = None, stroke_width: float = 0) -> str:
    pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    attrs = [f'points="{pts}"', f'fill="{fill}"']
    if stroke and stroke_width > 0:
        attrs.append(f'stroke="{stroke}"')
        attrs.append(f'stroke-width="{stroke_width}"')
        attrs.append('stroke-linejoin="miter"')
    return f"<polygon {' '.join(attrs)} />"


def rect(x: float, y: float, w: float, h: float, fill: str) -> str:
    return f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" />'


def generate_svg(size: int, depth: int, color: str, bg: str) -> str:
    width = float(size)
    height = math.sqrt(3.0) * 0.5 * width

    # Outer equilateral triangle (pointing up)
    a: Point = (0.0, height)
    b: Point = (width, height)
    c: Point = (width * 0.5, 0.0)

    holes: List[Triangle] = []
    carve_holes((a, b, c), depth, holes)

    parts: List[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.3f} {height:.3f}">')

    if bg.lower() not in {"none", "transparent"}:
        parts.append(rect(0.0, 0.0, width, height, bg))

    # Solid outer triangle
    parts.append(polygon((a, b, c), fill=color))

    # Carved holes, filled with background color (or white if transparent)
    hole_color = bg if bg.lower() not in {"none", "transparent"} else "white"
    for tri in holes:
        parts.append(polygon(tri, fill=hole_color))

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a Sierpinski triangle as an SVG (no dependencies).")
    p.add_argument("--depth", type=int, default=6, help="Recursion depth (default: 6)")
    p.add_argument("--size", type=int, default=800, help="Triangle width in px (default: 800)")
    p.add_argument("--color", type=str, default="#1a1a1a", help="Triangle fill color (default: #1a1a1a)")
    p.add_argument("--bg", type=str, default="white", help="Background color or 'transparent' (default: white)")
    p.add_argument("--output", type=str, default="sierpinski.svg", help="Output SVG path (default: sierpinski.svg)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    depth = max(0, int(args.depth))
    size = max(10, int(args.size))

    svg = generate_svg(size=size, depth=depth, color=args.color, bg=args.bg)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path.resolve()} (depth={depth}, size={size})")


if __name__ == "__main__":
    main()

